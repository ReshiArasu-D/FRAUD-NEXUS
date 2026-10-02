import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

page_id = "e4358577c32b43d0e54832f1b40131d0" # fnx_home
widget_id = "2f258577c32b43d0e54832f1b401317f" # fnx_customer_experience

# 1. Create sp_container
r_con = requests.post(f"{url}/api/now/table/sp_container", auth=auth, headers=headers, json={
    "sp_page": page_id,
    "name": "FRAUDNEXUS Container",
    "order": "1",
    "width": "container-fluid",
    "bootstrap_alt": "false"
})
container_id = r_con.json()['result']['sys_id']
print("Created sp_container:", container_id)

# 2. Create sp_row
r_row = requests.post(f"{url}/api/now/table/sp_row", auth=auth, headers=headers, json={
    "sp_container": container_id,
    "order": "1"
})
row_id = r_row.json()['result']['sys_id']
print("Created sp_row:", row_id)

# 3. Create sp_column
r_col = requests.post(f"{url}/api/now/table/sp_column", auth=auth, headers=headers, json={
    "sp_row": row_id,
    "size": "12",
    "order": "1"
})
col_id = r_col.json()['result']['sys_id']
print("Created sp_column:", col_id)

# 4. Create or update sp_instance linked to column
r_inst = requests.post(f"{url}/api/now/table/sp_instance", auth=auth, headers=headers, json={
    "sp_widget": widget_id,
    "sp_column": col_id,
    "order": "1",
    "title": "FRAUDNEXUS Portal View"
})
print("Created sp_instance linked to column:", r_inst.json()['result']['sys_id'])
