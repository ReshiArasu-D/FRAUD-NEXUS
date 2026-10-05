import json

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']
idx = 122564
print(tpl[max(0, idx-1000):min(len(tpl), idx+1500)])
