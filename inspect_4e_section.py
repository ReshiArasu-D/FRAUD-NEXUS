import requests, json

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
template = r.json()['result']['template']

idx_start = template.find('4E. TRACK CASES')
idx_end = template.find('4F. EVIDENCE VAULT')

print(f"Track cases region: {idx_start} to {idx_end}")
print(template[idx_start-50:idx_start+800])

