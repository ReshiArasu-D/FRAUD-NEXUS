with open('d:/KPMG/widget_template.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
directives = ['ng-if', 'ng-show', 'ng-hide', 'ng-click', 'ng-model', 'ng-repeat', 'ng-class']
for d in directives:
    matches = re.findall(rf'{d}="\{{.*?\}}"', text)
    if matches:
        print(f"Found {len(matches)} with {d}=\"{{...}}\":")
        for m in matches[:5]:
            print("  ", m)
