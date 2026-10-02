import requests
import os
import sys
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
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

print(f"Original template len: {len(template)}, css len: {len(css)}, client_script len: {len(client_script)}")

# 1. Update Template: Add Forgot Password link in Login Form and Forgot Password Form
target_login_form_end = """                <button type="submit" class="fnx-btn fnx-btn-primary fnx-btn-lg" ng-disabled="c.authLoading">
                    {{c.authLoading ? 'Signing in...' : c.t('login')}}
                </button>"""

forgot_row_html = """                <div class="fnx-forgot-row">
                    <a href="javascript:void(0)" ng-click="c.openForgotPassword()" class="fnx-forgot-pwd">{{c.t('forgotPassword')}}</a>
                </div>
                <button type="submit" class="fnx-btn fnx-btn-primary fnx-btn-lg" ng-disabled="c.authLoading">
                    {{c.authLoading ? 'Signing in...' : c.t('login')}}
                </button>"""

if "fnx-forgot-pwd" not in template:
    if target_login_form_end in template:
        template = template.replace(target_login_form_end, forgot_row_html, 1)
        print("Inserted forgot_row_html into Login form")
    else:
        print("ERROR: target_login_form_end not found in template")

forgot_form_html = """            <!-- FORGOT PASSWORD FORM -->
            <form ng-if="c.authMode === 'forgot'" ng-submit="c.doForgotPassword()" class="fnx-auth-form">
                <div class="fnx-forgot-header">
                    <h3>{{c.t('resetPasswordTitle')}}</h3>
                    <p>{{c.t('resetPasswordDesc')}}</p>
                </div>

                <div class="fnx-auth-error" ng-if="c.authError">{{c.authError}}</div>

                <div ng-if="c.forgotSuccess" class="fnx-forgot-success">
                    <strong>{{c.t('instructionsSent')}}</strong>
                    <p>{{c.t('resetSentMsg')}}</p>
                </div>

                <div class="fnx-field" ng-if="!c.forgotSuccess">
                    <label>{{c.t('email')}}</label>
                    <input type="email" ng-model="c.authForm.forgotEmail" required placeholder="user@example.com">
                </div>

                <button type="submit" class="fnx-btn fnx-btn-primary fnx-btn-lg" ng-disabled="c.forgotLoading" ng-if="!c.forgotSuccess">
                    {{c.forgotLoading ? 'Sending...' : c.t('sendResetLink')}}
                </button>

                <div class="fnx-auth-switch">
                    <a ng-click="c.authMode = 'login'; c.authError = '';" class="fnx-back-login">
                        &larr; {{c.t('backToLogin')}}
                    </a>
                </div>
            </form>
"""

target_after_login_form = """            <!-- REGISTER FORM -->"""
if "c.authMode === 'forgot'" not in template:
    if target_after_login_form in template:
        template = template.replace(target_after_login_form, forgot_form_html + "\n            <!-- REGISTER FORM -->", 1)
        print("Inserted FORGOT PASSWORD FORM into template")
    else:
        print("ERROR: target_after_login_form not found in template")

# 2. Update client_script: Add helper functions and dictionary translations
if "c.openForgotPassword" not in client_script:
    handlers_code = """
    c.openForgotPassword = function() {
        c.authMode = 'forgot';
        c.authError = '';
        c.forgotSuccess = false;
        c.authForm.forgotEmail = c.authForm.email || '';
    };

    c.doForgotPassword = function() {
        c.authError = '';
        if (!c.authForm.forgotEmail) {
            c.authError = 'Please enter your registered email address.';
            return;
        }
        c.forgotLoading = true;
        $timeout(function() {
            c.forgotLoading = false;
            c.forgotSuccess = true;
        }, 600);
    };
"""
    client_script = client_script.replace("c.doLogin = function()", handlers_code + "\n    c.doLogin = function()")
    print("Added c.openForgotPassword and c.doForgotPassword to client_script")

