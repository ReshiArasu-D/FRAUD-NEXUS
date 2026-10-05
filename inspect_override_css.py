import json

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

css = d['css']
idx = 165608
print(css[max(0, idx-500):min(len(css), idx+500)])
