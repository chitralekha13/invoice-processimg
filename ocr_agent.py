import pytesseract
from PIL import Image
import os
import json

# Path to Tesseract binary
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Chitra\Desktop\tesseract.exe"

EXTRACTED_FOLDER = "./data/extracted/"
os.makedirs(EXTRACTED_FOLDER, exist_ok=True)

def process_invoice(filepath):
    """
    Extracts text and bounding boxes from the given invoice image.
    """
    try:
        image = Image.open(filepath)
        ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

        # Prepare extracted data
        extracted_data = {"words": [], "bounding_boxes": []}
        for i in range(len(ocr_data["text"])):
            word = ocr_data["text"][i].strip()
            if word:
                bbox = [
                    ocr_data["left"][i],
                    ocr_data["top"][i],
                    ocr_data["width"][i],
                    ocr_data["height"][i],
                ]
                extracted_data["words"].append(word)
                extracted_data["bounding_boxes"].append(bbox)

        # Save the extracted data to a JSON file
        filename = os.path.basename(filepath).split('.')[0] + ".json"
        extracted_filepath = os.path.join(EXTRACTED_FOLDER, filename)
        with open(extracted_filepath, "w", encoding="utf-8") as file:
            json.dump(extracted_data, file, indent=4)

        return extracted_filepath
    except Exception as e:
        return f"Error processing invoice: {e}"

if __name__ == "__main__":
    sample_path = "./data/invoices/sample_invoice.jpg"
    result = process_invoice(sample_path)
    print(f"OCR Output saved to: {result}")
