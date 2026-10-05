import requests, json

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
w = r.json()['result']
css = w['css']

print("CSS length:", len(css))
lines = css.split('\n')
for i, line in enumerate(lines):
    if any(k in line.lower() for k in ['animate', 'transition', 'active', 'fnx-nav-item', 'evidence-vault', 'help-view']):
        print(f"Line {i+1}: {line}")

