import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://dev187180.service-now.com/api/now/table/sp_widget/2f258577c32b43d0e54832f1b401317f'
auth = ('admin', 'mn%XC1^ScdA4')
r = requests.get(url, auth=auth)
css = r.json()['result']['css']

lines = css.splitlines()
for i in range(1495, 1545):
    print(f'{i}: {lines[i]}')
