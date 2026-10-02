import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

# 1. Update fnx_portal UI page to seamless redirect & fallback link
redirect_jelly = """<?xml version="1.0" encoding="utf-8" ?>
<j:jelly trim="false" xmlns:j="jelly:core" xmlns:g="glide" xmlns:j2="null" xmlns:g2="null">
<![CDATA[
<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="refresh" content="0;url=/fnx" />
  <script type="text/javascript">
    window.location.replace("/fnx");
  </script>
</head>
<body style="font-family: sans-serif; background: #0B1F3A; color: #FFFFFF; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0;">
  <div style="text-align: center;">
    <h2 style="color: #00B8D9;">Loading FRAUDNEXUS Portal...</h2>
    <p>If you are not redirected automatically, <a href="/fnx" style="color: #00B8D9; text-decoration: underline;">click here to launch</a>.</p>
  </div>
</body>
</html>
]]>
</j:jelly>"""

r_page = requests.get(f"{url}/api/now/table/sys_ui_page?sysparm_query=name=fnx_portal", auth=auth, headers=headers)
p_id = r_page.json()['result'][0]['sys_id']

payload = {
    "html": redirect_jelly,
    "direct": "true"
}

r_patch = requests.patch(f"{url}/api/now/table/sys_ui_page/{p_id}", auth=auth, headers=headers, json=payload)
print("Updated fnx_portal UI page:", r_patch.status_code)

# Check fnx_portal.do GET
r_test = requests.get(f"{url}/fnx_portal.do")
print("fnx_portal.do status:", r_test.status_code, "Length:", len(r_test.text))
print("Preview:\n", r_test.text[:300])
