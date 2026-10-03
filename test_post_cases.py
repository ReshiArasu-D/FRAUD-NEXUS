import requests
import os
from dotenv import load_dotenv

load_dotenv('d:/KPMG/.env')
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
endpoint = f"{url}/api/2229367/fnx_api/admin_cases"

r = requests.post(endpoint, auth=auth, json={"action": "add_task", "case_id": "test"})
print("Status:", r.status_code)
print("Keys in response:", list(r.json().keys()))
if 'result' in r.json():
    print("Result keys:", list(r.json()['result'].keys()) if isinstance(r.json()['result'], dict) else type(r.json()['result']))
