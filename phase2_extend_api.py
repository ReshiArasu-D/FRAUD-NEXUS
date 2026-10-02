"""
FRAUDNEXUS Phase 2 — Step 2: Extend POST /cases API
Adds transaction record creation when financial details are submitted.
PRESERVES all existing case creation, evidence, custody, and audit logic.
"""
import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv('d:/KPMG/.env')
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

# ============================================================
# Extended POST /cases script
# PRESERVES: case creation, evidence, custody, audit
# ADDS: u_x_fnx_transaction record creation
# ============================================================

post_script = """(function process(request, response) {
    try {
        var data = request.body.data || {};
        var userSysId = data.user_id || '';
        var custSysId = data.customer_id || '';

        // ====================================================
        // ADDITIONAL EVIDENCE (Phase 1 — Preserved exactly)
        // ====================================================
        if (data.action === 'add_evidence' && data.case_id) {
            var grEvAdd = new GlideRecord('u_x_fnx_evidence');
            grEvAdd.initialize();
            grEvAdd.setValue('u_case', data.case_id);
            grEvAdd.setValue('u_evidence_type', data.evidence_type || 'Document');
            grEvAdd.setValue('u_description', data.evidence_description || (data.attachment_name ? 'Attachment: ' + data.attachment_name : 'Additional customer evidence'));
            grEvAdd.setValue('u_source', 'Customer');
            if (userSysId) grEvAdd.setValue('u_uploaded_by', userSysId);
            grEvAdd.setValue('u_uploaded_on', new GlideDateTime());
            grEvAdd.setValue('u_processing_status', 'Uploaded');
            grEvAdd.setValue('u_verification_status', 'Pending');
            var addEvId = grEvAdd.insert();

            // Create Custody log
            var grCustodyAdd = new GlideRecord('u_x_fnx_custody_log');
            grCustodyAdd.initialize();
            grCustodyAdd.setValue('u_evidence', addEvId);
            grCustodyAdd.setValue('u_action', 'Uploaded');
            if (userSysId) grCustodyAdd.setValue('u_performed_by', userSysId);
            grCustodyAdd.setValue('u_timestamp', new GlideDateTime());
            grCustodyAdd.setValue('u_notes', 'Additional evidence uploaded via Customer Portal: ' + (data.evidence_type || 'Document'));
            grCustodyAdd.insert();

            // Re-read evidence number
            var addEvNum = '';
            var grEvRead = new GlideRecord('u_x_fnx_evidence');
            if (grEvRead.get(addEvId)) {
                addEvNum = grEvRead.getValue('u_number') || ('EV-' + addEvId.substring(0,6).toUpperCase());
            }

            response.setStatus(200);
            response.setBody({
                success: true,
                evidence_id: addEvId,
                evidence_number: addEvNum,
                message: 'Additional evidence attached successfully'
            });
            return;
        }

        // ====================================================
        // CASE CREATION (Phase 1 — Preserved, extended)
        // ====================================================
        var fraudType = data.type || 'Payment Fraud';
        var desc = data.description || '';
        var incDate = data.incident_date || new GlideDate().getValue();
        var incTime = data.incident_time || '';
        var location = data.location || '';
        var area = data.area || '';
        var pincode = data.pincode || '';
        var platform = data.digital_platform || '';
        var amount = data.exposure || '0';

        var fullDesc = desc;
        if (data.financial_involvement === 'Yes' || data.payment_mode || data.institution_name) {
            fullDesc += '\\n\\n--- Financial & Transaction Details ---';
            if (data.payment_mode) fullDesc += '\\nPayment Mode: ' + data.payment_mode;
            if (data.institution_name) fullDesc += '\\nInstitution / Org: ' + data.institution_name + (data.institution_type ? ' (' + data.institution_type + ')' : '');
            if (data.branch) fullDesc += '\\nBranch / Service Location: ' + data.branch;
            if (data.transaction_reference) fullDesc += '\\nTransaction Ref / UTR: ' + data.transaction_reference;
            if (data.suspect_name) fullDesc += '\\nSuspect / Beneficiary: ' + data.suspect_name;
            if (data.suspect_contact) fullDesc += '\\nSuspect Contact: ' + data.suspect_contact;
            if (data.communication_channel) fullDesc += '\\nChannel: ' + data.communication_channel;
            if (data.blocked_amount) fullDesc += '\\nCustomer-Reported Blocked: ' + data.blocked_amount;
            if (data.recovered_amount) fullDesc += '\\nCustomer-Reported Recovered: ' + data.recovered_amount;
        }

        var grCase = new GlideRecord('u_x_fnx_case');
        grCase.initialize();
        grCase.setValue('short_description', fraudType + ' Report: ' + (desc.length > 50 ? desc.substring(0, 50) + '...' : desc));
        grCase.setValue('description', fullDesc);
        grCase.setValue('u_type', fraudType);
        grCase.setValue('u_incident_date', incDate);
        grCase.setValue('u_incident_time', incTime);
        grCase.setValue('u_location', location);
        grCase.setValue('u_area', area);
        grCase.setValue('u_pincode', pincode);
        grCase.setValue('u_digital_platform', platform);
        grCase.setValue('u_exposure', amount);
        if (data.blocked_amount) grCase.setValue('u_blocked_amount', data.blocked_amount);
        if (data.recovered_amount) grCase.setValue('u_recovered_amount', data.recovered_amount);
        grCase.setValue('u_source', 'Portal');
        grCase.setValue('u_status', 'New');
        grCase.setValue('u_stage', 'New');
        grCase.setValue('u_severity', data.severity || 'Medium');
        if (userSysId) grCase.setValue('u_reporter', userSysId);
        if (custSysId) grCase.setValue('u_customer', custSysId);
        
        var newCaseSysId = grCase.insert();

        // Re-read generated number
        var caseNumber = '';
        var grRead = new GlideRecord('u_x_fnx_case');
        if (grRead.get(newCaseSysId)) {
            caseNumber = grRead.getValue('number') || ('FNX-2026-' + newCaseSysId.substring(0, 6).toUpperCase());
        }

        // ====================================================
        // PHASE 2 NEW: Create Transaction Record
        // ====================================================
        var txnSysId = '';
        if (data.financial_involvement === 'Yes' || data.payment_mode || data.institution_name || data.transaction_reference) {
            var grTxn = new GlideRecord('u_x_fnx_transaction');
            grTxn.initialize();
            grTxn.setValue('u_case', newCaseSysId);
            if (data.payment_mode) grTxn.setValue('u_payment_mode', data.payment_mode);
            if (data.institution_name) grTxn.setValue('u_institution_name', data.institution_name);
            if (data.institution_type) grTxn.setValue('u_institution_type', data.institution_type);
            if (data.branch) grTxn.setValue('u_branch', data.branch);
            if (data.platform) grTxn.setValue('u_platform', data.platform);
            if (data.reference_type) grTxn.setValue('u_reference_type', data.reference_type || 'UTR');
            if (data.transaction_reference) grTxn.setValue('u_reference_value', data.transaction_reference);
            if (data.exposure) grTxn.setValue('u_amount', data.exposure);
            grTxn.setValue('u_currency', data.currency || 'INR');
            if (data.transaction_date) grTxn.setValue('u_transaction_date', data.transaction_date);
            if (data.direction) grTxn.setValue('u_direction', data.direction);
            if (data.transaction_status) grTxn.setValue('u_transaction_status', data.transaction_status);
            if (data.number_of_transactions) grTxn.setValue('u_number_of_transactions', data.number_of_transactions);
            if (data.suspect_name) grTxn.setValue('u_suspect_name', data.suspect_name);
            if (data.suspect_contact) grTxn.setValue('u_suspect_contact', data.suspect_contact);
            if (data.suspect_identifier) grTxn.setValue('u_suspect_identifier', data.suspect_identifier);
            if (data.communication_channel) grTxn.setValue('u_communication_channel', data.communication_channel);
            grTxn.setValue('u_notes', 'Transaction reported through Customer Portal');
            if (userSysId) grTxn.setValue('u_reported_by', userSysId);
            txnSysId = grTxn.insert();
        }

        // ====================================================
        // EVIDENCE (Phase 1 — Preserved exactly)
        // ====================================================
        var evSysId = '';
        if (data.evidence_type || data.evidence_description || data.attachment_name) {
            var grEv = new GlideRecord('u_x_fnx_evidence');
            grEv.initialize();
            grEv.setValue('u_case', newCaseSysId);
            grEv.setValue('u_evidence_type', data.evidence_type || 'Document');
            grEv.setValue('u_description', data.evidence_description || (data.attachment_name ? 'Attachment: ' + data.attachment_name : 'Customer evidence submission'));
            grEv.setValue('u_source', 'Customer');
            if (userSysId) grEv.setValue('u_uploaded_by', userSysId);
            grEv.setValue('u_uploaded_on', new GlideDateTime());
            grEv.setValue('u_processing_status', 'Uploaded');
            grEv.setValue('u_verification_status', 'Pending');
            evSysId = grEv.insert();

            // Create Custody log
            var grCustody = new GlideRecord('u_x_fnx_custody_log');
            grCustody.initialize();
            grCustody.setValue('u_evidence', evSysId);
            grCustody.setValue('u_action', 'Uploaded');
            if (userSysId) grCustody.setValue('u_performed_by', userSysId);
            grCustody.setValue('u_timestamp', new GlideDateTime());
            grCustody.setValue('u_notes', 'Initial evidence uploaded via Customer Portal');
            grCustody.insert();
        }

        // ====================================================
        // AUDIT (Phase 1 — Preserved exactly)
        // ====================================================
        var grAudit = new GlideRecord('u_x_fnx_audit');
        grAudit.initialize();
        grAudit.setValue('u_case', newCaseSysId);
        grAudit.setValue('u_record_type', 'Case');
        grAudit.setValue('u_record_id', caseNumber);
        grAudit.setValue('u_action', 'Created');
        grAudit.setValue('u_details', 'Fraud case reported through Portal by user ' + (userSysId || 'anonymous'));
        if (userSysId) grAudit.setValue('u_performed_by', userSysId);
        grAudit.setValue('u_timestamp', new GlideDateTime());
        grAudit.insert();

        // ====================================================
        // RESPONSE (Extended with transaction_id)
        // ====================================================
        response.setStatus(201);
        response.setBody({
            success: true,
            case_id: newCaseSysId,
            number: caseNumber,
            status: 'New',
            transaction_id: txnSysId || '',
            submitted_on: new GlideDateTime().getDisplayValue()
        });
    } catch (e) {
        response.setStatus(500);
        response.setBody({ error: e.toString() });
    }
})(request, response);"""

