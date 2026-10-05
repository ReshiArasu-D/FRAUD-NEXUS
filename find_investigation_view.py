import re, sys

sys.stdout.reconfigure(encoding='utf-8')
with open('d:/KPMG/current_deployed_template.html', 'r', encoding='utf-8') as f:
    t = f.read()

# search all occurrences of c.adminModule === 'investigation'
matches = [m.start() for m in re.finditer(r"c\.adminModule\s*===\s*'investigation'", t)]
print("Occurrences of investigation:", matches)

for idx in matches:
    print("\n--- Match at index", idx, "---")
    print(t[max(0, idx-50):min(len(t), idx+400)])
