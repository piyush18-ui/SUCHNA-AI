import os

from PIL import Image


def perform_ocr(file_path):
    """
    Extract text from a PDF or image notice using pdfplumber or pytesseract.
    Falls back gracefully when OCR dependencies are missing.
    """
    ext = os.path.splitext(file_path)[1].lower()
    extracted_text = ""

    if ext == ".pdf":
        try:
            import pdfplumber

            print(f"Extracting text from PDF: {file_path}")
            with pdfplumber.open(file_path) as pdf:
                text_pages = [
                    page.extract_text()
                    for page in pdf.pages
                    if page.extract_text()
                ]
                extracted_text = "\n".join(text_pages)
        except Exception as exc:
            print(f"pdfplumber extraction failed: {exc}")

    elif ext in (".png", ".jpg", ".jpeg", ".bmp"):
        try:
            import pytesseract
        except ImportError as exc:
            print(f"pytesseract is not installed: {exc}")
            extracted_text = (
                "[OCR Engine unavailable: install pytesseract and Tesseract OCR. "
                "Please edit text manually.]"
            )
        else:
            try:
                print(f"Extracting text from image via OCR: {file_path}")
                img = Image.open(file_path)
                extracted_text = pytesseract.image_to_string(img)
            except Exception as exc:
                print(f"pytesseract OCR extraction failed: {exc}")
                extracted_text = (
                    "[OCR Engine unavailable or Tesseract not installed. "
                    "Please edit text manually.]"
                )

    return extracted_text.strip() if extracted_text else ""
