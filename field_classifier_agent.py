# field_classifier_agent.py
import re
import pandas as pd
import os

def classify_fields(extracted_text: str) -> str:
    # Define patterns
    invoice_number = re.search(r"Invoice\s*(Number|No|#)\s*[:\-]?\s*([A-Za-z0-9\-]+)", extracted_text, re.IGNORECASE)
    invoice_date = re.search(r"Invoice\s*Date\s*[:\-]?\s*([0-9]{1,2}\s\w+\s[0-9]{4})", extracted_text, re.IGNORECASE)
    due_date = re.search(r"Due\s*Date\s*[:\-]?\s*([0-9]{1,2}\s\w+\s[0-9]{4})", extracted_text, re.IGNORECASE)
    client_number = re.search(r"Client\s*(Number|ID)?\s*[:\-]?\s*([A-Za-z0-9\-]+)", extracted_text, re.IGNORECASE)
    total_due = re.search(r"(Total\s*Due|Total)\s*[:\-]?\s*\$?([0-9,]+\.\d{2})", extracted_text, re.IGNORECASE)

    # Store extracted values
    data = {
        "Invoice Number": invoice_number.group(2) if invoice_number else "",
        "Invoice Date": invoice_date.group(1) if invoice_date else "",
        "Due Date": due_date.group(1) if due_date else "",
        "Client Number": client_number.group(2) if client_number else "",
        "Total Due": total_due.group(2) if total_due else ""
    }

    df = pd.DataFrame([data])

    os.makedirs("output", exist_ok=True)
    structured_path = "output/structured_data.csv"
    df.to_csv(structured_path, index=False)

    return structured_path
