import json

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

css = d['css']

for term in [".fnx-auth-right", ".fnx-auth-box", ".fnx-auth-tabs", ".fnx-auth-form", ".fnx-auth-page"]:
    print("=== SEARCH FOR:", term)
    idx = css.find(term)
    while idx != -1:
        print(f"[{idx}]", css[idx:idx+300])
        print("-" * 20)
        idx = css.find(term, idx+1)
