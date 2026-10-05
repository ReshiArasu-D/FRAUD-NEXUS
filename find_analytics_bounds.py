import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
tpl = r.json()['result']['template']

p_analytics = tpl.find("<div ng-if=\"c.adminModule === 'analytics'\"")
p_settings = tpl.find("<div ng-if=\"c.adminModule === 'settings'\"", p_analytics)

cb = tpl.rfind("<!--", 0, p_analytics)
if cb != -1 and "VIEW 6" in tpl[cb:p_analytics]:
    start = cb
else:
    start = p_analytics

# find the comment before settings
cb_set = tpl.rfind("<!--", p_analytics, p_settings)
if cb_set != -1 and "VIEW 7" in tpl[cb_set:p_settings]:
    end = cb_set
else:
    end = p_settings

print(f"Analytics view spans from index {start} to {end} (length: {end - start})")
print("--- PREVIEW ---")
print(tpl[start:start+200])
print("--- END PREVIEW ---")
print(tpl[end-150:end])
