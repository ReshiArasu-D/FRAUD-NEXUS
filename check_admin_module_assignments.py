import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
cs = r.json()['result'].get('client_script', '')

idx = cs.find("c.adminModule =")
while idx != -1:
    print("Found c.adminModule = around:", idx)
    print(cs[idx-30:idx+80])
    idx = cs.find("c.adminModule =", idx+1)
