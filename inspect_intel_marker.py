import requests, sys, os

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
tpl = r.json()['result']['template']

pos_intel = tpl.find("c.adminModule === 'intelligence'")
print("--- AROUND INTEL MARKER ---")
start = max(0, pos_intel - 100)
end = min(len(tpl), pos_intel + 600)
print(tpl[start:end])
