# agents/ocr_agent.py
import pytesseract
from PIL import Image
import re
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Path for Windows if Tesseract isn’t in PATH
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_salary_from_image(image_path: str):
    """Reads an image and extracts the numeric salary value."""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)

    # Try to find numbers that look like salary
    matches = re.findall(r"\d{4,7}", text.replace(",", ""))
    if not matches:
        return {"salary": None, "raw_text": text, "confidence": 0.0}

    salary = max(map(int, matches))
    return {"salary": salary, "raw_text": text, "confidence": 0.95}
