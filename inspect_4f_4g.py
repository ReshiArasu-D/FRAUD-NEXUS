import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
template = r.json()['result']['template']

idx_4f = template.find('4F. EVIDENCE VAULT')
idx_admin = template.find('adminWorkspace')
if idx_admin == -1:
    idx_admin = template.find('<!-- ============ 5.')

print(template[idx_4f:idx_4f+12000])

