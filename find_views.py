import requests, os, re
from dotenv import load_dotenv
load_dotenv('d:/KPMG/.env')
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json'}
r = requests.get(f'{url}/api/now/table/sp_widget/2f258577c32b43d0e54832f1b401317f', auth=auth, headers=headers)
t = r.json()['result']['template']
views = re.findall(r"c\.currentView\s*[!=]==?\s*['\"][^'\"]+['\"]", t)
print("CurrentView checks in template:", set(views))

# Also check outer wrapping conditions
outer_ng_ifs = re.findall(r'ng-if="[^"]*"', t)
print("\nFirst 10 ng-if statements:")
for o in outer_ng_ifs[:10]:
    print(" ", o)
