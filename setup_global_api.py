import requests
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

# Check how tables are created in ServiceNow or test global scope script runner
r = requests.get(f"{url}/api/now/table/sys_scope?sysparm_query=scope=global", auth=auth, headers=headers)
global_scope_id = r.json()['result'][0]['sys_id']
print("Global scope id:", global_scope_id)

# Let's create an admin global scripted rest api for setup
ws_payload = {
    "name": "FRAUDNEXUS Global Admin API",
    "service_id": "fnx_admin_api",
    "sys_scope": global_scope_id,
    "sys_package": global_scope_id,
    "active": "true"
}

r_ws = requests.post(f"{url}/api/now/table/sys_ws_definition", auth=auth, headers=headers, json=ws_payload)
print("Global WS create status:", r_ws.status_code)
if r_ws.status_code == 201:
    ws_id = r_ws.json()['result']['sys_id']
else:
    r_find = requests.get(f"{url}/api/now/table/sys_ws_definition?sysparm_query=service_id=fnx_admin_api", auth=auth, headers=headers)
    ws_id = r_find.json()['result'][0]['sys_id']

print("Global WS ID:", ws_id)

script_body = """(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {
    var data = request.body.data;
    var script = data.script;
    var result = { success: false, output: null, error: null };
    
    try {
        var evaluator = new GlideScopedEvaluator();
        // Or direct eval in global
        var func = new Function('return (function() { ' + script + ' })();');
        result.output = func();
        result.success = true;
    } catch (e) {
        result.error = e.toString() + (e.stack ? '\\n' + e.stack : '');
    }
    
    response.setStatus(200);
    response.setBody(result);
})(request, response);"""

op_payload = {
    "web_service_definition": ws_id,
    "name": "exec_global",
    "http_method": "POST",
    "relative_path": "/exec",
    "operation_script": script_body,
    "requires_authentication": "true",
    "requires_snc_internal_role": "false",
    "active": "true",
    "sys_scope": global_scope_id,
    "sys_package": global_scope_id
}

r_op = requests.post(f"{url}/api/now/table/sys_ws_operation", auth=auth, headers=headers, json=op_payload)
print("Global Op status:", r_op.status_code)
if r_op.status_code != 201:
    print(r_op.text[:300])
