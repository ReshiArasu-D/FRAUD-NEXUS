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

print(f"Current template len: {len(template)}, css len: {len(css)}")

# 2. Remove Login and Register buttons from fnx-landing-actions
# Pattern to match the buttons inside fnx-landing-actions
old_actions = """        <div class="fnx-landing-actions">
            <button class="fnx-lang-btn" ng-click="c.toggleLang()">{{c.lang === 'en' ? 'தமிழ்' : 'English'}}</button>
            <button class="fnx-btn fnx-btn-outline" ng-click="c.goToAuth('login')">{{c.t('login')}}</button>
            <button class="fnx-btn fnx-btn-primary" ng-click="c.goToAuth('register')">{{c.t('register')}}</button>
        </div>"""

new_actions = """        <div class="fnx-landing-actions">
            <button class="fnx-lang-btn" ng-click="c.toggleLang()">{{c.lang === 'en' ? 'தமிழ்' : 'English'}}</button>
        </div>"""

if old_actions in template:
    template = template.replace(old_actions, new_actions)
    print("Replaced exact old_actions block successfully!")
else:
    # Use regex replacement
    template = re.sub(
        r'<div class="fnx-landing-actions">[\s\S]*?</div>',
        '<div class="fnx-landing-actions">\n            <button class="fnx-lang-btn" ng-click="c.toggleLang()">{{c.lang === \'en\' ? \'தமிழ்\' : \'English\'}}</button>\n        </div>',
        template,
        count=1
    )
    print("Replaced via regex!")

# 3. Add CSS rule to hide generic ServiceNow banner header (servicenow ... Log in)
hide_sn_header_rule = """
/* Hide ServiceNow stock header on landing */
header[role="banner"], .sp-page-root > header, #sp-nav-bar {
    display: none !important;
}
"""
if "header[role=\"banner\"]" not in css:
    css = hide_sn_header_rule + "\n" + css

# 4. Patch widget
payload = {
    "template": template,
    "css": css,
    "client_script": client_script,
    "script": script
}

print("--- 2. Updating widget on ServiceNow ---")
r_patch = requests.patch(
    f"{url}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth, headers=headers,
    json=payload
)

if r_patch.status_code == 200:
    print(f"[SUCCESS] Updated widget fnx_customer_experience! Status: {r_patch.status_code}")
else:
    print(f"[ERROR] Failed: {r_patch.status_code} - {r_patch.text}")
    exit(1)
