import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

print("Forcing injection of Partners Module UI...")

# 1. READ LATEST TEMPLATE FROM SERVICENOW
r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
data = r.json()['result']
tpl = data['template']
css = data['css']
js = data['client_script']

# 2. READ LOCAL FILES
with open('d:/KPMG/partner_template.html', 'r', encoding='utf-8') as f:
    partner_template = f.read()

# 3. REPLACE ENTIRE fnx-partners-page BLOCK
idx_start = tpl.find('<div ng-if="c.adminModule === \'partners\'" class="fnx-admin-page-view fnx-partners-page">')
if idx_start == -1:
    print("Could not find start of fnx-partners-page block")
    sys.exit(1)

# Find the end of the block (the view marker for intelligence workspace)
idx_end = tpl.find('<!-- ==========================================\n                 VIEW 5: INTELLIGENCE WORKSPACE', idx_start)
if idx_end == -1:
    print("Could not find end of fnx-partners-page block")
    sys.exit(1)

tpl = tpl[:idx_start] + partner_template + "\n\n" + tpl[idx_end:]
print("  [OK] Successfully replaced fnx-partners-page block with full partner_template.html content.")

# 4. DEPLOY TO SERVICENOW
resp = requests.patch(
    f"{base}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    json={'template': tpl}
)

if resp.status_code == 200:
    print("SUCCESS: Partners Module UI deployed successfully!")
else:
    print(f"ERROR: {resp.text[:400]}")
