import requests, re, sys
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://dev187180.service-now.com/api/now/table/sp_widget/2f258577c32b43d0e54832f1b401317f'
auth = ('admin', 'mn%XC1^ScdA4')
r = requests.get(url, auth=auth)
data = r.json()['result']
template = data['template']
css = data['css']

idx_ai = template.find('5. FLOATING NOW ASSIST AI')
print('=== TEMPLATE AI SECTION (first 1000 chars) ===')
print(template[idx_ai:idx_ai+1500])

print('=== CSS SEARCH FOR fnx-ai-widget OR fnx-ai-trigger ===')
for m in re.finditer(r'(\.fnx-ai-[^{]+)\{([^}]+)\}', css):
    print(m.group(1).strip(), '-->', m.group(2).strip()[:100])
