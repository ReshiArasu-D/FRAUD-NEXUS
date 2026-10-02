import requests
import os
import time
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

def ensure_number_maintenance(table: str, prefix: str, digits: int = 6):
    r = requests.get(f"{url}/api/now/table/sys_number?sysparm_query=category={table}", auth=auth, headers=headers)
    existing = r.json().get('result', [])
    if existing:
        print(f"Number maintenance exists for {table}: {existing[0].get('prefix')}")
        return
    payload = {
        "category": table,
        "prefix": prefix,
        "maximum_digits": str(digits),
        "number": "1000"
    }
    r_post = requests.post(f"{url}/api/now/table/sys_number", auth=auth, headers=headers, json=payload)
    print(f"Configured Number Maintenance for {table}: status {r_post.status_code}")

def ensure_field(table: str, element: str, label: str, internal_type: str, max_length: str = "100", mandatory: bool = False, reference: str = "", default_value: str = ""):
    # Check if field exists
    r_check = requests.get(f"{url}/api/now/table/sys_dictionary?sysparm_query=name={table}^element={element}", auth=auth, headers=headers)
    existing = r_check.json().get('result', [])
    if existing:
        # print(f"Field {table}.{element} already exists")
        return existing[0]

    payload = {
        "name": table,
        "element": element,
        "column_label": label,
        "internal_type": internal_type,
        "max_length": max_length,
        "mandatory": "true" if mandatory else "false",
        "read_only": "false",
        "active": "true"
    }
    if reference:
        payload["reference"] = reference
    if default_value:
        payload["default_value"] = default_value

    r_post = requests.post(f"{url}/api/now/table/sys_dictionary", auth=auth, headers=headers, json=payload)
    if r_post.status_code in [200, 201]:
        print(f"Created field: {table}.{element} ({label})")
        return r_post.json().get('result')
    else:
        print(f"Failed creating field {table}.{element}: {r_post.text[:200]}")
        return None

def ensure_choice(table: str, element: str, label: str, value: str, sequence: int = 0):
    r_check = requests.get(f"{url}/api/now/table/sys_choice?sysparm_query=name={table}^element={element}^value={value}", auth=auth, headers=headers)
    existing = r_check.json().get('result', [])
    if existing:
        return
    payload = {
        "name": table,
        "element": element,
        "label": label,
        "value": value,
        "language": "en",
        "sequence": str(sequence),
        "inactive": "false"
    }
    requests.post(f"{url}/api/now/table/sys_choice", auth=auth, headers=headers, json=payload)

print("--- 1. NUMBER MAINTENANCE ---")
ensure_number_maintenance("u_x_fnx_case", "FNX-2026-", 6)
ensure_number_maintenance("u_x_fnx_customer", "CNX-2026-", 6)
ensure_number_maintenance("u_x_fnx_evidence", "EV", 6)

print("\n--- 2. FIELDS FOR u_x_fnx_customer ---")
ensure_field("u_x_fnx_customer", "u_customer_id", "Customer ID", "string", "50", default_value="javascript:getNextObjNumberPadded();")
ensure_field("u_x_fnx_customer", "u_user", "User", "reference", reference="sys_user", mandatory=True)
ensure_field("u_x_fnx_customer", "u_name", "Full Name", "string", "100", mandatory=True)
ensure_field("u_x_fnx_customer", "u_email", "Email", "string", "100", mandatory=True)
ensure_field("u_x_fnx_customer", "u_mobile", "Mobile", "string", "40", mandatory=True)
ensure_field("u_x_fnx_customer", "u_status", "Status", "choice", default_value="Active")
for idx, ch in enumerate(["Active", "Inactive", "Suspended"]):
    ensure_choice("u_x_fnx_customer", "u_status", ch, ch, idx)

ensure_field("u_x_fnx_customer", "u_date_of_birth", "Date of Birth", "glide_date")
ensure_field("u_x_fnx_customer", "u_government_id_type", "Government ID Type", "choice")
for idx, ch in enumerate(["Aadhaar", "PAN", "Passport", "Driving Licence", "Voter ID", "Other"]):
    ensure_choice("u_x_fnx_customer", "u_government_id_type", ch, ch, idx)

ensure_field("u_x_fnx_customer", "u_masked_government_id", "Masked Government ID", "string", "50")
ensure_field("u_x_fnx_customer", "u_proof_attachment", "Proof Attachment", "string", "255")
ensure_field("u_x_fnx_customer", "u_kyc_status", "KYC Status", "choice", default_value="Pending")
for idx, ch in enumerate(["Pending", "Under Review", "Verified", "Rejected"]):
    ensure_choice("u_x_fnx_customer", "u_kyc_status", ch, ch, idx)

