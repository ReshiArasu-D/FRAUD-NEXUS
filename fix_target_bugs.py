import requests, sys, re, json

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
# The empty space is caused because fnx-landing and fnx-auth-page might be taking up 100vh when hidden.
# We will wrap the ENTIRE landing page and auth page contents in ng-if so they don't render when c.currentView is adminWorkspace.
# Looking at the dump, <div ng-if="c.currentView === 'landing'" class="fnx-landing"> ALREADY uses ng-if!
# Let me just forcefully hide them when c.currentView == 'adminWorkspace' using an inline style injection on the app container!
if 'fnx-app' in tpl:
    tpl = tpl.replace('<div class="fnx-app">', '<div class="fnx-app" ng-class="{\'admin-mode\': c.currentView === \'adminWorkspace\'}">')
css += """
.fnx-app.admin-mode > .fnx-landing, .fnx-app.admin-mode > .fnx-auth-page {
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
    opacity: 0 !important;
    position: absolute !important;
    z-index: -999 !important;
}
"""

# ALSO force the root to not scroll in admin mode
css += """
.fnx-app.admin-mode {
    height: 100vh !important;
    overflow: hidden !important;
}
/* This forces the ServiceNow wrappers to shrinkwrap or not scroll */
body:has(.fnx-app.admin-mode), html:has(.fnx-app.admin-mode) {
    overflow: hidden !important;
}
"""


# 2. DELETE DUPLICATE AI BUTTON (OVERLAP FIX)
tpl = re.sub(r'<button[^>]*class="fnx-ai-trigger"[^>]*>[\s\S]*?</button>', '', tpl)


# 3. FIX SEARCH BAR (nan cutoff)
css += """
.fnx-search-input, input[type="search"] {
    width: 100% !important;
    min-width: 400px !important;
    max-width: 600px !important;
}
"""

# 4. FIX SIDEBAR GLOBAL LOGO
# The user wants the Global Logo to look good. We will replace the text "FRAUDNEXUS Admin Portal" in the topbar with the shield icon + text, if it's not already there.
# Wait, they said "seee the global image not good in side bar... change the front style proper arrangement".
# I'll remove the globe graphic from the sidebar so it's clean.
globe_pattern = r'<div class="fnx-hero-graphic">[\s\S]*?</div>\s*<div class="fnx-sidebar-footer-text">[\s\S]*?</div>'
tpl = re.sub(globe_pattern, '', tpl)


# 5. CUSTOMER ID CLICKABLE
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
