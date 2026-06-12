from flask_app import create_app
from ocr_utils import perform_ocr

# Local development entrypoint with uploads stored beside this file.
app = create_app()

if __name__ == "__main__":
    print("Launching AI NoticeBoard Flask backend on port 5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)
