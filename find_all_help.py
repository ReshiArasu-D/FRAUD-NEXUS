import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
template = r.json()['result']['template']

pos = 0
while True:
    pos = template.find('help', pos)
    if pos == -1:
        break
    snippet = template[max(0, pos-40):min(len(template), pos+60)].replace('\n', ' ')
    print(f"Pos {pos}: {snippet}")
    pos += 5

