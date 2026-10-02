import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

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
                evidence: evidenceList
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

post_script = """(function process(request, response) {
    try {
        var data = request.body.data || {};
        var userSysId = data.user_id || '';
        var custSysId = data.customer_id || '';

        // Check for Additional Evidence submission
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

        // Case creation
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
            if (data.blocked_amount) fullDesc += '\\nCustomer-Reported Blocked: ₹' + data.blocked_amount;
            if (data.recovered_amount) fullDesc += '\\nCustomer-Reported Recovered: ₹' + data.recovered_amount;
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

        // Create Evidence record if submitted
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

        // Create Audit log
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

        response.setStatus(201);
        response.setBody({
            success: true,
            case_id: newCaseSysId,
            number: caseNumber,
            status: 'New',
            submitted_on: new GlideDateTime().getDisplayValue()
        });
    } catch (e) {
        response.setStatus(500);
        response.setBody({ error: e.toString() });
    }
})(request, response);"""

# Update GET /cases operation
r_get_op = requests.get(f"{url}/api/now/table/sys_ws_operation?sysparm_query=name=case_management", auth=auth, headers=headers)
get_id = r_get_op.json()['result'][0]['sys_id']
r1 = requests.patch(f"{url}/api/now/table/sys_ws_operation/{get_id}", auth=auth, headers=headers, json={"operation_script": get_script})
print("Updated case_management (GET /cases):", r1.status_code)

# Update POST /cases operation
r_post_op = requests.get(f"{url}/api/now/table/sys_ws_operation?sysparm_query=name=case_creation", auth=auth, headers=headers)
post_id = r_post_op.json()['result'][0]['sys_id']
r2 = requests.patch(f"{url}/api/now/table/sys_ws_operation/{post_id}", auth=auth, headers=headers, json={"operation_script": post_script})
print("Updated case_creation (POST /cases):", r2.status_code)
