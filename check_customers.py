import json
with open('d:/KPMG/widget_dump.json', 'r', encoding='utf-8') as f:
    tpl = json.load(f)['template']

idx2 = tpl.find('Customer ID')
print(tpl[idx2:idx2+1500])
