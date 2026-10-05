import json, re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']
sub = tpl[41802:92980]

matches = list(re.finditer(r'<(/?[a-zA-Z0-9\-]+)[^>]*>', sub))
stack = []
for m in matches:
    t = m.group(1).lower()
    pos = 41802 + m.start()
    if t.startswith('/'):
        tag = t[1:]
        if stack and stack[-1][0] == tag:
            stack.pop()
        else:
            print(f"MISMATCH at {pos}: expected '{stack[-1][0] if stack else 'NONE'}', found '</{tag}>'")
            # print surrounding snippet
            print(tpl[max(0, pos-100):min(len(tpl), pos+100)])
            print("="*40)
    else:
        tag = t.split()[0]
        if tag not in ['img', 'input', 'br', 'hr', 'meta', 'link']:
            stack.append((tag, pos))

print("\nFinal stack at end of reportFraud:", [x[0] for x in stack])
