import requests, sys, time, re

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
data = r.json()['result']
tpl = data['template']

tpl = re.sub(r'<!-- CACHE BUST: .*? -->\n*', '', tpl)
tpl = f'<!-- CACHE BUST: {int(time.time())} -->\n' + tpl

resp = requests.patch(
    f"{base}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    json={'template': tpl}
)

if resp.status_code == 200:
    print('Template cache busted successfully!')
else:
    print('Error:', resp.text[:200])
