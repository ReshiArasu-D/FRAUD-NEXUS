import requests, json

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
client = r.json()['result']['client_script']

idx_trans = client.find('c.translations =')
if idx_trans != -1:
    print(client[idx_trans:idx_trans+1200])

