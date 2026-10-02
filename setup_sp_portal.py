import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

# Check if sp_portal with url_suffix 'fnx' exists
r_chk = requests.get(f"{url}/api/now/table/sp_portal?sysparm_query=url_suffix=fnx", auth=auth, headers=headers)
existing = r_chk.json().get('result', [])

if existing:
    print(f"Portal /fnx already exists: {existing[0]['sys_id']}")
else:
    # Get a theme or page
    r_sp = requests.get(f"{url}/api/now/table/sp_portal?sysparm_query=url_suffix=sp", auth=auth, headers=headers)
    sp_sample = r_sp.json().get('result', [])[0]
    
    payload = {
        "title": "FRAUDNEXUS Customer Portal",
        "url_suffix": "fnx",
        "homepage": sp_sample.get('homepage'),
        "theme": sp_sample.get('theme'),
        "logo": sp_sample.get('logo'),
        "short_description": "From Fraud Report to Resolution - One Intelligent Investigation Workspace"
    }
    r_create = requests.post(f"{url}/api/now/table/sp_portal", auth=auth, headers=headers, json=payload)
    print("Portal create status:", r_create.status_code)
    if r_create.status_code == 201:
        print("Created /fnx portal:", r_create.json()['result'].get('sys_id'))
