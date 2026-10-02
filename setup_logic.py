import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

def ensure_script_include(name: str, script: str, description: str = ""):
    r_chk = requests.get(f"{url}/api/now/table/sys_script_include?sysparm_query=name={name}", auth=auth, headers=headers)
    existing = r_chk.json().get('result', [])
    payload = {
        "name": name,
        "api_name": f"global.{name}",
        "script": script,
        "description": description,
        "access": "public",
        "client_callable": "false",
        "active": "true"
    }
    if existing:
        si_id = existing[0]['sys_id']
        requests.patch(f"{url}/api/now/table/sys_script_include/{si_id}", auth=auth, headers=headers, json=payload)
        print(f"Updated Script Include: {name}")
    else:
        requests.post(f"{url}/api/now/table/sys_script_include", auth=auth, headers=headers, json=payload)
        print(f"Created Script Include: {name}")

def ensure_business_rule(name: str, collection: str, when: str, action_insert: bool, action_update: bool, script: str, order: int = 100):
    r_chk = requests.get(f"{url}/api/now/table/sys_script?sysparm_query=name={name}", auth=auth, headers=headers)
    existing = r_chk.json().get('result', [])
    payload = {
        "name": name,
        "collection": collection,
        "when": when,
        "action_insert": "true" if action_insert else "false",
        "action_update": "true" if action_update else "false",
        "action_delete": "false",
        "action_query": "false",
        "advanced": "true",
        "order": str(order),
        "script": script,
        "active": "true"
    }
    if existing:
        br_id = existing[0]['sys_id']
        requests.patch(f"{url}/api/now/table/sys_script/{br_id}", auth=auth, headers=headers, json=payload)
        print(f"Updated Business Rule: {name}")
    else:
        requests.post(f"{url}/api/now/table/sys_script", auth=auth, headers=headers, json=payload)
        print(f"Created Business Rule: {name}")

# ========================================================
# 1. SCRIPT INCLUDES
# ========================================================

si_customer_service = """var FNX_CustomerService = Class.create();
FNX_CustomerService.prototype = {
    initialize: function() {},

    createCustomer: function(userSysId, name, email, mobile) {
        var grCust = new GlideRecord('u_x_fnx_customer');
        grCust.addQuery('u_user', userSysId);
        grCust.query();
        if (grCust.next()) {
            return grCust.getUniqueValue();
        }

        grCust.initialize();
        grCust.setValue('u_user', userSysId);
        grCust.setValue('u_name', name);
        grCust.setValue('u_email', email);
        grCust.setValue('u_mobile', mobile);
        grCust.setValue('u_status', 'Active');
        grCust.setValue('u_kyc_status', 'Pending');
        return grCust.insert();
    },

    findCustomerByUser: function(userSysId) {
        var grCust = new GlideRecord('u_x_fnx_customer');
        grCust.addQuery('u_user', userSysId);
        grCust.query();
        if (grCust.next()) {
            return {
                sys_id: grCust.getUniqueValue(),
                customer_id: grCust.getValue('u_customer_id') || grCust.getValue('u_number'),
                name: grCust.getValue('u_name'),
                email: grCust.getValue('u_email'),
                mobile: grCust.getValue('u_mobile'),
                status: grCust.getValue('u_status'),
                kyc_status: grCust.getValue('u_kyc_status')
            };
        }
        return null;
    },

    type: 'FNX_CustomerService'
};"""

