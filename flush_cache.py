import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'

print("Flushing ServiceNow server cache...")
r = requests.get(f'{base}/cache.do', auth=auth)

if r.status_code == 200:
    print("SUCCESS: Cache flushed successfully!")
else:
    print(f"ERROR: {r.status_code} - {r.text[:200]}")
