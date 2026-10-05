import json

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']
idx = 11118
v_start = tpl.rfind("ng-if=\"c.currentView === 'auth'\"", 0, idx)

print(tpl[v_start:idx+300])
