import requests
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json'}

# Check app engine studio
r = requests.get(f"{url}/api/now/table/sys_plugins?sysparm_query=idLIKEstudio^ORidLIKEapp_engine&sysparm_fields=id,name,active", auth=auth, headers=headers)
print("Studio plugins:", r.json().get('result'))

# Check sys_ui_page for studio or table creator
r2 = requests.get(f"{url}/api/now/table/sys_ui_page?sysparm_query=nameLIKEtable^ORnameLIKEschema&sysparm_limit=5&sysparm_fields=name,title", auth=auth, headers=headers)
print("UI pages:", r2.json().get('result'))
