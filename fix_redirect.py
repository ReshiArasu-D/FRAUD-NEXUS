import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

r_page = requests.get(f"{url}/api/now/table/sys_ui_page?sysparm_query=name=fnx_portal", auth=auth, headers=headers)
p_id = r_page.json()['result'][0]['sys_id']

html_content = """<?xml version="1.0" encoding="utf-8" ?>
<j:jelly trim="false" xmlns:j="jelly:core" xmlns:g="glide" xmlns:j2="null" xmlns:g2="null">
<script>
window.location.href = "/fnx";
</script>
<div style="font-family: sans-serif; background: #0B1F3A; color: #FFFFFF; padding: 4rem 2rem; text-align: center;">
  <h2 style="color: #00B8D9; margin-bottom: 1rem;">Opening FRAUDNEXUS Customer Portal...</h2>
  <p><a href="/fnx" style="color: #00B8D9; text-decoration: underline; font-size: 1.2rem;">Click here if not redirected automatically</a></p>
</div>
</j:jelly>"""

r_patch = requests.patch(f"{url}/api/now/table/sys_ui_page/{p_id}", auth=auth, headers=headers, json={"html": html_content, "direct": "false"})
print("Patch status:", r_patch.status_code)

r = requests.get(f"{url}/fnx_portal.do")
print("fnx_portal.do status:", r.status_code, "Length:", len(r.text))
print("Contains /fnx?", "/fnx" in r.text)
