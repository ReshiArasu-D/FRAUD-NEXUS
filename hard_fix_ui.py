import requests, sys, re

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

print("Fetching template...")
r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
data = r.json()['result']
tpl = data['template']

# FIX 1: The duplicate AI trigger button needs ng-if to hide it in the admin workspace!
# Find: <button class="fnx-ai-trigger"
ai_btn_pattern = r'(<button class="fnx-ai-trigger"[^>]*ng-click="c\.showAI = !c\.showAI"[^>]*>)'
if 'ng-if="c.currentView !== \'adminWorkspace\'"' not in tpl:
    # Wrap it with an ng-if attribute directly
    tpl = re.sub(
        ai_btn_pattern,
        r'\1'.replace('<button ', '<button ng-if="c.currentView !== \'adminWorkspace\'" '),
        tpl,
        count=1
    )
    print("Fixed AI button overlap")

# FIX 2: Inline CSS to force the admin layout to work properly and avoid ANY empty space
admin_layout_pattern = r'<div ng-if="c\.currentView === \'adminWorkspace\'" class="fnx-admin-layout">'
tpl = tpl.replace(
    admin_layout_pattern,
    '<div ng-if="c.currentView === \'adminWorkspace\'" class="fnx-admin-layout" style="display: flex; flex-direction: column; height: 100vh; min-height: 100vh; overflow: hidden; margin: 0; padding: 0; position: absolute; top: 0; left: 0; right: 0; bottom: 0;">'
)

admin_body_pattern = r'<div class="fnx-admin-body">'
tpl = tpl.replace(
    admin_body_pattern,
    '<div class="fnx-admin-body" style="display: flex; flex: 1; overflow: hidden; min-height: 0;">'
)

print("Fixed Admin Layout empty space")

# Push updates
print("Deploying...")
resp = requests.patch(
    f"{base}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    json={'template': tpl}
)

if resp.status_code == 200:
    print("SUCCESS: Fixes deployed!")
else:
    print(f"ERROR: {resp.text[:400]}")
