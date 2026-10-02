import requests
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

# Check app sys_id
r_app = requests.get(f"{url}/api/now/table/sys_app?sysparm_query=name=FRAUDNEXUS", auth=auth, headers=headers)
app_info = r_app.json()['result'][0]
app_id = app_info['sys_id']
scope = app_info['scope']
print(f"Using App: {app_id}, Scope: {scope}")

# Create or check sys_ws_definition
r_ws = requests.get(f"{url}/api/now/table/sys_ws_definition?sysparm_query=service_id=fnx_api", auth=auth, headers=headers)
existing_ws = r_ws.json()['result']

if existing_ws:
    ws_id = existing_ws[0]['sys_id']
    print(f"Existing Scripted REST API found: {ws_id}")
else:
    ws_payload = {
        "name": "FRAUDNEXUS Management API",
        "service_id": "fnx_api",
        "sys_scope": app_id,
        "sys_package": app_id,
        "active": "true"
    }
    r_create = requests.post(f"{url}/api/now/table/sys_ws_definition", auth=auth, headers=headers, json=ws_payload)
    print("Create API status:", r_create.status_code)
    print("Response:", r_create.text[:300])
    if r_create.status_code == 201:
        ws_id = r_create.json()['result']['sys_id']
        print(f"Created Scripted REST API: {ws_id}")
    else:
        # Try without scope/package if scope restriction occurs
        ws_payload.pop("sys_scope", None)
        ws_payload.pop("sys_package", None)
        r_create2 = requests.post(f"{url}/api/now/table/sys_ws_definition", auth=auth, headers=headers, json=ws_payload)
        print("Create API fallback status:", r_create2.status_code, r_create2.text[:300])
        ws_id = r_create2.json()['result']['sys_id']

print("WS ID:", ws_id)
