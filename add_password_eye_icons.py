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

# 1. Update client_script to add state variables and hide any stock header
if "c.showPassword" not in client_script:
    client_script = client_script.replace(
        "c.sidebarCollapsed = false;",
        "c.sidebarCollapsed = false;\n    c.showPassword = false;\n    c.showConfirmPassword = false;\n    c.showLoginPassword = false;\n    $timeout(function() { var h = document.querySelector('header[role=\"banner\"], .navbar-default, .sp-portal-header'); if (h) h.style.display = 'none'; }, 20);"
    )
    print("Updated client_script with showPassword states and header cleaner")

# 2. Update template for Login password field
old_login_pwd = """                <div class="fnx-field">
                    <label>{{c.t('password')}}</label>
                    <input type="password" ng-model="c.authForm.password" required placeholder="Enter your password">
                </div>"""

new_login_pwd = """                <div class="fnx-field">
                    <label>{{c.t('password')}}</label>
                    <div class="fnx-password-wrap">
                        <input type="{{c.showLoginPassword ? 'text' : 'password'}}" ng-model="c.authForm.password" required placeholder="Enter your password">
                        <button type="button" class="fnx-eye-btn" ng-click="c.showLoginPassword = !c.showLoginPassword" title="{{c.showLoginPassword ? 'Hide password' : 'Show password'}}" aria-label="Toggle password visibility">
                            <svg ng-if="!c.showLoginPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                            <svg ng-if="c.showLoginPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00B8D9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                        </button>
                    </div>
                </div>"""

if old_login_pwd in template:
    template = template.replace(old_login_pwd, new_login_pwd)
    print("Replaced Login password field with eye icon wrap")
else:
    # Pattern fallback
    template = re.sub(
        r'<div class="fnx-field">\s*<label>\{\{c\.t\(\'password\'\)\}\}<\/label>\s*<input type="password" ng-model="c\.authForm\.password"[^>]*placeholder="Enter your password"[^>]*>\s*<\/div>',
        new_login_pwd,
        template,
        count=1
    )
    print("Replaced Login password field via regex")

# 3. Update template for Register password and confirmPassword fields
old_reg_pwd = """                <div class="fnx-field">
                    <label>{{c.t('password')}}</label>
                    <input type="password" ng-model="c.authForm.password" required placeholder="Create password">
                </div>
                <div class="fnx-field">
                    <label>{{c.t('confirmPassword')}}</label>
                    <input type="password" ng-model="c.authForm.confirmPassword" required placeholder="Confirm password">
                </div>"""

new_reg_pwd = """                <div class="fnx-field">
                    <label>{{c.t('password')}}</label>
                    <div class="fnx-password-wrap">
                        <input type="{{c.showPassword ? 'text' : 'password'}}" ng-model="c.authForm.password" required placeholder="Create password">
                        <button type="button" class="fnx-eye-btn" ng-click="c.showPassword = !c.showPassword" title="{{c.showPassword ? 'Hide password' : 'Show password'}}" aria-label="Toggle password visibility">
                            <svg ng-if="!c.showPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                            <svg ng-if="c.showPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00B8D9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                        </button>
                    </div>
                </div>
                <div class="fnx-field">
                    <label>{{c.t('confirmPassword')}}</label>
                    <div class="fnx-password-wrap">
                        <input type="{{c.showConfirmPassword ? 'text' : 'password'}}" ng-model="c.authForm.confirmPassword" required placeholder="Confirm password">
                        <button type="button" class="fnx-eye-btn" ng-click="c.showConfirmPassword = !c.showConfirmPassword" title="{{c.showConfirmPassword ? 'Hide password' : 'Show password'}}" aria-label="Toggle password visibility">
                            <svg ng-if="!c.showConfirmPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                            <svg ng-if="c.showConfirmPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00B8D9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                        </button>
                    </div>
                </div>"""

if old_reg_pwd in template:
    template = template.replace(old_reg_pwd, new_reg_pwd)
    print("Replaced Register password & confirmPassword fields with eye icon wrap")
else:
    # Pattern fallback
    template = re.sub(
        r'<div class="fnx-field">\s*<label>\{\{c\.t\(\'password\'\)\}\}<\/label>\s*<input type="password" ng-model="c\.authForm\.password"[^>]*placeholder="Create password"[^>]*>\s*<\/div>\s*<div class="fnx-field">\s*<label>\{\{c\.t\(\'confirmPassword\'\)\}\}<\/label>\s*<input type="password" ng-model="c\.authForm\.confirmPassword"[^>]*placeholder="Confirm password"[^>]*>\s*<\/div>',
        new_reg_pwd,
        template,
        count=1
    )
    print("Replaced Register password & confirmPassword via regex")

# 4. Add CSS styles for eye icon wrap
eye_css = """
/* PASSWORD EYE ICON TOGGLE */
.fnx-password-wrap {
    position: relative !important;
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
}

.fnx-password-wrap input {
    width: 100% !important;
    padding-right: 42px !important;
}

.fnx-eye-btn {
    position: absolute !important;
    right: 12px !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    background: transparent !important;
    border: none !important;
    cursor: pointer !important;
    padding: 4px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    color: #475569 !important;
    z-index: 3 !important;
}

.fnx-eye-btn:hover {
    color: #00B8D9 !important;
}

.fnx-eye-btn:hover svg {
    stroke: #00B8D9 !important;
}

header[role="banner"], .navbar-default, .sp-portal-header, #sp-nav-bar {
    display: none !important;
    height: 0 !important;
    visibility: hidden !important;
}
"""

if ".fnx-eye-btn" not in css:
    css = eye_css + "\n" + css
    print("Appended eye button CSS styles")

# 5. Patch widget
payload = {
    "template": template,
    "css": css,
    "client_script": client_script,
    "script": script
}

print("--- 2. Deploying updated widget to ServiceNow ---")
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
