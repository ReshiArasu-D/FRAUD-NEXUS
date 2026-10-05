"""
Create u_x_fnx_partner and u_x_fnx_partner_request tables in ServiceNow
along with all required dictionary fields and number maintenance.
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

def ensure_table(table_name, table_label, extends_task=False):
    r_check = requests.get(
        f"{url}/api/now/table/sys_db_object?sysparm_query=name={table_name}&sysparm_fields=name,label,sys_id",
        auth=auth, headers=headers
    )
    existing = r_check.json().get('result', [])
    if existing:
        print(f"[EXISTS] Table: {existing[0]['name']} (sys_id: {existing[0]['sys_id']})")
        return existing[0]['sys_id']

    payload = {
        "name": table_name,
        "label": table_label,
        "is_extendable": "true",
        "create_access_controls": "false",
        "create_module": "false",
        "number_ref": "false"
    }
    if extends_task:
        payload["super_class"] = "06ff39c5c3530310e54832f1b40131f5" # Task sys_id
    
    r_create = requests.post(f"{url}/api/now/table/sys_db_object", auth=auth, headers=headers, json=payload)
    if r_create.status_code in [200, 201]:
        res = r_create.json().get('result', {})
        sys_id = res.get('sys_id')
        print(f"[CREATED] Table: {table_name} (sys_id: {sys_id})")
        time.sleep(3)
        return sys_id
    else:
        print(f"[ERROR] Failed to create {table_name}: {r_create.status_code} - {r_create.text}")
        return None

def add_field(table_name, element, field_type, max_length=None, label=None, reference=None, mandatory=False, default_value=None):
    check_r = requests.get(
        f"{url}/api/now/table/sys_dictionary?sysparm_query=name={table_name}^element={element}",
        auth=auth, headers=headers
    )
    if check_r.json().get('result', []):
        print(f"  [EXISTS] {table_name}.{element}")
        return

    payload = {
        "name": table_name,
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
    if default_value is not None:
        payload["default_value"] = str(default_value)

    r = requests.post(f"{url}/api/now/table/sys_dictionary", auth=auth, headers=headers, json=payload)
    if r.status_code in [200, 201]:
        print(f"  [ADDED] {table_name}.{element} ({field_type})")
    else:
        print(f"  [ERROR] {table_name}.{element}: {r.status_code} - {r.text[:100]}")

def ensure_number_maintenance(category, prefix, start_number=1000, digits=6):
    r_check = requests.get(
        f"{url}/api/now/table/sys_number?sysparm_query=category={category}",
        auth=auth, headers=headers
    )
    existing = r_check.json().get('result', [])
    if existing:
        print(f"[EXISTS] Number maintenance for {category}: prefix {existing[0].get('prefix')}")
        return

    payload = {
        "category": category,
        "prefix": prefix,
        "maximum_digits": str(digits),
        "number": str(start_number)
    }
    r = requests.post(f"{url}/api/now/table/sys_number", auth=auth, headers=headers, json=payload)
    if r.status_code in [200, 201]:
        print(f"[CREATED] Number maintenance for {category}: prefix {prefix}")
    else:
        print(f"[ERROR] Number maintenance {category}: {r.status_code}")

print("==================================================")
print("CREATING u_x_fnx_partner TABLE")
print("==================================================")
ensure_table("u_x_fnx_partner", "FRAUDNEXUS Partner")

# Add fields for u_x_fnx_partner
add_field("u_x_fnx_partner", "u_partner_number", "string", max_length=40, label="Partner Number")
add_field("u_x_fnx_partner", "u_name", "string", max_length=200, label="Partner Name", mandatory=True)
add_field("u_x_fnx_partner", "u_category", "string", max_length=100, label="Category", mandatory=True)
add_field("u_x_fnx_partner", "u_organization", "string", max_length=200, label="Organization", mandatory=True)
add_field("u_x_fnx_partner", "u_description", "string", max_length=4000, label="Description")
add_field("u_x_fnx_partner", "u_contact_person", "string", max_length=100, label="Contact Person")
add_field("u_x_fnx_partner", "u_contact_email", "string", max_length=100, label="Contact Email")
add_field("u_x_fnx_partner", "u_contact_phone", "string", max_length=40, label="Contact Phone")
add_field("u_x_fnx_partner", "u_status", "string", max_length=40, label="Status", default_value="Active")
add_field("u_x_fnx_partner", "u_integration_type", "string", max_length=100, label="Integration Type", default_value="Simulated API")
add_field("u_x_fnx_partner", "u_endpoint_reference", "string", max_length=500, label="Endpoint Reference")
add_field("u_x_fnx_partner", "u_sla", "string", max_length=50, label="SLA", default_value="4 Hours")
add_field("u_x_fnx_partner", "u_demo_flag", "boolean", label="Demo Flag", default_value="true")
add_field("u_x_fnx_partner", "u_active", "boolean", label="Active", default_value="true")
add_field("u_x_fnx_partner", "u_notes", "string", max_length=4000, label="Notes")

ensure_number_maintenance("u_x_fnx_partner", "PRT-", start_number=1000, digits=6)

print("\n==================================================")
print("CREATING u_x_fnx_partner_request TABLE")
print("==================================================")
ensure_table("u_x_fnx_partner_request", "FRAUDNEXUS Partner Request")

# Add fields for u_x_fnx_partner_request
add_field("u_x_fnx_partner_request", "u_request_number", "string", max_length=40, label="Request Number")
add_field("u_x_fnx_partner_request", "u_case", "reference", reference="u_x_fnx_case", label="Case")
add_field("u_x_fnx_partner_request", "u_partner", "reference", reference="u_x_fnx_partner", label="Partner")
add_field("u_x_fnx_partner_request", "u_request_type", "string", max_length=100, label="Request Type")
add_field("u_x_fnx_partner_request", "u_requested_by", "string", max_length=100, label="Requested By")
add_field("u_x_fnx_partner_request", "u_request_date", "glide_date_time", label="Request Date")
add_field("u_x_fnx_partner_request", "u_priority", "string", max_length=40, label="Priority", default_value="High")
add_field("u_x_fnx_partner_request", "u_description", "string", max_length=4000, label="Description")
add_field("u_x_fnx_partner_request", "u_reference", "string", max_length=200, label="Evidence / Reference")
add_field("u_x_fnx_partner_request", "u_status", "string", max_length=40, label="Status", default_value="Submitted")
add_field("u_x_fnx_partner_request", "u_due_date", "glide_date_time", label="Due Date")
add_field("u_x_fnx_partner_request", "u_response", "string", max_length=4000, label="Response")
add_field("u_x_fnx_partner_request", "u_response_date", "glide_date_time", label="Response Date")
add_field("u_x_fnx_partner_request", "u_resolution_notes", "string", max_length=4000, label="Resolution Notes")
add_field("u_x_fnx_partner_request", "u_demo_request", "boolean", label="Demo Request", default_value="true")

ensure_number_maintenance("u_x_fnx_partner_request", "PRTREQ-", start_number=1000, digits=6)

print("\n--- Table Creation Complete ---")
