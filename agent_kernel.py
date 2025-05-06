# agent_kernel.py
from ocr_agent import process_invoice
from field_classifier_agent import classify_fields
from approval_agent import route_for_approval

def run_pipeline(file_path: str) -> dict:
    try:
        print("🤖 Agent 1: OCR extraction...")
        extracted_path = process_invoice(file_path)

        print("🤖 Agent 2: Classifying fields...")
        structured_path = classify_fields(extracted_path)

        print("🤖 Agent 3: Routing for approval...")
        result = route_for_approval(structured_path)

        return result
    except Exception as e:
        return {
            "error": f"⚠️ Pipeline execution failed: {str(e)}",
            "status": "Error"
        }
