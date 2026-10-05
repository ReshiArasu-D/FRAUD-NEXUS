import requests, re, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

# Load template and css
with open('d:/KPMG/working_template.html', 'r', encoding='utf-8') as f:
    tpl = f.read()
    
with open('d:/KPMG/working_css.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Define the new HTML
new_html = """
<div ng-if="c.currentView === 'adminLogin'" class="fnx-admin-login-page">
    <div class="fnx-admin-login-left">
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
        
        <div class="fnx-features-row">
            <div class="fnx-feature">
                <div class="fnx-feature-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="#0B57D0" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                </div>
                <span>Centralized<br>Case Management</span>
            </div>
            <div class="fnx-feature">
                <div class="fnx-feature-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="#0B57D0" stroke-width="2"><circle cx="12" cy="5" r="3"></circle><line x1="12" y1="22" x2="12" y2="8"></line><path d="M5 12H2a10 10 0 0 0 20 0h-3"></path></svg>
                </div>
                <span>AI-Powered<br>Evidence Intelligence</span>
            </div>
            <div class="fnx-feature">
                <div class="fnx-feature-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="#0B57D0" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                </div>
                <span>Risk Analysis<br>& Insights</span>
            </div>
            <div class="fnx-feature">
                <div class="fnx-feature-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="#0B57D0" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><polyline points="9 12 11 14 15 10"></polyline></svg>
                </div>
                <span>Compliant &<br>Secure Platform</span>
            </div>
        </div>
    </div>
    
    <div class="fnx-admin-login-right">
        <div class="fnx-login-card">
            <div class="fnx-login-header">
                <span class="fnx-subtitle">A D M I N &nbsp;&nbsp;P O R T A L</span>
                <h2>Welcome Back</h2>
                <p>Sign in to access the FRAUDNEXUS administration dashboard.</p>
            </div>
            
            <div ng-if="c.adminError" class="fnx-alert fnx-alert-error" style="margin-bottom:1.5rem">
                {{c.adminError}}
            </div>

            <form ng-submit="c.doAdminLogin()">
                <div class="fnx-form-group">
                    <label>Username</label>
                    <div class="fnx-input-icon-wrap">
                        <svg class="fnx-input-icon" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                        <input type="email" class="fnx-input" ng-model="c.adminForm.email" placeholder="Enter your username" required>
                    </div>
                </div>

                <div class="fnx-form-group">
                    <label>Password</label>
                    <div class="fnx-input-icon-wrap">
                        <svg class="fnx-input-icon" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                        <input type="{{c.adminForm.showPassword ? 'text' : 'password'}}" class="fnx-input" ng-model="c.adminForm.password" placeholder="Enter your password" required>
                        <button type="button" class="fnx-pwd-toggle" ng-click="c.adminForm.showPassword = !c.adminForm.showPassword">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                        </button>
                    </div>
                </div>

                <div class="fnx-login-options">
                    <label class="fnx-checkbox">
                        <input type="checkbox">
                        <span>Remember me</span>
                    </label>
                    <a href="javascript:void(0)" ng-click="c.adminError = 'Password reset instructions have been logged for this investigator account.'">Forgot Password?</a>
                </div>

                <button type="submit" class="fnx-btn-primary">Login &rarr;</button>

                <div class="fnx-divider">
                    <span>OR</span>
                </div>

                <button type="button" class="fnx-btn-demo" ng-click="c.adminForm.email='alex.morgan@fraudnexus.com'; c.adminForm.password='admin123'; c.doAdminLogin()">
                    <span class="rocket-icon">🚀</span>
                    <div class="demo-btn-text">
                        <strong>Demo Quick Login</strong>
                        <span>Access a pre-configured demo account</span>
                    </div>
                </button>
            </form>
        </div>
    </div>
</div>
"""

# Extract the old HTML block and replace
html_pattern = re.compile(r'<div ng-if="c\.currentView === \'adminLogin\'" class="fnx-admin-login-page">.*?</div>\s*</div>\s*</div>', re.DOTALL)
if html_pattern.search(tpl):
    tpl = html_pattern.sub(new_html, tpl, 1)
else:
    print("Warning: Could not find exact HTML bounds with regex. Using a simpler replace.")
    start = tpl.find('<div ng-if="c.currentView === \'adminLogin\'"')
    end = tpl.find('<!-- 2. ADMIN SHELL -->')
    if start != -1 and end != -1:
        tpl = tpl[:start] + new_html + "\n\n" + tpl[end:]
    else:
        print("Failed to replace HTML.")
        sys.exit(1)

# Define the new CSS
new_css = """
/* ============================================================
   ADMIN LOGIN SCREEN REDESIGN
   ============================================================ */
.fnx-admin-login-page {
    display: flex;
    min-height: 100vh;
    width: 100%;
    background-color: #F8FAFC;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.fnx-admin-login-left {
    flex: 1.2;
    background: linear-gradient(135deg, #FFFFFF 0%, #E3F2FD 100%);
    padding: 4rem 5rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
    overflow: hidden;
}

.fnx-admin-login-left::after {
    content: '';
    position: absolute;
    bottom: -100px;
    left: 0;
    right: 0;
    height: 400px;
    background: url('https://cdn.pixabay.com/photo/2016/10/09/08/32/digital-marketing-1725340_1280.jpg') no-repeat center bottom;
    background-size: cover;
    opacity: 0.15;
    pointer-events: none;
}

.fnx-login-brand {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 3rem;
}

.fnx-login-brand svg {
    filter: drop-shadow(0 4px 6px rgba(0, 51, 102, 0.1));
}

.fnx-brand-text h1 {
    font-size: 2.2rem;
    font-weight: 800;
    color: #0044CC;
    margin: 0;
    letter-spacing: -0.5px;
}

.fnx-brand-text p {
    font-size: 0.95rem;
    color: #475569;
    margin: 0;
    font-weight: 500;
}

.fnx-hero-content {
    margin-bottom: 3rem;
}

.fnx-hero-content h2 {
    font-size: 2.8rem;
    font-weight: 700;
    color: #0F172A;
    line-height: 1.2;
    margin-bottom: 1.25rem;
}

.fnx-hero-content p {
    font-size: 1.1rem;
    color: #64748B;
    line-height: 1.6;
    max-width: 500px;
}

.fnx-features-row {
    display: flex;
    gap: 1.5rem;
    margin-top: 1rem;
}

.fnx-feature {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    flex: 1;
}

.fnx-feature-icon {
    width: 56px;
    height: 56px;
    background-color: #E0F2FE;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
    box-shadow: 0 4px 12px rgba(11, 87, 208, 0.1);
}

.fnx-feature-icon svg {
    width: 28px;
    height: 28px;
}

.fnx-feature span {
    font-size: 0.85rem;
    font-weight: 600;
    color: #1E293B;
    line-height: 1.4;
}

.fnx-admin-login-right {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #F8FAFC;
    padding: 2rem;
}

.fnx-login-card {
    background: #FFFFFF;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.05);
    padding: 3.5rem 3rem;
    width: 100%;
    max-width: 480px;
}

.fnx-login-header {
    text-align: center;
    margin-bottom: 2.5rem;
}

.fnx-subtitle {
    display: block;
    font-size: 0.8rem;
    font-weight: 700;
    color: #94A3B8;
    margin-bottom: 0.5rem;
    letter-spacing: 2px;
}

.fnx-login-header h2 {
    font-size: 2rem;
    font-weight: 700;
    color: #0F172A;
    margin: 0 0 0.5rem 0;
}

.fnx-login-header p {
    font-size: 0.95rem;
    color: #64748B;
    margin: 0;
}

.fnx-form-group {
    margin-bottom: 1.5rem;
}

.fnx-form-group label {
    display: block;
    font-size: 0.85rem;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 0.5rem;
}

.fnx-input-icon-wrap {
    position: relative;
    display: flex;
    align-items: center;
}

.fnx-input-icon {
    position: absolute;
    left: 1rem;
    width: 20px;
    height: 20px;
    pointer-events: none;
}

.fnx-input {
    width: 100%;
    padding: 0.85rem 1rem 0.85rem 3rem !important;
    font-size: 0.95rem;
    color: #0F172A;
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    transition: all 0.2s ease;
}

.fnx-input:focus {
    outline: none;
    border-color: #0B57D0;
    box-shadow: 0 0 0 3px rgba(11, 87, 208, 0.1);
}

.fnx-pwd-toggle {
    position: absolute;
    right: 0.5rem;
    background: none;
    border: none;
    padding: 0.5rem;
    color: #94A3B8;
    cursor: pointer;
}

.fnx-pwd-toggle svg {
    width: 20px;
    height: 20px;
}

.fnx-login-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.fnx-checkbox {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    color: #64748B;
    cursor: pointer;
}

.fnx-checkbox input {
    width: 16px;
    height: 16px;
    accent-color: #0B57D0;
}

.fnx-login-options a {
    font-size: 0.85rem;
    color: #0B57D0;
    text-decoration: none;
    font-weight: 600;
}

.fnx-login-options a:hover {
    text-decoration: underline;
}

.fnx-btn-primary {
    width: 100%;
    padding: 1rem;
    background-color: #0B57D0;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s;
}

.fnx-btn-primary:hover {
    background-color: #084298;
}

.fnx-divider {
    display: flex;
    align-items: center;
    text-align: center;
    margin: 2rem 0;
}

.fnx-divider::before,
.fnx-divider::after {
    content: '';
    flex: 1;
    border-bottom: 1px solid #E2E8F0;
}

.fnx-divider span {
    padding: 0 1rem;
    color: #94A3B8;
    font-size: 0.8rem;
    font-weight: 600;
}

.fnx-btn-demo {
    width: 100%;
    padding: 1rem;
    background-color: #F8FAFC;
    border: 1px solid #93C5FD;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    cursor: pointer;
    transition: all 0.2s;
}

.fnx-btn-demo:hover {
    background-color: #EFF6FF;
    border-color: #60A5FA;
}

.rocket-icon {
    font-size: 1.5rem;
}

.demo-btn-text {
    text-align: left;
}

.demo-btn-text strong {
    display: block;
    color: #1E3A8A;
    font-size: 0.95rem;
    margin-bottom: 0.15rem;
}

.demo-btn-text span {
    display: block;
    color: #3B82F6;
    font-size: 0.75rem;
}
"""

# Append CSS (we don't worry about removing old because !important or later overrides will work)
css += "\n\n" + new_css

# Deploy
resp = requests.patch(
    f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
    auth=auth,
    headers={'Accept':'application/json', 'Content-Type':'application/json'},
    json={'template': tpl, 'css': css}
)
if resp.status_code == 200:
    print('Deployment successful!')
else:
    print('Failed:', resp.status_code, resp.text)
