import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

# Test inserting a field in sys_dictionary for u_x_fnx_customer
dict_payload = {
    "name": "u_x_fnx_customer",
    "element": "u_email",
    "column_label": "Email",
    "internal_type": "string",
    "max_length": "100",
    "mandatory": "false"
}

r = requests.post(f"{url}/api/now/table/sys_dictionary", auth=auth, headers=headers, json=dict_payload)
print("sys_dictionary insert status:", r.status_code)
if r.status_code in [200, 201]:
    print("Created field:", r.json()['result'].get('element'))
    
    # Now let's test inserting a record in u_x_fnx_customer with u_email!
    rec_payload = {
        "u_email": "test@example.com"
    }
    r_rec = requests.post(f"{url}/api/now/table/u_x_fnx_customer", auth=auth, headers=headers, json=rec_payload)
    print("Record insert status:", r_rec.status_code)
    print("Record result:", r_rec.json())
else:
    print("Error:", r.text[:300])
