import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
css = r.json()['result']['css']

# 1. Fix missing dots for custom element tag names that should be classes
css = css.replace('fnx-admin-login-page {', '.fnx-admin-login-page {')
css = css.replace('fnx-admin-login-left {', '.fnx-admin-login-left {')
css = css.replace('fnx-admin-login-right {', '.fnx-admin-login-right {')

# 2. Premium form styles
premium_styles = """
/* PREMIUM ADMIN LOGIN FORM STYLES */
.fnx-form-group {
    margin-bottom: 1.5rem !important;
    text-align: left !important;
}

.fnx-form-group label {
    display: block !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    color: #475569 !important;
    margin-bottom: 0.5rem !important;
}

.fnx-input {
    width: 100% !important;
    padding: 0.85rem 1rem !important;
    font-size: 0.95rem !important;
    color: #0F172A !important;
    background-color: #F8FAFC !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
}

.fnx-input:focus {
    outline: none !important;
    background-color: #FFFFFF !important;
    border-color: #00B8D9 !important;
    box-shadow: 0 0 0 3px rgba(0, 184, 217, 0.15) !important;
}

.fnx-btn-demo, button[type="submit"] {
    width: 100% !important;
    padding: 0.9rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    border-radius: 8px !important;
    margin-top: 1rem !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    text-align: center !important;
}

button[type="submit"] {
    background-color: #0B1F3A !important;
    color: #FFFFFF !important;
    border: none !important;
}

button[type="submit"]:hover {
    background-color: #1a365d !important;
    box-shadow: 0 4px 12px rgba(11, 31, 58, 0.2) !important;
}

.fnx-btn-demo {
    background-color: #E0F2FE !important;
    color: #0369A1 !important;
    border: 1.5px solid #00B8D9 !important;
}

.fnx-btn-demo:hover {
    background-color: #00B8D9 !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 12px rgba(0, 184, 217, 0.3) !important;
}

.fnx-input-pwd-wrap {
    position: relative !important;
    display: flex !important;
    align-items: center !important;
}

.fnx-pwd-toggle {
    background: #E2E8F0 !important;
    border: 1px solid #CBD5E1 !important;
    border-left: none !important;
    border-radius: 0 8px 8px 0 !important;
    padding: 0.85rem 1rem !important;
    cursor: pointer !important;
    color: #64748B !important;
    transition: all 0.2s ease !important;
}

.fnx-pwd-toggle:hover {
    background: #CBD5E1 !important;
    color: #0F172A !important;
}
"""

# append premium styles at the end
css = css + '\n\n' + premium_styles

resp = requests.patch(
    f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
    auth=auth,
    headers={'Accept':'application/json', 'Content-Type':'application/json'},
    json={'css': css}
)
print('Deploy CSS status:', resp.status_code)
