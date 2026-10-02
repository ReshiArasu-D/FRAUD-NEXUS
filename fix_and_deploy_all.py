import requests
import os
import re
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv('d:/KPMG/.env')
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

WIDGET_ID = "2f258577c32b43d0e54832f1b401317f"

print("--- 1. Fetch current widget ---")
r_w = requests.get(f"{url}/api/now/table/sp_widget/{WIDGET_ID}", auth=auth, headers=headers)
widget_data = r_w.json().get('result', {})

template = widget_data.get('template', '')
css = widget_data.get('css', '')
client_script = widget_data.get('client_script', '')
script = widget_data.get('script', '')

# Remove any <style> block from template if present
cleaned_template = re.sub(r'<style>.*?</style>', '', template, flags=re.DOTALL)

# Fix 1: ng-repeat="f in [{{icon:...
cleaned_template = re.sub(r'ng-repeat="f in \[\{\{(.*?)\}\}\]"', r'ng-repeat="f in [{\1}]"', cleaned_template)
cleaned_template = cleaned_template.replace("ng-repeat=\"f in [{{", "ng-repeat=\"f in [{")
cleaned_template = cleaned_template.replace("}}]\"", "}]\"")
cleaned_template = cleaned_template.replace("}},{{", "},{")

# Fix 2: ng-class="{{{...}}}" -> ng-class="{...}"
cleaned_template = re.sub(r'ng-class="\{\{\{(.*?)\}\}\}"', r'ng-class="{\1}"', cleaned_template)

# Also fix any remaining triple curlies
cleaned_template = cleaned_template.replace("{{{", "{").replace("}}}", "}")

# Scan for any remaining invalid ng- directives with {{
ng_attrs = re.findall(r'(ng-[a-z]+="[^"]*\{\{[^"]*"[^>]*)', cleaned_template)
print(f"Remaining invalid ng- attributes with {{{{ : {len(ng_attrs)}")
for a in ng_attrs:
    print("  Remaining:", a[:100])

# Ensure CSS is high contrast
import fix_ui_visibility
css = fix_ui_visibility.css_content

payload = {
    "template": cleaned_template,
    "css": css,
    "client_script": client_script,
    "script": script
}

print("--- 2. Deploying clean widget to ServiceNow ---")
r_patch = requests.patch(
    f"{url}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth, headers=headers,
    json=payload
)

if r_patch.status_code == 200:
    print(f"[SUCCESS] Deployed clean widget! Template len: {len(cleaned_template)}, CSS len: {len(css)}")
else:
    print(f"[ERROR] Failed to deploy: {r_patch.status_code}")
    print(r_patch.text[:500])
