import requests
import os
import re
import urllib.parse
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
user = os.getenv('SERVICENOW_USERNAME')
pwd = os.getenv('SERVICENOW_PASSWORD')

s = requests.Session()
login_url = f"{url}/login.do?user_name={urllib.parse.quote(user)}&sys_action=sysverb_login&user_password={urllib.parse.quote(pwd)}"
s.get(login_url)

# Load form to get tokens and all default hidden inputs
r_form = s.get(f"{url}/sys_db_object.do?sys_id=-1")
g_ck_match = re.search(r'g_ck\s*=\s*["\']([^"\']+)["\']', r_form.text)
g_ck = g_ck_match.group(1) if g_ck_match else ""

# Extract all input fields from form
form_data = {}
for m in re.finditer(r'<input[^>]+name=["\']([^"\']+)["\'][^>]*>', r_form.text):
    val_m = re.search(r'value=["\']([^"\']*)["\']', m.group(0))
    val = val_m.group(1) if val_m else ""
    form_data[m.group(1)] = val

# Set required fields for creating table
form_data['sys_action'] = 'sysverb_insert'
form_data['sysparm_ck'] = g_ck
form_data['sys_target'] = 'sys_db_object'
form_data['sys_uniqueValue'] = '-1'
form_data['sys_db_object.label'] = 'FRAUDNEXUS Customer'
form_data['sys_db_object.name'] = 'x_fnx_customer'
form_data['sys_db_object.create_access_controls'] = 'true'

# Post to sys_db_object.do
r_post = s.post(f"{url}/sys_db_object.do", data=form_data)
print("POST status:", r_post.status_code)

# Check if table now exists in sys_db_object and table api
r_chk = s.get(f"{url}/api/now/table/sys_db_object?sysparm_query=name=x_fnx_customer")
print("sys_db_object query:", r_chk.status_code, r_chk.json().get('result'))

r_api = s.get(f"{url}/api/now/table/x_fnx_customer?sysparm_limit=1")
print("Table API query on x_fnx_customer:", r_api.status_code, r_api.text[:200])
