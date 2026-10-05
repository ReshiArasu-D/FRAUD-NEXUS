import requests, re, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
data = r.json()['result']
tpl = data['template']
css = data['css']

# Find the adminLogin block
idx = tpl.find('<div ng-if="c.currentView === \'adminLogin\'"')
end_idx = tpl.find('<!-- 2. ADMIN SHELL -->')

if idx != -1 and end_idx != -1:
    admin_block = tpl[idx:end_idx]
    
    # We injected the admin login page, let's fix the extra closing div issue.
    # Count open and close divs in this block
    open_d = admin_block.count('<div')
    close_d = admin_block.count('</div')
    
    print(f"Admin block divs before: {open_d} open, {close_d} close")
    
    if close_d > open_d:
        # We have an extra closing div. Let's remove the last one before end_idx
        last_div = admin_block.rfind('</div>')
        if last_div != -1:
            admin_block = admin_block[:last_div] + admin_block[last_div+6:]
            tpl = tpl[:idx] + admin_block + tpl[end_idx:]
            print("Successfully removed the extra closing div.")
    
# Force the layout to stick to the top and fill the screen
css_fixes = """
/* ============================================================
   ADMIN LOGIN STRUCTURAL FIXES
   ============================================================ */
.fnx-admin-login-page {
    display: flex !important;
    align-items: stretch !important;
    min-height: 100vh !important;
    height: 100vh !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    z-index: 9999 !important;
    background-color: #F8FAFC !important;
}

/* Ensure the ServiceNow wrapper doesn't push it down */
.sp-page-root {
    position: static !important;
}
"""

css += '\n\n' + css_fixes

resp = requests.patch(
    f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
    auth=auth,
    headers={'Accept':'application/json', 'Content-Type':'application/json'},
    json={'template': tpl, 'css': css}
)

if resp.status_code == 200:
    print('Deployment successful! Admin layout fixed.')
else:
    print('Failed:', resp.status_code)
