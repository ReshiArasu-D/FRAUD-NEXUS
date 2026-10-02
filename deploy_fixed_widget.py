"""
Fix FRAUDNEXUS Blank Screen Bug:
1. Removes broken triple-curly interpolation in ng-class (e.g. ng-class="{{{'active': ...}}}")
2. Removes embedded <style> tag from widget template so AngularJS compiler runs cleanly
3. Ensures high-contrast CSS is properly set in the sp_widget 'css' field
4. Repairs corrupted theme link on sp_portal 'fnx'
"""
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

# 1. Fix corrupted theme on sp_portal
print("--- 1. Fixing sp_portal theme ---")
r_portal = requests.get(f"{url}/api/now/table/sp_portal?sysparm_query=url_suffix=fnx", auth=auth, headers=headers)
portals = r_portal.json().get('result', [])
if portals:
    portal_id = portals[0]['sys_id']
    # Set to Stock Theme sys_id
    r_patch_portal = requests.patch(
        f"{url}/api/now/table/sp_portal/{portal_id}",
        auth=auth, headers=headers,
        json={"theme": "281507c44317d210ca4c1f425db8f2fd"}
    )
    print(f"Updated portal theme (Status: {r_patch_portal.status_code})")

# 2. Load existing widget
print("\n--- 2. Fetching current widget from ServiceNow ---")
r_w = requests.get(f"{url}/api/now/table/sp_widget/{WIDGET_ID}", auth=auth, headers=headers)
widget_data = r_w.json().get('result', {})

template = widget_data.get('template', '')
css = widget_data.get('css', '')
client_script = widget_data.get('client_script', '')
script = widget_data.get('script', '')

print(f"Current Template length: {len(template)}")
print(f"Current CSS length: {len(css)}")

# 3. Clean template: remove <style>...</style> block
cleaned_template = re.sub(r'<style>.*?</style>', '', template, flags=re.DOTALL)
print(f"Template length after removing <style>: {len(cleaned_template)}")

# 4. Fix triple-curly braces in ng-class
# Replace ng-class="{{{...}}}" with ng-class="{...}"
cleaned_template = re.sub(r'ng-class="\{\{\{(.*?)\}\}\}"', r'ng-class="{\1}"', cleaned_template)

# Also check for any remaining {{{ or }}}
matches_left = re.findall(r'\{\{\{.*?\}\}\}', cleaned_template)
print(f"Remaining triple curlies: {len(matches_left)}")
if matches_left:
    for m in matches_left:
        print("  Warning leftover:", m)
    cleaned_template = cleaned_template.replace("{{{", "{").replace("}}}", "}")

# 5. Ensure high-contrast CSS is fully present
# If CSS in widget is empty or short, load it from fix_ui_visibility.py
if len(css) < 1000:
    import fix_ui_visibility
    css = fix_ui_visibility.css_content

# 6. Deploy patched widget to ServiceNow
print("\n--- 3. Deploying patched widget to ServiceNow ---")
payload = {
    "template": cleaned_template,
    "css": css,
    "client_script": client_script,
    "script": script
}

r_patch = requests.patch(
    f"{url}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth, headers=headers,
    json=payload
)

if r_patch.status_code == 200:
    print("[SUCCESS] Widget fnx_customer_experience successfully patched!")
    print(f"New Template length: {len(cleaned_template)}")
    print(f"New CSS length: {len(css)}")
else:
    print(f"[ERROR] Failed to patch widget: {r_patch.status_code}")
    print(r_patch.text[:500])
    exit(1)

# 7. Verification of clean template
print("\n--- 4. Verifying deployed template on ServiceNow ---")
r_verify = requests.get(f"{url}/api/now/table/sp_widget/{WIDGET_ID}", auth=auth, headers=headers)
v_data = r_verify.json().get('result', {})
v_tmpl = v_data.get('template', '')
print("Has <style> in template:", "<style>" in v_tmpl)
print("Has {{{ in template:", "{{{" in v_tmpl)
print("Has ng-class=\"{\" in template:", "ng-class=\"{" in v_tmpl)
print("Template start:\n", v_tmpl[:200])
