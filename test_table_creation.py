import requests
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
endpoint = f"{url}/api/2229367/fnx_api/exec"

def run_sn_script(script):
    r = requests.post(endpoint, auth=auth, headers=headers, json={"script": script})
    return r.json().get('result', {})

test_script = """
var res = {};
res.tableCreatorExists = (typeof GlideTableCreator !== 'undefined');

// Check if x_fnx_customer already exists
var grCheck = new GlideRecord('sys_db_object');
grCheck.addQuery('name', 'x_fnx_customer');
grCheck.query();
if (grCheck.next()) {
    res.customerTableExists = true;
    res.tableId = grCheck.getUniqueValue();
} else {
    res.customerTableExists = false;
    if (res.tableCreatorExists) {
        var tc = new GlideTableCreator('x_fnx_customer', 'FRAUDNEXUS Customer');
        tc.create();
        
        var grVerify = new GlideRecord('sys_db_object');
        grVerify.addQuery('name', 'x_fnx_customer');
        grVerify.query();
        res.created = grVerify.next();
        if (res.created) {
            res.newTableId = grVerify.getUniqueValue();
        }
    }
}
return res;
"""

print(run_sn_script(test_script))
