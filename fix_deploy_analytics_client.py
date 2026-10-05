import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

print("=== FIXING CLIENT SCRIPT INJECTION ===")

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
cur_cs = r.json()['result'].get('client_script', '')

with open('d:/KPMG/analytics_workspace_client.js', 'r', encoding='utf-8') as f:
    client_code = f.read()

# Remove old extension if accidentally inserted anywhere
sig = "/* ============================================================\n   FRAUDNEXUS — ENTERPRISE ANALYTICS WORKSPACE CLIENT EXTENSION"
if sig in cur_cs:
    print("Found existing extension block, cleaning it out first...")
    p1 = cur_cs.find(sig)
    # find where it ends or goes to last brace
    p2 = cur_cs.rfind("};")
    cur_cs = cur_cs[:p1] + "\n" + cur_cs[p2:]

# Now find the last };
last_brace = cur_cs.rfind("};")
if last_brace == -1:
    last_brace = cur_cs.rfind("}")

new_cs = cur_cs[:last_brace] + "\n\n" + client_code + "\n\n" + cur_cs[last_brace:]

print(f"Original CS length: {len(cur_cs)}")
print(f"New CS length: {len(new_cs)}")
print("Verification: contains 'c.processAnalyticsAggregation'?", "c.processAnalyticsAggregation" in new_cs)
print("Verification: contains 'c.fetchAnalyticsData'?", "c.fetchAnalyticsData" in new_cs)

patch_url = f'{base}/api/now/table/sp_widget/{WIDGET_ID}'
pr = requests.patch(patch_url, auth=auth, json={'client_script': new_cs}, headers={'Content-Type':'application/json','Accept':'application/json'})
print(f"Deploy status code: {pr.status_code}")

if pr.status_code in [200, 201]:
    print("Flushing cache (/cache.do)...")
    try:
        cr = requests.get(f'{base}/cache.do', auth=auth, timeout=10)
        print(f"Cache flush status: {cr.status_code}")
    except Exception as e:
        print(f"Cache flush note: {e}")
    print("=== CLIENT SCRIPT FIXED & DEPLOYED ===")
else:
    print("Error:", pr.text)
