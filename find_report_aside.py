import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']
idx = tpl.find("<aside", 41802)
print("Found <aside at:", idx)
print(tpl[max(0, idx-500):idx+500])
