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

print("Applying final 2 fixes...")

# 1. FIX SEARCH BAR WIDTH (Hardcode style into HTML to guarantee it works)
old_input = '<input type="text" placeholder="Search customer ID, name, email, phone..." ng-model="c.custSearch" ng-change="c.loadAdminCustomers()" class="fnx-search-input">'
new_input = '<input type="text" placeholder="Search customer ID, name, email, phone..." ng-model="c.custSearch" ng-change="c.loadAdminCustomers()" class="fnx-search-input" style="min-width: 450px; width: 100%;">'
if old_input in tpl:
    tpl = tpl.replace(old_input, new_input)
    print("Fixed Search Bar inline style")
else:
    # Try more robust replacement
    import re
    tpl = re.sub(
        r'<input type="text" placeholder="Search customer ID, name, email, phone\.\.\." ng-model="c\.custSearch"[^>]*>', 
        '<input type="text" placeholder="Search customer ID, name, email, phone..." ng-model="c.custSearch" ng-change="c.loadAdminCustomers()" class="fnx-search-input" style="min-width: 450px; width: 100%;">', 
        tpl
    )
    print("Fixed Search Bar via regex")


# 2. FIX SIDEBAR GLOBAL LOGO
# A. Remove the globe graphic from the sidebar
# We must ONLY target the one in the sidebar. Let's find the exact string.
sidebar_bottom = """<div class="fnx-sidebar-footer">
                <div class="fnx-hero-graphic">
                    <svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="0.5">
                        <circle cx="50" cy="50" r="40" stroke="#3B82F6"/>
                        <circle cx="50" cy="50" r="40" stroke="#60A5FA" opacity="0.3" transform="rotate(45 50 50) scale(1 0.4)"/>
                        <circle cx="50" cy="50" r="40" stroke="#60A5FA" opacity="0.3" transform="rotate(-45 50 50) scale(1 0.4)"/>
                        <path d="M50 10 L50 90" stroke="#3B82F6" opacity="0.5"/>
                        <path d="M10 50 L90 50" stroke="#3B82F6" opacity="0.5"/>
                        <circle cx="30" cy="40" r="2" fill="#00E5FF"/>
                        <circle cx="70" cy="60" r="2" fill="#00E5FF"/>
                        <circle cx="60" cy="30" r="2" fill="#00E5FF"/>
                        <path d="M30 40 L60 30 L70 60" stroke="#00E5FF" opacity="0.7"/>
                    </svg>
                </div>
                <div class="fnx-sidebar-footer-text">
                    <strong>From Fraud Report<br>to Resolution</strong>
                    <p>One Investigation Workspace</p>
                </div>
            </div>"""

if sidebar_bottom in tpl:
    tpl = tpl.replace(sidebar_bottom, '')
    print("Removed globe from sidebar safely")

# B. Add the Global Logo to the top of the sidebar
sidebar_nav = '<nav class="fnx-sidebar-nav">'
global_logo_sidebar = """
            <div class="fnx-sidebar-logo" style="padding: 1.5rem; display: flex; align-items: center; gap: 0.75rem; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 1rem;">
                <svg width="28" height="28" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M26 4L8 11v14c0 11.05 7.68 21.37 18 24 10.32-2.63 18-12.95 18-24V11L26 4z" fill="#E8F0FE" stroke="#3B82F6" stroke-width="2"/>
                    <circle cx="24" cy="24" r="7" fill="none" stroke="#3B82F6" stroke-width="2.5"/>
                    <line x1="29" y1="29" x2="35" y2="35" stroke="#3B82F6" stroke-width="2.5" stroke-linecap="round"/>
                </svg>
                <div style="display: flex; flex-direction: column;">
                    <span style="color: #FFFFFF; font-weight: 800; font-size: 1.1rem; letter-spacing: 0.5px;">FRAUDNEXUS</span>
                    <span style="color: #60A5FA; font-weight: 600; font-size: 0.7rem; text-transform: uppercase;">Admin Portal</span>
                </div>
            </div>
"""

# Only inject if not already there
if 'class="fnx-sidebar-logo"' not in tpl:
    tpl = tpl.replace(sidebar_nav, global_logo_sidebar + sidebar_nav)
    print("Injected global logo into sidebar")

# 3. Clean up the Header Logo since we moved it to the sidebar
# Actually, modern dashboards usually don't have duplicate logos. Let's remove the logo from fnx-admin-topbar.
topbar_logo = """<div class="fnx-brand-wordmark fnx-topbar-wordmark">
                <span class="fnx-brand-name">FRAUDNEXUS</span>
                <span class="fnx-brand-tagline">Admin Portal</span>
            </div>"""
if topbar_logo in tpl:
    tpl = tpl.replace(topbar_logo, '')
    # Also remove the svg shield next to it
    topbar_shield = """<svg width="28" height="28" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M26 4L8 11v14c0 11.05 7.68 21.37 18 24 10.32-2.63 18-12.95 18-24V11L26 4z" fill="#E8F0FE" stroke="#0B57D0" stroke-width="2"/>
                <circle cx="24" cy="24" r="7" fill="none" stroke="#0B57D0" stroke-width="2.5"/>
                <line x1="29" y1="29" x2="35" y2="35" stroke="#0B57D0" stroke-width="2.5" stroke-linecap="round"/>
            </svg>"""
    tpl = tpl.replace(topbar_shield, '')
    print("Removed duplicate logo from top header")

# Cache bust
import time
tpl = re.sub(r'<!-- CACHE BUST: .*? -->\n*', '', tpl)
tpl = f'<!-- CACHE BUST: {int(time.time())} -->\n' + tpl

# Deploy
resp = requests.patch(
    f"{base}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    json={'template': tpl}
)

if resp.status_code == 200:
    print("SUCCESS!")
    requests.get(f'{base}/cache.do', auth=auth)
else:
    print(f"ERROR: {resp.text[:400]}")
