import requests
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'

r = requests.get(f'{base}/api/now/table/sp_widget/2f258577c32b43d0e54832f1b401317f', auth=auth, headers={'Accept':'application/json'})
w = r.json()['result']
tpl = w.get('template', '')
cs = w.get('client_script', '')
css = w.get('css', '')

print('Template length:', len(tpl))
print('Client Script length:', len(cs))
print('CSS length:', len(css))

checks = [
    ('Has Partners sidebar button', "c.adminModule === 'partners'" in tpl),
    ('Has Partners workspace view (fnx-partners-page)', 'fnx-partners-page' in tpl),
    ('Has Partners KPI grid', 'fnx-partners-kpi-grid' in tpl),
    ('Has Partner directory table', 'fnx-partner-filter-bar' in tpl),
    ('Has Partner Requests sub-tab', "c.partnerTab === 'requests'" in tpl),
    ('Has Add Partner modal', 'showAddPartnerModal' in tpl),
    ('Has Create Request modal', 'showPartnerReqModal' in tpl),
    ('Has Deletion Blocked modal', 'showPartnerBlockedModal' in tpl),
    ('Has Partner Drawer', 'fnx-partner-drawer-overlay' in tpl),
    ('Has Inv Workspace Partner Req tab', "c.investigationTab === 'partnerRequests'" in tpl),
    ('Has Partner client methods', "c.partnerTab = 'directory'" in cs),
    ('Has loadPartners call in setAdminModule', "if (mod === 'partners') c.loadPartners();" in cs),
    ('Has EN translations for partners', "partnerDirectory: 'Partner Directory'" in cs),
    ('Has TA translations for partners', "partnerDirectory: '\u0b95\u0bc2\u0b9f\u0bcd\u0b9f\u0bbe\u0bb3\u0bb0\u0bcd \u0b85\u0b9f\u0bc8\u0bb5\u0bc1'" in cs),
    ('Has partner CSS classes', '.fnx-partners-kpi-grid' in css),
    ('Has partner drawer CSS', '.fnx-partner-drawer-overlay' in css),
]

for label, result in checks:
    print(f'  [{"OK" if result else "MISSING"}] {label}')
