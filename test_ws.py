import requests
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json'}

r1 = requests.get(f"{url}/api/now/table/sys_ws_definition?sysparm_limit=1", auth=auth, headers=headers)
print("sys_ws_definition fields:", list(r1.json()['result'][0].keys()))

r2 = requests.get(f"{url}/api/now/table/sys_ws_operation?sysparm_limit=1", auth=auth, headers=headers)
print("sys_ws_operation fields:", list(r2.json()['result'][0].keys()))
