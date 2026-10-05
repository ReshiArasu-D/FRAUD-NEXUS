import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
template = r.json()['result']['template']

idx_aside = template.find('<aside')
idx_aside_end = template.find('</aside>')
print("=== ASIDE SIDEBAR ===")
print(template[idx_aside:idx_aside_end+8])

print("\n=== SEARCHING ALL ng-if='c.currentView ===' ===")
import re
for m in re.finditer(r'ng-if="[^"]*c\.currentView[^"]*"', template):
    print(m.group(0))

for m in re.finditer(r"c\.navigate\('[^']+'\)", template):
    print(m.group(0))

