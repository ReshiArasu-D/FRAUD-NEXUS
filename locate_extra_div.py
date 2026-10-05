import json, re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']
sub = tpl[30644:94090]

# Find matches with positions
matches = list(re.finditer(r'<(/?[a-zA-Z0-9\-]+)[^>]*>', sub))
ec = matches[1217]
pos = 30644 + ec.start()
print("Position of extra close in template:", pos)
print("Snippet around extra close:")
print(tpl[max(0, pos-250):min(len(tpl), pos+250)])
