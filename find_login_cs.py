import json

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

cs = d['client_script']

for term in ['doDemoLogin', 'doLogin', 'loadCases', 'loadCustomerDashboard']:
    idx = cs.find(term)
    print(f"=== Searching for '{term}' ===")
    while idx != -1:
        print(f"[{idx}]", cs[idx:idx+400])
        print("-" * 20)
        idx = cs.find(term, idx+1)
