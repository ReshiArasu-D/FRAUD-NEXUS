import requests, json

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
css = r.json()['result']['css']

lines = css.split('\n')
for i, line in enumerate(lines):
    if 'fnx-nav-item' in line:
        start = max(0, i - 1)
        end = min(len(lines), i + 10)
        print(f"--- Around line {i+1} ---")
        print('\n'.join(lines[start:end]))

