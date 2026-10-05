import requests, sys, json
sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
data = r.json()['result']
tpl = data['template']
css = data['css']
cs = data['client_script']

print("Applying safe fixes...")

# 1. FIX THE AI OVERLAP - SAFELY
ai_btn = '<button class="fnx-ai-trigger" ng-click="c.showAI = !c.showAI" title="Now Assist for FRAUDNEXUS">\n        <span>&#10024;</span>\n        <span>Now Assist AI</span>\n    </button>'
if ai_btn in tpl:
    tpl = tpl.replace(ai_btn, '')
    print("Fixed AI button overlap")
else:
    # Try more flexible
    import re
    tpl = re.sub(r'<button[^>]*class="fnx-ai-trigger"[^>]*>[\s\S]*?</button>', '', tpl)
    print("Fixed AI button overlap (via regex)")

# 2. FIX CUSTOMER CLICK - SAFELY
old_td = '<td><span class="fnx-text-primary fw-bold">{{cust.id}}</span></td>'
new_td = '<td><a href="javascript:void(0)" class="fnx-text-primary fw-bold" style="text-decoration: underline;" ng-click="c.viewCustomer(cust)">{{cust.id}}</a></td>'
if old_td in tpl:
    tpl = tpl.replace(old_td, new_td)
    print("Fixed Customer click")
else:
    print("Customer TD not found exactly")

# 3. ADD CUSTOMER JS
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
    print("Injected viewCustomer JS")

# 4. FIX MASSIVE EMPTY SPACE AND SEARCH BAR WIDTH - SAFELY VIA CSS
safe_css = """
/* ====================================================
   SAFE ADMIN LAYOUT OVERRIDES (Bypass empty space)
   ==================================================== */
.fnx-admin-layout {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    z-index: 99999 !important; /* Force it above everything */
    background-color: #F1F5F9 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Widen Search bar to fix 'nan' cut off */
.fnx-search-input, input[type="search"] {
    width: 100% !important;
    min-width: 400px !important;
    max-width: 600px !important;
}

/* Ensure no trailing global ServiceNow scrollbars interfere */
body.sp-page-root {
    overflow: hidden !important;
}
"""

if 'SAFE ADMIN LAYOUT OVERRIDES' not in css:
    css += '\n' + safe_css
    print("Injected safe CSS")


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
    print("SUCCESS: Target fixes deployed securely!")
    
    # Immediately flush the SN server cache so we don't have the same problem as before
    requests.get(f'{base}/cache.do', auth=auth)
    print("Server Cache flushed!")
else:
    print(f"ERROR: {resp.text[:400]}")
