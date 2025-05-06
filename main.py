from ocr_agent import extract_text
from field_parser import parse_invoice_text
from data_parser import save_structured_data

if __name__ == "__main__":
    image_path = "data/invoices/invoice3.webp"  # Use correct path
    text = extract_text(image_path)
    print("📝 OCR Text Extracted:\n", text)

    structured_fields = parse_invoice_text(text)
    print("📋 Extracted Fields:\n", structured_fields)

    save_structured_data(structured_fields)
