import json

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

css = d['css']

idx = css.find(".fnx-auth-page")
while idx != -1:
    print("Found .fnx-auth-page around:", idx)
    print(css[idx:idx+800])
    print("="*40)
    idx = css.find(".fnx-auth-page", idx+1)
