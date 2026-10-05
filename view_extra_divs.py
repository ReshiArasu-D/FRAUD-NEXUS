import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']
pos = 92957
print(tpl[pos-400:pos+300])
