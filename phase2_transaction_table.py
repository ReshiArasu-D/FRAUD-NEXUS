"""
FRAUDNEXUS Phase 2 — Step 1: Create u_x_fnx_transaction Table
Stores structured financial transaction data linked to fraud cases.
"""
import requests
import os
import time
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv('d:/KPMG/.env')
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

# ============================================================
# 1. Check if table already exists
# ============================================================
print("=" * 60)
print("PHASE 2 — STEP 1: CREATE u_x_fnx_transaction TABLE")
print("=" * 60)

r_check = requests.get(
    f"{url}/api/now/table/sys_db_object?sysparm_query=nameLIKEx_fnx_transaction&sysparm_fields=name,label,sys_id",
    auth=auth, headers=headers
)
existing = r_check.json().get('result', [])
if existing:
    print(f"[SKIP] Table already exists: {existing[0]['name']} (sys_id: {existing[0]['sys_id']})")
    table_sys_id = existing[0]['sys_id']
    table_name = existing[0]['name']
else:
    # Create the table
    table_payload = {
        "name": "u_x_fnx_transaction",
        "label": "FRAUDNEXUS Transaction",
        "is_extendable": "true",
        "create_access_controls": "false",
        "create_module": "false",
        "number_ref": "false"
    }
    r_create = requests.post(
        f"{url}/api/now/table/sys_db_object",
        auth=auth, headers=headers, json=table_payload
    )
    if r_create.status_code in [200, 201]:
        table_sys_id = r_create.json()['result']['sys_id']
        table_name = r_create.json()['result']['name']
        print(f"[CREATED] Table: {table_name} (sys_id: {table_sys_id})")
        time.sleep(2)  # Allow ServiceNow to register the table
    else:
        print(f"[ERROR] Failed to create table: {r_create.status_code} — {r_create.text}")
        exit(1)

# ============================================================
# 2. Add fields to the table
# ============================================================
print("\n--- Adding fields to u_x_fnx_transaction ---")

def add_field(element, field_type, max_length=None, label=None, reference=None, mandatory=False, default_value=None):
    """Add a field to u_x_fnx_transaction if it doesn't already exist."""
    check_r = requests.get(
        f"{url}/api/now/table/sys_dictionary?sysparm_query=name=u_x_fnx_transaction^element={element}",
        auth=auth, headers=headers
    )
    if check_r.json().get('result', []):
        print(f"  [EXISTS] {element}")
        return

    payload = {
        "name": "u_x_fnx_transaction",
        "element": element,
        "internal_type": field_type,
        "column_label": label or element.replace('u_', '').replace('_', ' ').title(),
        "active": "true",
        "mandatory": "true" if mandatory else "false"
    }
    if max_length:
        payload["max_length"] = str(max_length)
    if reference:
        payload["reference"] = reference
    if default_value:
        payload["default_value"] = default_value

    r = requests.post(f"{url}/api/now/table/sys_dictionary", auth=auth, headers=headers, json=payload)
    if r.status_code in [200, 201]:
        print(f"  [ADDED] {element} ({field_type})")
    else:
        print(f"  [ERROR] {element}: {r.status_code}")


def add_choice(element, value, label, sequence=0):
    """Add a choice value for a field."""
    check_r = requests.get(
        f"{url}/api/now/table/sys_choice?sysparm_query=name=u_x_fnx_transaction^element={element}^value={value}",
        auth=auth, headers=headers
    )
    if check_r.json().get('result', []):
        return  # Already exists

    payload = {
        "name": "u_x_fnx_transaction",
        "element": element,
        "value": value,
        "label": label,
        "sequence": str(sequence),
        "language": "en"
    }
    requests.post(f"{url}/api/now/table/sys_choice", auth=auth, headers=headers, json=payload)


# --- Core Reference ---
add_field("u_case", "reference", label="Fraud Case", reference="u_x_fnx_case", mandatory=True)

# --- Payment Mode ---
add_field("u_payment_mode", "string", max_length=100, label="Payment Mode")

# --- Institution ---
add_field("u_institution_name", "string", max_length=200, label="Institution / Organization")
add_field("u_institution_type", "string", max_length=100, label="Institution Type")
add_field("u_branch", "string", max_length=200, label="Branch / Service Location")
add_field("u_platform", "string", max_length=200, label="Application / Platform")

