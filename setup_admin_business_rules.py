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

br_js = """
var result = { brs: [] };

function ensureBR(name, table, when, onInsert, onUpdate, filterCond, script) {
    var grBR = new GlideRecord('sys_script');
    grBR.addQuery('name', name);
    grBR.query();
    var brId = '';
    if (!grBR.next()) {
        grBR.initialize();
        grBR.setValue('name', name);
        grBR.setValue('collection', table);
        grBR.setValue('when', when);
        grBR.setValue('action_insert', onInsert);
        grBR.setValue('action_update', onUpdate);
        grBR.setValue('filter_condition', filterCond || '');
        grBR.setValue('script', script);
        grBR.setValue('active', true);
        brId = grBR.insert();
        result.brs.push({ created: name, id: brId });
    } else {
        grBR.setValue('script', script);
        grBR.setValue('active', true);
        grBR.update();
        result.brs.push({ updated: name, id: grBR.getUniqueValue() });
    }
}

// 1. BR-FNX-006 Case Assignment
var br6Script = "(function executeRule(current, previous /*null when async*/) {\\n" +
"    var handlerName = current.assigned_to.getDisplayValue() || current.u_assigned_handler.getDisplayValue() || 'Investigator';\\n" +
"    var grAudit = new GlideRecord('u_x_fnx_audit');\\n" +
"    grAudit.initialize();\\n" +
"    grAudit.setValue('u_case', current.getUniqueValue());\\n" +
"    grAudit.setValue('u_record_type', 'Case');\\n" +
"    grAudit.setValue('u_record_id', current.getValue('number') || '');\\n" +
"    grAudit.setValue('u_action', 'Case Assigned');\\n" +
"    grAudit.setValue('u_details', 'Assigned to ' + handlerName);\\n" +
"    grAudit.setValue('u_performed_by', gs.getUserID());\\n" +
"    grAudit.setValue('u_timestamp', new GlideDateTime());\\n" +
"    grAudit.insert();\\n" +
"})(current, previous);";
ensureBR('BR-FNX-006 Case Assignment', 'u_x_fnx_case', 'after', false, true, 'assigned_toVALCHANGES^ORu_assigned_handlerVALCHANGES', br6Script);

// 2. BR-FNX-007 Case Status Transition
var br7Script = "(function executeRule(current, previous /*null when async*/) {\\n" +
"    var oldSt = previous ? previous.getValue('u_status') : '';\\n" +
"    var newSt = current.getValue('u_status');\\n" +
"    if (newSt === 'Resolved') current.setValue('u_stage', 'Resolved');\\n" +
"    else if (newSt === 'Closed') current.setValue('u_stage', 'Closed');\\n" +
"    else if (newSt === 'In Progress' || newSt === 'Active') current.setValue('u_stage', 'Investigation');\\n" +
"    var grAudit = new GlideRecord('u_x_fnx_audit');\\n" +
"    grAudit.initialize();\\n" +
"    grAudit.setValue('u_case', current.getUniqueValue());\\n" +
"    grAudit.setValue('u_record_type', 'Case');\\n" +
"    grAudit.setValue('u_record_id', current.getValue('number') || '');\\n" +
"    grAudit.setValue('u_action', 'Status Changed');\\n" +
"    grAudit.setValue('u_details', 'Status changed from ' + (oldSt || 'New') + ' to ' + newSt);\\n" +
"    grAudit.setValue('u_performed_by', gs.getUserID());\\n" +
"    grAudit.setValue('u_timestamp', new GlideDateTime());\\n" +
"    grAudit.insert();\\n" +
"})(current, previous);";
ensureBR('BR-FNX-007 Case Status Transition', 'u_x_fnx_case', 'after', false, true, 'u_statusVALCHANGES', br7Script);

// 3. BR-FNX-009 Task Lifecycle
var br9Script = "(function executeRule(current, previous /*null when async*/) {\\n" +
"    var caseId = current.getValue('u_case');\\n" +
"    if (!caseId) return;\\n" +
"    var isNew = current.isNewRecord();\\n" +
"    var taskNum = current.getValue('u_number') || 'Task';\\n" +
"    var grAudit = new GlideRecord('u_x_fnx_audit');\\n" +
"    grAudit.initialize();\\n" +
"    grAudit.setValue('u_case', caseId);\\n" +
"    grAudit.setValue('u_record_type', 'Task');\\n" +
"    grAudit.setValue('u_record_id', taskNum);\\n" +
"    grAudit.setValue('u_action', isNew ? 'Task Created' : 'Task Updated');\\n" +
"    grAudit.setValue('u_details', (isNew ? 'New task created: ' : 'Task updated: ') + (current.getValue('short_description') || '') + ' [' + (current.getValue('state') || 'Open') + ']');\\n" +
"    grAudit.setValue('u_performed_by', gs.getUserID());\\n" +
"    grAudit.setValue('u_timestamp', new GlideDateTime());\\n" +
"    grAudit.insert();\\n" +
"})(current, previous);";
ensureBR('BR-FNX-009 Task Lifecycle', 'u_x_fnx_task', 'after', true, true, '', br9Script);

return JSON.stringify(result);
"""

res = run_script(br_js)
print("BR Result:", res)
