import requests
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json'}

# Query a small task-extended table or custom table dictionary entries
r = requests.get(f"{url}/api/now/table/sys_dictionary?sysparm_query=name=incident^internal_type=collection&sysparm_fields=name,internal_type,element,sys_id", auth=auth, headers=headers)
print("Collection dict for incident:", r.json().get('result'))
