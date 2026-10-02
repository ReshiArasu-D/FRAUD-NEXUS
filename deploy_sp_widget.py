import requests
import os
import re
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

# Read the HTML template from create_ui_page.py
with open("create_ui_page.py", "r", encoding="utf-8") as f:
    content = f.read()

# Extract css
css_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
css_content = css_match.group(1).strip() if css_match else ""

# Extract body html
body_match = re.search(r'<body>(.*?)<script>', content, re.DOTALL)
body_html = body_match.group(1).strip() if body_match else ""

# Extract client js
js_match = re.search(r'<script>(.*?)</script>\s*</body>', content, re.DOTALL)
js_content = js_match.group(1).strip() if js_match else ""

# In Service Portal widget, client script is wrapped in function($scope, $http, $window)
widget_client_script = f"""function($scope, $http, $window) {{
    var c = this;
    
    // Inject vanilla client logic into window context for full compatibility
    $window.setTimeout(function() {{
        var scriptEl = document.createElement('script');
        scriptEl.type = 'text/javascript';
        scriptEl.text = {repr(js_content)};
        document.body.appendChild(scriptEl);
    }}, 100);
}}"""

# Find widget sys_id
r_w = requests.get(f"{url}/api/now/table/sp_widget?sysparm_query=id=fnx_customer_experience", auth=auth, headers=headers)
w_id = r_w.json()['result'][0]['sys_id']

payload = {
    "template": body_html,
    "css": css_content,
    "client_script": widget_client_script,
    "public": "true"
}

r_patch = requests.patch(f"{url}/api/now/table/sp_widget/{w_id}", auth=auth, headers=headers, json=payload)
print("Updated sp_widget fnx_customer_experience:", r_patch.status_code)

# Check /fnx portal
r_fnx = requests.get(f"{url}/fnx")
print("/fnx status:", r_fnx.status_code, "Length:", len(r_fnx.text))
print("Contains FRAUDNEXUS in /fnx?", "FRAUDNEXUS" in r_fnx.text)
