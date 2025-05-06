import pandas as pd

def route_for_approval(sk_context):
    path = sk_context["structured_path"]
    try:
        df = pd.read_csv(path)
        due = df.loc[0].get("Total Due", "")
        routed_to = "Accounts Payable" if due and due != "0.00" else "Audit"
        result = {
            "routed_to": routed_to,
            "status": "Pending Approval"
        }
        sk_context["approval_result"] = result
        return sk_context
    except Exception as e:
        sk_context["approval_result"] = {"error": str(e), "status": "Error"}
        return sk_context
