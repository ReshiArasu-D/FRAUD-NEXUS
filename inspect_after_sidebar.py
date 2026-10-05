import json

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']
idx = tpl.find("</aside>")
print(tpl[idx:idx+800])
