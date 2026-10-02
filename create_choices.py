import requests
import os
import time
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

choices_def = [
    # Customer
    ("u_x_fnx_customer", "u_status", ["Active", "Inactive", "Suspended"]),
    ("u_x_fnx_customer", "u_government_id_type", ["Aadhaar", "PAN", "Passport", "Driving Licence", "Voter ID", "Other"]),
    ("u_x_fnx_customer", "u_kyc_status", ["Pending", "Under Review", "Verified", "Rejected"]),

    # Case
    ("u_x_fnx_case", "u_customer_status", ["Known", "Unverified", "Unknown"]),
    ("u_x_fnx_case", "u_type", [
        "Payment Fraud", "Unauthorized Transaction", "Phishing",
        "Account Compromise", "Identity Theft", "Cyber Fraud",
        "Money Laundering", "Financial Crime", "Other"
    ]),
    ("u_x_fnx_case", "u_severity", ["Low", "Medium", "High", "Critical"]),
    ("u_x_fnx_case", "u_stage", ["New", "Initial Review", "Investigation", "Resolved", "Closed"]),
    ("u_x_fnx_case", "u_status", ["New", "Open", "In Progress", "Pending", "Resolved", "Closed"]),
    ("u_x_fnx_case", "u_source", ["Portal", "AML", "Fraud Engine", "SIEM", "Email"]),
    ("u_x_fnx_case", "u_outcome", ["Confirmed Fraud", "Suspicious – Inconclusive", "False Positive", "No Fraud"]),

    # Evidence
    ("u_x_fnx_evidence", "u_evidence_type", [
        "Image", "Video", "Audio", "PDF", "Document", "Spreadsheet",
        "Email", "Chat Export", "Text", "URL", "Transaction Reference", "Other"
    ]),
    ("u_x_fnx_evidence", "u_source", ["Customer", "Investigator", "External Feed", "Email"]),
    ("u_x_fnx_evidence", "u_processing_status", ["Uploaded", "Processing", "Processed", "Failed", "Reviewed"]),
    ("u_x_fnx_evidence", "u_verification_status", ["Pending", "Verified", "Rejected"]),

    # Custody
    ("u_x_fnx_custody_log", "u_action", ["Uploaded", "Registered", "Processed", "Viewed", "Reviewed", "Verified", "Rejected"])
]

def add_choice(table, element, val, seq):
    try:
        r_chk = requests.get(f"{url}/api/now/table/sys_choice?sysparm_query=name={table}^element={element}^value={val}", auth=auth, headers=headers, timeout=10)
        if r_chk.status_code == 200 and len(r_chk.json().get('result', [])) > 0:
            return
        payload = {
            "name": table,
            "element": element,
            "label": val,
            "value": val,
            "language": "en",
            "sequence": str(seq),
            "inactive": "false"
        }
        requests.post(f"{url}/api/now/table/sys_choice", auth=auth, headers=headers, json=payload, timeout=10)
    except Exception as e:
        print(f"Choice err {table}.{element}={val}: {e}")

total_choices = sum(len(c[2]) for c in choices_def)
print(f"Creating {total_choices} choices across all tables...")
count = 0
for tbl, elem, vals in choices_def:
    for idx, v in enumerate(vals):
        add_choice(tbl, elem, v, idx)
        count += 1

print(f"Done! {count} choices verified.")