# ============================================================
# Extended GET /cases script — adds transaction data to response
# ============================================================

get_script = """(function process(request, response) {
    try {
        var userSysId = '';
        if (request.queryParams && request.queryParams.user_id) {
            userSysId = String(request.queryParams.user_id);
        }

        var cases = [];
        var grCase = new GlideRecord('u_x_fnx_case');
        if (userSysId) {
            grCase.addQuery('u_reporter', userSysId);
        }
        grCase.orderByDesc('sys_created_on');
        grCase.query();
        while (grCase.next()) {
            var caseId = grCase.getUniqueValue();
            
            // Get evidence
            var grEv = new GlideRecord('u_x_fnx_evidence');
            grEv.addQuery('u_case', caseId);
            grEv.orderByDesc('sys_created_on');
            grEv.query();
            var evidenceList = [];
            while (grEv.next()) {
                evidenceList.push({
                    sys_id: grEv.getUniqueValue(),
                    number: grEv.getValue('u_number') || ('EV-' + grEv.getUniqueValue().substring(0,6).toUpperCase()),
                    type: grEv.getValue('u_evidence_type'),
                    description: grEv.getValue('u_description'),
                    uploaded_on: grEv.getValue('u_uploaded_on'),
                    status: grEv.getValue('u_verification_status') || 'Pending'
                });
            }

            // PHASE 2 NEW: Get transactions
            var transactions = [];
            var grTxn = new GlideRecord('u_x_fnx_transaction');
            grTxn.addQuery('u_case', caseId);
            grTxn.orderByDesc('sys_created_on');
            grTxn.query();
            while (grTxn.next()) {
                transactions.push({
                    sys_id: grTxn.getUniqueValue(),
                    payment_mode: grTxn.getValue('u_payment_mode') || '',
                    institution_name: grTxn.getValue('u_institution_name') || '',
                    institution_type: grTxn.getValue('u_institution_type') || '',
                    branch: grTxn.getValue('u_branch') || '',
                    platform: grTxn.getValue('u_platform') || '',
                    reference_type: grTxn.getValue('u_reference_type') || '',
                    reference_value: grTxn.getValue('u_reference_value') || '',
                    amount: grTxn.getValue('u_amount') || '0',
                    currency: grTxn.getValue('u_currency') || 'INR',
                    direction: grTxn.getValue('u_direction') || '',
                    transaction_status: grTxn.getValue('u_transaction_status') || '',
                    suspect_name: grTxn.getValue('u_suspect_name') || '',
                    suspect_contact: grTxn.getValue('u_suspect_contact') || ''
                });
            }

            cases.push({
                sys_id: caseId,
                number: grCase.getValue('number'),
                type: grCase.getValue('u_type') || 'Payment Fraud',
                description: grCase.getValue('description') || grCase.getValue('short_description'),
                status: grCase.getValue('u_status') || 'New',
                stage: grCase.getValue('u_stage') || 'New',
                severity: grCase.getValue('u_severity') || 'Medium',
                exposure: grCase.getValue('u_exposure') || '0',
                blocked_amount: grCase.getValue('u_blocked_amount') || '0',
                recovered_amount: grCase.getValue('u_recovered_amount') || '0',
                incident_date: grCase.getValue('u_incident_date'),
                incident_time: grCase.getValue('u_incident_time') || '',
                digital_platform: grCase.getValue('u_digital_platform') || '',
                location: grCase.getValue('u_location') || '',
                area: grCase.getValue('u_area') || '',
                pincode: grCase.getValue('u_pincode') || '',
                created_on: grCase.getValue('sys_created_on'),
                evidence: evidenceList,
                transactions: transactions
            });
        }

        var total = cases.length;
        var active = 0;
        var resolved = 0;
        var closed = 0;
        for (var i = 0; i < cases.length; i++) {
            var st = cases[i].status;
            if (st === 'Closed') closed++;
            else if (st === 'Resolved') resolved++;
            else active++;
        }

        response.setStatus(200);
        response.setBody({
            success: true,
            stats: { total: total, active: active, resolved: resolved, closed: closed },
            cases: cases
        });
    } catch (e) {
        response.setStatus(500);
        response.setBody({ error: e.toString() });
    }
})(request, response);"""

