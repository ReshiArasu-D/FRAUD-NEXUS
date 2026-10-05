import requests, sys, os

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
data = r.json()['result']
tpl = data['template']

# Check markers
inv_marker = "<!-- ============================================================\n     FRAUDNEXUS — FINAL ENTERPRISE VERIFICATION WORKSPACE"
intel_marker = "c.adminModule === 'intelligence'"

print("inv_marker in live tpl:", inv_marker in tpl)
print("intel_marker in live tpl:", intel_marker in tpl)

# Find positions
pos_inv = tpl.find(inv_marker)
pos_intel = tpl.find(intel_marker)
print("pos_inv:", pos_inv)
print("pos_intel:", pos_intel)
