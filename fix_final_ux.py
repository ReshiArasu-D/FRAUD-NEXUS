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

# 1. KILL ALL NATIVE SCROLLING
nuke_scroll_style = """
<style>
    body, html, .sp-page-root, .sp-widget-content, section.page, main.body, .sp-page-row {
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        height: 100vh !important;
        max-height: 100vh !important;
    }
</style>
"""
if '<style>' not in tpl:
    tpl = nuke_scroll_style + tpl

# 2. DELETE THE DUPLICATE AI BUTTON ENTIRELY to permanently stop overlap
# Find: <button class="fnx-ai-trigger" ... </button>
tpl = re.sub(r'<button[^>]*class="fnx-ai-trigger"[^>]*>[\s\S]*?</button>', '', tpl)

# 3. FIX SEARCH BAR WIDTH SO PLACEHOLDER ISN'T CUT OFF
css += """
.fnx-search-input, input[type="search"] {
    width: 100% !important;
    min-width: 400px !important;
    max-width: 600px !important;
}
"""

# 4. REMOVE GLOBE LOGO FROM SIDEBAR
globe_pattern = r'<div class="fnx-hero-graphic">[\s\S]*?</div>\s*<div class="fnx-sidebar-footer-text">[\s\S]*?</div>'
tpl = re.sub(globe_pattern, '', tpl)

# 5. ADD CUSTOMER CLICK LISTENER
# Find the customer ID cell: <td><span class="fnx-text-primary fw-bold">{{cust.id}}</span></td>
# We will wrap the text in an anchor tag and add ng-click
cust_id_pattern = r'<td><span class="fnx-text-primary fw-bold">{{cust\.id}}</span></td>'
tpl = re.sub(cust_id_pattern, r'<td><a href="javascript:void(0)" class="fnx-text-primary fw-bold" style="text-decoration: none;" ng-click="c.viewCustomer(cust)">{{cust.id}}</a></td>', tpl)

# Inject client script function to show customer details
cs_inject = """
    c.viewCustomer = function(cust) {
        c.selectedCustomer = cust;
        // Simple built-in alert or custom modal. We'll use a standard alert for now to ensure it works.
        // Or if spModal is injected, use it. But alert is safest if we don't know dependencies.
        if (typeof spModal !== 'undefined') {
            spModal.alert('Customer Profile: ' + cust.name + '\\nID: ' + cust.id + '\\nEmail: ' + cust.email);
        } else {
            alert('Customer Details:\\n\\nID: ' + cust.id + '\\nName: ' + cust.name + '\\nEmail: ' + cust.email + '\\nKYC Status: ' + cust.kycStatus);
        }
    };
"""
if 'c.viewCustomer =' not in cs:
    cs = cs.replace('c.loadAdminCustomers = function() {', cs_inject + '\n    c.loadAdminCustomers = function() {')

# Deploy updates
resp = requests.patch(
    f"{base}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    json={'template': tpl, 'css': css, 'client_script': cs}
)

if resp.status_code == 200:
    print("SUCCESS: Fixes deployed!")
else:
    print(f"ERROR: {resp.text[:400]}")
