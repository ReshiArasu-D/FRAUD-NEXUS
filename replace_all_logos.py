import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

# The NEW global logo SVG (shield with magnifying glass like the screenshot)
# Uses inline SVG matching the blue shield + Q/search icon from user's reference image
LOGO_SVG_LARGE = """<svg width="52" height="52" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M26 4L8 11v14c0 11.05 7.68 21.37 18 24 10.32-2.63 18-12.95 18-24V11L26 4z" fill="#E8F0FE" stroke="#0B57D0" stroke-width="2"/>
    <circle cx="24" cy="24" r="7" fill="none" stroke="#0B57D0" stroke-width="2.5"/>
    <line x1="29" y1="29" x2="35" y2="35" stroke="#0B57D0" stroke-width="2.5" stroke-linecap="round"/>
</svg>"""

LOGO_SVG_MEDIUM = """<svg width="38" height="38" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M26 4L8 11v14c0 11.05 7.68 21.37 18 24 10.32-2.63 18-12.95 18-24V11L26 4z" fill="#E8F0FE" stroke="#0B57D0" stroke-width="2"/>
    <circle cx="24" cy="24" r="7" fill="none" stroke="#0B57D0" stroke-width="2.5"/>
    <line x1="29" y1="29" x2="35" y2="35" stroke="#0B57D0" stroke-width="2.5" stroke-linecap="round"/>
</svg>"""

LOGO_SVG_SMALL = """<svg width="28" height="28" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M26 4L8 11v14c0 11.05 7.68 21.37 18 24 10.32-2.63 18-12.95 18-24V11L26 4z" fill="#E8F0FE" stroke="#0B57D0" stroke-width="2"/>
    <circle cx="24" cy="24" r="7" fill="none" stroke="#0B57D0" stroke-width="2.5"/>
    <line x1="29" y1="29" x2="35" y2="35" stroke="#0B57D0" stroke-width="2.5" stroke-linecap="round"/>
</svg>"""

# Read the current template
with open('d:/KPMG/working_template.html', 'r', encoding='utf-8') as f:
    tpl = f.read()

# ---------------------------------------------------------------
# 1. LANDING PAGE NAV LOGO (line ~10-12)
# ---------------------------------------------------------------
old_landing_logo = '''<div class="fnx-landing-brand">
            <svg width="34" height="34" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="none" stroke="#00B8D9" stroke-width="2.5"/><path d="M13 15h14M13 20h10M13 25h7" stroke="#00B8D9" stroke-width="2" stroke-linecap="round"/><circle cx="28" cy="25" r="4" fill="none" stroke="#00B8D9" stroke-width="1.5"/><line x1="31" y1="28" x2="34" y2="31" stroke="#00B8D9" stroke-width="1.5" stroke-linecap="round"/></svg>
            <span class="fnx-brand-text">{{c.t('brand')}}</span>
        </div>'''

new_landing_logo = '''<div class="fnx-landing-brand">
            ''' + LOGO_SVG_MEDIUM + '''
            <div class="fnx-brand-wordmark">
                <span class="fnx-brand-name">FRAUDNEXUS</span>
                <span class="fnx-brand-tagline">Financial &amp; Cyber Fraud Investigation Hub</span>
            </div>
        </div>'''

if old_landing_logo in tpl:
    tpl = tpl.replace(old_landing_logo, new_landing_logo)
    print('✓ Landing page logo replaced')
else:
    print('✗ Landing page logo NOT found - trying partial')
    idx = tpl.find('<div class="fnx-landing-brand">')
    if idx != -1:
        print(f'  Found at index {idx}: {tpl[idx:idx+200]}')

# ---------------------------------------------------------------
# 2. CUSTOMER LOGIN LEFT PANEL (line ~142-145)
# ---------------------------------------------------------------
old_auth_logo = '''<div class="fnx-auth-brand" ng-click="c.currentView = 'landing'">
            <svg width="34" height="34" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="none" stroke="#00B8D9" stroke-width="2.5"/><path d="M13 15h14M13 20h10M13 25h7" stroke="#00B8D9" stroke-width="2" stroke-linecap="round"/><circle cx="28" cy="25" r="4" fill="none" stroke="#00B8D9" stroke-width="1.5"/><line x1="31" y1="28" x2="34" y2="31" stroke="#00B8D9" stroke-width="1.5" stroke-linecap="round"/></svg>
            <span>FRAUDNEXUS</span>
        </div>'''

