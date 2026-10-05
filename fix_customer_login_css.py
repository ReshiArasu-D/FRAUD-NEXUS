import requests, sys, json

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

print("=== FIXING CUSTOMER LOGIN PAGE CSS ===")

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
res = r.json()['result']
css = res.get('css', '')

# 1. Replace the problematic wildcard selector div[ng-if*="auth"]
old_block = """/* Auth views (login, register etc): self-contained */
.fnx-auth-view,
div[ng-if="c.currentView === 'auth'"],
div[ng-if*="auth"] {
    height: 100vh !important;
    overflow-y: auto !important;
}"""

new_block = """/* Auth views (login, register etc): self-contained - FIXED (removed wildcard div[ng-if*="auth"]) */
.fnx-auth-view,
.fnx-auth-page,
div[ng-if="c.currentView === 'auth'"] {
    height: 100vh !important;
    min-height: 100vh !important;
    overflow: hidden !important;
}"""

if old_block in css:
    css = css.replace(old_block, new_block)
    print("Replaced old_block with new_block successfully.")
else:
    # Try more flexible replacement
    target = 'div[ng-if*="auth"]'
    if target in css:
        idx = css.find(target)
        p_start = css.rfind('.fnx-auth-view', 0, idx)
        p_end = css.find('}', idx)
        if p_start != -1 and p_end != -1:
            css = css[:p_start] + new_block + css[p_end+1:]
            print("Replaced wildcard via slice.")

# 2. Fix double dot typo ..fnx-admin-login-page
if "..fnx-admin-login-page" in css:
    css = css.replace("..fnx-admin-login-page", ".fnx-admin-login-page")
    print("Fixed ..fnx-admin-login-page typo.")

# 3. Append explicit Customer Auth Page layout rules
auth_override_css = """
/* ============================================================
   CUSTOMER AUTHENTICATION PAGE — BULLETPROOF ENTERPRISE LAYOUT
   ============================================================ */
.fnx-auth-page {
    display: flex !important;
    flex-direction: row !important;
    height: 100vh !important;
    min-height: 100vh !important;
    max-height: 100vh !important;
    width: 100vw !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
    background-color: #0B1F3A !important;
}

.fnx-auth-left {
    flex: 0 0 45% !important;
    max-width: 45% !important;
    background-color: #0B1F3A !important;
    color: #FFFFFF !important;
    padding: 4rem 3.5rem !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    height: 100vh !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
}

.fnx-auth-right {
    flex: 1 1 55% !important;
    background-color: #F8FAFC !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    padding: 2.5rem !important;
    height: 100vh !important;
    overflow-y: auto !important;
    box-sizing: border-box !important;
}

.fnx-auth-box {
    width: 100% !important;
    max-width: 480px !important;
    height: auto !important;
    min-height: auto !important;
    max-height: none !important;
    background-color: #FFFFFF !important;
    padding: 2.5rem !important;
    border-radius: 16px !important;
    border: 1.5px solid #E2E8F0 !important;
    box-shadow: 0 10px 30px rgba(11, 31, 58, 0.08) !important;
    box-sizing: border-box !important;
    margin: auto 0 !important;
}

.fnx-auth-tabs {
    display: flex !important;
    flex-direction: row !important;
    height: auto !important;
    min-height: auto !important;
    max-height: none !important;
    overflow: visible !important;
    overflow-y: visible !important;
    margin-bottom: 1.75rem !important;
    border-bottom: 2px solid #E2E8F0 !important;
    padding: 0 !important;
}

.fnx-auth-tabs button {
    flex: 1 !important;
    height: auto !important;
    padding: 0.75rem 1rem !important;
    border: none !important;
    background: transparent !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: #64748B !important;
    cursor: pointer !important;
    border-bottom: 3px solid transparent !important;
    margin-bottom: -2px !important;
    transition: all 0.2s ease !important;
}

.fnx-auth-tabs button.active {
    color: #0B1F3A !important;
    border-bottom-color: #00B8D9 !important;
}

.fnx-auth-form {
    display: flex !important;
    flex-direction: column !important;
    height: auto !important;
    min-height: auto !important;
    max-height: none !important;
    overflow: visible !important;
    overflow-y: visible !important;
    gap: 1.25rem !important;
    margin: 0 !important;
    padding: 0 !important;
}

.fnx-back-to-portal {
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
    background: none !important;
    border: none !important;
    color: #64748B !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    padding: 0 0 1rem 0 !important;
    margin: 0 !important;
    transition: color 0.15s ease !important;
}

.fnx-back-to-portal:hover {
    color: #0284C7 !important;
}
"""

if "CUSTOMER AUTHENTICATION PAGE — BULLETPROOF ENTERPRISE LAYOUT" not in css:
    css = css + "\n\n" + auth_override_css
    print("Appended bulletproof customer auth CSS rules.")
else:
    # replace existing
    idx = css.find("CUSTOMER AUTHENTICATION PAGE — BULLETPROOF ENTERPRISE LAYOUT")
    c_start = css.rfind("/*", 0, idx)
    css = css[:c_start] + auth_override_css
    print("Replaced existing customer auth CSS rules.")

# Deploy to ServiceNow
patch_url = f'{base}/api/now/table/sp_widget/{WIDGET_ID}'
pr = requests.patch(patch_url, auth=auth, json={'css': css}, headers={'Content-Type':'application/json','Accept':'application/json'})
print(f"Deploy status code: {pr.status_code}")

if pr.status_code in [200, 201]:
    # Flush cache
    cr = requests.get(f'{base}/cache.do', auth=auth, timeout=10)
    print(f"Cache flush status: {cr.status_code}")
    print("=== CUSTOMER LOGIN CSS FIX DEPLOYED SUCCESSFULLY ===")
else:
    print("Error:", pr.text)
