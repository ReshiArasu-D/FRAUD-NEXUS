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

si_js = """
var grSI = new GlideRecord('sys_script_include');
grSI.addQuery('name', 'FNX_AdminCaseService');
grSI.query();

var siScript = "var FNX_AdminCaseService = Class.create();\\n" +
"FNX_AdminCaseService.prototype = {\\n" +
"    initialize: function() {},\\n" +
"\\n" +
"    getDashboardStats: function() {\\n" +
"        var stats = {\\n" +
"            newCases: 0,\\n" +
"            activeCases: 0,\\n" +
"            criticalCases: 0,\\n" +
"            escalatedCases: 0,\\n" +
"            pendingApprovals: 0,\\n" +
"            financialExposure: 0,\\n" +
"            blockedAmount: 0,\\n" +
"            recoveredAmount: 0,\\n" +
"            outstandingAmount: 0\\n" +
"        };\\n" +
"        var grCase = new GlideRecord('u_x_fnx_case');\\n" +
"        grCase.query();\\n" +
"        while (grCase.next()) {\\n" +
"            var st = grCase.getValue('u_status') || 'New';\\n" +
"            var sev = grCase.getValue('u_severity') || 'Medium';\\n" +
"            var exp = parseFloat(grCase.getValue('u_exposure') || '0');\\n" +
"            var blk = parseFloat(grCase.getValue('u_blocked_amount') || '0');\\n" +
"            var rec = parseFloat(grCase.getValue('u_recovered_amount') || '0');\\n" +
"            if (isNaN(exp)) exp = 0;\\n" +
"            if (isNaN(blk)) blk = 0;\\n" +
"            if (isNaN(rec)) rec = 0;\\n" +
"\\n" +
"            if (st === 'New') stats.newCases++;\\n" +
"            if (st !== 'Resolved' && st !== 'Closed') {\\n" +
"                stats.activeCases++;\\n" +
"                stats.financialExposure += exp;\\n" +
"                stats.blockedAmount += blk;\\n" +
"                stats.recoveredAmount += rec;\\n" +
"            }\\n" +
"            if (sev === 'Critical' && st !== 'Closed' && st !== 'Resolved') stats.criticalCases++;\\n" +
"            if (st === 'Escalated' || (grCase.getValue('description') || '').indexOf('[ESCALATED]') !== -1) stats.escalatedCases++;\\n" +
"            if (st === 'Pending' || st === 'In Progress' || st === 'New') stats.pendingApprovals++;\\n" +
"        }\\n" +
"        stats.outstandingAmount = Math.max(0, stats.financialExposure - stats.blockedAmount - stats.recoveredAmount);\\n" +
"        return stats;\\n" +
"    },\\n" +
"\\n" +
"    type: 'FNX_AdminCaseService'\\n" +
"};";

if (!grSI.next()) {
    grSI.initialize();
    grSI.setValue('name', 'FNX_AdminCaseService');
    grSI.setValue('api_name', 'global.FNX_AdminCaseService');
    grSI.setValue('description', 'Operational Admin Case Management Service for FRAUDNEXUS');
    grSI.setValue('script', siScript);
    grSI.setValue('active', true);
    var id = grSI.insert();
    return JSON.stringify({ created: id });
} else {
    grSI.setValue('script', siScript);
    grSI.setValue('active', true);
    grSI.update();
    return JSON.stringify({ updated: grSI.getUniqueValue() });
}
"""

res = run_script(si_js)
print("Script Include Result:", res)
