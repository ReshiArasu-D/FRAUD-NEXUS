import requests, sys
sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
tpl = r.json()['result']['template']

idx = tpl.find('class="fnx-landing"')
print(tpl[max(0, idx-50):idx+50])

idx2 = tpl.find('fnx-ai-trigger')
print(tpl[max(0, idx2-50):idx2+100])
