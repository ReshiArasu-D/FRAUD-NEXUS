import requests, re, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

# Fetch latest
r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
data = r.json()['result']
tpl = data['template']
css = data['css']
js = data['client_script']

# 1. Fix JS Pre-filled data
js = js.replace(
    "c.adminForm = { email: 'alex.morgan@fraudnexus.com', password: 'DemoPass123!', showPassword: false };",
    "c.adminForm = { email: '', password: '', showPassword: false };"
)

# 2. Fix Left Panel HTML
left_panel_pattern = re.compile(r'<div class="fnx-admin-login-left">.*?</div>\s*<div class="fnx-admin-login-right">', re.DOTALL)
new_left_panel = """
<div class="fnx-admin-login-left">
    <div class="fnx-left-inner">
        <div class="fnx-login-brand">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#003366" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                <circle cx="12" cy="11" r="3"></circle>
                <line x1="14" y1="13" x2="16" y2="15"></line>
            </svg>
            <div class="fnx-brand-text">
                <h1>FRAUDNEXUS</h1>
                <p>Financial & Cyber Fraud Investigation Hub</p>
            </div>
        </div>
        
        <div class="fnx-hero-content">
            <h2>Smarter Investigations<br>for a Safer Digital World.</h2>
            <p>Unifying people, evidence and intelligence to detect, investigate and prevent financial and cyber fraud.</p>
        </div>
        
        <div class="fnx-features-grid">
            <div class="fnx-feature-item">
                <div class="fnx-feature-icon-box">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                </div>
                <span>Centralized<br>Case Management</span>
            </div>
            <div class="fnx-feature-item">
                <div class="fnx-feature-icon-box">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="5" r="3"></circle><line x1="12" y1="22" x2="12" y2="8"></line><path d="M5 12H2a10 10 0 0 0 20 0h-3"></path></svg>
                </div>
                <span>AI-Powered<br>Evidence Intelligence</span>
            </div>
            <div class="fnx-feature-item">
                <div class="fnx-feature-icon-box">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                </div>
                <span>Risk Analysis<br>& Insights</span>
            </div>
            <div class="fnx-feature-item">
                <div class="fnx-feature-icon-box">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><polyline points="9 12 11 14 15 10"></polyline></svg>
                </div>
                <span>Compliant &<br>Secure Platform</span>
            </div>
        </div>
    </div>
    <div class="fnx-globe-bg">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 200" preserveAspectRatio="xMidYMax slice" width="100%" height="100%" style="position:absolute; bottom:0; opacity:0.6;">
            <circle cx="200" cy="180" r="160" fill="none" stroke="#60A5FA" stroke-width="1" opacity="0.3"/>
            <circle cx="200" cy="180" r="120" fill="none" stroke="#60A5FA" stroke-width="1" opacity="0.4"/>
            <circle cx="200" cy="180" r="80" fill="none" stroke="#60A5FA" stroke-width="1" opacity="0.5"/>
            <path d="M40 180 Q200 -20 360 180" fill="none" stroke="#60A5FA" stroke-width="1.5" opacity="0.4"/>
            <path d="M80 180 Q200 40 320 180" fill="none" stroke="#60A5FA" stroke-width="1.5" opacity="0.5"/>
            <path d="M120 180 Q200 100 280 180" fill="none" stroke="#60A5FA" stroke-width="1.5" opacity="0.6"/>
            <!-- Dots -->
            <circle cx="120" cy="95" r="3" fill="#2563EB"/>
            <circle cx="280" cy="95" r="3" fill="#2563EB"/>
            <circle cx="200" cy="20" r="3" fill="#2563EB"/>
            <circle cx="160" cy="120" r="3" fill="#2563EB"/>
            <circle cx="240" cy="120" r="3" fill="#2563EB"/>
            <line x1="120" y1="95" x2="200" y2="20" stroke="#93C5FD" stroke-width="1" opacity="0.8"/>
            <line x1="280" y1="95" x2="200" y2="20" stroke="#93C5FD" stroke-width="1" opacity="0.8"/>
            <line x1="120" y1="95" x2="160" y2="120" stroke="#93C5FD" stroke-width="1" opacity="0.8"/>
            <line x1="280" y1="95" x2="240" y2="120" stroke="#93C5FD" stroke-width="1" opacity="0.8"/>
            <line x1="160" y1="120" x2="240" y2="120" stroke="#93C5FD" stroke-width="1" opacity="0.8"/>
        </svg>
    </div>
</div>
<div class="fnx-admin-login-right">"""

if left_panel_pattern.search(tpl):
    tpl = left_panel_pattern.sub(new_left_panel, tpl, 1)
else:
    print("Failed to find left panel HTML to replace")

# 3. Add Left Panel CSS Overrides
css_fixes = """
/* OVERRIDES TO FIX LEFT PANEL LAYOUT EXACTLY AS IMAGE */
.fnx-admin-login-left {
    flex: 1.2 !important;
    background: linear-gradient(180deg, #F8FAFC 0%, #E0F2FE 100%) !important;
    padding: 0 !important;
    display: block !important;
    position: relative !important;
    overflow: hidden !important;
}

.fnx-admin-login-left::after {
    display: none !important;
}

.fnx-left-inner {
    padding: 6rem 5rem !important;
    position: relative !important;
    z-index: 10 !important;
    height: 100% !important;
    box-sizing: border-box !important;
}

.fnx-features-grid {
    display: flex !important;
    gap: 1.5rem !important;
    margin-top: 3.5rem !important;
}

.fnx-feature-item {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    text-align: center !important;
    flex: 1 !important;
}

.fnx-feature-icon-box {
    width: 60px !important;
    height: 60px !important;
    background: #EFF6FF !important;
    border-radius: 12px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin-bottom: 1rem !important;
    color: #2563EB !important;
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.08) !important;
}

.fnx-feature-icon-box svg {
    width: 26px !important;
    height: 26px !important;
}

.fnx-feature-item span {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: #1E293B !important;
    line-height: 1.4 !important;
}

.fnx-globe-bg {
    position: absolute !important;
    bottom: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 35vh !important;
    z-index: 1 !important;
    pointer-events: none !important;
    background: radial-gradient(circle at 50% 100%, #BFDBFE 0%, transparent 70%) !important;
}
"""

css += '\n\n' + css_fixes

# Push changes
resp = requests.patch(
    f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
    auth=auth,
    headers={'Accept':'application/json', 'Content-Type':'application/json'},
    json={'template': tpl, 'css': css, 'client_script': js}
)
if resp.status_code == 200:
    print('Deploy successful! Left layout and JS fixed.')
else:
    print('Deploy failed:', resp.text)
