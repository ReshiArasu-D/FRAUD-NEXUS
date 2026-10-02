import os
import requests
from dotenv import load_dotenv

load_dotenv('d:/KPMG/.env')
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

fields = [
    ("u_x_fnx_customer", "u_gender", "Gender", "choice", "40"),
    ("u_x_fnx_customer", "u_occupation", "Occupation", "string", "100"),
    ("u_x_fnx_customer", "u_address", "Address", "string", "500"),
]

for table, element, label, itype, max_len in fields:
    # check
    r_chk = requests.get(f"{url}/api/now/table/sys_dictionary?sysparm_query=name={table}^element={element}", auth=auth, headers=headers)
    if r_chk.json().get('result', []):
        print(f"[EXISTS] {table}.{element}")
        continue
    payload = {
        "name": table,
        "element": element,
        "column_label": label,
        "internal_type": itype,
        "max_length": max_len,
        "active": "true"
    }
    r = requests.post(f"{url}/api/now/table/sys_dictionary", auth=auth, headers=headers, json=payload)
    print(f"[{r.status_code}] Created {table}.{element}")
