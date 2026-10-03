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

setup_js = """
var result = { roles: [], users: [], tables: [], numbers: [] };

// 1. Roles
var roles = ['fnx_investigator', 'fnx_manager', 'fnx_admin', 'fnx_compliance', 'fnx_kyc'];
for (var i = 0; i < roles.length; i++) {
    var rName = roles[i];
    var grRole = new GlideRecord('sys_user_role');
    grRole.addQuery('name', rName);
    grRole.query();
    if (!grRole.next()) {
        grRole.initialize();
        grRole.setValue('name', rName);
        grRole.setValue('description', 'FRAUDNEXUS ' + rName.replace('fnx_', '').toUpperCase() + ' Role');
        var roleId = grRole.insert();
        result.roles.push({ created: rName, id: roleId });
    } else {
        result.roles.push({ exists: rName, id: grRole.getUniqueValue() });
    }
}

// 2. Seed Demo Investigator Account: alex.morgan@fraudnexus.com
var demoEmail = 'alex.morgan@fraudnexus.com';
var grUser = new GlideRecord('sys_user');
grUser.addQuery('email', demoEmail);
grUser.query();
var userSysId = '';
if (!grUser.next()) {
    grUser.initialize();
    grUser.setValue('user_name', 'alex.morgan');
    grUser.setValue('email', demoEmail);
    grUser.setValue('first_name', 'Alex');
    grUser.setValue('last_name', 'Morgan');
    grUser.setValue('name', 'Alex Morgan');
    grUser.setValue('title', 'Senior Fraud Investigator');
    grUser.setValue('department', 'Financial Crimes Investigation');
    grUser.setValue('mobile_phone', '9876543210');
    grUser.setValue('active', true);
    grUser.setValue('user_password', 'DemoPass123!');
    userSysId = grUser.insert();
    result.users.push({ created: demoEmail, id: userSysId });
} else {
    userSysId = grUser.getUniqueValue();
    grUser.setValue('first_name', 'Alex');
    grUser.setValue('last_name', 'Morgan');
    grUser.setValue('name', 'Alex Morgan');
    grUser.setValue('title', 'Senior Fraud Investigator');
    grUser.setValue('active', true);
    grUser.setValue('user_password', 'DemoPass123!');
    grUser.update();
    result.users.push({ updated: demoEmail, id: userSysId });
}

// Assign fnx_investigator and fnx_admin roles to Alex Morgan
for (var j = 0; j < roles.length; j++) {
    var rName2 = roles[j];
    var grR = new GlideRecord('sys_user_role');
    grR.addQuery('name', rName2);
    grR.query();
    if (grR.next()) {
        var rSysId = grR.getUniqueValue();
        var grUR = new GlideRecord('sys_user_has_role');
        grUR.addQuery('user', userSysId);
        grUR.addQuery('role', rSysId);
        grUR.query();
        if (!grUR.next()) {
            grUR.initialize();
            grUR.setValue('user', userSysId);
            grUR.setValue('role', rSysId);
            grUR.insert();
        }
    }
}

// Also seed a couple more investigators for assignment dropdown
var handlers = [
    { email: 'sophia.r@fraudnexus.com', first: 'Sophia', last: 'Reynolds', name: 'Sophia Reynolds', title: 'Cyber Fraud Specialist' },
    { email: 'james.d@fraudnexus.com', first: 'James', last: 'Davis', name: 'James Davis', title: 'Senior AML Analyst' },
    { email: 'maria.k@fraudnexus.com', first: 'Maria', last: 'Kumar', name: 'Maria Kumar', title: 'Forensic Investigator' },
    { email: 'liam.t@fraudnexus.com', first: 'Liam', last: 'Taylor', name: 'Liam Taylor', title: 'Payment Fraud Specialist' },
    { email: 'ava.p@fraudnexus.com', first: 'Ava', last: 'Patel', name: 'Ava Patel', title: 'Intelligence Analyst' }
];

for (var k = 0; k < handlers.length; k++) {
    var h = handlers[k];
    var grH = new GlideRecord('sys_user');
    grH.addQuery('email', h.email);
    grH.query();
    if (!grH.next()) {
        grH.initialize();
        grH.setValue('user_name', h.email.split('@')[0]);
        grH.setValue('email', h.email);
        grH.setValue('first_name', h.first);
        grH.setValue('last_name', h.last);
        grH.setValue('name', h.name);
        grH.setValue('title', h.title);
        grH.setValue('active', true);
        grH.setValue('user_password', 'DemoPass123!');
        var hId = grH.insert();
        result.users.push({ created: h.email, id: hId });
    }
}

// 3. Create u_x_fnx_task table if not exists
var grTbl = new GlideRecord('sys_db_object');
grTbl.addQuery('name', 'u_x_fnx_task');
grTbl.query();
if (!grTbl.next()) {
    grTbl.initialize();
    grTbl.setValue('name', 'u_x_fnx_task');
    grTbl.setValue('label', 'FRAUDNEXUS Investigation Task');
    grTbl.setValue('user_role', 'fnx_investigator');
    grTbl.setValue('super_class', ''); // standalone or task
    var tblId = grTbl.insert();
    result.tables.push({ created: 'u_x_fnx_task', id: tblId });

    // Helper to create dictionary column
    function createCol(el, label, type, len, ref) {
        var grCol = new GlideRecord('sys_dictionary');
        grCol.initialize();
        grCol.setValue('name', 'u_x_fnx_task');
        grCol.setValue('element', el);
        grCol.setValue('column_label', label);
        grCol.setValue('internal_type', type);
        grCol.setValue('max_length', len || '40');
        if (ref) grCol.setValue('reference', ref);
        grCol.insert();
    }

    createCol('u_number', 'Task Number', 'string', '40');
    createCol('u_case', 'Case', 'reference', '32', 'u_x_fnx_case');
    createCol('short_description', 'Short Description', 'string', '255');
    createCol('description', 'Description', 'string', '4000');
    createCol('assigned_to', 'Assigned To', 'reference', '32', 'sys_user');
    createCol('assignment_group', 'Assignment Group', 'string', '100');
    createCol('priority', 'Priority', 'string', '40');
    createCol('due_date', 'Due Date', 'glide_date_time', '40');
    createCol('state', 'State', 'string', '40');
    createCol('u_completion_notes', 'Completion Notes', 'string', '4000');
    createCol('u_evidence_required', 'Evidence Required', 'boolean', '40');
} else {
    result.tables.push({ exists: 'u_x_fnx_task', id: grTbl.getUniqueValue() });
}

// 4. Number Maintenance for u_x_fnx_task
var grNum = new GlideRecord('sys_number');
grNum.addQuery('category', 'u_x_fnx_task');
grNum.query();
if (!grNum.next()) {
    grNum.initialize();
    grNum.setValue('category', 'u_x_fnx_task');
    grNum.setValue('prefix', 'TSK-2026-');
    grNum.setValue('maximum_digits', 6);
    grNum.setValue('number', 1000);
    var numId = grNum.insert();
    result.numbers.push({ created: 'TSK-2026-', id: numId });
} else {
    result.numbers.push({ exists: 'TSK-2026-' });
}

return JSON.stringify(result);
"""

res = run_script(setup_js)
print("Setup Result:", res)
