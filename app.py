from flask import Flask, request, render_template
import os

from ocr_agent import process_invoice
from field_extractor import extract_fields_with_spacy
from data_parser import organize_data

# Flask app config
app = Flask(__name__)
UPLOAD_FOLDER = "./data/invoices/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in the request", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Step 1: OCR
    extracted_file_path = process_invoice(filepath)
    if isinstance(extracted_file_path, str) and extracted_file_path.startswith("Error"):
        return extracted_file_path

    # Step 2: Read text from saved file
    try:
        with open(extracted_file_path, "r", encoding="utf-8") as f:
            extracted_text = f.read()
    except Exception as e:
        return f"Error reading extracted text: {e}"

    # Step 3: Field Extraction
    try:
        extracted_fields = extract_fields_with_spacy(extracted_text)
    except Exception as e:
        return f"Error extracting fields: {e}"

    # Step 4: Organize and Save
    try:
        excel_file = organize_data(extracted_fields)
    except Exception as e:
        return f"Error saving structured data: {e}"

    return f"✅ Invoice processed and structured! Check file: {excel_file}"

if __name__ == '__main__':
    app.run(debug=True)
