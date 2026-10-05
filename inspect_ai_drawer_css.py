import json

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

css = d['css']
idx = 107536
print(css[idx-300:idx+300])
