import requests
import os
import json
from dotenv import load_dotenv

load_dotenv('d:/KPMG/.env')
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
endpoint = f"{url}/api/2229367/fnx_api/exec"

js = """
try {
    var filter = 'all';
    var search = '';
    var cases = [];
    var grCases = new GlideRecord('u_x_fnx_case');
    grCases.orderByDesc('sys_created_on');
    grCases.query();
    var count = 0;
    while (grCases.next()) {
        count++;
        var cid = grCases.getUniqueValue();
        var cnum = grCases.getValue('number') || ('FNX-2026-' + cid.substring(0,6).toUpperCase());
        var ctype = grCases.getValue('u_type') || 'Payment Fraud';
        var csev = grCases.getValue('u_severity') || 'Medium';
        var cstatus = grCases.getValue('u_status') || 'New';
        var chandler = grCases.assigned_to.getDisplayValue() || grCases.u_assigned_handler.getDisplayValue() || 'Unassigned';
        var cexp = grCases.getValue('u_exposure') || '0';
        cases.push({
            sys_id: cid,
            number: cnum,
            type: ctype,
            severity: csev,
            status: cstatus,
            exposure: cexp,
            handler: chandler
        });
        if (cases.length >= 5) break;
    }
    return JSON.stringify({ total: count, sample: cases });
} catch(e) {
    return JSON.stringify({ error: e.message });
}
"""

r = requests.post(endpoint, auth=auth, json={"script": js})
print(r.json())
