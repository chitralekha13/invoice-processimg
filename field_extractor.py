import spacy
import re

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_fields_with_spacy(text):
    doc = nlp(text)

    extracted_fields = {
        "Invoice Number": None,
        "Client Number": None,
        "Invoice Date": None,
        "Due Date": None,
        "Total Due": None
    }

    # Regex rules to match common invoice fields
    invoice_number = re.search(r"(Invoice\s*Number|Invoice\s*#)\s*[:\-]?\s*(\w+)", text, re.IGNORECASE)
    client_number = re.search(r"(Client\s*Number)\s*[:\-]?\s*(\w+)", text, re.IGNORECASE)
    invoice_date = re.search(r"(Invoice\s*Date)\s*[:\-]?\s*([\d./-]+)", text, re.IGNORECASE)
    due_date = re.search(r"(Due\s*Date)\s*[:\-]?\s*([\d./-]+)", text, re.IGNORECASE)
    total_due = re.search(r"(Total\s*Due|Amount\s*Due|Total)\s*[:\-]?\s*\$?\s*([\d,]+\.\d{2})", text, re.IGNORECASE)

    if invoice_number: extracted_fields["Invoice Number"] = invoice_number.group(2)
    if client_number: extracted_fields["Client Number"] = client_number.group(2)
    if invoice_date: extracted_fields["Invoice Date"] = invoice_date.group(2)
    if due_date: extracted_fields["Due Date"] = due_date.group(2)
    if total_due: extracted_fields["Total Due"] = total_due.group(2)

    return extracted_fields
