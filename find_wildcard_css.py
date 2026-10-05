import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
css = r.json()['result'].get('css', '')

idx = css.find('ng-if*="auth"')
if idx == -1:
    idx = css.find("ng-if*='auth'")
if idx == -1:
    idx = css.find("ng-if*=")

print("Found at:", idx)
if idx != -1:
    print(css[max(0, idx-200):min(len(css), idx+400)])
