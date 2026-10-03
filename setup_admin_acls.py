import requests
import os
import json
from dotenv import load_dotenv

load_dotenv('d:/KPMG/.env')
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
endpoint = f"{url}/api/2229367/fnx_api/exec"

def run_script(js):
    r = requests.post(endpoint, auth=auth, headers=headers, json={"script": js})
    try:
        res = r.json()
        if 'result' in res and 'output' in res['result']:
            return res['result']['output']
        return res
    except Exception as e:
        return {"error": str(e), "raw": r.text}

acl_js = """
var result = { acls: [] };

function ensureACL(type, name, operation, roleName) {
    var grRole = new GlideRecord('sys_user_role');
    grRole.addQuery('name', roleName);
    grRole.query();
    var roleSysId = '';
    if (grRole.next()) roleSysId = grRole.getUniqueValue();

    var grACL = new GlideRecord('sys_security_acl');
    grACL.addQuery('type', type);
    grACL.addQuery('name', name);
    grACL.addQuery('operation', operation);
    grACL.query();
    var aclSysId = '';
    if (!grACL.next()) {
        grACL.initialize();
        grACL.setValue('type', type);
        grACL.setValue('name', name);
        grACL.setValue('operation', operation);
        grACL.setValue('active', true);
        grACL.setValue('description', 'FRAUDNEXUS Security ACL: ' + operation + ' on ' + name + ' for ' + roleName);
        aclSysId = grACL.insert();
        result.acls.push({ created: name + ' (' + operation + ')', id: aclSysId });
    } else {
        aclSysId = grACL.getUniqueValue();
        result.acls.push({ exists: name + ' (' + operation + ')', id: aclSysId });
    }

    if (roleSysId && aclSysId) {
        var grACLR = new GlideRecord('sys_security_acl_role');
        grACLR.addQuery('sys_security_acl', aclSysId);
        grACLR.addQuery('sys_user_role', roleSysId);
        grACLR.query();
        if (!grACLR.next()) {
            grACLR.initialize();
            grACLR.setValue('sys_security_acl', aclSysId);
            grACLR.setValue('sys_user_role', roleSysId);
            grACLR.insert();
        }
    }
}

// Ensure investigator role has read/write on u_x_fnx_task
ensureACL('record', 'u_x_fnx_task', 'read', 'fnx_investigator');
ensureACL('record', 'u_x_fnx_task', 'write', 'fnx_investigator');
ensureACL('record', 'u_x_fnx_task', 'create', 'fnx_investigator');

// Ensure investigator role has read/write on u_x_fnx_case
ensureACL('record', 'u_x_fnx_case', 'read', 'fnx_investigator');
ensureACL('record', 'u_x_fnx_case', 'write', 'fnx_investigator');

// Ensure investigator role has read/write on u_x_fnx_evidence
ensureACL('record', 'u_x_fnx_evidence', 'read', 'fnx_investigator');
ensureACL('record', 'u_x_fnx_evidence', 'write', 'fnx_investigator');

// Ensure investigator role has read on u_x_fnx_customer
ensureACL('record', 'u_x_fnx_customer', 'read', 'fnx_investigator');

return JSON.stringify(result);
"""

res = run_script(acl_js)
print("ACL Result:", res)
