import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

# 1. Create or get sp_widget
widget_template = """<div class="fnx-portal-wrapper">
  <iframe src="/fnx_portal.do" style="width: 100%; min-height: 92vh; border: none; overflow: auto;"></iframe>
</div>"""

r_w_chk = requests.get(f"{url}/api/now/table/sp_widget?sysparm_query=id=fnx_customer_experience", auth=auth, headers=headers)
existing_w = r_w_chk.json().get('result', [])

widget_payload = {
    "name": "FRAUDNEXUS Customer Experience",
    "id": "fnx_customer_experience",
    "template": widget_template,
    "public": "true"
}

if existing_w:
    w_id = existing_w[0]['sys_id']
    requests.patch(f"{url}/api/now/table/sp_widget/{w_id}", auth=auth, headers=headers, json=widget_payload)
    print("Updated widget:", w_id)
else:
    r_create_w = requests.post(f"{url}/api/now/table/sp_widget", auth=auth, headers=headers, json=widget_payload)
    w_id = r_create_w.json()['result']['sys_id']
    print("Created widget:", w_id)

# 2. Create or get sp_page
r_p_chk = requests.get(f"{url}/api/now/table/sp_page?sysparm_query=id=fnx_home", auth=auth, headers=headers)
existing_p = r_p_chk.json().get('result', [])

page_payload = {
    "title": "FRAUDNEXUS Home",
    "id": "fnx_home",
    "public": "true"
}

if existing_p:
    p_id = existing_p[0]['sys_id']
    print("Page fnx_home exists:", p_id)
else:
    r_create_p = requests.post(f"{url}/api/now/table/sp_page", auth=auth, headers=headers, json=page_payload)
    p_id = r_create_p.json()['result']['sys_id']
    print("Created page fnx_home:", p_id)

# 3. Add widget instance to page
r_inst_chk = requests.get(f"{url}/api/now/table/sp_instance?sysparm_query=sp_widget={w_id}", auth=auth, headers=headers)
if not r_inst_chk.json().get('result', []):
    inst_payload = {
        "sp_widget": w_id,
        "title": "FRAUDNEXUS Experience",
        "order": "1"
    }
    requests.post(f"{url}/api/now/table/sp_instance", auth=auth, headers=headers, json=inst_payload)
    print("Created sp_instance for widget")

# 4. Update portal homepage
r_port = requests.patch(f"{url}/api/now/table/sp_portal/961449b3c32b43d0e54832f1b401318a", auth=auth, headers=headers, json={"homepage": p_id})
print("Updated portal homepage to fnx_home:", r_port.status_code)
