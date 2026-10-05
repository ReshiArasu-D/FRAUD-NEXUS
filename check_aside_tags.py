import json, re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']

aside_start = tpl.find("<aside class=\"fnx-report-side\">")
aside_end = tpl.find("</aside>", aside_start)

sub = tpl[aside_start:aside_end+8]
print(sub)

# Check tag balance of this sub
matches = list(re.finditer(r'<(/?[a-zA-Z0-9\-]+)[^>]*>', sub))
stack = []
for m in matches:
    t = m.group(1).lower()
    if t.startswith('/'):
        tag = t[1:]
        if stack and stack[-1] == tag:
            stack.pop()
        else:
            print(f"Mismatch in aside: stack={stack}, found </{tag}>")
    else:
        tag = t.split()[0]
        if tag not in ['img', 'input', 'br', 'hr', 'meta', 'link']:
            stack.append(tag)

print("Stack after aside:", stack)
