import json

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']

print("=== ALL OCCURRENCES OF trackCases ===")
idx = tpl.find("trackCases")
while idx != -1:
    print(f"[{idx}]", tpl[max(0, idx-50):min(len(tpl), idx+150)])
    print("-" * 30)
    idx = tpl.find("trackCases", idx+1)

print("\n=== ALL OCCURRENCES OF evidenceVault ===")
idx = tpl.find("evidenceVault")
while idx != -1:
    print(f"[{idx}]", tpl[max(0, idx-50):min(len(tpl), idx+150)])
    print("-" * 30)
    idx = tpl.find("evidenceVault", idx+1)

print("\n=== ALL OCCURRENCES OF 'help' ===")
idx = tpl.find("'help'")
while idx != -1:
    print(f"[{idx}]", tpl[max(0, idx-50):min(len(tpl), idx+150)])
    print("-" * 30)
    idx = tpl.find("'help'", idx+1)
