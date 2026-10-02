import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv('d:/KPMG/.env')
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

# 1. Check if FRAUDNEXUS Theme already exists
r_chk = requests.get(f"{url}/api/now/table/sp_theme?sysparm_query=name=FRAUDNEXUS Theme", auth=auth, headers=headers)
existing = r_chk.json().get('result', [])

if existing:
    theme_id = existing[0]['sys_id']
    print("Theme already exists:", theme_id)
    # Ensure header is empty
    requests.patch(f"{url}/api/now/table/sp_theme/{theme_id}", auth=auth, headers=headers, json={
        "header": "",
        "footer": "",
        "css_variables": "$navbar-height: 0px !important;\n$grid-gutter-width: 0px !default;"
    })
else:
    theme_payload = {
        "name": "FRAUDNEXUS Theme",
        "header": "",
        "footer": "",
        "navbar_fixed": "false",
        "footer_fixed": "false",
        "css_variables": "$navbar-height: 0px !important;\n$grid-gutter-width: 0px !default;",
        "matching_now_experience_theme": "fad87d2ca304121029a4d1aed31e610f"
    }
    r_create = requests.post(f"{url}/api/now/table/sp_theme", auth=auth, headers=headers, json=theme_payload)
    theme_id = r_create.json()['result']['sys_id']
    print("Created FRAUDNEXUS Theme:", theme_id)

# 2. Update sp_portal 'fnx' with the new headerless theme
r_portal = requests.get(f"{url}/api/now/table/sp_portal?sysparm_query=url_suffix=fnx", auth=auth, headers=headers)
portal_id = r_portal.json()['result'][0]['sys_id']

r_patch = requests.patch(
    f"{url}/api/now/table/sp_portal/{portal_id}",
    auth=auth, headers=headers,
    json={
        "theme": theme_id,
        "sp_rectangle_menu": ""
    }
)
print(f"Updated portal fnx with FRAUDNEXUS Theme (Status: {r_patch.status_code})")

# 3. Verify on portal
r_v = requests.get(f"{url}/api/now/table/sp_portal/{portal_id}", auth=auth, headers=headers)
p = r_v.json().get('result', {})
print("New portal theme:", p.get('theme'))
