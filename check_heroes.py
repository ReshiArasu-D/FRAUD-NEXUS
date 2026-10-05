import re
with open('d:/KPMG/working_template.html', 'r', encoding='utf-8') as f:
    tpl = f.read()

count = tpl.count('<section class="fnx-hero">')
print('Hero section count:', count)

matches = list(re.finditer(r'<section class="fnx-hero">', tpl))
for m in matches:
    idx = m.start()
    print("--------------------------------------------------")
    print(tpl[max(0, idx-500):idx+100])
