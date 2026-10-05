"""
Setup Admin API Endpoints for Partners Module in ServiceNow
Endpoints:
- GET /admin_partners
- POST /admin_partners
"""
import requests
import os
import json
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv('d:/KPMG/.env')
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

ws_id = "4e92fc73c36743d0e54832f1b401317d" # fnx_api

def ensure_operation(name, method, rel_path, script):
    r_chk = requests.get(
        f"{url}/api/now/table/sys_ws_operation?sysparm_query=web_service_definition={ws_id}^name={name}",
        auth=auth, headers=headers
    )
    existing = r_chk.json().get('result', [])
    payload = {
        "web_service_definition": ws_id,
        "name": name,
        "http_method": method,
        "relative_path": rel_path,
        "operation_script": script,
        "requires_authentication": "false",
        "requires_snc_internal_role": "false",
        "active": "true"
    }
    if existing:
        op_id = existing[0]['sys_id']
        r = requests.patch(f"{url}/api/now/table/sys_ws_operation/{op_id}", auth=auth, headers=headers, json=payload)
        print(f"Updated API Operation: {name} ({method} {rel_path}) -> {r.status_code}")
    else:
        r = requests.post(f"{url}/api/now/table/sys_ws_operation", auth=auth, headers=headers, json=payload)
        print(f"Created API Operation: {name} ({method} {rel_path}) -> {r.status_code}")

