import requests, json

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
template = r.json()['result']['template']

idx_main = template.find('<main')
print("idx_main:", idx_main)

for view in ['trackCases', 'evidenceVault', 'help', 'editProfile']:
    pos = idx_main
    while True:
        pos = template.find(f"c.currentView === '{view}'", pos)
        if pos == -1:
            break
        print(f"View '{view}' at pos {pos}:")
        print(template[pos-50:pos+150])
        pos += len(view) + 10

