import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']
cs = d['client_script']

print("=== CHECKING TEMPLATE FOR CUSTOMER VIEWS ===")
for view in ['trackCases', 'evidenceVault', 'help', 'reportFraud', 'dashboard']:
    idx = tpl.find(f"currentView === '{view}'")
    print(f"Template has currentView === '{view}': {idx != -1} (at {idx})")
    if idx != -1:
        print(tpl[idx-50:idx+250])
        print("-" * 30)

print("\n=== CHECKING CLIENT SCRIPT FOR NAVIGATE ===")
idx_nav = cs.find("c.navigate =")
if idx_nav != -1:
    print(cs[idx_nav:idx_nav+500])

print("\n=== CHECKING AI ASSISTANT / CHAT ===")
for term in ['fnx-ai-trigger', 'showAI', 'aiMessages', 'Ask FRAUDNEXUS']:
    idx = tpl.find(term)
    print(f"Template has '{term}': {idx != -1} (at {idx})")
    if idx != -1:
        print(tpl[idx-50:idx+200])
        print("-" * 30)
