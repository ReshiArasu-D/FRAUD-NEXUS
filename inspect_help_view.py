import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
template = r.json()['result']['template']

idx_help = template.find("c.currentView === 'help'")
print(f"Index of c.currentView === 'help': {idx_help}")
if idx_help != -1:
    print(template[idx_help-100:idx_help+2500])

