import requests, sys, re
sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
tpl = r.json()['result']['template']

print("--- AI BUTTON MATCHES ---")
for m in re.finditer(r'.{0,50}Ask FRAUDNEXUS AI.{0,50}', tpl):
    # Escape emojis or odd chars safely by using repr or just encode/decode
    text = m.group(0).encode('ascii', 'ignore').decode('ascii')
    print(text)

print("\n--- ADMIN VIEWS MATCHES ---")
for m in re.finditer(r'adminWorkspace', tpl):
    print("Found adminWorkspace!")

print("--- COMMAND CENTER ---")
idx = tpl.find('c.adminModule === \'commandCenter\'')
if idx != -1:
    print(tpl[max(0, idx-100):idx+300].encode('ascii', 'ignore').decode('ascii'))
