import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

with open('d:/KPMG/working_template.html', 'r', encoding='utf-8') as f:
    tpl = f.read()

# Fetch current css to append to
r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
css = r.json()['result']['css']

# New global logo CSS
logo_css = """
/* ================================================
   GLOBAL FRAUDNEXUS LOGO / WORDMARK STYLES
   ================================================ */
.fnx-brand-wordmark {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    line-height: 1.2 !important;
}

.fnx-brand-name {
    font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif !important;
    font-size: 1.3rem !important;
    font-weight: 800 !important;
    color: #0B57D0 !important;
    letter-spacing: 0.5px !important;
    display: block !important;
}

.fnx-brand-tagline {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.7rem !important;
    font-weight: 500 !important;
    color: #64748B !important;
    letter-spacing: 0.2px !important;
    display: block !important;
    margin-top: 1px !important;
}

/* Landing Nav Brand */
.fnx-landing-brand {
    display: flex !important;
    align-items: center !important;
    gap: 0.75rem !important;
    cursor: pointer !important;
}

/* Auth / Customer Login Brand */
.fnx-auth-brand {
    display: flex !important;
    align-items: center !important;
    gap: 0.75rem !important;
    cursor: pointer !important;
    margin-bottom: 2rem !important;
}

.fnx-auth-brand .fnx-brand-name {
    color: #FFFFFF !important;
}

.fnx-auth-brand .fnx-brand-tagline {
    color: rgba(255,255,255,0.65) !important;
}

/* Admin Login Left Panel Brand */
.fnx-login-brand {
    display: flex !important;
    align-items: center !important;
    gap: 0.85rem !important;
    margin-bottom: 2.5rem !important;
}

.fnx-login-brand .fnx-brand-name {
    font-size: 1.6rem !important;
}

.fnx-login-brand .fnx-brand-tagline {
    font-size: 0.78rem !important;
}

/* Admin Topbar Brand */
.fnx-admin-topbar-brand {
    display: flex !important;
    align-items: center !important;
    gap: 0.6rem !important;
}

.fnx-topbar-wordmark .fnx-brand-name {
    font-size: 1rem !important;
    color: #FFFFFF !important;
}

.fnx-topbar-wordmark .fnx-brand-tagline {
    font-size: 0.6rem !important;
    color: rgba(255,255,255,0.6) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}
"""

css += '\n\n' + logo_css

# Deploy template + css
resp = requests.patch(
    f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
    auth=auth,
    headers={'Accept':'application/json', 'Content-Type':'application/json'},
    json={'template': tpl, 'css': css}
)

if resp.status_code == 200:
    print('Global logo deployed successfully across all pages!')
else:
    print('Deploy failed:', resp.status_code, resp.text[:200])
