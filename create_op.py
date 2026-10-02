import requests
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

ws_id = "4e92fc73c36743d0e54832f1b401317d"
app_id = "b4617cbfc32743d0e54832f1b40131f8"

# Check if operation exists
r_op = requests.get(f"{url}/api/now/table/sys_ws_operation?sysparm_query=web_service_definition={ws_id}^name=exec", auth=auth, headers=headers)
ops = r_op.json().get('result', [])

script_body = """(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {
    var data = request.body.data;
    var script = data.script;
    var result = { success: false, output: null, error: null };
    
    try {
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
    "name": "exec",
    "http_method": "POST",
    "relative_path": "/exec",
    "operation_script": script_body,
    "requires_authentication": "true",
    "requires_snc_internal_role": "false",
    "active": "true",
    "sys_scope": app_id,
    "sys_package": app_id
}

if ops:
    op_id = ops[0]['sys_id']
    r_update = requests.patch(f"{url}/api/now/table/sys_ws_operation/{op_id}", auth=auth, headers=headers, json=op_payload)
    print("Updated operation:", r_update.status_code)
else:
    r_create = requests.post(f"{url}/api/now/table/sys_ws_operation", auth=auth, headers=headers, json=op_payload)
    print("Created operation:", r_create.status_code, r_create.text[:200])

