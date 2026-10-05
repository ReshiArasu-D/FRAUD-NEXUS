import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']
idx = 89653
p = tpl.rfind("fnx-report-", 41802, idx)
while p != -1:
    print(f"[{p}]", tpl[p-30:p+100])
    p = tpl.rfind("fnx-report-", 41802, p-1)
