import json

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']
idx = tpl.find("c.adminModule")
while idx != -1:
    print("Found in template around:", idx)
    print(tpl[max(0, idx-100):min(len(tpl), idx+100)])
    print("="*40)
    idx = tpl.find("c.adminModule", idx+1)
    if idx > 50000:
        break