ensure_field("u_x_fnx_customer", "u_kyc_reviewed_by", "KYC Reviewed By", "reference", reference="sys_user")
ensure_field("u_x_fnx_customer", "u_kyc_reviewed_on", "KYC Reviewed On", "glide_date_time")
ensure_field("u_x_fnx_customer", "u_kyc_notes", "KYC Notes", "string", "4000")

print("\n--- 3. FIELDS FOR u_x_fnx_case ---")
ensure_field("u_x_fnx_case", "u_customer", "Customer", "reference", reference="u_x_fnx_customer")
ensure_field("u_x_fnx_case", "u_customer_status", "Customer Status", "choice", default_value="Unknown")
for idx, ch in enumerate(["Known", "Unverified", "Unknown"]):
    ensure_choice("u_x_fnx_case", "u_customer_status", ch, ch, idx)

ensure_field("u_x_fnx_case", "u_type", "Fraud Type", "choice", mandatory=True)
fraud_types = [
    "Payment Fraud", "Unauthorized Transaction", "Phishing",
    "Account Compromise", "Identity Theft", "Cyber Fraud",
    "Money Laundering", "Financial Crime", "Other"
]
for idx, ch in enumerate(fraud_types):
    ensure_choice("u_x_fnx_case", "u_type", ch, ch, idx)

ensure_field("u_x_fnx_case", "u_classification", "Classification", "string", "100")
ensure_field("u_x_fnx_case", "u_subtype", "Subtype", "string", "100")
ensure_field("u_x_fnx_case", "u_severity", "Severity", "choice", default_value="Medium")
for idx, ch in enumerate(["Low", "Medium", "High", "Critical"]):
    ensure_choice("u_x_fnx_case", "u_severity", ch, ch, idx)

ensure_field("u_x_fnx_case", "u_risk_score", "Risk Score", "integer", default_value="0")
ensure_field("u_x_fnx_case", "u_exposure", "Exposure Amount", "decimal", default_value="0")
ensure_field("u_x_fnx_case", "u_blocked_amount", "Blocked Amount", "decimal", default_value="0")
ensure_field("u_x_fnx_case", "u_recovered_amount", "Recovered Amount", "decimal", default_value="0")

ensure_field("u_x_fnx_case", "u_stage", "Stage", "choice", default_value="New")
for idx, ch in enumerate(["New", "Initial Review", "Investigation", "Resolved", "Closed"]):
    ensure_choice("u_x_fnx_case", "u_stage", ch, ch, idx)

ensure_field("u_x_fnx_case", "u_status", "Status", "choice", default_value="New")
for idx, ch in enumerate(["New", "Open", "In Progress", "Pending", "Resolved", "Closed"]):
    ensure_choice("u_x_fnx_case", "u_status", ch, ch, idx)

ensure_field("u_x_fnx_case", "u_source", "Source", "choice", default_value="Portal")
for idx, ch in enumerate(["Portal", "AML", "Fraud Engine", "SIEM", "Email"]):
    ensure_choice("u_x_fnx_case", "u_source", ch, ch, idx)

ensure_field("u_x_fnx_case", "u_reporter", "Reporter", "reference", reference="sys_user")
ensure_field("u_x_fnx_case", "u_suggested_handler", "Suggested Handler", "reference", reference="sys_user")
ensure_field("u_x_fnx_case", "u_assigned_handler", "Assigned Handler", "reference", reference="sys_user")
ensure_field("u_x_fnx_case", "u_incident_date", "Incident Date", "glide_date", mandatory=True)
ensure_field("u_x_fnx_case", "u_incident_time", "Incident Time", "string", "20")
ensure_field("u_x_fnx_case", "u_location", "Location", "string", "200")
ensure_field("u_x_fnx_case", "u_area", "Area", "string", "100")
ensure_field("u_x_fnx_case", "u_pincode", "Pincode", "string", "20")
ensure_field("u_x_fnx_case", "u_digital_platform", "Digital Platform", "string", "100")

ensure_field("u_x_fnx_case", "u_outcome", "Outcome", "choice")
for idx, ch in enumerate(["Confirmed Fraud", "Suspicious – Inconclusive", "False Positive", "No Fraud"]):
    ensure_choice("u_x_fnx_case", "u_outcome", ch, ch, idx)

