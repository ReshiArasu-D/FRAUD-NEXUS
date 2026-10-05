import requests, sys, re, time

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

print("=== DEPLOYING FRAUDNEXUS VERIFICATION WORKSPACE ===")

# 1. Fetch current live widget
print("1. Fetching live widget from ServiceNow...")
r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
if r.status_code != 200:
    print(f"Error fetching widget: {r.status_code} - {r.text[:200]}")
    sys.exit(1)

data = r.json()['result']
live_tpl = data['template']
live_css = data['css']
live_cs = data['client_script']

print(f"Current live template length: {len(live_tpl)}")
print(f"Current live CSS length: {len(live_css)}")
print(f"Current live client script length: {len(live_cs)}")

# Backup current live state locally
with open('d:/KPMG/pre_vw_backup_template.html', 'w', encoding='utf-8') as f:
    f.write(live_tpl)
with open('d:/KPMG/pre_vw_backup_css.css', 'w', encoding='utf-8') as f:
    f.write(live_css)
with open('d:/KPMG/pre_vw_backup_cs.js', 'w', encoding='utf-8') as f:
    f.write(live_cs)
print("Backup files created.")

# 2. Prepare Template Replacement
print("2. Integrating Verification Workspace HTML...")
vw_template = open('d:/KPMG/verification_workspace_template.html', 'r', encoding='utf-8').read()

# Locate investigation block in template
inv_start_marker = "c.adminModule === 'investigation'\" class=\"fnx-investigation-workspace\""
inv_pos = live_tpl.find(inv_start_marker)
if inv_pos == -1:
    print("ERROR: Investigation workspace start marker not found in live template!")
    sys.exit(1)

div_start = live_tpl.rfind("<div", 0, inv_pos)

# Find where partners module starts
part_marker = "c.adminModule === 'partners'"
part_pos = live_tpl.find(part_marker, inv_pos + 50)
if part_pos == -1:
    print("ERROR: Partners module marker not found after investigation block!")
    sys.exit(1)

# Find closing </div> before partners
div_end = live_tpl.rfind("</div>", 0, part_pos) + 6

print(f"Replacing investigation block from index {div_start} to {div_end} (length: {div_end - div_start})")
new_tpl = live_tpl[:div_start] + vw_template + live_tpl[div_end:]

# Cache bust marker
new_tpl = re.sub(r'<!-- CACHE BUST: .*? -->\n*', '', new_tpl)
new_tpl = f'<!-- CACHE BUST: {int(time.time())} -->\n' + new_tpl

# 3. Prepare CSS Replacement
print("3. Integrating Verification Workspace CSS...")
vw_css = open('d:/KPMG/verification_workspace_styles.css', 'r', encoding='utf-8').read()

css_marker = "/* === FRAUDNEXUS VERIFICATION WORKSPACE STYLES === */"
if css_marker in live_css:
    # replace existing
    c_start = live_css.find(css_marker)
    new_css = live_css[:c_start] + f"{css_marker}\n" + vw_css
else:
    new_css = live_css + f"\n\n{css_marker}\n" + vw_css

# 4. Prepare Client Script Integration
print("4. Integrating Verification Workspace Client Logic...")
vw_client = open('d:/KPMG/verification_workspace_client.js', 'r', encoding='utf-8').read()

cs_marker = "// === FRAUDNEXUS VERIFICATION WORKSPACE CONTROLLER EXTENSION ==="
if cs_marker in live_cs:
    cs_start = live_cs.find(cs_marker)
    base_cs = live_cs[:cs_start]
else:
    # Find last closing };
    last_brace = live_cs.rfind("};")
    if last_brace != -1:
        base_cs = live_cs[:last_brace]
    else:
        base_cs = live_cs

new_cs = base_cs + f"\n\n{cs_marker}\n" + vw_client + "\n};\n"

print(f"New template length: {len(new_tpl)}")
print(f"New CSS length: {len(new_css)}")
print(f"New client script length: {len(new_cs)}")

# 5. Deploy to ServiceNow
print("5. Deploying to ServiceNow REST API...")
patch_resp = requests.patch(
    f"{base}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    json={'template': new_tpl, 'css': new_css, 'client_script': new_cs}
)

if patch_resp.status_code == 200:
    print("SUCCESS: Verification Workspace successfully deployed to ServiceNow widget!")
    
    # 6. Flush cache
    print("6. Flushing ServiceNow server cache...")
    requests.get(f'{base}/cache.do', auth=auth)
    print("Server cache successfully flushed!")
else:
    print(f"ERROR deploying widget: {patch_resp.status_code} - {patch_resp.text[:400]}")
    sys.exit(1)

print("=== DEPLOYMENT COMPLETE ===")
