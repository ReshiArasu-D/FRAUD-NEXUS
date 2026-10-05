import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('d:/KPMG/build_vw_template.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(508, 615):
    print(f'{i+1}: {lines[i]}', end='')
