import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
data = r.json()['result']
tpl = data['template']
css = data['css']

# ---------------------------------------------------------------
# 1. ADD BACK BUTTON TO CUSTOMER LOGIN FORM HEADER
# ---------------------------------------------------------------
old_login_header = """<form ng-if="c.authMode === 'login' && !c.regSuccess" ng-submit="c.doLogin()" action="javascript:void(0);" class="fnx-auth-form">
                <div class="fnx-auth-form-header">
                    <h3 class="fnx-auth-form-title">WELCOME BACK</h3>
                    <p class="fnx-auth-form-sub">Sign in to continue to your FRAUDNEXUS workspace.</p>
                </div>"""

new_login_header = """<form ng-if="c.authMode === 'login' && !c.regSuccess" ng-submit="c.doLogin()" action="javascript:void(0);" class="fnx-auth-form">
                <button type="button" class="fnx-back-to-portal" ng-click="c.currentView = 'portalSelect'">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
                    Back to Portal Selection
                </button>
                <div class="fnx-auth-form-header">
                    <h3 class="fnx-auth-form-title">WELCOME BACK</h3>
                    <p class="fnx-auth-form-sub">Sign in to continue to your FRAUDNEXUS workspace.</p>
                </div>"""

if old_login_header in tpl:
    tpl = tpl.replace(old_login_header, new_login_header, 1)
    print('[DONE] Back button added to customer login')
else:
    print('[FAIL] Customer login header not found - check exact HTML')

# ---------------------------------------------------------------
# 2. ADD BACK BUTTON TO CUSTOMER REGISTRATION FORM
# ---------------------------------------------------------------
old_reg_header = """<form ng-if="c.authMode === 'register' && !c.regSuccess" ng-submit="c.doRegister()" action="javascript:void(0);" class="fnx-auth-form">
                <!-- 1. Full Name -->"""

new_reg_header = """<form ng-if="c.authMode === 'register' && !c.regSuccess" ng-submit="c.doRegister()" action="javascript:void(0);" class="fnx-auth-form">
                <button type="button" class="fnx-back-to-portal" ng-click="c.currentView = 'portalSelect'">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
                    Back to Portal Selection
                </button>
                <!-- 1. Full Name -->"""

if old_reg_header in tpl:
    tpl = tpl.replace(old_reg_header, new_reg_header, 1)
    print('[DONE] Back button added to registration form')
else:
    print('[FAIL] Register header not found - check exact HTML')

# ---------------------------------------------------------------
# 3. VERIFY ADMIN LOGIN BACK BUTTON EXISTS (already found from audit)
# ---------------------------------------------------------------
if "'portalSelect'" in tpl:
    print('[DONE] Admin login already has back button to portalSelect')
else:
    # Find admin login card and add back button
    old_admin_header = """<div class="fnx-login-header">
                <span class="fnx-subtitle">A D M I N &nbsp;&nbsp;P O R T A L</span>
                <h2>Welcome Back</h2>"""

    new_admin_header = """<button type="button" class="fnx-back-to-portal" ng-click="c.currentView = 'portalSelect'">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
                    Back to Portal Selection
                </button>
                <div class="fnx-login-header">
                <span class="fnx-subtitle">A D M I N &nbsp;&nbsp;P O R T A L</span>
                <h2>Welcome Back</h2>"""

    if old_admin_header in tpl:
        tpl = tpl.replace(old_admin_header, new_admin_header, 1)
        print('[DONE] Back button added to admin login')

# ---------------------------------------------------------------
# 4. CSS for back button
# ---------------------------------------------------------------
back_btn_css = """
/* ==========================================
   BACK TO PORTAL SELECTION BUTTON
   ========================================== */
.fnx-back-to-portal {
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.4rem !important;
    background: none !important;
    border: none !important;
    color: #64748B !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    padding: 0.5rem 0 !important;
    margin-bottom: 1.5rem !important;
    transition: color 0.2s ease !important;
    text-decoration: none !important;
}

.fnx-back-to-portal:hover {
    color: #0B57D0 !important;
}

.fnx-back-to-portal svg {
    flex-shrink: 0 !important;
    transition: transform 0.2s ease !important;
}

.fnx-back-to-portal:hover svg {
    transform: translateX(-3px) !important;
}

/* For admin login right card */
.fnx-login-card .fnx-back-to-portal {
    color: #94A3B8 !important;
}

.fnx-login-card .fnx-back-to-portal:hover {
    color: #0B57D0 !important;
}
"""

css += '\n\n' + back_btn_css

# Deploy
resp = requests.patch(
    f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
    auth=auth,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    json={'template': tpl, 'css': css}
)

if resp.status_code == 200:
    print('[DONE] All back buttons deployed successfully!')
else:
    print('[FAIL] Deploy failed:', resp.status_code, resp.text[:300])
