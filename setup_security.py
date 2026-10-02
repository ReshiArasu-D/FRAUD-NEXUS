import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

def ensure_role(name: str, desc: str):
    r_chk = requests.get(f"{url}/api/now/table/sys_user_role?sysparm_query=name={name}", auth=auth, headers=headers)
    existing = r_chk.json().get('result', [])
    if existing:
        print(f"Role exists: {name}")
        return existing[0]['sys_id']
    payload = {
        "name": name,
        "description": desc
    }
    r = requests.post(f"{url}/api/now/table/sys_user_role", auth=auth, headers=headers, json=payload)
    print(f"Created role: {name} (status {r.status_code})")
    return r.json().get('result', {}).get('sys_id')

def ensure_acl(name: str, operation: str, script: str = "", condition: str = ""):
    # Check existing acl
    r_chk = requests.get(f"{url}/api/now/table/sys_security_acl?sysparm_query=name={name}^operation={operation}", auth=auth, headers=headers)
    existing = r_chk.json().get('result', [])
    payload = {
        "name": name,
        "operation": operation,
        "type": "record",
        "active": "true",
        "advanced": "true" if script else "false",
        "script": script,
        "condition": condition
    }
    if existing:
        acl_id = existing[0]['sys_id']
        requests.patch(f"{url}/api/now/table/sys_security_acl/{acl_id}", auth=auth, headers=headers, json=payload)
        print(f"Updated ACL: {name} ({operation})")
    else:
        requests.post(f"{url}/api/now/table/sys_security_acl", auth=auth, headers=headers, json=payload)
        print(f"Created ACL: {name} ({operation})")

print("--- Setting up Roles ---")
role_id = ensure_role("x_fnx_customer_user", "FRAUDNEXUS Customer Portal User")

print("\n--- Setting up Record ACLs ---")
# Case read ACL: User can only see their own cases
case_read_script = """answer = false;
if (gs.hasRole('admin') || gs.hasRole('x_fnx_investigator')) {
    answer = true;
} else if (current.u_reporter == gs.getUserID() || (current.u_customer && current.u_customer.u_user == gs.getUserID())) {
    answer = true;
}"""
ensure_acl("u_x_fnx_case", "read", script=case_read_script)

# Customer profile read ACL: User can only see their own customer profile
cust_read_script = """answer = false;
if (gs.hasRole('admin') || gs.hasRole('x_fnx_investigator')) {
    answer = true;
} else if (current.u_user == gs.getUserID()) {
    answer = true;
}"""
ensure_acl("u_x_fnx_customer", "read", script=cust_read_script)

# Evidence read ACL: User can only see evidence for their cases
ev_read_script = """answer = false;
if (gs.hasRole('admin') || gs.hasRole('x_fnx_investigator')) {
    answer = true;
} else if (current.u_case && (current.u_case.u_reporter == gs.getUserID() || (current.u_case.u_customer && current.u_case.u_customer.u_user == gs.getUserID()))) {
    answer = true;
}"""
ensure_acl("u_x_fnx_evidence", "read", script=ev_read_script)

# Custody Log & Audit Log: Delete denied for non-admins (append-only)
deny_delete_script = "answer = gs.hasRole('admin');"
ensure_acl("u_x_fnx_custody_log", "delete", script=deny_delete_script)
ensure_acl("u_x_fnx_audit", "delete", script=deny_delete_script)

print("\nSecurity and ACL configuration completed!")
