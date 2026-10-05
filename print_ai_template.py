import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://dev187180.service-now.com/api/now/table/sp_widget/2f258577c32b43d0e54832f1b401317f'
auth = ('admin', 'mn%XC1^ScdA4')
r = requests.get(url, auth=auth)
template = r.json()['result']['template']

idx_ai = template.find('5. FLOATING NOW ASSIST AI')
idx_ai_end = template.find('6. MODALS')
if idx_ai_end == -1:
    idx_ai_end = idx_ai + 4000

print(template[idx_ai:idx_ai_end])
