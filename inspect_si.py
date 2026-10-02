import requests
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json'}

r = requests.get(f"{url}/api/now/table/sys_script_include?sysparm_query=nameLIKEtable^ORnameLIKEappcreator^ORscriptLIKEGlideTableCreator&sysparm_fields=name,sys_id&sysparm_limit=20", auth=auth, headers=headers)
print("Script includes count:", len(r.json().get('result', [])))
for s in r.json().get('result', []):
    print(" -", s.get('name'))
