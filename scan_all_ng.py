import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('d:/KPMG/widget_template.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Look for ng- attributes containing {{ or }}
ng_attrs = re.findall(r'(ng-[a-z]+="[^"]*\{\{[^"]*"[^>]*)', text)
print(f"Found {len(ng_attrs)} ng- attributes with {{{{ :")
for a in ng_attrs:
    # safe print
    print(" ", repr(a[:140]))

print("\n--- Check ng-repeat with objects ---")
repeats = re.findall(r'ng-repeat="[^"]*"', text)
for r in repeats:
    if '{' in r or '[' in r:
        print(" ", repr(r))
