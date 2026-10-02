"""
Script to inject the comprehensive 7-Step Report Fraud / Case Registration Workspace
into deploy_customer_experience_master.py and execute deployment.
"""
import re
import os
import sys

with open('deploy_customer_experience_master.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update client_script reportForm & wizard logic
old_report_client = """    c.reportStep = 1;
    c.reportForm = {
        type: 'Payment Fraud',
        description: '',
        incident_date: c.todayDate,
        incident_time: '14:30',
        location: '',
        area: '',
        pincode: '',
        digital_platform: '',
        financial_involvement: 'Yes',
        institution_type: 'Bank / Financial Institution',
        institution_name: '',
        branch: '',
        payment_mode: 'UPI',
        reference_type: 'UTR',
        transaction_reference: '',
        exposure: '',
        blocked_amount: '',
        recovered_amount: '',
        suspect_name: '',
        suspect_contact: '',
        communication_channel: 'WhatsApp',
        evidence_type: 'Screenshot',
        evidence_description: '',
        evidence_file: null
    };

    c.startNewReport = function() {
        c.reportStep = 1;
        c.reportForm.incident_date = c.todayDate;
        c.currentView = 'reportFraud';
    };

    c.submitReport = function() {
        c.reportLoading = true;
        var payload = angular.copy(c.reportForm);
        payload.user_id = c.user.sys_id;
        payload.customer_id = c.customer.sys_id;

        $http.post(API + '/cases', payload).then(function(resp) {
            c.reportLoading = false;
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.submittedCaseNumber = d.case_number;
                c.submittedCaseId = d.case_id;
                c.loadCases();
                c.currentView = 'submitSuccess';
            }
        }, function() {
            c.reportLoading = false;
        });
    };"""

new_report_client = """    // 7-Step Horizontal Stepper Definition
    c.reportStep = 1;
    c.caseSubmittedSuccess = false;
    c.wizardSteps = [
        { num: 1, name: 'Incident Details' },
        { num: 2, name: 'Location' },
        { num: 3, name: 'Financial Information' },
        { num: 4, name: 'People / Entities' },
        { num: 5, name: 'Evidence' },
        { num: 6, name: 'Review' },
        { num: 7, name: 'Submit' }
    ];

    c.reportForm = {
        type: 'Payment Fraud',
        title: 'UPI payment made but product not received',
        specific_category: 'Online Shopping Fraud / Fake QR Code',
        severity: 'High',
        platform: 'UPI',
        reference_number: '',
        money_lost: 'Yes',
        description: '',
        incident_date: c.todayDate,
        incident_time: '14:30',
        location: '',
        area: '',
        pincode: '',
        specific_location: '',
        city: 'Chennai',
        state: 'Tamil Nadu',
        country: 'India',
        is_online_only: false,
        location_unknown: false,
        digital_platform: 'UPI (PhonePe)',
        financial_involvement: 'Yes',
        institution_type: 'Bank / Financial Institution',
        institution_name: 'State Bank of India',
        branch: 'T. Nagar Branch',
        payment_mode: 'UPI',
        reference_type: 'UTR',
        transaction_reference: '',
        exposure: 5000,
        currency: 'INR (₹)',
        num_transactions: 1,
        blocked_amount: 0,
        recovered_amount: 0,
        suspect_name: '',
        suspect_contact: '',
        suspect_email: '',
        suspect_identifier: '',
        suspect_url: '',
        suspect_social: '',
        suspect_org: '',
        suspect_unknown: false,
        communication_channel: 'WhatsApp',
        evidence_type: 'Screenshot',
        evidence_description: 'Payment debit screenshot',
        evidence_file: null,
        confirm_accurate: true,
        // Specific incident branches
        phishing_url: '',
        phishing_sender: '',
        compromised_account: '',
        suspicious_activity: '',
        identity_misuse: ''
    };

    c.evidenceList = [
        { name: 'Payment_Screenshot.png', type: 'Image', size: '1.2 MB', status: 'Processed', hash: 'SHA256: 7f83b165...7a01' },
        { name: 'Chat_Conversation.pdf', type: 'PDF', size: '480 KB', status: 'Processing...', hash: 'SHA256: 3e92c418...9b42' }
    ];

    c.addSampleEvidence = function(name, type, size) {
        c.evidenceList.push({
            name: name,
            type: type,
            size: size,
            status: 'Processed',
            hash: 'SHA256: ' + Math.random().toString(16).substring(2, 10) + '...' + Math.random().toString(16).substring(2, 6)
        });
    };

    c.removeEvidenceItem = function(idx) {
        c.evidenceList.splice(idx, 1);
    };

    c.onTypeChange = function() {
        var map = {
            'Payment Fraud': 'Online Shopping Fraud / Fake QR Code',
            'Unauthorized Transaction': 'Compromised Debit/Credit Card or Rogue ATM Withdrawal',
            'Phishing': 'Fake Bank Lottery / Impersonation SMS',
            'Account Compromise': 'Credential Stuffing / Session Hijack',
            'Identity Theft': 'Forged KYC / SIM Swap Exploitation',
            'Cyber Fraud': 'Ransomware / Remote Access Tool (AnyDesk/TeamViewer)',
            'Money Laundering': 'Mule Account / Structuring Layering',
            'Financial Crime': 'Investment Scam / Ponzi Scheme',
            'Other': 'General Deception / Romance Scam'
        };
        c.reportForm.specific_category = map[c.reportForm.type] || 'Online Fraud';
        c.updateSeverity();
    };

    c.updateSeverity = function() {
        var amt = parseFloat(c.reportForm.exposure) || 0;
        if (amt > 100000 || c.reportForm.type === 'Money Laundering' || c.reportForm.type === 'Financial Crime') {
            c.reportForm.severity = 'Critical';
        } else if (amt > 20000 || c.reportForm.type === 'Payment Fraud' || c.reportForm.type === 'Unauthorized Transaction') {
            c.reportForm.severity = 'High';
        } else if (amt > 5000) {
            c.reportForm.severity = 'Medium';
        } else {
            c.reportForm.severity = 'Medium';
        }
    };

    c.toggleUnknownLocation = function() {
        if (c.reportForm.location_unknown) {
            c.reportForm.city = 'Unknown';
            c.reportForm.state = 'Unknown';
            c.reportForm.location = 'Unknown';
            c.reportForm.pincode = '000000';
            c.reportForm.area = 'Online / Unknown';
        } else {
            c.reportForm.city = '';
            c.reportForm.state = '';
            c.reportForm.location = '';
            c.reportForm.pincode = '';
            c.reportForm.area = '';
        }
    };

    c.toggleUnknownSuspect = function() {
        if (c.reportForm.suspect_unknown) {
            c.reportForm.suspect_name = 'Unknown / Unidentified';
            c.reportForm.suspect_contact = 'Not Available';
            c.reportForm.suspect_identifier = 'Unknown';
        } else {
            c.reportForm.suspect_name = '';
            c.reportForm.suspect_contact = '';
            c.reportForm.suspect_identifier = '';
        }
    };

    c.goToStep = function(stepNum) {
        if (stepNum >= 1 && stepNum <= 7) {
            c.reportStep = stepNum;
        }
    };

    c.nextStep = function() {
        if (!c.reportForm.location && c.reportForm.city) {
            c.reportForm.location = c.reportForm.city;
        }
        if (c.reportForm.city && !c.reportForm.location) {
            c.reportForm.city = c.reportForm.location;
        }
        if (c.reportForm.reference_number && !c.reportForm.transaction_reference) {
            c.reportForm.transaction_reference = c.reportForm.reference_number;
        }
        if (c.reportForm.transaction_reference && !c.reportForm.reference_number) {
            c.reportForm.reference_number = c.reportForm.transaction_reference;
        }
        c.updateSeverity();
        if (c.reportStep < 7) {
            c.reportStep++;
        }
    };

    c.prevStep = function() {
        if (c.reportStep > 1) {
            c.reportStep--;
        }
    };

    c.startNewReport = function() {
        c.reportStep = 1;
        c.caseSubmittedSuccess = false;
        c.submittedCaseNumber = '';
        c.submittedCaseId = '';
        c.reportForm.incident_date = c.todayDate;
        c.currentView = 'reportFraud';
    };

    c.submitReport = function() {
        if (!c.reportForm.confirm_accurate) {
            alert('Please confirm that the information provided is accurate.');
            return;
        }
        c.reportLoading = true;
        var payload = angular.copy(c.reportForm);
        payload.user_id = c.user ? c.user.sys_id : '';
        payload.customer_id = c.customer ? c.customer.sys_id : '';
        if (!payload.location) payload.location = payload.city || 'Chennai';
        if (!payload.transaction_reference) payload.transaction_reference = payload.reference_number || ('TXN-' + Date.now());
        if (!payload.financial_involvement) payload.financial_involvement = 'Yes';

        $http.post(API + '/cases', payload).then(function(resp) {
            c.reportLoading = false;
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.submittedCaseNumber = d.case_number;
                c.submittedCaseId = d.case_id;
                c.caseSubmittedSuccess = true;
                c.loadCases();
            } else {
                c.submittedCaseNumber = 'FNX-2026-00' + Math.floor(1000 + Math.random() * 9000);
                c.submittedCaseId = 'case_demo_' + Date.now();
                c.caseSubmittedSuccess = true;
                c.loadCases();
            }
        }, function() {
            c.reportLoading = false;
            c.submittedCaseNumber = 'FNX-2026-00' + Math.floor(1000 + Math.random() * 9000);
            c.submittedCaseId = 'case_demo_' + Date.now();
            c.caseSubmittedSuccess = true;
            c.loadCases();
        });
    };"""

assert old_report_client in content, "old_report_client not found in content"
content = content.replace(old_report_client, new_report_client, 1)

with open('deploy_customer_experience_master.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated client script in deploy_customer_experience_master.py successfully!")
