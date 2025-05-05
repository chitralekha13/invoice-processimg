import pandas as pd
import json
import os

PROCESSED_FOLDER = "./data/processed/"
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def organize_data(json_file):
    """
    Converts extracted fields into a structured CSV format.
    """
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            extracted_fields = json.load(file)

        fields = {
            "Invoice Number": extracted_fields.get("Invoice Number", "").strip(),
            "Client Number": extracted_fields.get("Client Number", "").strip(),
            "Invoice Date": extracted_fields.get("Invoice Date", "").strip(),
            "Due Date": extracted_fields.get("Due Date", "").strip(),
            "Total Due": extracted_fields.get("Total Due", "").strip(),
        }

        # Save organized data as a DataFrame
        df = pd.DataFrame(fields.items(), columns=["Field", "Value"])
        output_file = os.path.join(PROCESSED_FOLDER, "structured_data.csv")
        df.to_csv(output_file, index=False)

        return output_file
    except Exception as e:
        return f"Error organizing data: {e}"

if __name__ == "__main__":
    json_path = "./data/processed/fields.json"
    result = organize_data(json_path)
    print(f"Data organized and saved to: {result}")
