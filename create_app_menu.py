import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

# 1. Create or get sys_app_application
r_app_chk = requests.get(f"{url}/api/now/table/sys_app_application?sysparm_query=title=FRAUDNEXUS", auth=auth, headers=headers)
existing_app = r_app_chk.json().get('result', [])

if existing_app:
    app_menu_id = existing_app[0]['sys_id']
    print(f"App menu FRAUDNEXUS exists: {app_menu_id}")
else:
    app_payload = {
        "title": "FRAUDNEXUS",
        "description": "Financial & Cyber Fraud Investigation Workspace",
        "order": "100",
        "active": "true"
    }
    r_create_app = requests.post(f"{url}/api/now/table/sys_app_application", auth=auth, headers=headers, json=app_payload)
    app_menu_id = r_create_app.json()['result']['sys_id']
    print(f"Created App menu FRAUDNEXUS: {app_menu_id}")

# 2. Modules definition
modules = [
    {"title": "Customer Portal", "link_type": "DIRECT", "query": "/fnx", "order": "10", "name": ""},
    {"title": "Fraud Cases", "link_type": "LIST", "name": "u_x_fnx_case", "order": "20", "query": ""},
    {"title": "Customers", "link_type": "LIST", "name": "u_x_fnx_customer", "order": "30", "query": ""},
    {"title": "Evidence Registry", "link_type": "LIST", "name": "u_x_fnx_evidence", "order": "40", "query": ""},
    {"title": "Custody Log (Chain of Custody)", "link_type": "LIST", "name": "u_x_fnx_custody_log", "order": "50", "query": ""},
    {"title": "Audit Trail", "link_type": "LIST", "name": "u_x_fnx_audit", "order": "60", "query": ""}
]

for m in modules:
    r_mod_chk = requests.get(f"{url}/api/now/table/sys_app_module?sysparm_query=application={app_menu_id}^title={m['title']}", auth=auth, headers=headers)
    if r_mod_chk.json().get('result', []):
        print(f"Module exists: {m['title']}")
    else:
        mod_payload = {
            "application": app_menu_id,
            "title": m['title'],
            "link_type": m['link_type'],
            "order": m['order'],
            "active": "true"
        }
        if m['name']:
            mod_payload['name'] = m['name']
        if m['query']:
            mod_payload['query'] = m['query']
        r_mod = requests.post(f"{url}/api/now/table/sys_app_module", auth=auth, headers=headers, json=mod_payload)
        print(f"Created module: {m['title']} ({r_mod.status_code})")

print("All FRAUDNEXUS Navigation Modules Configured!")
