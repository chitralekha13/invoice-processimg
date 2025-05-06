# approval_agent.py

import pandas as pd

def route_for_approval(structured_csv_path):
    try:
        if not structured_csv_path or not structured_csv_path.endswith(".csv"):
            raise ValueError("Invalid CSV path")

        df = pd.read_csv(structured_csv_path)
        if df.empty or "Total Due" not in df.columns:
            raise ValueError("Missing or empty 'Total Due' field")

        total_due_str = str(df.loc[0, "Total Due"]).replace(",", "").replace("$", "").strip()

        routed_to = "Unknown"
        try:
            amount = float(total_due_str)
            if amount < 1000:
                routed_to = "Accounts Payable"
            elif amount < 5000:
                routed_to = "Finance Department"
            else:
                routed_to = "Director Approval"
        except ValueError:
            routed_to = "Manual Review"

        return {
            "routed_to": routed_to,
            "status": "Pending Approval"
        }

    except Exception as e:
        return {
            "error": f"Approval routing failed: {str(e)}",
            "status": "Error"
        }
