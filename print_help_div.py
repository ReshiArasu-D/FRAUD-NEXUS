import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
template = r.json()['result']['template']

idx_help_div = template.find('<div ng-if="c.currentView === \'help\'"')
print("idx_help_div:", idx_help_div)
idx_main_end = template.find('</main>', idx_help_div)
print("idx_main_end:", idx_main_end)

print(template[idx_help_div:idx_main_end+7])