# ============================================================
# 1. GET /admin_partners
# ============================================================
admin_partners_get_script = """(function process(request, response) {
    try {
        var queryParams = request.queryParams || {};
        var partnerIdFilter = (queryParams.partner_id || [''])[0];
        var caseIdFilter = (queryParams.case_id || [''])[0];

        // 1. Fetch Partners
        var partners = [];
        var grP = new GlideRecord('u_x_fnx_partner');
        if (partnerIdFilter) {
            grP.addQuery('sys_id', partnerIdFilter);
        }
        grP.orderBy('u_name');
        grP.query();

        var totalPartners = 0;
        var activePartners = 0;
        var inactivePartners = 0;

        while (grP.next()) {
            totalPartners++;
            var pId = grP.getUniqueValue();
            var st = grP.getValue('u_status') || 'Active';
            if (st === 'Active') {
                activePartners++;
            } else {
                inactivePartners++;
            }

            // Count active requests for this partner
            var activeReqCount = 0;
            var totalReqCount = 0;
            var grCnt = new GlideRecord('u_x_fnx_partner_request');
            grCnt.addQuery('u_partner', pId);
            grCnt.query();
            while (grCnt.next()) {
                totalReqCount++;
                var rSt = grCnt.getValue('u_status') || '';
                if (rSt !== 'Completed' && rSt !== 'Cancelled' && rSt !== 'Rejected') {
                    activeReqCount++;
                }
            }

            partners.push({
                sys_id: pId,
                partner_number: grP.getValue('u_partner_number') || '',
                name: grP.getValue('u_name') || '',
                category: grP.getValue('u_category') || '',
                organization: grP.getValue('u_organization') || '',
                description: grP.getValue('u_description') || '',
                contact_person: grP.getValue('u_contact_person') || '',
                contact_email: grP.getValue('u_contact_email') || '',
                contact_phone: grP.getValue('u_contact_phone') || '',
                status: st,
                integration_type: grP.getValue('u_integration_type') || 'Simulated API',
                endpoint_reference: grP.getValue('u_endpoint_reference') || '',
                sla: grP.getValue('u_sla') || '4 Hours',
                demo_flag: grP.getValue('u_demo_flag') == '1' || grP.getValue('u_demo_flag') == 'true' || true,
                active: grP.getValue('u_active') == '1' || grP.getValue('u_active') == 'true',
                notes: grP.getValue('u_notes') || '',
                active_requests: activeReqCount,
                total_requests: totalReqCount,
                created_on: grP.getValue('sys_created_on') || ''
            });
        }

        // 2. Fetch Requests
        var requests = [];
        var pendingRequests = 0;
        var awaitingResponse = 0;
        var overdueRequests = 0;

        var grR = new GlideRecord('u_x_fnx_partner_request');
        if (caseIdFilter) {
            grR.addQuery('u_case', caseIdFilter);
        }
        grR.orderByDesc('sys_created_on');
        grR.query();

        while (grR.next()) {
            var rStatus = grR.getValue('u_status') || 'Draft';
            if (rStatus === 'Draft' || rStatus === 'Submitted' || rStatus === 'In Progress') {
                pendingRequests++;
            }
            if (rStatus === 'Awaiting Response') {
                awaitingResponse++;
            }
            if (rStatus === 'Overdue') {
                overdueRequests++;
            }

            var caseSysId = grR.getValue('u_case') || '';
            var caseNum = '';
            var caseTitle = '';
            if (caseSysId) {
                var grC = new GlideRecord('u_x_fnx_case');
                if (grC.get(caseSysId)) {
                    caseNum = grC.getValue('number') || grC.getValue('task_effective_number') || grC.getValue('u_number') || '';
                    caseTitle = grC.getValue('short_description') || '';
                }
            }

            var partSysId = grR.getValue('u_partner') || '';
            var partName = '';
            var partCat = '';
            var partDemo = true;
            if (partSysId) {
                var grP2 = new GlideRecord('u_x_fnx_partner');
                if (grP2.get(partSysId)) {
                    partName = grP2.getValue('u_name') || '';
                    partCat = grP2.getValue('u_category') || '';
                    partDemo = grP2.getValue('u_demo_flag') == '1' || grP2.getValue('u_demo_flag') == 'true';
                }
            }

            requests.push({
                sys_id: grR.getUniqueValue(),
                request_number: grR.getValue('u_request_number') || '',
                case_id: caseSysId,
                case_number: caseNum,
                case_title: caseTitle,
                partner_id: partSysId,
                partner_name: partName,
                partner_category: partCat,
                partner_demo: partDemo,
                request_type: grR.getValue('u_request_type') || '',
                requested_by: grR.getValue('u_requested_by') || 'Alex Morgan',
                request_date: grR.getValue('u_request_date') || grR.getValue('sys_created_on') || '',
                priority: grR.getValue('u_priority') || 'Medium',
                description: grR.getValue('u_description') || '',
                reference: grR.getValue('u_reference') || '',
                status: rStatus,
                due_date: grR.getValue('u_due_date') || '',
                response: grR.getValue('u_response') || '',
                response_date: grR.getValue('u_response_date') || '',
                resolution_notes: grR.getValue('u_resolution_notes') || '',
                demo_request: grR.getValue('u_demo_request') == '1' || grR.getValue('u_demo_request') == 'true',
                created_on: grR.getValue('sys_created_on') || ''
            });
        }

        // 3. Fetch Case Options for dropdown
        var casesList = [];
        var grCaseOpt = new GlideRecord('u_x_fnx_case');
        grCaseOpt.orderByDesc('sys_created_on');
        grCaseOpt.setLimit(50);
        grCaseOpt.query();
        while (grCaseOpt.next()) {
            casesList.push({
                sys_id: grCaseOpt.getUniqueValue(),
                number: grCaseOpt.getValue('number') || grCaseOpt.getValue('task_effective_number') || grCaseOpt.getValue('u_number') || '',
                title: grCaseOpt.getValue('short_description') || '',
                status: grCaseOpt.getValue('u_status') || 'New',
                priority: grCaseOpt.getValue('priority') || 'Medium'
            });
        }

        // 4. Fetch Recent Partner Audit History
        var recentAudit = [];
        var grAudit = new GlideRecord('u_x_fnx_audit');
        grAudit.addQuery('u_record_type', 'IN', 'Partner,Partner Request');
        grAudit.orderByDesc('sys_created_on');
        grAudit.setLimit(20);
        grAudit.query();
        while (grAudit.next()) {
            recentAudit.push({
                sys_id: grAudit.getUniqueValue(),
                action: grAudit.getValue('u_action') || '',
                record_id: grAudit.getValue('u_record_id') || '',
                record_type: grAudit.getValue('u_record_type') || '',
                details: grAudit.getValue('u_details') || '',
                timestamp: grAudit.getValue('u_timestamp') || grAudit.getValue('sys_created_on') || '',
                case_id: grAudit.getValue('u_case') || ''
            });
        }

        response.setStatus(200);
        response.setBody({
            success: true,
            kpis: {
                total_partners: totalPartners,
                active_partners: activePartners,
                inactive_partners: inactivePartners,
                pending_requests: pendingRequests,
                awaiting_response: awaitingResponse,
                overdue_requests: overdueRequests
            },
            partners: partners,
            requests: requests,
            cases: casesList,
            recent_audit: recentAudit
        });
    } catch (ex) {
        response.setStatus(500);
        response.setBody({ success: false, error: ex.message });
    }
})(request, response);"""

