import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
r = requests.get(f'{base}/api/now/table/sp_widget/2f258577c32b43d0e54832f1b401317f', auth=auth, headers={'Accept':'application/json'})
cs = r.json()['result']['client_script']

# Find Tamil addTask to know where to insert
idx_ta_addt = cs.find("addTask: 'பணி சேர்க்க'")
print('TA addTask at:', idx_ta_addt)
if idx_ta_addt > 0:
    snippet = cs[idx_ta_addt:idx_ta_addt+200]
    print(snippet)
