import requests, sys, json
sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

print("Restoring widget to the state before the UX fixes...")
with open('d:/KPMG/widget_dump.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# The dump contains 'template', 'css', 'client_script'
resp = requests.patch(
    f"{base}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    json={
        'template': data['template'],
        'css': data['css'],
        'client_script': data['client_script']
    }
)

if resp.status_code == 200:
    print("RESTORED SUCCESSFULLY!")
else:
    print(f"ERROR RESTORING: {resp.text[:400]}")
