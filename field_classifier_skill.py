import re
import pandas as pd
import os

def classify_fields(sk_context):
    raw_text = sk_context["raw_text"]
    extracted_data = {
        "Invoice Number": re.search(r"Invoice.*?(\\d+)", raw_text, re.IGNORECASE),
        "Invoice Date": re.search(r"Invoice Date[:\\s]*([0-9a-zA-Z \\-/]+)", raw_text, re.IGNORECASE),
        "Due Date": re.search(r"Due Date[:\\s]*([0-9a-zA-Z \\-/]+)", raw_text, re.IGNORECASE),
        "Total Due": re.search(r"Total[:\\s$]*([0-9\\.,]+)", raw_text, re.IGNORECASE),
        "Client Name": re.search(r"Bill To\\s+([a-zA-Z ]+)", raw_text, re.IGNORECASE),
    }
    structured = {key: (match.group(1).strip() if match else "") for key, match in extracted_data.items()}
    df = pd.DataFrame([structured])
    os.makedirs("output", exist_ok=True)
    df.to_csv("output/structured.csv", index=False)
    sk_context["structured_path"] = "output/structured.csv"
    return sk_context
