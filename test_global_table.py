import requests
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

# Get base_uri of global ws
r = requests.get(f"{url}/api/now/table/sys_ws_definition/5e1374f3c36743d0e54832f1b4013146", auth=auth, headers=headers)
base_uri = r.json()['result']['base_uri']
print("Global base URI:", base_uri)

endpoint = f"{url}{base_uri}/exec"
print("Global Endpoint:", endpoint)

test_script = """
var tc = new GlideTableCreator('x_fnx_customer', 'FRAUDNEXUS Customer');
tc.setScope('x_fnx_fraudnexus');
tc.create();

var gr = new GlideRecord('sys_db_object');
gr.addQuery('name', 'x_fnx_customer');
gr.query();
if (gr.next()) {
    return { created: true, sys_id: gr.getUniqueValue(), name: gr.getValue('name'), label: gr.getValue('label') };
}
return { created: false };
"""

r2 = requests.post(endpoint, auth=auth, headers=headers, json={"script": test_script})
print("Result:", r2.json())
