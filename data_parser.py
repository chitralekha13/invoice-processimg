import re

def parse_invoice_text(text):
    fields = {}

    patterns = {
        "Invoice Number": r"(?:Invoice\s*Number|Inv\s*#|Invoice\s*No\.?)\s*[:\-]?\s*(\w+)",
        "Client Number": r"(?:Client\s*ID|Client\s*Number)\s*[:\-]?\s*(\w+)",
        "Invoice Date": r"(?:Invoice\s*Date)\s*[:\-]?\s*([\d\/\-]+)",
        "Due Date": r"(?:Due\s*Date)\s*[:\-]?\s*([\d\/\-]+)",
        "Total Due": r"(?:Total\s*Due|Amount\s*Due|Balance\s*Due)\s*[:\-]?\s*\$?([\d,]+\.\d{2})"
    }

    for field, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        fields[field] = match.group(1).strip() if match else ""

    return fields
