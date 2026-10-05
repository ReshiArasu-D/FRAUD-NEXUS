import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']
idx = tpl.find("c.currentView === 'reportFraud'", 31000)
print("reportFraud starts at:", idx)
print(tpl[idx-100:idx+800])
