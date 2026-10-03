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

audit_js = """
var audit = {};

// 1. Applications & Scope
audit.apps = [];
var grApp = new GlideRecord('sys_app');
grApp.addQuery('name', 'CONTAINS', 'FRAUD').addOrCondition('scope', 'CONTAINS', 'fnx');
grApp.query();
while (grApp.next()) {
    audit.apps.push({
        name: grApp.getValue('name'),
        scope: grApp.getValue('scope'),
        sys_id: grApp.getUniqueValue()
    });
}

// 2. Tables
audit.tables = [];
var grTable = new GlideRecord('sys_db_object');
grTable.addQuery('name', 'CONTAINS', 'fnx');
grTable.query();
while (grTable.next()) {
    var tName = grTable.getValue('name');
    var grCount = new GlideRecord(tName);
    var count = 0;
    try {
        grCount.query();
        count = grCount.getRowCount();
    } catch(e) { count = -1; }
    audit.tables.push({
        label: grTable.getValue('label'),
        name: tName,
        super_class: grTable.getDisplayValue('super_class'),
        records_count: count
    });
}

// 3. Table Fields
audit.fields = {};
for (var i = 0; i < audit.tables.length; i++) {
    var tn = audit.tables[i].name;
    audit.fields[tn] = [];
    var grDict = new GlideRecord('sys_dictionary');
    grDict.addQuery('name', tn);
    grDict.query();
    while (grDict.next()) {
        audit.fields[tn].push({
            element: grDict.getValue('element'),
            column_label: grDict.getValue('column_label'),
            internal_type: grDict.getValue('internal_type'),
            max_length: grDict.getValue('max_length'),
            reference: grDict.getValue('reference')
        });
    }
}

// 4. Service Portals
audit.portals = [];
var grSP = new GlideRecord('sp_portal');
grSP.addQuery('url_suffix', 'CONTAINS', 'fnx').addOrCondition('title', 'CONTAINS', 'FRAUD');
grSP.query();
while (grSP.next()) {
    audit.portals.push({
        title: grSP.getValue('title'),
        url_suffix: grSP.getValue('url_suffix'),
        homepage: grSP.getDisplayValue('homepage_page'),
        sys_id: grSP.getUniqueValue()
    });
}

// 5. Pages
audit.pages = [];
var grPage = new GlideRecord('sp_page');
grPage.addQuery('id', 'CONTAINS', 'fnx').addOrCondition('title', 'CONTAINS', 'FRAUD');
grPage.query();
while (grPage.next()) {
    audit.pages.push({
        id: grPage.getValue('id'),
        title: grPage.getValue('title'),
        sys_id: grPage.getUniqueValue()
    });
}

// 6. Widgets
audit.widgets = [];
var grWidget = new GlideRecord('sp_widget');
grWidget.addQuery('id', 'CONTAINS', 'fnx').addOrCondition('name', 'CONTAINS', 'FRAUD');
grWidget.query();
while (grWidget.next()) {
    audit.widgets.push({
        name: grWidget.getValue('name'),
        id: grWidget.getValue('id'),
        sys_id: grWidget.getUniqueValue()
    });
}

// 7. REST APIs
audit.apis = [];
var grWS = new GlideRecord('sys_ws_definition');
grWS.addQuery('name', 'CONTAINS', 'fnx').addOrCondition('service_id', 'CONTAINS', 'fnx');
grWS.query();
while (grWS.next()) {
    var wsId = grWS.getUniqueValue();
    var ops = [];
    var grOp = new GlideRecord('sys_ws_operation');
    grOp.addQuery('web_service_definition', wsId);
    grOp.query();
    while (grOp.next()) {
        ops.push({
            name: grOp.getValue('name'),
            http_method: grOp.getValue('http_method'),
            relative_path: grOp.getValue('relative_path')
        });
    }
    audit.apis.push({
        name: grWS.getValue('name'),
        service_id: grWS.getValue('service_id'),
        namespace: grWS.getValue('namespace'),
        operations: ops
    });
}

// 8. Script Includes
audit.script_includes = [];
var grSI = new GlideRecord('sys_script_include');
grSI.addQuery('name', 'CONTAINS', 'FNX').addOrCondition('name', 'CONTAINS', 'fnx');
grSI.query();
while (grSI.next()) {
    audit.script_includes.push({
        name: grSI.getValue('name'),
        api_name: grSI.getValue('api_name'),
        description: grSI.getValue('description')
    });
}

// 9. Business Rules
audit.business_rules = [];
var grBR = new GlideRecord('sys_script');
grBR.addQuery('name', 'CONTAINS', 'FNX').addOrCondition('collection', 'CONTAINS', 'fnx');
grBR.query();
while (grBR.next()) {
    audit.business_rules.push({
        name: grBR.getValue('name'),
        collection: grBR.getValue('collection'),
        when: grBR.getValue('when'),
        action_insert: grBR.getValue('action_insert'),
        action_update: grBR.getValue('action_update')
    });
}

// 10. Roles
audit.roles = [];
var grRole = new GlideRecord('sys_user_role');
grRole.addQuery('name', 'CONTAINS', 'fnx');
grRole.query();
while (grRole.next()) {
    audit.roles.push({
        name: grRole.getValue('name'),
        description: grRole.getValue('description')
    });
}

// 11. Number Maintenance
audit.numbers = [];
var grNum = new GlideRecord('sys_number');
grNum.addQuery('category', 'CONTAINS', 'fnx').addOrCondition('prefix', 'IN', 'FNX,CNX,EV,TSK');
grNum.query();
while (grNum.next()) {
    audit.numbers.push({
        category: grNum.getValue('category'),
        prefix: grNum.getValue('prefix'),
        maximum_digits: grNum.getValue('maximum_digits'),
        number: grNum.getValue('number')
    });
}

// 12. Choices for Case status, severity, type
audit.choices = {};
var grChoice = new GlideRecord('sys_choice');
grChoice.addQuery('name', 'u_x_fnx_case');
grChoice.query();
while (grChoice.next()) {
    var el = grChoice.getValue('element');
    if (!audit.choices[el]) audit.choices[el] = [];
    audit.choices[el].push({
        value: grChoice.getValue('value'),
        label: grChoice.getValue('label')
    });
}

return JSON.stringify(audit);
"""

res = run_script(audit_js)
with open('d:/KPMG/instance_audit_result.json', 'w', encoding='utf-8') as f:
    if isinstance(res, str):
        try:
            parsed = json.loads(res)
            json.dump(parsed, f, indent=2)
            print("Audit success! Saved to d:/KPMG/instance_audit_result.json")
            print(f"Tables: {[t['name'] for t in parsed.get('tables', [])]}")
            print(f"APIs: {[a['name'] for a in parsed.get('apis', [])]}")
            print(f"Roles: {[r['name'] for r in parsed.get('roles', [])]}")
            print(f"Business Rules: {[b['name'] for b in parsed.get('business_rules', [])]}")
        except:
            f.write(res)
            print("Saved raw string")
    else:
        json.dump(res, f, indent=2)
        print("Audit returned object")
