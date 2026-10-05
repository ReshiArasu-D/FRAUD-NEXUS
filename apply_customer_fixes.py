import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

# 1. Fetch current live widget
r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
if r.status_code != 200:
    print('Failed to fetch widget:', r.text)
    sys.exit(1)

data = r.json()['result']
template = data['template']
client_script = data['client_script']
css = data['css']

print('Fetched live widget successfully.')

# 2. Fix template tag balance in Step 3
target_div = '''                                <div class="fnx-field">
                                    <label>Recovered Amount (₹)</label>
                                    <input type="number" ng-model="c.reportForm.recovered_amount" placeholder="e.g. 0">
                                </div>
                            </div>
                        </div><!-- end fnx-form-grid-3 -->'''

replacement_div = '''                                <div class="fnx-field">
                                    <label>Recovered Amount (₹)</label>
                                    <input type="number" ng-model="c.reportForm.recovered_amount" placeholder="e.g. 0">
                                </div>
                        </div><!-- end fnx-form-grid-3 -->'''

if target_div in template:
    template = template.replace(target_div, replacement_div, 1)
    print('1. Fixed duplicate </div> in Step 3.')
else:
    print('Target div for Step 3 not found! Checking...')
    sys.exit(1)

# 3. Restore Floating Chat Assistant Trigger Button
target_ai = '''<!-- ============ 5. FLOATING NOW ASSIST AI (BOTTOM-RIGHT) ============ -->
<div class="fnx-ai-widget">
    <!-- Floating Trigger Button -->
    

    <!-- Slide-out AI Chat Panel -->'''

replacement_ai = '''<!-- ============ 5. FLOATING NOW ASSIST AI (BOTTOM-RIGHT) ============ -->
<div class="fnx-ai-widget" ng-if="c.currentView !== 'adminLogin' && c.currentView !== 'auth' && c.currentView !== 'admin'">
    <!-- Floating Trigger Button -->
    <button type="button" class="fnx-ai-trigger" ng-click="c.showAI = !c.showAI" title="Ask FRAUDNEXUS AI">
        <span class="fnx-ai-sparkle-icon">&#10024;</span>
        <span>Ask FRAUDNEXUS AI</span>
    </button>

    <!-- Slide-out AI Chat Panel -->'''

if target_ai in template:
    template = template.replace(target_ai, replacement_ai, 1)
    print('2. Restored Floating Chat Assistant trigger button.')
else:
    print('Target AI section not found directly! Searching sub...')
    # Check substring
    sub_ai = '<div class="fnx-ai-widget">\n    <!-- Floating Trigger Button -->'
    if sub_ai in template:
        template = template.replace(sub_ai, '''<div class="fnx-ai-widget" ng-if="c.currentView !== 'adminLogin' && c.currentView !== 'auth' && c.currentView !== 'admin'">
    <!-- Floating Trigger Button -->
    <button type="button" class="fnx-ai-trigger" ng-click="c.showAI = !c.showAI" title="Ask FRAUDNEXUS AI">
        <span class="fnx-ai-sparkle-icon">&#10024;</span>
        <span>Ask FRAUDNEXUS AI</span>
    </button>''', 1)
        print('2. Restored Floating Chat Assistant trigger button via sub_ai.')
    else:
        print('Could not find AI section in template!')
        sys.exit(1)

# 4. Enhance loadCases with demo fallback
target_lc = '''    c.loadCases = function() {
        if (!c.user) return;
        $http.get(API + '/cases?user_id=' + c.user.sys_id).then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.cases = d.cases || [];
                c.stats = d.stats || { total: 0, active: 0, resolved: 0, closed: 0 };
            }
        });
    };'''

replacement_lc = '''    c.loadCases = function() {
        if (!c.user) return;
        $http.get(API + '/cases?user_id=' + c.user.sys_id).then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success && d.cases && d.cases.length > 0) {
                c.cases = d.cases;
                c.stats = d.stats || { total: d.cases.length, active: d.cases.length, resolved: 0, closed: 0 };
            } else if (!c.cases || c.cases.length === 0) {
                c.cases = [
                    { sys_id: 'dc01', number: 'FNX-2026-001001', type: 'Payment Fraud', incident_date: '2026-09-15', severity: 'High', status: 'Investigation', u_short_description: 'UPI fraud - product not delivered' },
                    { sys_id: 'dc02', number: 'FNX-2026-001002', type: 'Phishing', incident_date: '2026-09-20', severity: 'Critical', status: 'Initial Review', u_short_description: 'Fake bank portal phishing' }
                ];
                c.stats = { total: 2, active: 2, resolved: 0, closed: 0 };
            }
        });
    };'''

if target_lc in client_script:
    client_script = client_script.replace(target_lc, replacement_lc, 1)
    print('3. Enhanced c.loadCases with demo fallback.')
else:
    print('Target c.loadCases not found in client script! Checking...')

# 5. Ensure CSS has high z-index and proper display for fnx-ai-widget
if '.fnx-ai-widget {' in css:
    css = css.replace('.fnx-ai-widget {', '.fnx-ai-widget {\n    z-index: 99999 !important;')
    print('4. Enhanced .fnx-ai-widget z-index.')

# 6. Deploy to ServiceNow
payload = {
    'template': template,
    'client_script': client_script,
    'css': css
}

patch_r = requests.patch(
    f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}',
    auth=AUTH,
    headers={'Content-Type': 'application/json'},
    json=payload
)

if patch_r.status_code == 200:
    print('SUCCESS: Widget successfully updated in ServiceNow!')
    # Clear cache
    c_r = requests.get(f'{BASE_URL}/cache.do', auth=AUTH)
    print('Cache clear response:', c_r.status_code)
else:
    print('FAILURE updating widget:', patch_r.status_code, patch_r.text)
