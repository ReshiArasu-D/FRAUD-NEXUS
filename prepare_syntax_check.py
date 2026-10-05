import requests

auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
cs = r.json()['result']['client_script']

with open('d:/KPMG/test_cs.js', 'w', encoding='utf-8') as f:
    f.write('function test(c, scope, http, win, timeout, loc) {\n' + cs + '\n}')
