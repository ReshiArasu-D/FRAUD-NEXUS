import requests, json

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
template = r.json()['result']['template']

idx_nav = template.find('fnx-sidebar')
if idx_nav != -1:
    print("=== SIDEBAR NAV ===")
    print(template[idx_nav:idx_nav+1800])
else:
    print('fnx-sidebar not found')

# Also check 4F and 4G view conditions
for marker in ['4E. TRACK', '4F. EVIDENCE', '4G. HELP', 'support', 'evidenceVault', 'evidence']:
    pos = 0
    while True:
        pos = template.find(marker, pos)
        if pos == -1:
            break
        print(f"Marker '{marker}' at {pos}:")
        snippet_start = max(0, pos - 50)
        snippet_end = min(len(template), pos + 120)
        print(repr(template[snippet_start:snippet_end]))
        pos += len(marker) + 1
