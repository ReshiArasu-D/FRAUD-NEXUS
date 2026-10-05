import requests, sys, json

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

print("=== DEPLOYING FRAUDNEXUS ANALYTICS WORKSPACE ===")

# 1. Fetch current widget
print("Fetching current widget record...")
r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
res = r.json()['result']

cur_template = res.get('template', '')
cur_css = res.get('css', '')
cur_cs = res.get('client_script', '')

# Backup current state
with open('d:/KPMG/widget_backup_before_analytics.json', 'w', encoding='utf-8') as f:
    json.dump({
        'template': cur_template,
        'css': cur_css,
        'client_script': cur_cs
    }, f, indent=2)
print("Backup saved to d:/KPMG/widget_backup_before_analytics.json")

# 2. Prepare Template Replacement
p_analytics = cur_template.find("<div ng-if=\"c.adminModule === 'analytics'\"")
p_settings = cur_template.find("<div ng-if=\"c.adminModule === 'settings'\"", p_analytics)

cb = cur_template.rfind("<!--", 0, p_analytics)
if cb != -1 and "VIEW 6" in cur_template[cb:p_analytics]:
    start = cb
else:
    start = p_analytics

cb_set = cur_template.rfind("<!--", p_analytics, p_settings)
if cb_set != -1 and "VIEW 7" in cur_template[cb_set:p_settings]:
    end = cb_set
else:
    end = p_settings

print(f"Target template span: {start} to {end} (len {end - start})")

with open('d:/KPMG/analytics_workspace_template.html', 'r', encoding='utf-8') as f:
    new_template_block = f.read()

new_template = cur_template[:start] + new_template_block + "\n\n            " + cur_template[end:]
print(f"New template total length: {len(new_template)} (was {len(cur_template)})")

# 3. Prepare CSS Update
with open('d:/KPMG/analytics_workspace_styles.css', 'r', encoding='utf-8') as f:
    new_css_block = f.read()

if "fnx-analytics-workspace" not in cur_css:
    new_css = cur_css + "\n\n" + new_css_block
    print(f"Appended Analytics CSS. New CSS length: {len(new_css)}")
else:
    print("Analytics CSS already present in widget CSS. Skipping append.")
    new_css = cur_css

# 4. Prepare Client Script Update
with open('d:/KPMG/analytics_workspace_client.js', 'r', encoding='utf-8') as f:
    new_cs_block = f.read()

# Add hook to c.setAdminModule if not already there
hook_code = """
        if (mod === 'analytics') {
            if (c.initAnalyticsWorkspace) {
                c.initAnalyticsWorkspace();
            }
        }
"""

if "if (mod === 'analytics')" not in cur_cs:
    target_pos = cur_cs.find("if (mod === 'commandCenter')")
    if target_pos != -1:
        cur_cs = cur_cs[:target_pos] + hook_code.strip() + "\n        " + cur_cs[target_pos:]
        print("Inserted analytics hook into c.setAdminModule")

# Find last closing brace of api.controller
last_brace = cur_cs.rfind("};")
if last_brace == -1:
    last_brace = cur_cs.rfind("}")

if "c.initAnalyticsWorkspace" not in cur_cs:
    new_cs = cur_cs[:last_brace] + "\n\n" + new_cs_block + "\n\n" + cur_cs[last_brace:]
    print(f"Inserted Analytics client logic. New Client Script length: {len(new_cs)}")
else:
    print("Analytics client logic already present. Replacing previous injection...")
    idx_start = cur_cs.find("FRAUDNEXUS — ENTERPRISE ANALYTICS WORKSPACE CLIENT EXTENSION")
    if idx_start != -1:
        comment_start = cur_cs.rfind("/*", 0, idx_start)
        new_cs = cur_cs[:comment_start] + new_cs_block + "\n\n" + cur_cs[last_brace:]
    else:
        new_cs = cur_cs

# 5. Send PATCH to ServiceNow
print("Deploying updated widget to ServiceNow...")
patch_url = f'{base}/api/now/table/sp_widget/{WIDGET_ID}'
payload = {
    'template': new_template,
    'css': new_css,
    'client_script': new_cs
}

pr = requests.patch(patch_url, auth=auth, json=payload, headers={'Content-Type':'application/json','Accept':'application/json'})
print(f"Deploy status code: {pr.status_code}")

if pr.status_code in [200, 201]:
    print("Successfully deployed Analytics Workspace widget!")
    
    # 6. Flush cache
    print("Flushing cache (/cache.do)...")
    try:
        cr = requests.get(f'{base}/cache.do', auth=auth, timeout=10)
        print(f"Cache flush status: {cr.status_code}")
    except Exception as e:
        print(f"Cache flush note: {e}")
        
    print("=== DEPLOYMENT COMPLETE ===")
else:
    print(f"Deploy error: {pr.text}")