# ============================================================
# 2. POST /admin_partners
# ============================================================
admin_partners_post_script = """(function process(request, response) {
    try {
        var data = request.body.data || {};
        var action = data.action || '';
        var actor = data.actor || 'Alex Morgan';

        // Helper: Log to u_x_fnx_audit
        function logAudit(act, recType, recId, details, caseSysId) {
            try {
                var grA = new GlideRecord('u_x_fnx_audit');
                grA.initialize();
                grA.setValue('u_action', act);
                grA.setValue('u_record_type', recType);
                grA.setValue('u_record_id', recId);
                grA.setValue('u_details', details);
                grA.setValue('u_timestamp', new GlideDateTime());
                if (caseSysId) grA.setValue('u_case', caseSysId);
                grA.insert();
            } catch(e) {}
        }

        // Helper: Generate simulated response based on type
        function getSimulatedResponse(reqType, ref, partnerName) {
            var ts = new GlideDateTime().getDisplayValue();
            var responses = {
                'Request Transaction Information': 'SIMULATED INTEGRATION RESPONSE [' + partnerName + ']: Transaction ' + (ref || 'TXN-TRACE') + ' confirmed routed via clearing switch. Originating IP flagged in fraud velocity cluster. Beneficiary account balance restricted under protective hold. Timestamp: ' + ts,
                'Request Account Information': 'SIMULATED INTEGRATION RESPONSE [' + partnerName + ']: Account profile retrieved. Account opened 14 days prior to event; high-frequency inbound UPI transfers observed. Registered device IMEI matched with secondary suspect profile. Timestamp: ' + ts,
                'Request KYC Verification': 'SIMULATED INTEGRATION RESPONSE [' + partnerName + ']: Automated biometric face match score: 98.2%. Government ID verification passed. Document issuance location cross-checked against registered IP geofence. Timestamp: ' + ts,
                'Request Payment Trace': 'SIMULATED INTEGRATION RESPONSE [' + partnerName + ']: End-to-end trace complete. Hop 1: Wallet Gateway (Settled) -> Hop 2: Escrow Node (Frozen) -> Hop 3: Destination Account (Blocked). Recovery advisory generated. Timestamp: ' + ts,
                'Request Evidence': 'SIMULATED INTEGRATION RESPONSE [' + partnerName + ']: Certified cryptographic transaction receipt, network packet captures, and server access logs successfully packaged into encrypted evidence bundle. SHA256 checksum recorded. Timestamp: ' + ts,
                'Request Threat Intelligence': 'SIMULATED INTEGRATION RESPONSE [' + partnerName + ']: Threat Actor profile match: Syndicate "ShadowVolt". 4 active phishing domains identified and added to regional telecommunications firewall blocklist. Timestamp: ' + ts,
                'Request AML Information': 'SIMULATED INTEGRATION RESPONSE [' + partnerName + ']: Suspicious Activity Report (SAR) cross-reference positive. Matched with structuring pattern below statutory thresholds across 4 partner banks. Timestamp: ' + ts,
                'Request Regulatory Information': 'SIMULATED INTEGRATION RESPONSE [' + partnerName + ']: Regulatory incident notification acknowledged under statutory cyber-fraud reporting guidelines. Reference ticket REG-CYB-2026-9901 registered. Timestamp: ' + ts,
                'Request Investigation Assistance': 'SIMULATED INTEGRATION RESPONSE [' + partnerName + ']: Special Fraud Investigation Unit officer assigned to coordinate digital evidence preservation and formal court notice dispatch. Timestamp: ' + ts
            };
            return responses[reqType] || ('SIMULATED INTEGRATION RESPONSE [' + partnerName + ']: Request processed successfully through automated secure gateway. Timestamp: ' + ts);
        }

        // ----------------------------------------------------
        // ACTION: create_partner
        // ----------------------------------------------------
        if (action === 'create_partner') {
            var pData = data.partner || {};
            if (!pData.name || !pData.category || !pData.organization) {
                response.setStatus(400);
                response.setBody({ success: false, error: 'Partner Name, Category, and Organization are required.' });
                return;
            }

            // Generate Partner ID
            var grCnt = new GlideRecord('u_x_fnx_partner');
            grCnt.query();
            var count = grCnt.getRowCount();
            var pNumber = 'PRT-' + ('000000' + (count + 1001)).slice(-6);

            var grP = new GlideRecord('u_x_fnx_partner');
            grP.initialize();
            grP.setValue('u_partner_number', pNumber);
            grP.setValue('u_name', pData.name);
            grP.setValue('u_category', pData.category);
            grP.setValue('u_organization', pData.organization);
            grP.setValue('u_description', pData.description || '');
            grP.setValue('u_contact_person', pData.contact_person || '');
            grP.setValue('u_contact_email', pData.contact_email || '');
            grP.setValue('u_contact_phone', pData.contact_phone || '');
            grP.setValue('u_status', pData.status || 'Active');
            grP.setValue('u_integration_type', pData.integration_type || 'Simulated API');
            grP.setValue('u_endpoint_reference', pData.endpoint_reference || '');
            grP.setValue('u_sla', pData.sla || '4 Hours');
            grP.setValue('u_demo_flag', pData.demo_flag !== false);
            grP.setValue('u_active', (pData.status || 'Active') === 'Active');
            grP.setValue('u_notes', pData.notes || 'SIMULATED DEMO PARTNER');
            var newId = grP.insert();

            logAudit('Partner Created', 'Partner', pNumber, actor + ' created partner ' + pData.name + ' (' + pData.category + ')');

            response.setStatus(200);
            response.setBody({ success: true, sys_id: newId, partner_number: pNumber });
            return;
        }

        // ----------------------------------------------------
        // ACTION: update_partner
        // ----------------------------------------------------
        if (action === 'update_partner') {
            var pId = data.sys_id;
            var uData = data.partner || {};
            var grP2 = new GlideRecord('u_x_fnx_partner');
            if (!grP2.get(pId)) {
                response.setStatus(404);
                response.setBody({ success: false, error: 'Partner not found.' });
                return;
            }

            if (uData.name) grP2.setValue('u_name', uData.name);
            if (uData.category) grP2.setValue('u_category', uData.category);
            if (uData.organization) grP2.setValue('u_organization', uData.organization);
            if (uData.description !== undefined) grP2.setValue('u_description', uData.description);
            if (uData.contact_person !== undefined) grP2.setValue('u_contact_person', uData.contact_person);
            if (uData.contact_email !== undefined) grP2.setValue('u_contact_email', uData.contact_email);
            if (uData.contact_phone !== undefined) grP2.setValue('u_contact_phone', uData.contact_phone);
            if (uData.status) {
                grP2.setValue('u_status', uData.status);
                grP2.setValue('u_active', uData.status === 'Active');
            }
            if (uData.integration_type) grP2.setValue('u_integration_type', uData.integration_type);
            if (uData.endpoint_reference !== undefined) grP2.setValue('u_endpoint_reference', uData.endpoint_reference);
            if (uData.sla) grP2.setValue('u_sla', uData.sla);
            if (uData.notes !== undefined) grP2.setValue('u_notes', uData.notes);
            grP2.update();

            var pNum = grP2.getValue('u_partner_number') || grP2.getValue('u_name');
            logAudit('Partner Updated', 'Partner', pNum, actor + ' updated partner details for ' + grP2.getValue('u_name'));

            response.setStatus(200);
            response.setBody({ success: true });
            return;
        }

        // ----------------------------------------------------
        // ACTION: set_status (Active / Inactive / Suspended)
        // ----------------------------------------------------
        if (action === 'set_status') {
            var stId = data.sys_id;
            var newStatus = data.status; // 'Active', 'Inactive', 'Suspended'
            var grSt = new GlideRecord('u_x_fnx_partner');
            if (!grSt.get(stId)) {
                response.setStatus(404);
                response.setBody({ success: false, error: 'Partner not found.' });
                return;
            }

            grSt.setValue('u_status', newStatus);
            grSt.setValue('u_active', newStatus === 'Active');
            grSt.update();

            var actLabel = newStatus === 'Active' ? 'Partner Reactivated' : 'Partner Deactivated';
            logAudit(actLabel, 'Partner', grSt.getValue('u_partner_number') || '', actor + ' changed partner status to ' + newStatus);

            response.setStatus(200);
            response.setBody({ success: true, status: newStatus });
            return;
        }

        // ----------------------------------------------------
        // ACTION: delete_partner (SAFE REMOVAL CHECK)
        // ----------------------------------------------------
        if (action === 'delete_partner') {
            var delId = data.sys_id;
            var grDel = new GlideRecord('u_x_fnx_partner');
            if (!grDel.get(delId)) {
                response.setStatus(404);
                response.setBody({ success: false, error: 'Partner not found.' });
                return;
            }

            // CRITICAL CHECK: Check if referenced by existing partner requests
            var grChkRef = new GlideRecord('u_x_fnx_partner_request');
            grChkRef.addQuery('u_partner', delId);
            grChkRef.query();
            if (grChkRef.hasNext()) {
                var refCount = grChkRef.getRowCount();
                response.setStatus(200); // Return 200 with blocked flag for friendly UI handling
                response.setBody({
                    success: false,
                    blocked: true,
                    reference_count: refCount,
                    message: 'Partner is referenced by existing records. Deactivate the partner instead of deleting it.'
                });
                return;
            }

            var delNum = grDel.getValue('u_partner_number') || '';
            var delName = grDel.getValue('u_name') || '';
            grDel.deleteRecord();

            logAudit('Partner Removed', 'Partner', delNum, actor + ' safely removed unreferenced partner ' + delName);

            response.setStatus(200);
            response.setBody({ success: true, message: 'Partner removed successfully.' });
            return;
        }

        // ----------------------------------------------------
        // ACTION: create_request
        // ----------------------------------------------------
        if (action === 'create_request') {
            var reqData = data.request || {};
            if (!reqData.partner_id || !reqData.case_id || !reqData.request_type) {
                response.setStatus(400);
                response.setBody({ success: false, error: 'Partner, Case, and Request Type are required.' });
                return;
            }

            // Generate Request Number
            var grReqCnt = new GlideRecord('u_x_fnx_partner_request');
            grReqCnt.query();
            var rCount = grReqCnt.getRowCount();
            var reqNumber = 'PRTREQ-' + ('000000' + (rCount + 1001)).slice(-6);

            var grPRef = new GlideRecord('u_x_fnx_partner');
            var partName = '';
            var partIntType = 'Simulated API';
            if (grPRef.get(reqData.partner_id)) {
                partName = grPRef.getValue('u_name') || '';
                partIntType = grPRef.getValue('u_integration_type') || 'Simulated API';
            }

            var grReq = new GlideRecord('u_x_fnx_partner_request');
            grReq.initialize();
            grReq.setValue('u_request_number', reqNumber);
            grReq.setValue('u_case', reqData.case_id);
            grReq.setValue('u_partner', reqData.partner_id);
            grReq.setValue('u_request_type', reqData.request_type);
            grReq.setValue('u_requested_by', actor);
            grReq.setValue('u_request_date', new GlideDateTime());
            grReq.setValue('u_priority', reqData.priority || 'High');
            grReq.setValue('u_description', reqData.description || '');
            grReq.setValue('u_reference', reqData.reference || '');
            grReq.setValue('u_demo_request', true);

            var autoSimulate = reqData.simulate !== false; // default true for demo
            if (autoSimulate) {
                grReq.setValue('u_status', 'Response Received');
                var simResp = getSimulatedResponse(reqData.request_type, reqData.reference, partName);
                grReq.setValue('u_response', simResp);
                grReq.setValue('u_response_date', new GlideDateTime());
                grReq.setValue('u_resolution_notes', 'Automated simulated partner verification workflow completed successfully.');
            } else {
                grReq.setValue('u_status', 'Submitted');
            }

            var newReqId = grReq.insert();

            // Log Audit
            logAudit('Partner Request Created', 'Partner Request', reqNumber, actor + ' created partner request to ' + partName + ' (' + reqData.request_type + ')', reqData.case_id);
            if (autoSimulate) {
                logAudit('Partner Response Received', 'Partner Request', reqNumber, 'Simulated integration response received from ' + partName, reqData.case_id);
            }

            // Update Case Timeline / Work notes
            try {
                var grCUpdate = new GlideRecord('u_x_fnx_case');
                if (grCUpdate.get(reqData.case_id)) {
                    var note = '\\n[PARTNER COORDINATION] ' + reqNumber + ' dispatched to ' + partName + ' (' + reqData.request_type + '). Priority: ' + (reqData.priority || 'High') + '.';
                    if (autoSimulate) {
                        note += '\\n[PARTNER RESPONSE] ' + grReq.getValue('u_response');
                    }
                    var curDesc = grCUpdate.getValue('description') || '';
                    grCUpdate.setValue('description', curDesc + note);
                    grCUpdate.update();
                }
            } catch(e) {}

            response.setStatus(200);
            response.setBody({
                success: true,
                sys_id: newReqId,
                request_number: reqNumber,
                status: autoSimulate ? 'Response Received' : 'Submitted'
            });
            return;
        }

        // ----------------------------------------------------
        // ACTION: simulate_response (on existing request)
        // ----------------------------------------------------
        if (action === 'simulate_response') {
            var simReqId = data.sys_id;
            var grSimReq = new GlideRecord('u_x_fnx_partner_request');
            if (!grSimReq.get(simReqId)) {
                response.setStatus(404);
                response.setBody({ success: false, error: 'Partner Request not found.' });
                return;
            }

            var pName2 = '';
            var grP3 = new GlideRecord('u_x_fnx_partner');
            if (grP3.get(grSimReq.getValue('u_partner'))) {
                pName2 = grP3.getValue('u_name') || 'Partner';
            }

            var simText = getSimulatedResponse(grSimReq.getValue('u_request_type'), grSimReq.getValue('u_reference'), pName2);
            grSimReq.setValue('u_status', 'Response Received');
            grSimReq.setValue('u_response', simText);
            grSimReq.setValue('u_response_date', new GlideDateTime());
            grSimReq.setValue('u_resolution_notes', 'Simulated partner response received and verified by investigator.');
            grSimReq.update();

            var rNum2 = grSimReq.getValue('u_request_number') || '';
            var cId2 = grSimReq.getValue('u_case') || '';
            logAudit('Partner Response Received', 'Partner Request', rNum2, 'Simulated integration response received from ' + pName2, cId2);

            response.setStatus(200);
            response.setBody({ success: true, response: simText, status: 'Response Received' });
            return;
        }

        // ----------------------------------------------------
        // ACTION: update_request_status
        // ----------------------------------------------------
        if (action === 'update_request_status') {
            var upReqId = data.sys_id;
            var reqStatus = data.status;
            var resNotes = data.resolution_notes;

            var grUpReq = new GlideRecord('u_x_fnx_partner_request');
            if (!grUpReq.get(upReqId)) {
                response.setStatus(404);
                response.setBody({ success: false, error: 'Partner Request not found.' });
                return;
            }

            if (reqStatus) grUpReq.setValue('u_status', reqStatus);
            if (resNotes !== undefined) grUpReq.setValue('u_resolution_notes', resNotes);
            grUpReq.update();

            logAudit('Partner Request ' + reqStatus, 'Partner Request', grUpReq.getValue('u_request_number') || '', actor + ' updated request status to ' + reqStatus, grUpReq.getValue('u_case'));

            response.setStatus(200);
            response.setBody({ success: true, status: reqStatus });
            return;
        }

        response.setStatus(400);
        response.setBody({ success: false, error: 'Unknown action: ' + action });
    } catch(ex) {
        response.setStatus(500);
        response.setBody({ success: false, error: ex.message });
    }
})(request, response);"""

print("--- Registering Partner Scripted REST Operations ---")
ensure_operation("admin_partners_get", "GET", "/admin_partners", admin_partners_get_script)
ensure_operation("admin_partners_post", "POST", "/admin_partners", admin_partners_post_script)
print("Partner API Operations Registered Successfully!")
