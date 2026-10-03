import requests
import os
import json
from dotenv import load_dotenv

load_dotenv('d:/KPMG/.env')
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
endpoint = f"{url}/api/2229367/fnx_api/exec"

js = """
var gr = new GlideRecord('sys_ws_operation');
gr.addQuery('name', 'STARTSWITH', 'admin_case');
gr.query();
var res = [];
while (gr.next()) {
    res.push({
        id: gr.getUniqueValue(),
        name: gr.getValue('name'),
        method: gr.getValue('http_method'),
        path: gr.getValue('relative_path'),
        script: gr.getValue('operation_script')
    });
}
return JSON.stringify(res);
"""

r = requests.post(endpoint, auth=auth, json={"script": js})
ops = json.loads(r.json()['result']['output'])
for o in ops:
    print(f"Name: {o['name']}, Method: {o['method']}, Path: {o['path']}, Script len: {len(o['script'] or '')}")
    if o['script'] and len(o['script']) > 0:
        print("First 200 chars:\n", o['script'][:200])
