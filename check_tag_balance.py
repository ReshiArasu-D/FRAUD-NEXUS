import json, re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']

sub = tpl[30644:94090]

# Let's count tags
tags = re.findall(r'<(/?[a-zA-Z0-9\-]+)[^>]*>', sub)

stack = []
extra_closes = []

for i, t in enumerate(tags):
    if t.startswith('/'):
        tag_name = t[1:].lower()
        if stack and stack[-1] == tag_name:
            stack.pop()
        else:
            extra_closes.append((i, tag_name, stack[-5:] if stack else []))
    else:
        tag_name = t.split()[0].lower()
        # ignore self-closing
        if tag_name not in ['img', 'input', 'br', 'hr', 'meta', 'link']:
            stack.append(tag_name)

print("Remaining open tags in stack at trackCases:", stack)
print("Extra closes found:", len(extra_closes))
for ec in extra_closes[:20]:
    print(ec)
