with open('d:/KPMG/widget_template.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'ng-class="{{' in line:
        print(f'Line {i+1}: {line.strip()[:140]}')