# ============================================================
# Deploy to ServiceNow
# ============================================================
print("=" * 60)
print("PHASE 2 — STEP 2: EXTEND REST API FOR TRANSACTIONS")
print("=" * 60)

# Update POST /cases operation
r_post_op = requests.get(
    f"{url}/api/now/table/sys_ws_operation?sysparm_query=name=case_creation",
    auth=auth, headers=headers
)
post_ops = r_post_op.json().get('result', [])
if post_ops:
    post_id = post_ops[0]['sys_id']
    r1 = requests.patch(
        f"{url}/api/now/table/sys_ws_operation/{post_id}",
        auth=auth, headers=headers,
        json={"operation_script": post_script}
    )
    print(f"Updated case_creation (POST /cases): {r1.status_code}")
else:
    print("[ERROR] case_creation operation not found!")

# Update GET /cases operation
r_get_op = requests.get(
    f"{url}/api/now/table/sys_ws_operation?sysparm_query=name=case_management",
    auth=auth, headers=headers
)
get_ops = r_get_op.json().get('result', [])
if get_ops:
    get_id = get_ops[0]['sys_id']
    r2 = requests.patch(
        f"{url}/api/now/table/sys_ws_operation/{get_id}",
        auth=auth, headers=headers,
        json={"operation_script": get_script}
    )
    print(f"Updated case_management (GET /cases): {r2.status_code}")
else:
    print("[ERROR] case_management operation not found!")

print("\n" + "=" * 60)
print("STEP 2 COMPLETE: REST API extended for transactions")
print("=" * 60)
