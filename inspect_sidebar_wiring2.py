import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
template = r.json()['result']['template']

idx_nav = template.find('fnx-sidebar')
if idx_nav != -1:
    print("=== SIDEBAR NAV ===")
    print(template[idx_nav:idx_nav+1500])

idx_4f = template.find('4F. EVIDENCE')
idx_4g = template.find('4G. HELP')
idx_4h = template.find('4H.')
if idx_4h == -1:
    idx_4h = template.find('<!-- ============ 5.')
if idx_4h == -1:
    idx_4h = template.find('</main>')

print(f"Indices: 4F={idx_4f}, 4G={idx_4g}, 4H/end={idx_4h}")
if idx_4g != -1:
    print("=== 4G SECTION HEADER ===")
    print(template[idx_4g:idx_4g+500])

