import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv('d:/KPMG/.env')
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

r = requests.get(f"{url}/api/2229367/fnx_api/admin_cases", auth=auth, headers=headers)
print("Status:", r.status_code)
print("Headers:", dict(r.headers))
print("Raw text len:", len(r.text))
print("Raw text:", repr(r.text))