si_case_service = """var FNX_CaseService = Class.create();
FNX_CaseService.prototype = {
    initialize: function() {},

    initializeCase: function(caseGr) {
        if (!caseGr.getValue('u_source')) caseGr.setValue('u_source', 'Portal');
        if (!caseGr.getValue('u_status')) caseGr.setValue('u_status', 'New');
        if (!caseGr.getValue('u_stage')) caseGr.setValue('u_stage', 'New');
        if (!caseGr.getValue('u_reporter') && gs.getUserID()) {
            caseGr.setValue('u_reporter', gs.getUserID());
        }

        // Link customer if reporter exists
        var reporterId = caseGr.getValue('u_reporter') || gs.getUserID();
        if (reporterId && !caseGr.getValue('u_customer')) {
            var grCust = new GlideRecord('u_x_fnx_customer');
            grCust.addQuery('u_user', reporterId);
            grCust.query();
            if (grCust.next()) {
                caseGr.setValue('u_customer', grCust.getUniqueValue());
                var kyc = grCust.getValue('u_kyc_status');
                caseGr.setValue('u_customer_status', kyc === 'Verified' ? 'Known' : 'Unverified');
            } else {
                caseGr.setValue('u_customer_status', 'Unknown');
            }
        }
    },

    type: 'FNX_CaseService'
};"""

si_evidence_service = """var FNX_EvidenceService = Class.create();
FNX_EvidenceService.prototype = {
    initialize: function() {},

    createEvidence: function(caseSysId, type, desc, attachmentSysId) {
        var grEv = new GlideRecord('u_x_fnx_evidence');
        grEv.initialize();
        grEv.setValue('u_case', caseSysId);
        grEv.setValue('u_evidence_type', type || 'Document');
        grEv.setValue('u_description', desc || '');
        grEv.setValue('u_source', 'Customer');
        grEv.setValue('u_uploaded_by', gs.getUserID());
        grEv.setValue('u_uploaded_on', new GlideDateTime());
        grEv.setValue('u_processing_status', 'Uploaded');
        grEv.setValue('u_verification_status', 'Pending');
        if (attachmentSysId) {
            grEv.setValue('u_attachment', attachmentSysId);
        }
        var evId = grEv.insert();

        // Create Custody log
        var grCustody = new GlideRecord('u_x_fnx_custody_log');
        grCustody.initialize();
        grCustody.setValue('u_evidence', evId);
        grCustody.setValue('u_action', 'Uploaded');
        grCustody.setValue('u_performed_by', gs.getUserID());
        grCustody.setValue('u_timestamp', new GlideDateTime());
        grCustody.setValue('u_notes', 'Evidence uploaded by reporter');
        grCustody.insert();

        return evId;
    },

    type: 'FNX_EvidenceService'
};"""

si_audit_service = """var FNX_AuditService = Class.create();
FNX_AuditService.prototype = {
    initialize: function() {},

    logAction: function(caseSysId, recType, recId, action, field, oldVal, newVal, details) {
        var grAudit = new GlideRecord('u_x_fnx_audit');
        grAudit.initialize();
        if (caseSysId) grAudit.setValue('u_case', caseSysId);
        grAudit.setValue('u_record_type', recType || 'Case');
        grAudit.setValue('u_record_id', recId || '');
        grAudit.setValue('u_action', action || 'Update');
        grAudit.setValue('u_field', field || '');
        grAudit.setValue('u_old_value', oldVal ? String(oldVal).substring(0, 1000) : '');
        grAudit.setValue('u_new_value', newVal ? String(newVal).substring(0, 1000) : '');
        grAudit.setValue('u_performed_by', gs.getUserID());
        grAudit.setValue('u_timestamp', new GlideDateTime());
        grAudit.setValue('u_details', details || '');
        return grAudit.insert();
    },

    type: 'FNX_AuditService'
};"""

print("--- Registering Script Includes ---")
ensure_script_include("FNX_CustomerService", si_customer_service, "Manages FRAUDNEXUS customer registration and lookup")
ensure_script_include("FNX_CaseService", si_case_service, "Manages FRAUDNEXUS case initialization and lifecycle")
ensure_script_include("FNX_EvidenceService", si_evidence_service, "Manages evidence creation and chain of custody")
ensure_script_include("FNX_AuditService", si_audit_service, "Handles tamper-evident audit logging for fraud investigations")

# ========================================================
# 2. BUSINESS RULES
# ========================================================

