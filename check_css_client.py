import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
res = r.json()['result']

css = res.get('css', '')
client_script = res.get('client_script', '')

print(f"CSS length: {len(css)}")
print(f"Client script length: {len(client_script)}")

# Check if analytics css or js is already present
print("Analytics in CSS?", 'fnx-analytics' in css)
print("Analytics in Client Script?", 'initAnalyticsWorkspace' in client_script)

# Check end of client script
print("Client script ends with:")
print(client_script[-200:])
