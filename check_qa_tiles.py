import requests, json, re

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
w = r.json()['result']
template = w['template']
client = w['client_script']

print("=== QUICK ACTIONS IN TEMPLATE ===")
for m in re.finditer(r'fnx-qa-tile[^"]*', template):
    start = max(0, m.start() - 50)
    end = min(len(template), m.end() + 250)
    print(template[start:end])
    print("-" * 50)

