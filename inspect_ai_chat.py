import json

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']
css = d['css']

print("=== SEARCHING FOR AI CHAT IN TEMPLATE ===")
idx = tpl.find("fnx-ai")
while idx != -1:
    print(f"[{idx}]", tpl[max(0, idx-50):min(len(tpl), idx+200)])
    print("-" * 30)
    idx = tpl.find("fnx-ai", idx+1)

print("\n=== SEARCHING FOR AI IN CSS ===")
idx_c = css.find("fnx-ai")
while idx_c != -1:
    print(f"[{idx_c}]", css[max(0, idx_c-50):min(len(css), idx_c+200)])
    print("-" * 30)
    idx_c = css.find("fnx-ai", idx_c+1)
