import json

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']

for view in ['trackCases', 'evidenceVault', 'help']:
    term = f"c.currentView === '{view}'"
    idx = tpl.find(term)
    # search for subsequent occurrences (the container div)
    while idx != -1:
        print(f"[{idx}] {term}")
        print(tpl[max(0, idx-50):min(len(tpl), idx+300)])
        print("="*40)
        idx = tpl.find(term, idx+1)
