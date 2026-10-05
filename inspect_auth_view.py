import json

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']
idx = 11118

# Find where this view starts
v_start = tpl.rfind("ng-if=\"c.currentView", 0, idx)
print("View starts at:", v_start)
print(tpl[v_start:idx])

# Find where this view ends
v_next = tpl.find("ng-if=\"c.currentView", idx)
print("Next view starts at:", v_next)
print(tpl[idx:v_next])
