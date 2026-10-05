import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
client_script = r.json()['result']['client_script']

idx_nav = client_script.find('c.navigate =')
if idx_nav == -1:
    idx_nav = client_script.find('navigate')

print("=== CLIENT SCRIPT c.navigate ===")
print(client_script[idx_nav:idx_nav+1000])

