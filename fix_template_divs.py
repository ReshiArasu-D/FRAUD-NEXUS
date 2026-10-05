import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
data = r.json()['result']
tpl = data['template']

# Let's fix the extra closing div at the end
# The last 100 characters usually look like:
#     </div>
# 
# </div>
# 
# </div>
#
# We will count div depth and remove the extra ones.
import re
tags = re.finditer(r'<(/?div)[^>]*>', tpl)
depth = 0
extra_divs = []
for t in tags:
    is_close = t.group(1) == '/div'
    if not is_close:
        depth += 1
    else:
        depth -= 1
        if depth < 0:
            extra_divs.append(t)
            depth = 0 # reset to continue parsing

# Remove the extra divs from the end backwards
for t in reversed(extra_divs):
    tpl = tpl[:t.start()] + tpl[t.end():]

print(f"Removed {len(extra_divs)} extra closing </div> tags.")

# Deploy CSS fix
resp = requests.patch(
    f"{base}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    json={'template': tpl}
)

if resp.status_code == 200:
    print("SUCCESS: Template fixed and deployed!")
else:
    print(f"ERROR: {resp.text[:400]}")
