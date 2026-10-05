import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
template = r.json()['result']['template']

idx_nav = template.find('<nav class="fnx-nav">')
idx_nav_end = template.find('</nav>', idx_nav)
print("=== NAV EXACT HTML ===")
print(template[idx_nav:idx_nav_end+6])

idx_ev = template.find('fnx-evidence-vault')
print("\n=== EV VIEW CONTAINER TAG ===")
print(template[idx_ev-100:idx_ev+200])

idx_hp = template.find('fnx-help-view')
print("\n=== HELP VIEW CONTAINER TAG ===")
print(template[idx_hp-100:idx_hp+400])