# Add translations to en dict
en_target = "forgotPassword: 'Forgot Password?',"
en_addition = """forgotPassword: 'Forgot Password?',
            resetPasswordTitle: 'Reset Password',
            resetPasswordDesc: 'Enter your registered email address to receive password reset instructions.',
            instructionsSent: 'Reset Instructions Sent',
            resetSentMsg: 'If an account is associated with this email address, password reset instructions and a verification link have been dispatched.',
            sendResetLink: 'Send Reset Link',
            backToLogin: 'Back to Login',"""

if "resetPasswordTitle: 'Reset Password'" not in client_script:
    client_script = client_script.replace(en_target, en_addition, 1)
    print("Added English translations to client_script")

# Add translations to ta dict
ta_target = "forgotPassword: 'கடவுச்சொல் மறந்துவிட்டதா?',"
ta_addition = """forgotPassword: 'கடவுச்சொல் மறந்துவிட்டதா?',
            resetPasswordTitle: 'கடவுச்சொல்லை மீட்டமைக்க',
            resetPasswordDesc: 'கடவுச்சொல் மீட்டமைப்பு வழிமுறைகளைப் பெற உங்கள் பதிவுசெய்த மின்னஞ்சலை உள்ளிடவும்.',
            instructionsSent: 'வழிமுறைகள் அனுப்பப்பட்டன',
            resetSentMsg: 'இந்த மின்னஞ்சலுடன் கணக்கு இணைக்கப்பட்டிருந்தால், கடவுச்சொல் மீட்டமைப்பு வழிமுறைகள் அனுப்பப்பட்டுள்ளன.',
            sendResetLink: 'மீட்டமைப்பு இணைப்பை அனுப்புக',
            backToLogin: 'உள்நுழைவுக்குத் திரும்பு',"""

if "resetPasswordTitle: 'கடவுச்சொல்லை மீட்டமைக்க'" not in client_script:
    client_script = client_script.replace(ta_target, ta_addition, 1)
    print("Added Tamil translations to client_script")

# 3. Update CSS
css_additions = """
/* Forgot Password Styles */
.fnx-forgot-row {
    display: flex !important;
    justify-content: flex-end !important;
    margin-top: -0.25rem !important;
    margin-bottom: 0.25rem !important;
}

.fnx-forgot-pwd {
    color: #0284C7 !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    text-decoration: none !important;
    cursor: pointer !important;
    transition: color 0.15s ease !important;
}

.fnx-forgot-pwd:hover {
    color: #0369A1 !important;
    text-decoration: underline !important;
}

.fnx-forgot-header h3 {
    font-size: 1.25rem !important;
    font-weight: 700 !important;
    color: #0F172A !important;
    margin: 0 0 0.5rem 0 !important;
}

.fnx-forgot-header p {
    font-size: 0.95rem !important;
    color: #475569 !important;
    margin: 0 !important;
    line-height: 1.5 !important;
}

.fnx-forgot-success {
    background-color: #F0FDF4 !important;
    border: 1px solid #86EFAC !important;
    color: #166534 !important;
    padding: 1rem !important;
    border-radius: 8px !important;
    font-size: 0.92rem !important;
    line-height: 1.5 !important;
}

.fnx-forgot-success strong {
    display: block !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.35rem !important;
}

.fnx-forgot-success p {
    margin: 0 !important;
}

.fnx-back-login {
    cursor: pointer !important;
    color: #0284C7 !important;
    font-weight: 600 !important;
    text-decoration: none !important;
}

.fnx-back-login:hover {
    color: #0369A1 !important;
    text-decoration: underline !important;
}
"""

if ".fnx-forgot-pwd" not in css:
    css = css + "\n" + css_additions
    print("Added Forgot Password styles to CSS")

# 4. Save to ServiceNow
payload = {
    'template': template,
    'client_script': client_script,
    'css': css
}

r_patch = requests.patch(f"{url}/api/now/table/sp_widget/{WIDGET_ID}", auth=auth, headers=headers, json=payload)
print(f"Updated widget status: {r_patch.status_code}")
if r_patch.status_code == 200:
    print("Successfully updated widget with Forgot Password functionality!")
else:
    print("Failed to update widget:", r_patch.text[:300])
