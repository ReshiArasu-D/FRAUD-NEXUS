import requests, sys, re

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
data = r.json()['result']
tpl = data['template']
css = data['css']
cs = data['client_script']

# 1. FIX THE MASSIVE EMPTY SPACE (ADMIN SCROLL)
# We use modern CSS :has() selector to detect if the Admin Dashboard is active.
# If it is, we forcefully rip it out of the normal document flow and pin it to the viewport, bypassing all ServiceNow padding!
# This leaves the landing page completely untouched.
css += """
/* Safe, targeted fix for Admin Dashboard empty space */
.fnx-app:has(.fnx-admin-layout) {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    z-index: 1000 !important;
    background-color: #F1F5F9 !important;
    height: 100vh !important;
    width: 100vw !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Force hidden landing/auth pages to 0 height when in admin mode */
.fnx-app:has(.fnx-admin-layout) .fnx-landing,
.fnx-app:has(.fnx-admin-layout) .fnx-auth-page {
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
    position: absolute !important;
    opacity: 0 !important;
}
"""

# 2. FIX DUPLICATE AI BUTTON (OVERLAP)
css += """
/* Hide global AI trigger when admin dashboard is active */
.fnx-app:has(.fnx-admin-layout) ~ .fnx-ai-trigger,
.fnx-ai-trigger:has(~ .fnx-admin-layout) {
    display: none !important;
}
/* Fallback if it's inside fnx-app */
.fnx-app:has(.fnx-admin-layout) .fnx-ai-trigger {
    display: none !important;
}
"""


# 3. FIX SEARCH BAR (nan cutoff)
css += """
.fnx-search-input, input[type="search"] {
    width: 100% !important;
    min-width: 400px !important;
    max-width: 600px !important;
}
"""

# 4. CUSTOMER ID CLICKABLE
# Targeted regex to change only the customer ID cell in the table
cust_id_pattern = r'<td><span class="fnx-text-primary fw-bold">{{cust\.id}}</span></td>'
tpl = re.sub(cust_id_pattern, r'<td><a href="javascript:void(0)" class="fnx-text-primary fw-bold" style="text-decoration: underline;" ng-click="c.viewCustomer(cust)">{{cust.id}}</a></td>', tpl)

cs_inject = """
    c.viewCustomer = function(cust) {
        c.selectedCustomer = cust;
        if (typeof spModal !== 'undefined') {
            spModal.alert('Customer Profile: ' + cust.name + '\\nID: ' + cust.id + '\\nEmail: ' + cust.email);
        } else {
            alert('Customer Details:\\n\\nID: ' + cust.id + '\\nName: ' + cust.name + '\\nEmail: ' + cust.email + '\\nKYC Status: ' + cust.kycStatus);
        }
    };
"""
if 'c.viewCustomer =' not in cs:
    cs = cs.replace('c.loadAdminCustomers = function() {', cs_inject + '\n    c.loadAdminCustomers = function() {')


# Force cache bust string
import time
tpl = re.sub(r'<!-- CACHE BUST: .*? -->\n*', '', tpl)
tpl = f'<!-- CACHE BUST: {int(time.time())} -->\n' + tpl

# Deploy updates
resp = requests.patch(
    f"{base}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    json={'template': tpl, 'css': css, 'client_script': cs}
)

if resp.status_code == 200:
    print("SUCCESS: Target fixes deployed!")
else:
    print(f"ERROR: {resp.text[:400]}")