ensure_field("u_x_fnx_case", "u_closure_notes", "Closure Notes", "string", "4000")

print("\n--- 4. FIELDS FOR u_x_fnx_evidence ---")
ensure_field("u_x_fnx_evidence", "u_number", "Evidence ID", "string", "50", default_value="javascript:getNextObjNumberPadded();")
ensure_field("u_x_fnx_evidence", "u_case", "Case", "reference", reference="u_x_fnx_case", mandatory=True)
ensure_field("u_x_fnx_evidence", "u_evidence_type", "Evidence Type", "choice", mandatory=True)
evidence_types = ["Image", "Video", "Audio", "PDF", "Document", "Spreadsheet", "Email", "Chat Export", "Text", "URL", "Transaction Reference", "Other"]
for idx, ch in enumerate(evidence_types):
    ensure_choice("u_x_fnx_evidence", "u_evidence_type", ch, ch, idx)

ensure_field("u_x_fnx_evidence", "u_attachment", "Attachment", "string", "255")
ensure_field("u_x_fnx_evidence", "u_source", "Source", "choice", default_value="Customer")
for idx, ch in enumerate(["Customer", "Investigator", "External Feed", "Email"]):
    ensure_choice("u_x_fnx_evidence", "u_source", ch, ch, idx)

ensure_field("u_x_fnx_evidence", "u_uploaded_by", "Uploaded By", "reference", reference="sys_user")
ensure_field("u_x_fnx_evidence", "u_uploaded_on", "Uploaded On", "glide_date_time")
ensure_field("u_x_fnx_evidence", "u_processing_status", "Processing Status", "choice", default_value="Uploaded")
for idx, ch in enumerate(["Uploaded", "Processing", "Processed", "Failed", "Reviewed"]):
    ensure_choice("u_x_fnx_evidence", "u_processing_status", ch, ch, idx)

ensure_field("u_x_fnx_evidence", "u_hash", "File Hash", "string", "128")
ensure_field("u_x_fnx_evidence", "u_extracted_entities", "Extracted Entities", "string", "4000")
ensure_field("u_x_fnx_evidence", "u_description", "Description", "string", "1000")
ensure_field("u_x_fnx_evidence", "u_verification_status", "Verification Status", "choice", default_value="Pending")
for idx, ch in enumerate(["Pending", "Verified", "Rejected"]):
    ensure_choice("u_x_fnx_evidence", "u_verification_status", ch, ch, idx)

print("\n--- 5. FIELDS FOR u_x_fnx_custody_log ---")
ensure_field("u_x_fnx_custody_log", "u_evidence", "Evidence", "reference", reference="u_x_fnx_evidence", mandatory=True)
ensure_field("u_x_fnx_custody_log", "u_action", "Action", "choice")
for idx, ch in enumerate(["Uploaded", "Registered", "Processed", "Viewed", "Reviewed", "Verified", "Rejected"]):
    ensure_choice("u_x_fnx_custody_log", "u_action", ch, ch, idx)

ensure_field("u_x_fnx_custody_log", "u_performed_by", "Performed By", "reference", reference="sys_user")
ensure_field("u_x_fnx_custody_log", "u_timestamp", "Timestamp", "glide_date_time")
ensure_field("u_x_fnx_custody_log", "u_hash", "Hash", "string", "128")
ensure_field("u_x_fnx_custody_log", "u_notes", "Notes", "string", "1000")

print("\n--- 6. FIELDS FOR u_x_fnx_audit ---")
ensure_field("u_x_fnx_audit", "u_case", "Case", "reference", reference="u_x_fnx_case")
ensure_field("u_x_fnx_audit", "u_record_type", "Record Type", "string", "50")
ensure_field("u_x_fnx_audit", "u_record_id", "Record ID", "string", "50")
ensure_field("u_x_fnx_audit", "u_action", "Action", "string", "50")
ensure_field("u_x_fnx_audit", "u_field", "Field", "string", "50")
ensure_field("u_x_fnx_audit", "u_old_value", "Old Value", "string", "1000")
ensure_field("u_x_fnx_audit", "u_new_value", "New Value", "string", "1000")
ensure_field("u_x_fnx_audit", "u_performed_by", "Performed By", "reference", reference="sys_user")
ensure_field("u_x_fnx_audit", "u_timestamp", "Timestamp", "glide_date_time")
ensure_field("u_x_fnx_audit", "u_details", "Details", "string", "4000")

print("\n=== SCHEMA CONFIGURATION COMPLETED ===")
