import requests, sys, json

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
data = r.json()['result']
tpl = data['template']
css = data['css']
cs = data['client_script']

print("Applying customer click fix...")

# 1. FIX THE HTML FOR THE CUSTOMER LINK
old_td = '<td><strong style="color:#0284C7;">{{cust.customer_id}}</strong></td>'
new_td = '<td><a href="javascript:void(0)" style="color:#0284C7; text-decoration:underline; font-weight:bold;" ng-click="c.viewCustomer(cust)">{{cust.customer_id}}</a></td>'
if old_td in tpl:
    tpl = tpl.replace(old_td, new_td)
    print("Fixed Customer TD")
else:
    print("Could not find the EXACT old_td string, trying a fallback replacement.")
    # Fallback if there are spaces
    import re
    tpl = re.sub(r'<td>\s*<strong[^>]*>\{\{cust\.customer_id\}\}</strong>\s*</td>', new_td, tpl)


# 2. FIX THE JS FUNCTION TO USE customer_id INSTEAD OF id
old_js = "ID: ' + cust.id"
new_js = "ID: ' + (cust.customer_id || cust.id)"
if old_js in cs:
    cs = cs.replace(old_js, new_js)
    print("Fixed JS ID reference")

# Cache bust
import time
import re
tpl = re.sub(r'<!-- CACHE BUST: .*? -->\n*', '', tpl)
tpl = f'<!-- CACHE BUST: {int(time.time())} -->\n' + tpl

# Deploy
resp = requests.patch(
    f"{base}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    json={'template': tpl, 'client_script': cs}
)

if resp.status_code == 200:
    print("SUCCESS: Customer click deployed!")
    requests.get(f'{base}/cache.do', auth=auth)
else:
    print(f"ERROR: {resp.text[:400]}")
