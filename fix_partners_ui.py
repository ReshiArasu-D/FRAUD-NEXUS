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

print("Applying styling and layout fixes...")

# 1. FIX THE PARTNERS TABLE STYLING
# The premium CSS targets .fnx-table, but the Partners table is .fnx-data-table!
css = css.replace('.fnx-table {', '.fnx-table, .fnx-data-table {')
css = css.replace('.fnx-table thead', '.fnx-table thead, .fnx-data-table thead')
css = css.replace('.fnx-table th', '.fnx-table th, .fnx-data-table th')
css = css.replace('.fnx-table td', '.fnx-table td, .fnx-data-table td')
css = css.replace('.fnx-table tbody', '.fnx-table tbody, .fnx-data-table tbody')

# Let's add extra spacing specific to the data table so columns don't squish
css += """
.fnx-data-table th {
    white-space: nowrap !important;
}
.fnx-data-table td {
    min-width: 120px !important;
}
.fnx-data-table td:nth-child(2),
.fnx-data-table th:nth-child(2) {
    min-width: 200px !important; /* Partner Name */
}
.fnx-data-table td:nth-child(4),
.fnx-data-table th:nth-child(4) {
    min-width: 180px !important; /* Organization */
}
.fnx-data-table td:last-child {
    min-width: 250px !important; /* Actions */
    white-space: nowrap !important;
}
"""

# 2. FIX SIDEBAR GLOBE & ADD GLOBAL LOGO
# The globe is in: <div class="fnx-hero-graphic">...</div>
# Let's completely wipe it using regex, matching only inside fnx-sidebar-footer
tpl = re.sub(
    r'(<div class="fnx-sidebar-footer">)[\s\S]*?(</div>\s*</aside>)',
    r'\1\n                <div class="fnx-sidebar-footer-text">\n                    <p>FraudNexus Admin Workspace</p>\n                </div>\n            \2',
    tpl
)
print("Cleaned up sidebar footer globe")


# Add the Global Logo at the top of the sidebar nav
sidebar_nav_pattern = r'<nav class="fnx-sidebar-nav">'
global_logo_html = """
            <div class="fnx-sidebar-brand" style="padding: 1.5rem; display: flex; align-items: center; gap: 0.75rem; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 1rem;">
                <svg width="32" height="32" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M26 4L8 11v14c0 11.05 7.68 21.37 18 24 10.32-2.63 18-12.95 18-24V11L26 4z" fill="#0B1F3A" stroke="#3B82F6" stroke-width="2"/>
                    <circle cx="24" cy="24" r="7" fill="none" stroke="#60A5FA" stroke-width="2.5"/>
                    <line x1="29" y1="29" x2="35" y2="35" stroke="#60A5FA" stroke-width="2.5" stroke-linecap="round"/>
                </svg>
                <div style="display: flex; flex-direction: column;">
                    <span style="color: #FFFFFF; font-weight: 800; font-size: 1.15rem; letter-spacing: 0.5px; line-height: 1;">FRAUDNEXUS</span>
                    <span style="color: #60A5FA; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; margin-top: 2px;">Admin Portal</span>
                </div>
            </div>
"""

# Only inject if it's not already there
if 'class="fnx-sidebar-brand"' not in tpl:
    tpl = tpl.replace(sidebar_nav_pattern, global_logo_html + '\n            ' + sidebar_nav_pattern)
    print("Injected global logo into sidebar top")


# Cache bust
import time
tpl = re.sub(r'<!-- CACHE BUST: .*? -->\n*', '', tpl)
tpl = f'<!-- CACHE BUST: {int(time.time())} -->\n' + tpl


# Deploy
resp = requests.patch(
    f"{base}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    json={'template': tpl, 'css': css}
)

if resp.status_code == 200:
    print("SUCCESS: Fixes deployed!")
    requests.get(f'{base}/cache.do', auth=auth)
    print("Server Cache flushed!")
else:
    print(f"ERROR: {resp.text[:400]}")
