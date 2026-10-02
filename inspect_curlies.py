with open('d:/KPMG/widget_template.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'ng-class="\{\{\{.*?\}\}\}"', text)
print(f"Total ng-class with triple curlies: {len(matches)}")
for m in matches:
    print(" ", m)

matches2 = re.findall(r'\{\{\{.*?\}\}\}', text)
print(f"Total triple curlies: {len(matches2)}")
for m in matches2:
    print(" ", m)
