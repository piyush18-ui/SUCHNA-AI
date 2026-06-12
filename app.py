import os

from flask_app import create_app

# Production entrypoint: uploads folder one level above the package directory.
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "uploads",
)

app = create_app(upload_folder=UPLOAD_FOLDER)

# Backward compatibility for modules that import perform_ocr from app.
from ocr_utils import perform_ocr  # noqa: E402

if __name__ == "__main__":
    print("Launching AI NoticeBoard Flask backend...")
    app.run(host="0.0.0.0", port=5000, debug=True)
