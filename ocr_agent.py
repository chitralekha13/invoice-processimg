# ocr_agent.py
import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Chitra\Desktop\tesseract.exe" # update if installed elsewhere

EXTRACTED_FOLDER = "./data/extracted"
os.makedirs(EXTRACTED_FOLDER, exist_ok=True)

def process_invoice(filepath):
    try:
        image = Image.open(filepath)
        extracted_text = pytesseract.image_to_string(image, lang="eng")

        filename = os.path.basename(filepath).split('.')[0] + ".txt"
        extracted_filepath = os.path.join(EXTRACTED_FOLDER, filename)
        
        with open(extracted_filepath, "w", encoding="utf-8") as file:
            file.write(extracted_text)

        print("✅ Text Extracted:\n", extracted_text)  # DEBUG
        return extracted_filepath
    except Exception as e:
        print("❌ Error in OCR:", e)
        return ""