br_001_script = """(function executeRule(current, previous /*null when async*/) {
    // Only process if user has valid email and name
    if (!current.email || !current.name) return;
    
    // Check if customer already exists for this user
    var grCust = new GlideRecord('u_x_fnx_customer');
    grCust.addQuery('u_user', current.getUniqueValue());
    grCust.query();
    if (!grCust.next()) {
        grCust.initialize();
        grCust.setValue('u_user', current.getUniqueValue());
        grCust.setValue('u_name', current.getValue('name'));
        grCust.setValue('u_email', current.getValue('email'));
        grCust.setValue('u_mobile', current.getValue('mobile_phone') || current.getValue('phone') || '');
        grCust.setValue('u_status', 'Active');
        grCust.setValue('u_kyc_status', 'Pending');
        grCust.insert();
    }
})(current, previous);"""

br_002_script = """(function executeRule(current, previous /*null when async*/) {
    if (!current.u_source) current.u_source = 'Portal';
    if (!current.u_status) current.u_status = 'New';
    if (!current.u_stage) current.u_stage = 'New';
    if (!current.u_reporter && gs.getUserID()) {
        current.u_reporter = gs.getUserID();
    }
})(current, previous);"""

br_003_script = """(function executeRule(current, previous /*null when async*/) {
    var reporterId = current.u_reporter || gs.getUserID();
    if (reporterId) {
        var grCust = new GlideRecord('u_x_fnx_customer');
        grCust.addQuery('u_user', reporterId);
        grCust.query();
        if (grCust.next()) {
            if (!current.u_customer) current.u_customer = grCust.getUniqueValue();
            var kyc = grCust.getValue('u_kyc_status');
            current.u_customer_status = (kyc === 'Verified') ? 'Known' : 'Unverified';
        } else {
            current.u_customer_status = 'Unknown';
        }
    } else {
        current.u_customer_status = 'Unknown';
    }
})(current, previous);"""

br_004_script = """(function executeRule(current, previous /*null when async*/) {
    var grCustody = new GlideRecord('u_x_fnx_custody_log');
    grCustody.initialize();
    grCustody.setValue('u_evidence', current.getUniqueValue());
    grCustody.setValue('u_action', 'Uploaded');
    grCustody.setValue('u_performed_by', gs.getUserID());
    grCustody.setValue('u_timestamp', new GlideDateTime());
    grCustody.setValue('u_notes', 'Evidence record registered');
    grCustody.insert();
})(current, previous);"""

br_005_script = """(function executeRule(current, previous /*null when async*/) {
    var grAudit = new GlideRecord('u_x_fnx_audit');
    grAudit.initialize();
    grAudit.setValue('u_case', current.getUniqueValue());
    grAudit.setValue('u_record_type', 'Case');
    grAudit.setValue('u_record_id', current.getValue('number'));
    
    if (current.isNewRecord()) {
        grAudit.setValue('u_action', 'Created');
        grAudit.setValue('u_details', 'Fraud case registered via ' + (current.getValue('u_source') || 'Portal'));
    } else {
        grAudit.setValue('u_action', 'Updated');
        grAudit.setValue('u_details', 'Status: ' + current.getValue('u_status') + ', Stage: ' + current.getValue('u_stage'));
    }
    grAudit.setValue('u_performed_by', gs.getUserID());
    grAudit.setValue('u_timestamp', new GlideDateTime());
    grAudit.insert();
})(current, previous);"""

print("\n--- Registering Business Rules ---")
ensure_business_rule("BR-FNX-001 Customer Record Creation", "sys_user", "after", True, False, br_001_script)
ensure_business_rule("BR-FNX-002 Case Initialization", "u_x_fnx_case", "before", True, False, br_002_script, 100)
ensure_business_rule("BR-FNX-003 Customer Status", "u_x_fnx_case", "before", True, False, br_003_script, 200)
ensure_business_rule("BR-FNX-004 Evidence Custody", "u_x_fnx_evidence", "after", True, False, br_004_script, 100)
ensure_business_rule("BR-FNX-005 Case Audit", "u_x_fnx_case", "after", True, True, br_005_script, 500)

print("\nAll Business Rules and Script Includes created!")
