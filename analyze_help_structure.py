import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
template = r.json()['result']['template']

idx_start = template.find('c.currentView === \'help\'')
idx_main = template.find('</main>', idx_start)
print("idx_start:", idx_start, "idx_main:", idx_main, "difference:", idx_main - idx_start)

# Print first 2000 chars of help view
print("\n--- FIRST 2000 CHARS OF HELP VIEW ---")
print(template[idx_start-60:idx_start+2000])

# Where are other views or sections?
import re
for m in re.finditer(r'<!-- =+ [^=]+ =+ -->', template[idx_start:idx_main]):
    print("Found section header inside help-view region:", m.group(0), "at offset", m.start())

for m in re.finditer(r'<div ng-if="[^"]+"', template[idx_start:idx_main]):
    print("Found ng-if inside help-view region:", m.group(0), "at offset", m.start())

