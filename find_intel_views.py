import requests, sys, os

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
tpl = r.json()['result']['template']

target = "adminModule === 'intelligence'"
indices = []
idx = 0
while True:
    pos = tpl.find(target, idx)
    if pos == -1:
        break
    indices.append(pos)
    idx = pos + len(target)

print("All occurrences of 'adminModule === intelligence':", indices)

for i, p in enumerate(indices):
    print(f"\n--- OCCURRENCE {i+1} (at {p}) ---")
    print(tpl[max(0, p-60):min(len(tpl), p+200)])
