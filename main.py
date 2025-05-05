import os
import re
import pandas as pd
from flask import Flask, request
from ocr_agent import extract_text_from_image

# Initialize Flask app
app = Flask(__name__)

# Paths
INVOICES_FOLDER = "data/invoices/"
PROCESSED_FOLDER = "data/processed/"
OUTPUT_CSV_PATH = "organized_invoices.csv"
VALIDATED_CSV_PATH = "validated_invoices.csv"
app.config['UPLOAD_FOLDER'] = INVOICES_FOLDER

# Ensure necessary directories exist
os.makedirs(INVOICES_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Function to parse invoice text
def parse_invoice_text(text):
    """
    Parse extracted invoice text to identify relevant fields.
    :param text: Extracted text from the invoice.
    :return: A dictionary of structured fields.
    """
    try:
        invoice_data = {
            "Invoice Number": re.search(r"Invoice\s*#\s*(\d+)", text, re.IGNORECASE).group(1) if re.search(r"Invoice\s*#\s*(\d+)", text, re.IGNORECASE) else None,
            "Date": re.search(r"Date\s*[:\-\s]*([\d/\-]+)", text, re.IGNORECASE).group(1) if re.search(r"Date\s*[:\-\s]*([\d/\-]+)", text, re.IGNORECASE) else None,
            "Amount": re.search(r"Total\s*Amount\s*[:$]\s*(\d+\.\d{2})", text, re.IGNORECASE).group(1) if re.search(r"Total\s*Amount\s*[:$]\s*(\d+\.\d{2})", text, re.IGNORECASE) else None,
            "Vendor Name": re.search(r"Vendor\s*[:\-\s]*(\w+(\s\w+)*)", text, re.IGNORECASE).group(1) if re.search(r"Vendor\s*[:\-\s]*(\w+(\s\w+)*)", text, re.IGNORECASE) else None,
        }
        return invoice_data
    except Exception as e:
        print(f"Error parsing text: {e}")
        return {}

# Function to validate data
def validate_data(df):
    """
    Validate the extracted and structured invoice data.
    :param df: Pandas DataFrame containing the invoice data.
    :return: A tuple (valid_data, errors).
    """
    errors = []
    valid_data = []

    for _, row in df.iterrows():
        row_errors = []

        # Validate Invoice Number
        if not row["Invoice Number"] or not str(row["Invoice Number"]).isdigit():
            row_errors.append("Invalid or missing Invoice Number.")

        # Validate Date (basic check)
        if not row["Date"]:
            row_errors.append("Missing Date.")
        else:
            try:
                pd.to_datetime(row["Date"], format='%Y-%m-%d', errors='raise')
            except ValueError:
                row_errors.append("Invalid Date format.")

        # Validate Amount
        if not row["Amount"] or not str(row["Amount"]).replace('.', '', 1).isdigit():
            row_errors.append("Invalid or missing Amount.")

        # Collect valid rows or log errors
        if row_errors:
            errors.append({"File Name": row["File Name"], "Errors": row_errors})
        else:
            valid_data.append(row)

    return pd.DataFrame(valid_data), errors

# Function to organize data into Excel
def organize_data_into_excel(extracted_text, invoice_filename):
    """
    Organize extracted text into a structured Excel file.
    :param extracted_text: The text extracted from the invoice.
    :param invoice_filename: The original invoice filename.
    :return: The path to the saved Excel file.
    """
    organized_data = parse_invoice_text(extracted_text)
    organized_data = {"Field": organized_data.keys(), "Value": organized_data.values()}
    
    df = pd.DataFrame(organized_data)
    excel_filepath = os.path.join(PROCESSED_FOLDER, invoice_filename.replace(".txt", ".xlsx"))
    
    # Save to Excel
    df.to_excel(excel_filepath, index=False)
    print(f"Organized data saved to {excel_filepath}")
    return excel_filepath

# Flask route for file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in the request", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Extract text and organize into Excel
        extracted_text = extract_text_from_image(filepath)
        organize_data_into_excel(extracted_text, os.path.basename(filepath))
        return f"File {file.filename} uploaded and processed successfully!", 200

if __name__ == "__main__":
    # Step 1: Process all invoices in the folder
    invoice_files = [os.path.join(INVOICES_FOLDER, f) for f in os.listdir(INVOICES_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.pdf'))]
    
    processed_data = []
    for invoice_file in invoice_files:
        print(f"Processing file: {invoice_file}")
        extracted_text = extract_text_from_image(invoice_file)
        structured_data = parse_invoice_text(extracted_text)
        structured_data["File Name"] = os.path.basename(invoice_file)
        processed_data.append(structured_data)

    # Save organized data to CSV
    df = pd.DataFrame(processed_data)
    df.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"Organized data saved to {OUTPUT_CSV_PATH}")

    # Step 2: Validate the data
    df_valid, validation_errors = validate_data(df)
    df_valid.to_csv(VALIDATED_CSV_PATH, index=False)
    print(f"Validated data saved to {VALIDATED_CSV_PATH}")

    # Log validation errors
    if validation_errors:
        print("\nValidation Errors Found:")
        for error in validation_errors:
            print(f"File: {error['File Name']}, Errors: {', '.join(error['Errors'])}")
    else:
        print("\nNo validation errors found.")

    # Start Flask app
    app.run(debug=True)
