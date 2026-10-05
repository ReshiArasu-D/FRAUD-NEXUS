import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

print("Preparing to inject Partners Module UI...")

# 1. READ LATEST TEMPLATE FROM SERVICENOW
r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
data = r.json()['result']
tpl = data['template']
css = data['css']
js = data['client_script']

# 2. READ LOCAL FILES
with open('d:/KPMG/partner_template.html', 'r', encoding='utf-8') as f:
    partner_template = f.read()

with open('d:/KPMG/partner_styles.css', 'r', encoding='utf-8') as f:
    partner_styles = f.read()

# 3. PATCH TEMPLATE (if missing)
if "fnx-partners-page" not in tpl:
    # Insert right before Intelligence Workspace
    intel_marker = "            <!-- ==========================================\n                 VIEW 5: INTELLIGENCE WORKSPACE"
    if intel_marker in tpl:
        tpl = tpl.replace(intel_marker, partner_template + "\n\n" + intel_marker)
        print("  [OK] Inserted partner_template.html into the main widget template.")
    else:
        # Fallback if marker changed
        idx = tpl.find('c.adminModule === \'intelligence\'')
        if idx != -1:
            div_start = tpl.rfind('<div', 0, idx)
            tpl = tpl[:div_start] + partner_template + "\n\n" + tpl[div_start:]
            print("  [OK] Inserted partner_template.html via fallback marker.")
        else:
            print("  [FAIL] Could not find where to insert partner template.")
            sys.exit(1)
else:
    print("  [SKIP] 'fnx-partners-page' already found in template.")

# 4. PATCH CSS (if missing)
if ".fnx-partners-page" not in css:
    css = css + "\n\n" + partner_styles
    print("  [OK] Appended partner styles to CSS.")
else:
    print("  [SKIP] Partner styles already found in CSS.")

# 5. DEPLOY TO SERVICENOW
resp = requests.patch(
    f"{base}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    json={'template': tpl, 'css': css, 'client_script': js}
)

if resp.status_code == 200:
    print("SUCCESS: Partners Module UI deployed successfully!")
else:
    print(f"ERROR: {resp.text[:400]}")
