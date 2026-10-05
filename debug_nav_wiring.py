import requests, json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
template = r.json()['result']['template']

print("=== SIDEBAR NAV ===")
idx_nav = template.find('<nav class="fnx-nav">')
if idx_nav != -1:
    print(template[idx_nav:idx_nav+1000])

print("\n=== SEARCHING ALL ng-if IN MAIN VIEW CONTAINER ===")
idx_main = template.find('<main class="fnx-content"')
idx_main_end = template.find('</main>')
if idx_main != -1 and idx_main_end != -1:
    main_content = template[idx_main:idx_main_end]
    for m in re.finditer(r'<!-- =+ (4[A-Z]\.[^=]+)=+ -->', main_content):
        print(f"Header: {m.group(1)} at rel pos {m.start()}")
    for m in re.finditer(r'ng-if="c\.currentView === [^"]+"', main_content):
        print(f"ng-if: {m.group(0)} at rel pos {m.start()}")

# Let's inspect the exact view content around 4F, 4G, help, evidenceVault
for view_name in ['evidenceVault', 'evidence', 'help', 'support']:
    print(f"\n--- Checking view: {view_name} ---")
    pos = 0
    while True:
        pos = template.find(f"'{view_name}'", pos)
        if pos == -1:
            break
        print(f"Found '{view_name}' at {pos}:")
        print(repr(template[max(0, pos-60):min(len(template), pos+80)]))
        pos += len(view_name) + 2