# --- Transaction Reference ---
add_field("u_reference_type", "string", max_length=100, label="Reference Type")
add_field("u_reference_value", "string", max_length=200, label="Reference Value")

# --- Financial ---
add_field("u_amount", "decimal", label="Amount")
add_field("u_currency", "string", max_length=10, label="Currency", default_value="INR")
add_field("u_transaction_date", "glide_date_time", label="Transaction Date/Time")
add_field("u_direction", "string", max_length=40, label="Direction")
add_field("u_transaction_status", "string", max_length=40, label="Transaction Status")
add_field("u_number_of_transactions", "integer", label="Number of Transactions")

# --- People / Entities ---
add_field("u_suspect_name", "string", max_length=200, label="Suspect / Beneficiary Name")
add_field("u_suspect_contact", "string", max_length=200, label="Suspect Contact")
add_field("u_suspect_identifier", "string", max_length=200, label="Suspect Identifier (UPI/Email/Phone)")
add_field("u_communication_channel", "string", max_length=200, label="Communication Channel")

# --- Notes ---
add_field("u_notes", "string", max_length=4000, label="Transaction Notes")
add_field("u_reported_by", "reference", label="Reported By", reference="sys_user")

time.sleep(1)

# ============================================================
# 3. Add Choice Values
# ============================================================
print("\n--- Adding choice values ---")

# Payment Mode choices
payment_modes = [
    "UPI", "Bank Transfer", "IMPS", "NEFT", "RTGS",
    "Debit Card", "Credit Card", "ATM / Cash Withdrawal",
    "Net Banking", "Mobile Banking", "Digital Wallet",
    "QR Code Payment", "Payment Gateway", "Cash", "Cheque",
    "Demand Draft", "Investment / Trading", "Insurance",
    "Loan / Lending", "E-commerce / Merchant Payment",
    "International Transfer", "Other", "I don't know"
]
for i, pm in enumerate(payment_modes):
    add_choice("u_payment_mode", pm, pm, i * 100)
print("  [DONE] Payment Mode choices")

# Institution Type choices
inst_types = [
    "Bank / Financial Institution", "Payment Provider",
    "Payment Application", "Insurance",
    "Investment / Brokerage", "Lending / NBFC",
    "E-commerce / Merchant", "Telecom", "Other"
]
for i, it in enumerate(inst_types):
    add_choice("u_institution_type", it, it, i * 100)
print("  [DONE] Institution Type choices")

# Reference Type choices
ref_types = [
    "UTR", "Transaction ID", "Payment Reference", "Order ID",
    "Cheque Reference", "Policy Reference", "Claim Reference",
    "Loan Application ID", "Investment Order ID", "Other"
]
for i, rt in enumerate(ref_types):
    add_choice("u_reference_type", rt, rt, i * 100)
print("  [DONE] Reference Type choices")

# Direction choices
for i, d in enumerate(["Outgoing (Debit)", "Incoming (Credit)", "Unknown"]):
    add_choice("u_direction", d, d, i * 100)
print("  [DONE] Direction choices")

# Transaction Status choices
for i, s in enumerate(["Completed", "Pending", "Failed", "Reversed", "Disputed", "Unknown"]):
    add_choice("u_transaction_status", s, s, i * 100)
print("  [DONE] Transaction Status choices")

# ============================================================
# 4. Verify
# ============================================================
print("\n--- Verifying table and fields ---")
r_verify = requests.get(
    f"{url}/api/now/table/sys_dictionary?sysparm_query=name=u_x_fnx_transaction^elementSTARTSWITHu_&sysparm_fields=element,internal_type,column_label",
    auth=auth, headers=headers
)
fields = r_verify.json().get('result', [])
print(f"\nTotal fields created: {len(fields)}")
for f in fields:
    print(f"  ✓ {f['element']} ({f.get('internal_type','')}) — {f.get('column_label','')}")

print("\n" + "=" * 60)
print("STEP 1 COMPLETE: u_x_fnx_transaction table ready")
print("=" * 60)
