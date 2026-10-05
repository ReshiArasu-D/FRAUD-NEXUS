import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
template = r.json()['result']['template']

idx_ev = template.find('<div ng-if="c.currentView === \'evidenceVault\'"')
idx_help_div = template.find('<div ng-if="c.currentView === \'help\'"')

print(template[idx_ev+9000:idx_help_div])

