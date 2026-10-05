import re
with open('d:/KPMG/working_template.html', 'r', encoding='utf-8') as f:
    tpl = f.read()

matches = re.finditer(r'<section class="fnx-hero">', tpl)
for m in matches:
    idx = m.start()
    print("--- FOUND fnx-hero ---")
    print(tpl[max(0, idx-200):idx+50])
