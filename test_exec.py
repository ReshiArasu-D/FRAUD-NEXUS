import requests
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

endpoint = f"{url}/api/2229367/fnx_api/exec"
payload = {
    "script": "return 'Hello from ServiceNow! User: ' + gs.getUserName() + ', Scope: ' + gs.getCurrentScopeName() + ', Instance: ' + gs.getProperty('instance_name');"
}

r = requests.post(endpoint, auth=auth, headers=headers, json=payload)
print("Status:", r.status_code)
print("Response:", r.json())
