import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
data = r.json()['result']
tpl = data['template']
css = data['css']
js = data['client_script']

# ---------------------------------------------------------------
# 1. FIX DEMO BUTTON HTML - send demo:true flag instead of email/password
# ---------------------------------------------------------------
old_demo_btn = """<button type="button" class="fnx-btn-demo" ng-click="c.adminForm.email='alex.morgan@fraudnexus.com'; c.adminForm.password='admin123'; c.doAdminLogin()">
                    <span class="rocket-icon">🚀</span>
                    <div class="demo-btn-text">
                        <strong>Demo Quick Login</strong>
                        <span>Access a pre-configured demo account</span>
                    </div>
                </button>"""

new_demo_btn = """<button type="button" class="fnx-btn-demo" ng-click="c.doAdminDemoLogin()">
                    <span class="rocket-icon">🚀</span>
                    <div class="demo-btn-text">
                        <strong>Demo Quick Login</strong>
                        <span>Access a pre-configured demo account</span>
                    </div>
                </button>"""

if old_demo_btn in tpl:
    tpl = tpl.replace(old_demo_btn, new_demo_btn)
    print('✓ Demo button HTML fixed')
else:
    # Fallback: find any ng-click with admin123 and fix it
    import re
    tpl = re.sub(
        r"ng-click=\"c\.adminForm\.email='[^']+';[^\"]+c\.doAdminLogin\(\)\"",
        "ng-click=\"c.doAdminDemoLogin()\"",
        tpl
    )
    print('✓ Demo button HTML fixed via regex')

# ---------------------------------------------------------------
# 2. FIX BUTTON CSS - make demo button text visible
# ---------------------------------------------------------------
demo_btn_css_fix = """
/* DEMO BUTTON - fix text visibility */
.fnx-btn-demo {
    width: 100% !important;
    padding: 1rem 1.5rem !important;
    background-color: #EFF6FF !important;
    border: 1.5px solid #93C5FD !important;
    border-radius: 8px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 1rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    color: #1E3A8A !important;
}

.fnx-btn-demo:hover {
    background-color: #DBEAFE !important;
    border-color: #3B82F6 !important;
}

.rocket-icon {
    font-size: 1.5rem !important;
    flex-shrink: 0 !important;
}

.demo-btn-text {
    text-align: left !important;
}

.demo-btn-text strong {
    display: block !important;
    color: #1E3A8A !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.1rem !important;
}

.demo-btn-text span {
    display: block !important;
    color: #3B82F6 !important;
    font-size: 0.75rem !important;
}
"""

css += '\n\n' + demo_btn_css_fix

# ---------------------------------------------------------------
# 3. ADD doAdminDemoLogin function to client script
# ---------------------------------------------------------------
demo_login_fn = """
    c.doAdminDemoLogin = function() {
        c.adminError = '';
        c.adminLoading = true;
        $http.post(API + '/admin_login', { demo: true })
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.adminUser = d.user;
                c.isAdminDemo = true;
                c.currentView = 'adminWorkspace';
                c.adminModule = 'commandCenter';
                c.scrollToTop();
                c.loadAdminDashboard();
                c.loadPartners();
            } else {
                c.adminError = d.error || 'Demo login failed.';
            }
            c.adminLoading = false;
        }, function(err) {
            c.adminError = 'Network error. Please try again.';
            c.adminLoading = false;
        });
    };
"""

# Insert before doAdminLogin
if 'doAdminDemoLogin' not in js:
    js = js.replace(
        'doAdminLogin = function() {',
        demo_login_fn + '\n    doAdminLogin = function() {'
    )
    print('✓ doAdminDemoLogin function added to client script')
else:
    print('✓ doAdminDemoLogin already exists in client script')

# Deploy
resp = requests.patch(
    f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
    auth=auth,
    headers={'Accept':'application/json', 'Content-Type':'application/json'},
    json={'template': tpl, 'css': css, 'client_script': js}
)

if resp.status_code == 200:
    print('✓ All fixes deployed successfully!')
else:
    print('✗ Deploy failed:', resp.status_code, resp.text[:300])
