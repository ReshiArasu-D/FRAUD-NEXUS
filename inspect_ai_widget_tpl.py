import json

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']
idx = tpl.find("fnx-ai-widget")
print("Found fnx-ai-widget at:", idx)
if idx != -1:
    print(tpl[max(0, idx-100):min(len(tpl), idx+800)])
