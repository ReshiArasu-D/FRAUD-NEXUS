import requests
import os
import time
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

def add_field(table: str, element: str, label: str, internal_type: str, max_length: str = "100", mandatory: bool = False, reference: str = "", default_value: str = ""):
    # 1. Check if exists
    try:
        r_chk = requests.get(f"{url}/api/now/table/sys_dictionary?sysparm_query=name={table}^element={element}", auth=auth, headers=headers, timeout=15)
        if r_chk.status_code == 200 and len(r_chk.json().get('result', [])) > 0:
            print(f"  [EXISTS] {table}.{element}")
            return True
    except Exception as e:
        print(f"  [CHECK ERR] {table}.{element}: {e}")

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

    try:
        r_post = requests.post(f"{url}/api/now/table/sys_dictionary", auth=auth, headers=headers, json=payload, timeout=30)
        if r_post.status_code in [200, 201]:
            print(f"  [CREATED] {table}.{element} ({label})")
            return True
        else:
            print(f"  [FAILED] {table}.{element}: {r_post.status_code} - {r_post.text[:150]}")
            return False
    except Exception as e:
        print(f"  [TIMEOUT/ERR] {table}.{element}: {e}")
        return False

# Define all fields to ensure
fields_to_add = [
    # Customer
    ("u_x_fnx_customer", "u_customer_id", "Customer ID", "string", "50", False, "", "javascript:getNextObjNumberPadded();"),
    ("u_x_fnx_customer", "u_user", "User", "reference", "32", True, "sys_user", ""),
    ("u_x_fnx_customer", "u_name", "Full Name", "string", "100", True, "", ""),
    ("u_x_fnx_customer", "u_email", "Email", "string", "100", True, "", ""),
    ("u_x_fnx_customer", "u_mobile", "Mobile", "string", "40", True, "", ""),
    ("u_x_fnx_customer", "u_status", "Status", "choice", "40", False, "", "Active"),
    ("u_x_fnx_customer", "u_date_of_birth", "Date of Birth", "glide_date", "40", False, "", ""),
    ("u_x_fnx_customer", "u_government_id_type", "Government ID Type", "choice", "40", False, "", ""),
    ("u_x_fnx_customer", "u_masked_government_id", "Masked Government ID", "string", "50", False, "", ""),
    ("u_x_fnx_customer", "u_proof_attachment", "Proof Attachment", "string", "255", False, "", ""),
    ("u_x_fnx_customer", "u_kyc_status", "KYC Status", "choice", "40", False, "", "Pending"),
    ("u_x_fnx_customer", "u_kyc_reviewed_by", "KYC Reviewed By", "reference", "32", False, "sys_user", ""),
    ("u_x_fnx_customer", "u_kyc_reviewed_on", "KYC Reviewed On", "glide_date_time", "40", False, "", ""),
    ("u_x_fnx_customer", "u_kyc_notes", "KYC Notes", "string", "4000", False, "", ""),

    # Case
    ("u_x_fnx_case", "u_customer", "Customer", "reference", "32", False, "u_x_fnx_customer", ""),
    ("u_x_fnx_case", "u_customer_status", "Customer Status", "choice", "40", False, "", "Unknown"),
    ("u_x_fnx_case", "u_type", "Fraud Type", "choice", "50", True, "", "Payment Fraud"),
    ("u_x_fnx_case", "u_classification", "Classification", "string", "100", False, "", ""),
    ("u_x_fnx_case", "u_subtype", "Subtype", "string", "100", False, "", ""),
    ("u_x_fnx_case", "u_severity", "Severity", "choice", "40", False, "", "Medium"),
    ("u_x_fnx_case", "u_risk_score", "Risk Score", "integer", "40", False, "", "0"),
    ("u_x_fnx_case", "u_exposure", "Exposure Amount", "decimal", "40", False, "", "0"),
    ("u_x_fnx_case", "u_blocked_amount", "Blocked Amount", "decimal", "40", False, "", "0"),
    ("u_x_fnx_case", "u_recovered_amount", "Recovered Amount", "decimal", "40", False, "", "0"),
    ("u_x_fnx_case", "u_stage", "Stage", "choice", "40", False, "", "New"),
    ("u_x_fnx_case", "u_status", "Status", "choice", "40", False, "", "New"),
    ("u_x_fnx_case", "u_source", "Source", "choice", "40", False, "", "Portal"),
    ("u_x_fnx_case", "u_reporter", "Reporter", "reference", "32", False, "sys_user", ""),
    ("u_x_fnx_case", "u_suggested_handler", "Suggested Handler", "reference", "32", False, "sys_user", ""),
    ("u_x_fnx_case", "u_assigned_handler", "Assigned Handler", "reference", "32", False, "sys_user", ""),
    ("u_x_fnx_case", "u_incident_date", "Incident Date", "glide_date", "40", True, "", ""),
    ("u_x_fnx_case", "u_incident_time", "Incident Time", "string", "20", False, "", ""),
    ("u_x_fnx_case", "u_location", "Location", "string", "200", False, "", ""),
    ("u_x_fnx_case", "u_area", "Area", "string", "100", False, "", ""),
    ("u_x_fnx_case", "u_pincode", "Pincode", "string", "20", False, "", ""),
    ("u_x_fnx_case", "u_digital_platform", "Digital Platform", "string", "100", False, "", ""),
    ("u_x_fnx_case", "u_outcome", "Outcome", "choice", "40", False, "", ""),
    ("u_x_fnx_case", "u_closure_notes", "Closure Notes", "string", "4000", False, "", ""),

    # Evidence
    ("u_x_fnx_evidence", "u_number", "Evidence ID", "string", "50", False, "", "javascript:getNextObjNumberPadded();"),
    ("u_x_fnx_evidence", "u_case", "Case", "reference", "32", True, "u_x_fnx_case", ""),
    ("u_x_fnx_evidence", "u_evidence_type", "Evidence Type", "choice", "50", True, "", "Document"),
    ("u_x_fnx_evidence", "u_attachment", "Attachment", "string", "255", False, "", ""),
    ("u_x_fnx_evidence", "u_source", "Source", "choice", "40", False, "", "Customer"),
    ("u_x_fnx_evidence", "u_uploaded_by", "Uploaded By", "reference", "32", False, "sys_user", ""),
    ("u_x_fnx_evidence", "u_uploaded_on", "Uploaded On", "glide_date_time", "40", False, "", ""),
    ("u_x_fnx_evidence", "u_processing_status", "Processing Status", "choice", "40", False, "", "Uploaded"),
    ("u_x_fnx_evidence", "u_hash", "File Hash", "string", "128", False, "", ""),
    ("u_x_fnx_evidence", "u_extracted_entities", "Extracted Entities", "string", "4000", False, "", ""),
    ("u_x_fnx_evidence", "u_description", "Description", "string", "1000", False, "", ""),
    ("u_x_fnx_evidence", "u_verification_status", "Verification Status", "choice", "40", False, "", "Pending"),

    # Custody Log
    ("u_x_fnx_custody_log", "u_evidence", "Evidence", "reference", "32", True, "u_x_fnx_evidence", ""),
    ("u_x_fnx_custody_log", "u_action", "Action", "choice", "40", False, "", "Uploaded"),
    ("u_x_fnx_custody_log", "u_performed_by", "Performed By", "reference", "32", False, "sys_user", ""),
    ("u_x_fnx_custody_log", "u_timestamp", "Timestamp", "glide_date_time", "40", False, "", ""),
    ("u_x_fnx_custody_log", "u_hash", "Hash", "string", "128", False, "", ""),
    ("u_x_fnx_custody_log", "u_notes", "Notes", "string", "1000", False, "", ""),

    # Audit
    ("u_x_fnx_audit", "u_case", "Case", "reference", "32", False, "u_x_fnx_case", ""),
    ("u_x_fnx_audit", "u_record_type", "Record Type", "string", "50", False, "", ""),
    ("u_x_fnx_audit", "u_record_id", "Record ID", "string", "50", False, "", ""),
    ("u_x_fnx_audit", "u_action", "Action", "string", "50", False, "", ""),
    ("u_x_fnx_audit", "u_field", "Field", "string", "50", False, "", ""),
    ("u_x_fnx_audit", "u_old_value", "Old Value", "string", "1000", False, "", ""),
    ("u_x_fnx_audit", "u_new_value", "New Value", "string", "1000", False, "", ""),
    ("u_x_fnx_audit", "u_performed_by", "Performed By", "reference", "32", False, "sys_user", ""),
    ("u_x_fnx_audit", "u_timestamp", "Timestamp", "glide_date_time", "40", False, "", ""),
    ("u_x_fnx_audit", "u_details", "Details", "string", "4000", False, "", "")
]

print(f"Total fields to process: {len(fields_to_add)}")
for i, f in enumerate(fields_to_add):
    print(f"[{i+1}/{len(fields_to_add)}] Processing {f[0]}.{f[1]}...")
    add_field(*f)
    time.sleep(0.5)

print("\nAll fields processed successfully!")
