import os

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

import db
from assistant import get_chatbot_response
from engine import detect_deadlines, generate_summary
from model import predict_category
from ocr_utils import perform_ocr
from services import build_recommendations, process_notice_ai_pipeline, registration_http_status

init_db = db.init_db
register_user = db.register_user
authenticate_user = db.authenticate_user
add_notice = db.add_notice
delete_notice = db.delete_notice
get_notices = db.get_notices
get_notice_by_id = db.get_notice_by_id
pin_notice = db.pin_notice
unpin_notice = db.unpin_notice


def create_app(upload_folder=None):
    """
    Application factory for the AI NoticeBoard REST API.
    Preserves backward compatibility for app.py (parent uploads) and server.py (local uploads).
    """
    app = Flask(__name__)

    if upload_folder is None:
        upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")

    os.makedirs(upload_folder, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = upload_folder
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

    init_db()
    _register_routes(app)
    return app


def _register_routes(app):
    @app.route("/api/auth/register", methods=["POST"])
    def api_register():
        data = request.get_json() or {}
        username = data.get("username")
        password = data.get("password")
        role = data.get("role", "student")
        branch = data.get("branch", "All")
        year = data.get("year", "All")
        email = data.get("email")

        if not username or not password:
            return jsonify({"success": False, "message": "Username and password are required."}), 400

        if role == "admin" and not email:
            return jsonify({
                "success": False,
                "message": "Admin accounts require a valid institutional email address.",
            }), 400

        result = register_user(username, password, role, branch, year, email=email)
        return jsonify(result), registration_http_status(result)

    @app.route("/api/auth/login", methods=["POST"])
    def api_login():
        data = request.get_json() or {}
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"success": False, "message": "Username and password are required."}), 400

        result = authenticate_user(username, password)
        status = 200 if result.get("success") else 401
        return jsonify(result), status

    @app.route("/api/notices", methods=["GET"])
    def api_get_notices():
        try:
            notices = get_notices(
                request.args.get("branch"),
                request.args.get("year"),
                request.args.get("category"),
                request.args.get("priority"),
                request.args.get("search"),
            )
            return jsonify({"success": True, "notices": notices})
        except Exception as exc:
            return jsonify({"success": False, "message": f"Failed to fetch notices: {exc}"}), 500

    @app.route("/api/notices/<int:notice_id>", methods=["GET"])
    def api_get_single_notice(notice_id):
        notice = get_notice_by_id(notice_id)
        if notice:
            return jsonify({"success": True, "notice": notice})
        return jsonify({"success": False, "message": "Notice not found."}), 404

    @app.route("/api/notices", methods=["POST"])
    def api_add_notice():
        title = request.form.get("title")
        branch = request.form.get("branch", "All")
        year = request.form.get("year", "All")
        priority = request.form.get("priority", "Medium")
        manual_content = request.form.get("content", "")
        manual_category = request.form.get("category", "")

        if not title:
            return jsonify({"success": False, "message": "Title is required."}), 400

        file_path = None
        extracted_text = ""

        if "file" in request.files:
            file = request.files["file"]
            if file and file.filename:
                filename = secure_filename(file.filename)
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(save_path)
                file_path = save_path
                extracted_text = perform_ocr(save_path)

        content = manual_content if manual_content else extracted_text
        if not content:
            return jsonify({
                "success": False,
                "message": (
                    "Notice content is empty. Please provide notice text or upload a document "
                    "with readable text."
                ),
            }), 400

        try:
            category, summary, deadlines = process_notice_ai_pipeline(
                content,
                manual_category=manual_category,
                predict_category_fn=predict_category,
                generate_summary_fn=generate_summary,
                detect_deadlines_fn=detect_deadlines,
            )
        except Exception as exc:
            return jsonify({"success": False, "message": f"AI processing failed: {exc}"}), 500

        result = add_notice(
            title=title,
            content=content,
            summary=summary,
            category=category,
            branch=branch,
            year=year,
            priority=priority,
            deadlines=deadlines,
            file_path=file_path,
        )

        if result.get("success"):
            return jsonify({
                "success": True,
                "notice_id": result["notice_id"],
                "ai_details": {
                    "predicted_category": category,
                    "generated_summary": summary,
                    "detected_deadlines": deadlines,
                    "file_attached": file_path is not None,
                },
                "message": "Notice added and processed successfully by AI.",
            })

        return jsonify(result), 500

    @app.route("/api/notices/<int:notice_id>", methods=["DELETE"])
    def api_delete_notice(notice_id):
        result = delete_notice(notice_id)
        status = 200 if result.get("success") else 404
        return jsonify(result), status

    @app.route("/api/notices/<int:notice_id>/pin", methods=["POST"])
    def api_pin_notice(notice_id):
        result = pin_notice(notice_id)
        status = 200 if result.get("success") else 404
        return jsonify(result), status

    @app.route("/api/notices/<int:notice_id>/unpin", methods=["POST"])
    def api_unpin_notice(notice_id):
        result = unpin_notice(notice_id)
        status = 200 if result.get("success") else 404
        return jsonify(result), status

    @app.route("/api/chatbot", methods=["POST"])
    def api_chatbot():
        data = request.get_json() or {}
        user_query = data.get("query")
        student_branch = data.get("branch", "All")
        student_year = data.get("year", "All")

        if not user_query:
            return jsonify({"success": False, "message": "Query parameter is required."}), 400

        try:
            notices = get_notices(branch=student_branch, year=student_year)
            response = get_chatbot_response(user_query, notices)
            return jsonify({"success": True, "response": response})
        except Exception as exc:
            return jsonify({"success": False, "message": f"Chatbot error: {exc}"}), 500

    @app.route("/api/recommendations", methods=["GET"])
    def api_recommendations():
        branch = request.args.get("branch", "All")
        year = request.args.get("year", "All")

        try:
            notices = get_notices(branch=branch, year=year)
            recommendations = build_recommendations(notices, branch=branch, year=year)
            return jsonify({"success": True, "notices": recommendations})
        except Exception as exc:
            return jsonify({"success": False, "message": f"Recommendation error: {exc}"}), 500