new_auth_logo = '''<div class="fnx-auth-brand" ng-click="c.currentView = 'landing'">
            ''' + LOGO_SVG_MEDIUM + '''
            <div class="fnx-brand-wordmark">
                <span class="fnx-brand-name">FRAUDNEXUS</span>
                <span class="fnx-brand-tagline">Financial &amp; Cyber Fraud Investigation Hub</span>
            </div>
        </div>'''

if old_auth_logo in tpl:
    tpl = tpl.replace(old_auth_logo, new_auth_logo)
    print('✓ Customer login logo replaced')
else:
    print('✗ Customer login logo NOT found - trying partial')

# ---------------------------------------------------------------
# 3. ADMIN LOGIN LEFT PANEL (line ~1684-1693)
# ---------------------------------------------------------------
old_admin_login_logo = '''<div class="fnx-login-brand">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#003366" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                <circle cx="12" cy="11" r="3"></circle>
                <line x1="14" y1="13" x2="16" y2="15"></line>
            </svg>
            <div class="fnx-brand-text">
                <h1>FRAUDNEXUS</h1>
                <p>Financial & Cyber Fraud Investigation Hub</p>
            </div>
        </div>'''

new_admin_login_logo = '''<div class="fnx-login-brand">
            ''' + LOGO_SVG_LARGE + '''
            <div class="fnx-brand-wordmark">
                <span class="fnx-brand-name">FRAUDNEXUS</span>
                <span class="fnx-brand-tagline">Financial &amp; Cyber Fraud Investigation Hub</span>
            </div>
        </div>'''

if old_admin_login_logo in tpl:
    tpl = tpl.replace(old_admin_login_logo, new_admin_login_logo)
    print('✓ Admin login logo replaced')
else:
    print('✗ Admin login logo NOT found')

# ---------------------------------------------------------------
# 4. ADMIN TOPBAR (line ~1815-1823)
# ---------------------------------------------------------------
old_admin_topbar_logo = '''<div class="fnx-admin-topbar-brand" ng-click="c.setAdminModule('commandCenter')">
                <svg width="28" height="28" viewBox="0 0 40 40">
                    <circle cx="20" cy="20" r="18" fill="none" stroke="#00B8D9" stroke-width="2.5"/>
                    <path d="M13 15h14M13 20h10M13 25h7" stroke="#00B8D9" stroke-width="2" stroke-linecap="round"/>
                    <circle cx="28" cy="25" r="4" fill="none" stroke="#00B8D9" stroke-width="1.5"/>
                    <line x1="31" y1="28" x2="34" y2="31" stroke="#00B8D9" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
                <span class="fnx-admin-topbar-title">FRAUDNEXUS</span>
            </div>'''

new_admin_topbar_logo = '''<div class="fnx-admin-topbar-brand" ng-click="c.setAdminModule('commandCenter')">
                ''' + LOGO_SVG_SMALL + '''
                <div class="fnx-brand-wordmark fnx-topbar-wordmark">
                    <span class="fnx-brand-name">FRAUDNEXUS</span>
                    <span class="fnx-brand-tagline">Admin Portal</span>
                </div>
            </div>'''

if old_admin_topbar_logo in tpl:
    tpl = tpl.replace(old_admin_topbar_logo, new_admin_topbar_logo)
    print('✓ Admin topbar logo replaced')
else:
    print('✗ Admin topbar logo NOT found - trying partial match')
    idx = tpl.find('class="fnx-admin-topbar-brand"')
    if idx != -1:
        print(f'  Found at index {idx}: {tpl[idx:idx+300]}')

# Save updated template
with open('d:/KPMG/working_template.html', 'w', encoding='utf-8') as f:
    f.write(tpl)

print('\nTemplate saved with logo updates.')
