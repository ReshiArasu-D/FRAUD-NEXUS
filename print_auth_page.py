import requests, re, sys
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://dev187180.service-now.com/api/now/table/sp_widget/2f258577c32b43d0e54832f1b401317f'
auth = ('admin', 'mn%XC1^ScdA4')
r = requests.get(url, auth=auth)
template = r.json()['result']['template']

idx_auth = template.find('fnx-auth-page')
idx_dash = template.find('4A. DASHBOARD')
print(template[idx_auth:idx_auth+4000])
