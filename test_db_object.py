import requests
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

# Check app id
r_app = requests.get(f"{url}/api/now/table/sys_app?sysparm_query=name=FRAUDNEXUS", auth=auth, headers=headers)
app_id = r_app.json()['result'][0]['sys_id']
scope = r_app.json()['result'][0]['scope']

payload = {
    "name": "x_fnx_customer",
    "label": "FRAUDNEXUS Customer",
    "sys_scope": app_id,
    "sys_package": app_id,
    "access": "public",
    "read_access": "true",
    "create_access": "true",
    "update_access": "true",
    "delete_access": "true"
}

r = requests.post(f"{url}/api/now/table/sys_db_object", auth=auth, headers=headers, json=payload)
print("Create sys_db_object status:", r.status_code)
print("Response:", r.text[:300])

# Check if table now exists in sys_db_object or table api
if r.status_code in [200, 201]:
    r_check = requests.get(f"{url}/api/now/table/x_fnx_customer?sysparm_limit=1", auth=auth, headers=headers)
    print("Direct Table API check on x_fnx_customer:", r_check.status_code, r_check.text[:200])
