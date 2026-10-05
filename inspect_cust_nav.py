import requests, re, sys
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://dev187180.service-now.com/api/now/table/sp_widget/2f258577c32b43d0e54832f1b401317f'
auth = ('admin', 'mn%XC1^ScdA4')
r = requests.get(url, auth=auth)
template = r.json()['result']['template']

idx = template.find('nav class="fnx-sidebar-nav"')
if idx == -1:
    idx = template.find('fnx-sidebar-nav')
print(template[idx-100:idx+1200])
