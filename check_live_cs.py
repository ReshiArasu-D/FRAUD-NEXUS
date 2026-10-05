import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
cs = r.json()['result'].get('client_script', '')

print("Total client_script len:", len(cs))
print("Contains initAnalyticsWorkspace?", "initAnalyticsWorkspace" in cs)
idx = cs.find("initAnalyticsWorkspace")
if idx != -1:
    print("Around initAnalyticsWorkspace:")
    print(cs[idx-100:idx+300])
else:
    print("Last 500 chars of cs:")
    print(cs[-500:])
