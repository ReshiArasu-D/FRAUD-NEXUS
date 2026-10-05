import json

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

cs = d['client_script']
idx = cs.find("c.loadDemoSession = function")
print(cs[idx:idx+1500])
