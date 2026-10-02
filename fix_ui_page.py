import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

# Read current html or portal html from create_ui_page.py
from create_ui_page import portal_html

# In Jelly, all & must be &amp;, and standard XML compliance is needed, OR wrapped in CDATA or direct Jelly
# Let's create a clean, valid Jelly UI page:
jelly_page = f"""<?xml version="1.0" encoding="utf-8" ?>
<j:jelly trim="false" xmlns:j="jelly:core" xmlns:g="glide" xmlns:j2="null" xmlns:g2="null">
{portal_html.replace('&', '&amp;')}
</j:jelly>"""

# Or with direct=true
r_page = requests.get(f"{url}/api/now/table/sys_ui_page?sysparm_query=name=fnx_portal", auth=auth, headers=headers)
p_id = r_page.json()['result'][0]['sys_id']

payload = {
    "html": jelly_page,
    "direct": "true"
}

r_patch = requests.patch(f"{url}/api/now/table/sys_ui_page/{p_id}", auth=auth, headers=headers, json=payload)
print("Updated sys_ui_page with Jelly wrapper:", r_patch.status_code)

# Test GET /fnx_portal.do
r_test = requests.get(f"{url}/fnx_portal.do")
print("fnx_portal.do GET status:", r_test.status_code)
print("Length:", len(r_test.text))
print("Contains FRAUDNEXUS?", "FRAUDNEXUS" in r_test.text)
if "FRAUDNEXUS" in r_test.text:
    idx = r_test.text.find("FRAUDNEXUS")
    print("Found preview:\n", r_test.text[idx:idx+200])
else:
    print("First 400 chars of output:\n", r_test.text[:400])
