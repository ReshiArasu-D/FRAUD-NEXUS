import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv('d:/KPMG/.env')
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

# 1. Create or get empty header widget
r_w = requests.get(f"{url}/api/now/table/sp_widget?sysparm_query=id=fnx_empty_header", auth=auth, headers=headers)
existing = r_w.json().get('result', [])

if existing:
    header_w_id = existing[0]['sys_id']
    print("Empty header widget exists:", header_w_id)
else:
    payload = {
        "name": "FRAUDNEXUS Empty Header",
        "id": "fnx_empty_header",
        "template": "<!-- empty header -->",
        "css": "header, .navbar, .navbar-default, #sp-nav-bar { display: none !important; height: 0 !important; margin: 0 !important; padding: 0 !important; }",
        "public": "true"
    }
    r_create = requests.post(f"{url}/api/now/table/sp_widget", auth=auth, headers=headers, json=payload)
    header_w_id = r_create.json()['result']['sys_id']
    print("Created empty header widget:", header_w_id)

# 2. Assign header_w_id to sp_portal 'fnx'
r_portal = requests.get(f"{url}/api/now/table/sp_portal?sysparm_query=url_suffix=fnx", auth=auth, headers=headers)
portal_id = r_portal.json()['result'][0]['sys_id']

r_patch = requests.patch(
    f"{url}/api/now/table/sp_portal/{portal_id}",
    auth=auth, headers=headers,
    json={"header": header_w_id}
)
print("Updated sp_portal with empty header widget (status):", r_patch.status_code)

# 3. Also update portal css_variables to completely eliminate navbar height
r_patch_css = requests.patch(
    f"{url}/api/now/table/sp_portal/{portal_id}",
    auth=auth, headers=headers,
    json={"css_variables": "$navbar-height: 0px !important;\n$grid-gutter-width: 0px !default;"}
)
print("Updated sp_portal css_variables (status):", r_patch_css.status_code)
