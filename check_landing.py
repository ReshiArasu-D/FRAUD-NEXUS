import json
with open('d:/KPMG/widget_dump.json', 'r', encoding='utf-8') as f:
    tpl = json.load(f)['template']

idx = tpl.find('fnx-landing')
print("--- fnx-landing ---")
print(tpl[max(0, idx-50):idx+50])

idx2 = tpl.find('fnx-app')
print("\n--- fnx-app ---")
print(tpl[max(0, idx2-50):idx2+50])
