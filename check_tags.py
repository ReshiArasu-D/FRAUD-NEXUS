import requests, sys, re
sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
tpl = r.json()['result']['template']

print("LANDING:")
for m in re.finditer(r'<div[^>]*class="fnx-landing"[^>]*>', tpl):
    print(m.group(0))

print("\nAI TRIGGER:")
for m in re.finditer(r'<button[^>]*class="fnx-ai-trigger"[^>]*>', tpl):
    print(m.group(0))
