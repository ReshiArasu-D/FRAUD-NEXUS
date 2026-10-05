import requests, re, sys
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://dev187180.service-now.com/api/now/table/sp_widget/2f258577c32b43d0e54832f1b401317f'
auth = ('admin', 'mn%XC1^ScdA4')
r = requests.get(url, auth=auth)
css = r.json()['result']['css']

for m in re.finditer(r'([^{]+fnx-ai-trigger[^{]*)\{([^}]+)\}', css):
    print('SELECTOR:', m.group(1).strip())
    print('RULE:', m.group(2).strip()[:100])
    print('---')
