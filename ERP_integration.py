# skills/erp_integration.py

def send_to_erp(structured_data: dict) -> dict:
    try:
        # Simulated ERP logic
        amount = float(structured_data.get("Total", 0))
        department = structured_data.get("Department", "Accounts Payable")

        # Routing logic (mocked)
        if amount > 1000:
            approver = "Finance Manager"
        elif "Software" in structured_data.get("Description", ""):
            approver = "IT Procurement"
        else:
            approver = department

        # Simulated API response from ERP
        return {
            "routed_to": approver,
            "status": "Pending Approval",
            "notes": "Routed through ERP simulation"
        }

    except Exception as e:
        return {
            "error": f"ERP simulation failed: {str(e)}",
            "status": "Error"
        }
