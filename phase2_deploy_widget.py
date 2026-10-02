"""
FRAUDNEXUS Phase 2 - Step 4: Complete Customer Experience Widget
Updates the fnx_customer_experience Service Portal widget with full UI.
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

WIDGET_ID = "2f258577c32b43d0e54832f1b401317f"

# ============================================================
# SERVER SCRIPT - Provides data to the widget
# ============================================================
server_script = """(function() {
    data.apiBase = gs.getProperty('glide.servlet.uri') + 'api/2229367/fnx_api';
    data.instanceUrl = gs.getProperty('glide.servlet.uri');
})();"""

# ============================================================
# CLIENT SCRIPT - AngularJS controller
# ============================================================
client_script = r"""api.controller = function($scope, $http, $timeout, $window) {
    var c = this;
    var API = '/api/2229367/fnx_api';

    // ========== STATE ==========
    c.currentView = 'landing';
    c.authMode = 'login';
    c.user = null;
    c.customer = null;
    c.cases = [];
    c.stats = { total: 0, active: 0, resolved: 0, closed: 0 };
    c.selectedCase = null;
    c.showAI = false;
    c.aiMessages = [];
    c.aiInput = '';
    c.showNotifications = false;
    c.notifications = [];
    c.lang = 'en';
    c.sidebarCollapsed = false;

    // ========== LANGUAGE ==========
    c.dict = {
        en: {
            brand: 'FRAUDNEXUS',
            tagline: 'Financial & Cyber Fraud Investigation Hub',
            heroTitle: 'From Fraud Report to Resolution',
            heroSub: 'One Intelligent Investigation Workspace',
            heroDesc: 'Report fraud securely, track your cases in real-time, submit evidence with full chain of custody, and get intelligent assistance throughout your investigation journey.',
            getStarted: 'Get Started',
            learnMore: 'Learn More',
            customerPortal: 'Customer Portal',
            customerPortalDesc: 'Report fraud, track cases, submit evidence, receive updates, and get help.',
            investigatorPortal: 'Investigator / Admin Portal',
            investigatorPortalDesc: 'Investigate cases, analyze intelligence, manage compliance, and generate reports.',
            enterPortal: 'Enter Portal',
            comingSoon: 'Coming Soon',
            login: 'Login',
            register: 'Register',
            email: 'Email Address',
            password: 'Password',
            confirmPassword: 'Confirm Password',
            fullName: 'Full Name',
            mobile: 'Mobile Number',
            forgotPassword: 'Forgot Password?',
            noAccount: "Don't have an account?",
            hasAccount: 'Already have an account?',
            dashboard: 'Dashboard',
            reportFraud: 'Report Fraud',
            trackCases: 'Track Cases',
            evidence: 'Evidence Vault',
            helpSupport: 'Help & Support',
            welcome: 'Welcome',
            totalCases: 'Total Cases',
            activeCases: 'Active Cases',
            resolvedCases: 'Resolved Cases',
            recentCases: 'Recent Cases',
            caseId: 'Case ID',
            incidentType: 'Incident Type',
            date: 'Date',
            severity: 'Severity',
            status: 'Status',
            viewCase: 'View',
            noCases: 'No cases found. Report a fraud to get started.',
            whatHappened: 'What happened?',
            describeIncident: 'Describe the incident in detail...',
            incidentDate: 'Incident Date',
            incidentTime: 'Incident Time (optional)',
            financialInvolvement: 'Was there financial involvement?',
            yes: 'Yes',
            no: 'No',
            notSure: "I'm not sure",
            paymentMode: 'Payment / Activity Mode',
            institution: 'Institution / Organization',
            institutionType: 'Institution Type',
            branch: 'Branch / Service Location',
            referenceType: 'Reference Type',
            referenceValue: 'Reference Value',
            amountInvolved: 'Amount Involved / Lost',
            currency: 'Currency',
            suspectName: 'Suspect / Beneficiary Name',
            suspectContact: 'Suspect Contact (Phone/Email/UPI)',
            channel: 'Communication Channel',
            location: 'Location',
            area: 'Area',
            pincode: 'Pincode',
            digitalPlatform: 'Digital Platform / App / Website',
            evidenceType: 'Evidence Type',
            evidenceDesc: 'Evidence Description',
            next: 'Next',
            back: 'Back',
            review: 'Review & Submit',
            submit: 'Submit Report',
            submitting: 'Submitting...',
            addEvidence: 'Add Evidence',
            caseTimeline: 'Case Timeline',
            submitted: 'Submitted',
            initialReview: 'Initial Review',
            investigation: 'Investigation',
            resolution: 'Resolution',
            closed: 'Closed',
            fraudAwareness: 'Fraud Awareness',
            phishing: 'Phishing',
            paymentFraud: 'Payment Fraud',
            accountSecurity: 'Account Security',
            identityTheft: 'Identity Theft',
            askAI: 'Ask FRAUDNEXUS AI',
            aiPlaceholder: 'Ask me anything about fraud reporting...',
            logout: 'Logout',
            profile: 'Profile',
            selectLanguage: 'Language',
            caseSubmitted: 'Fraud Report Submitted Successfully!',
            yourCaseId: 'Your Case ID',
            trackYourCase: 'Track Your Case',
            reportAnother: 'Report Another',
            selectType: 'Select Incident Type',
            step: 'Step'
        },
        ta: {
            brand: 'FRAUDNEXUS',
            tagline: 'நிதி & சைபர் மோசடி புலனாய்வு மையம்',
            heroTitle: 'மோசடி புகாரிலிருந்து தீர்வு வரை',
            heroSub: 'ஒரு புத்திசாலி புலனாய்வு பணிநிலையம்',
            heroDesc: 'மோசடியைப் பாதுகாப்பாகப் புகாரளியுங்கள், உங்கள் வழக்குகளை நிகழ்நேரத்தில் கண்காணியுங்கள், முழு சங்கிலி காவலுடன் ஆதாரங்களைச் சமர்ப்பியுங்கள்.',
            getStarted: 'தொடங்கு',
            learnMore: 'மேலும் அறிக',
            customerPortal: 'வாடிக்கையாளர் போர்டல்',
            customerPortalDesc: 'மோசடியைப் புகாரளியுங்கள், வழக்குகளைக் கண்காணியுங்கள், ஆதாரங்களைச் சமர்ப்பியுங்கள்.',
            investigatorPortal: 'புலனாய்வாளர் / நிர்வாக போர்டல்',
            investigatorPortalDesc: 'வழக்குகளை புலனாய்வு செய்யுங்கள், புலனாய்வு நிர்வகியுங்கள்.',
            enterPortal: 'போர்டலுக்குள் நுழை',
            comingSoon: 'விரைவில்',
            login: 'உள்நுழை',
            register: 'பதிவு',
            email: 'மின்னஞ்சல்',
            password: 'கடவுச்சொல்',
            confirmPassword: 'கடவுச்சொல்லை உறுதிப்படுத்தவும்',
            fullName: 'முழு பெயர்',
            mobile: 'மொபைல் எண்',
            forgotPassword: 'கடவுச்சொல் மறந்துவிட்டதா?',
            noAccount: 'கணக்கு இல்லையா?',
            hasAccount: 'ஏற்கனவே கணக்கு உள்ளதா?',
            dashboard: 'டேஷ்போர்டு',
            reportFraud: 'மோசடி புகார்',
            trackCases: 'வழக்கு கண்காணிப்பு',
            evidence: 'ஆதார காப்பகம்',
            helpSupport: 'உதவி & ஆதரவு',
            welcome: 'வரவேற்கிறோம்',
            totalCases: 'மொத்த வழக்குகள்',
            activeCases: 'செயலில் உள்ள வழக்குகள்',
            resolvedCases: 'தீர்க்கப்பட்ட வழக்குகள்',
            recentCases: 'சமீபத்திய வழக்குகள்',
            caseId: 'வழக்கு எண்',
            incidentType: 'சம்பவ வகை',
            date: 'தேதி',
            severity: 'தீவிரம்',
            status: 'நிலை',
            viewCase: 'காண்க',
            noCases: 'வழக்குகள் இல்லை. மோசடியைப் புகாரளியுங்கள்.',
            whatHappened: 'என்ன நடந்தது?',
            describeIncident: 'சம்பவத்தை விரிவாக விவரிக்கவும்...',
            incidentDate: 'சம்பவ தேதி',
            incidentTime: 'சம்பவ நேரம் (விருப்பம்)',
            financialInvolvement: 'நிதி சம்பந்தம் இருந்ததா?',
            yes: 'ஆம்',
            no: 'இல்லை',
            notSure: 'எனக்கு தெரியவில்லை',
            paymentMode: 'கட்டண முறை',
            institution: 'நிறுவனம்',
            institutionType: 'நிறுவன வகை',
            branch: 'கிளை / சேவை இடம்',
            referenceType: 'குறிப்பு வகை',
            referenceValue: 'குறிப்பு மதிப்பு',
            amountInvolved: 'தொகை',
            currency: 'நாணயம்',
            suspectName: 'சந்தேக நபர் பெயர்',
            suspectContact: 'சந்தேக நபர் தொடர்பு',
            channel: 'தொடர்பு சேனல்',
            location: 'இடம்',
            area: 'பகுதி',
            pincode: 'அஞ்சல் குறியீடு',
            digitalPlatform: 'டிஜிட்டல் தளம்',
            evidenceType: 'ஆதார வகை',
            evidenceDesc: 'ஆதார விவரம்',
            next: 'அடுத்து',
            back: 'பின்',
            review: 'சரிபார்த்து சமர்ப்பிக்கவும்',
            submit: 'புகார் சமர்ப்பி',
            submitting: 'சமர்ப்பிக்கிறது...',
            addEvidence: 'ஆதாரம் சேர்',
            caseTimeline: 'வழக்கு காலவரிசை',
            submitted: 'சமர்ப்பிக்கப்பட்டது',
            initialReview: 'ஆரம்ப மதிப்பாய்வு',
            investigation: 'புலனாய்வு',
            resolution: 'தீர்வு',
            closed: 'மூடப்பட்டது',
            fraudAwareness: 'மோசடி விழிப்புணர்வு',
            phishing: 'ஃபிஷிங்',
            paymentFraud: 'கட்டண மோசடி',
            accountSecurity: 'கணக்கு பாதுகாப்பு',
            identityTheft: 'அடையாள திருட்டு',
            askAI: 'FRAUDNEXUS AI கேளுங்கள்',
            aiPlaceholder: 'மோசடி புகாரைப் பற்றி என்னிடம் கேளுங்கள்...',
            logout: 'வெளியேறு',
            profile: 'சுயவிவரம்',
            selectLanguage: 'மொழி',
            caseSubmitted: 'மோசடி புகார் வெற்றிகரமாக சமர்ப்பிக்கப்பட்டது!',
            yourCaseId: 'உங்கள் வழக்கு எண்',
            trackYourCase: 'உங்கள் வழக்கைக் கண்காணியுங்கள்',
            reportAnother: 'மற்றொன்று புகாரளியுங்கள்',
            selectType: 'சம்பவ வகையைத் தேர்ந்தெடுக்கவும்',
            step: 'படி'
        }
    };

    c.t = function(key) {
        return (c.dict[c.lang] && c.dict[c.lang][key]) || (c.dict['en'] && c.dict['en'][key]) || key;
    };

    c.toggleLang = function() {
        c.lang = c.lang === 'en' ? 'ta' : 'en';
    };

    // ========== FRAUD TYPES ==========
    c.fraudTypes = [
        'Payment Fraud', 'Unauthorized Transaction', 'Phishing',
        'Account Compromise', 'Identity Theft', 'Cyber Fraud',
        'Money Laundering', 'Financial Crime', 'Other'
    ];

    c.paymentModes = [
        'UPI', 'Bank Transfer', 'IMPS', 'NEFT', 'RTGS',
        'Debit Card', 'Credit Card', 'ATM / Cash Withdrawal',
        'Net Banking', 'Mobile Banking', 'Digital Wallet',
        'QR Code Payment', 'Payment Gateway', 'Cash', 'Cheque',
        'Demand Draft', 'Investment / Trading', 'Insurance',
        'Loan / Lending', 'E-commerce / Merchant Payment',
        'International Transfer', 'Other', "I don't know"
    ];

    c.institutionTypes = [
        'Bank / Financial Institution', 'Payment Provider',
        'Payment Application', 'Insurance',
        'Investment / Brokerage', 'Lending / NBFC',
        'E-commerce / Merchant', 'Telecom', 'Other'
    ];

    c.referenceTypes = [
        'UTR', 'Transaction ID', 'Payment Reference', 'Order ID',
        'Cheque Reference', 'Policy Reference', 'Claim Reference',
        'Loan Application ID', 'Investment Order ID', 'Other'
    ];

    c.evidenceTypes = [
        'Image', 'Video', 'Audio', 'PDF', 'Document',
        'Spreadsheet', 'Email', 'Chat Export', 'Text',
        'URL', 'Transaction Reference', 'Other'
    ];

    // ========== REPORT WIZARD STATE ==========
    c.wizardStep = 1;
    c.totalSteps = 7;
    c.report = {
        type: '',
        description: '',
        incident_date: '',
        incident_time: '',
        financial_involvement: '',
        payment_mode: '',
        institution_name: '',
        institution_type: '',
        branch: '',
        reference_type: 'UTR',
        transaction_reference: '',
        exposure: '',
        currency: 'INR',
        blocked_amount: '',
        recovered_amount: '',
        suspect_name: '',
        suspect_contact: '',
        communication_channel: '',
        location: '',
        area: '',
        pincode: '',
        digital_platform: '',
        evidence_type: '',
        evidence_description: ''
    };
    c.submitResult = null;
    c.isSubmitting = false;

    // ========== AUTH ==========
    c.authForm = { name: '', email: '', mobile: '', password: '', confirmPassword: '' };
    c.authError = '';
    c.authLoading = false;

    c.doLogin = function() {
        c.authError = '';
        c.authLoading = true;
        $http.post(API + '/login', { email: c.authForm.email, password: c.authForm.password })
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.user = d.user;
                c.customer = d.customer;
                c.loadCases();
                c.currentView = 'dashboard';
            } else {
                c.authError = d.error || 'Login failed.';
            }
            c.authLoading = false;
        }, function(err) {
            c.authError = (err.data && err.data.result && err.data.result.error) || 'Login failed. Please try again.';
            c.authLoading = false;
        });
    };

    c.doRegister = function() {
        c.authError = '';
        if (c.authForm.password !== c.authForm.confirmPassword) {
            c.authError = 'Passwords do not match.';
            return;
        }
        c.authLoading = true;
        $http.post(API + '/register', {
            name: c.authForm.name, email: c.authForm.email,
            mobile: c.authForm.mobile, password: c.authForm.password
        }).then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.user = { sys_id: d.user_id, name: d.name, email: d.email };
                c.customer = { customer_id: d.customer_id };
                c.loadCases();
                c.currentView = 'dashboard';
            } else {
                c.authError = d.error || 'Registration failed.';
            }
            c.authLoading = false;
        }, function(err) {
            c.authError = (err.data && err.data.result && err.data.result.error) || 'Registration failed.';
            c.authLoading = false;
        });
    };

    c.logout = function() {
        c.user = null;
        c.customer = null;
        c.cases = [];
        c.stats = { total: 0, active: 0, resolved: 0, closed: 0 };
        c.currentView = 'landing';
        c.authForm = { name: '', email: '', mobile: '', password: '', confirmPassword: '' };
    };

    // ========== CASES ==========
    c.loadCases = function() {
        if (!c.user) return;
        $http.get(API + '/cases?user_id=' + c.user.sys_id)
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.cases = d.cases || [];
                c.stats = d.stats || { total: 0, active: 0, resolved: 0, closed: 0 };
            }
        });
    };

    c.viewCase = function(cs) {
        c.selectedCase = cs;
        c.currentView = 'caseDetail';
    };

    c.getStageIndex = function(stage) {
        var stages = ['New', 'Initial Review', 'Investigation', 'Resolved', 'Closed'];
        var idx = stages.indexOf(stage);
        return idx >= 0 ? idx : 0;
    };

    // ========== REPORT ==========
    c.nextStep = function() {
        if (c.wizardStep < c.totalSteps) c.wizardStep++;
    };
    c.prevStep = function() {
        if (c.wizardStep > 1) c.wizardStep--;
    };
    c.goToStep = function(step) {
        if (step <= c.wizardStep) c.wizardStep = step;
    };

    c.submitReport = function() {
        c.isSubmitting = true;
        var payload = {
            user_id: c.user.sys_id,
            customer_id: c.customer ? c.customer.sys_id : '',
            type: c.report.type,
            description: c.report.description,
            incident_date: c.report.incident_date,
            incident_time: c.report.incident_time,
            financial_involvement: c.report.financial_involvement,
            payment_mode: c.report.payment_mode,
            institution_name: c.report.institution_name,
            institution_type: c.report.institution_type,
            branch: c.report.branch,
            reference_type: c.report.reference_type,
            transaction_reference: c.report.transaction_reference,
            exposure: c.report.exposure,
            currency: c.report.currency || 'INR',
            blocked_amount: c.report.blocked_amount,
            recovered_amount: c.report.recovered_amount,
            suspect_name: c.report.suspect_name,
            suspect_contact: c.report.suspect_contact,
            communication_channel: c.report.communication_channel,
            location: c.report.location,
            area: c.report.area,
            pincode: c.report.pincode,
            digital_platform: c.report.digital_platform,
            evidence_type: c.report.evidence_type,
            evidence_description: c.report.evidence_description,
            severity: 'Medium'
        };
        $http.post(API + '/cases', payload)
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.submitResult = d;
                c.currentView = 'submitSuccess';
                c.loadCases();
            }
            c.isSubmitting = false;
        }, function() {
            c.isSubmitting = false;
        });
    };

    c.startNewReport = function() {
        c.wizardStep = 1;
        c.report = {
            type: '', description: '', incident_date: '', incident_time: '',
            financial_involvement: '', payment_mode: '', institution_name: '',
            institution_type: '', branch: '', reference_type: 'UTR',
            transaction_reference: '', exposure: '', currency: 'INR',
            blocked_amount: '', recovered_amount: '', suspect_name: '',
            suspect_contact: '', communication_channel: '', location: '',
            area: '', pincode: '', digital_platform: '', evidence_type: '',
            evidence_description: ''
        };
        c.submitResult = null;
        c.currentView = 'reportFraud';
    };

    // ========== ADDITIONAL EVIDENCE ==========
    c.addEvidenceForm = { evidence_type: '', evidence_description: '' };
    c.addEvidenceLoading = false;

    c.submitAdditionalEvidence = function() {
        if (!c.selectedCase) return;
        c.addEvidenceLoading = true;
        $http.post(API + '/cases', {
            action: 'add_evidence',
            case_id: c.selectedCase.sys_id,
            user_id: c.user.sys_id,
            evidence_type: c.addEvidenceForm.evidence_type,
            evidence_description: c.addEvidenceForm.evidence_description
        }).then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.loadCases();
                c.addEvidenceForm = { evidence_type: '', evidence_description: '' };
                $timeout(function() {
                    // Refresh selected case data
                    for (var i = 0; i < c.cases.length; i++) {
                        if (c.cases[i].sys_id === c.selectedCase.sys_id) {
                            c.selectedCase = c.cases[i];
                            break;
                        }
                    }
                }, 1500);
            }
            c.addEvidenceLoading = false;
        }, function() { c.addEvidenceLoading = false; });
    };

    // ========== AI ASSISTANT ==========
    c.aiResponses = {
        'how do i report fraud': 'To report fraud: Click "Report Fraud" in the sidebar, then follow the step-by-step wizard. Describe what happened, select the fraud type, provide financial details if applicable, and submit evidence.',
        'what evidence should i upload': 'You can upload: screenshots, bank statements (PDF), transaction receipts, chat/email exports, UPI payment confirmations, audio/video recordings, and any documents related to the fraud.',
        'what is my case status': 'Go to "Track Cases" in the sidebar to view all your cases and their current status. Each case shows a visual timeline from Submitted to Closed.',
        'what does this status mean': 'Case stages: New = Just submitted, Initial Review = Being reviewed by our team, Investigation = Active investigation underway, Resolved = Investigation complete, Closed = Case finalized.',
        'where can i track my case': 'Click "Track Cases" in the left sidebar to see all your cases. Click any case to view its full details, timeline, and evidence.',
        'what is phishing': 'Phishing is a cyber fraud where attackers impersonate legitimate organizations via email, SMS, or calls to steal your personal information, passwords, or financial details.',
        'what is payment fraud': 'Payment fraud involves unauthorized transactions using your bank account, UPI, credit/debit card, or other payment methods without your consent.',
        'how do i add evidence': 'Open any case from "Track Cases", scroll down to the Evidence section, and click "Add Evidence". Select the type and describe the evidence.',
        'how do i contact support': 'For urgent assistance, use the "Help & Support" section in the sidebar. For case-specific queries, view your case details and use the AI assistant.'
    };

    c.sendAIMessage = function() {
        if (!c.aiInput.trim()) return;
        var q = c.aiInput.trim();
        c.aiMessages.push({ role: 'user', text: q });
        c.aiInput = '';
        var lowerQ = q.toLowerCase();
        var bestMatch = 'I can help you with fraud reporting, case tracking, evidence submission, and general fraud awareness. Try asking: "How do I report fraud?" or "What evidence should I upload?"';
        for (var key in c.aiResponses) {
            if (lowerQ.indexOf(key) !== -1 || key.indexOf(lowerQ) !== -1) {
                bestMatch = c.aiResponses[key];
                break;
            }
        }
        // Check for keyword matches
        if (bestMatch.indexOf('I can help') === 0) {
            if (lowerQ.indexOf('report') !== -1) bestMatch = c.aiResponses['how do i report fraud'];
            else if (lowerQ.indexOf('evidence') !== -1 || lowerQ.indexOf('upload') !== -1) bestMatch = c.aiResponses['what evidence should i upload'];
            else if (lowerQ.indexOf('status') !== -1 || lowerQ.indexOf('track') !== -1) bestMatch = c.aiResponses['what is my case status'];
            else if (lowerQ.indexOf('phishing') !== -1) bestMatch = c.aiResponses['what is phishing'];
            else if (lowerQ.indexOf('payment') !== -1) bestMatch = c.aiResponses['what is payment fraud'];
            else if (lowerQ.indexOf('support') !== -1 || lowerQ.indexOf('help') !== -1 || lowerQ.indexOf('contact') !== -1) bestMatch = c.aiResponses['how do i contact support'];
        }
        $timeout(function() {
            c.aiMessages.push({ role: 'ai', text: bestMatch });
        }, 600);
    };

    // ========== NAVIGATION ==========
    c.navigate = function(view) {
        if (view === 'reportFraud') { c.startNewReport(); return; }
        if (view === 'trackCases') { c.loadCases(); }
        c.currentView = view;
    };

    c.goToPortalSelect = function() { c.currentView = 'portalSelect'; };
    c.goToAuth = function() { c.currentView = 'auth'; };
    c.getSeverityClass = function(s) {
        if (s === 'Critical') return 'sev-critical';
        if (s === 'High') return 'sev-high';
        if (s === 'Medium') return 'sev-medium';
        return 'sev-low';
    };
    c.getStatusClass = function(s) {
        if (s === 'Resolved' || s === 'Closed') return 'st-resolved';
        if (s === 'In Progress' || s === 'Investigation') return 'st-progress';
        return 'st-new';
    };
};"""

# ============================================================
# HTML TEMPLATE
# ============================================================
template = r"""<div class="fnx-app">
<!-- ============ LANDING PAGE ============ -->
<div ng-if="c.currentView === 'landing'" class="fnx-landing">
    <div class="fnx-landing-header">
        <div class="fnx-landing-brand">
            <svg width="36" height="36" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="none" stroke="#00B8D9" stroke-width="2.5"/><path d="M13 15h14M13 20h10M13 25h7" stroke="#00B8D9" stroke-width="2" stroke-linecap="round"/><circle cx="28" cy="25" r="4" fill="none" stroke="#00B8D9" stroke-width="1.5"/><line x1="31" y1="28" x2="34" y2="31" stroke="#00B8D9" stroke-width="1.5" stroke-linecap="round"/></svg>
            <span class="fnx-brand-text">{{c.t('brand')}}</span>
        </div>
        <div class="fnx-landing-actions">
            <button class="fnx-lang-btn" ng-click="c.toggleLang()">{{c.lang === 'en' ? 'தமிழ்' : 'English'}}</button>
            <button class="fnx-btn fnx-btn-outline" ng-click="c.currentView = 'auth'; c.authMode = 'login'">{{c.t('login')}}</button>
            <button class="fnx-btn fnx-btn-primary" ng-click="c.currentView = 'auth'; c.authMode = 'register'">{{c.t('register')}}</button>
        </div>
    </div>
    <div class="fnx-hero">
        <div class="fnx-hero-content">
            <div class="fnx-hero-badge">FRAUDNEXUS</div>
            <h1>{{c.t('heroTitle')}}</h1>
            <p class="fnx-hero-sub">{{c.t('heroSub')}}</p>
            <p class="fnx-hero-desc">{{c.t('heroDesc')}}</p>
            <div class="fnx-hero-btns">
                <button class="fnx-btn fnx-btn-primary fnx-btn-lg" ng-click="c.goToPortalSelect()">{{c.t('getStarted')}}</button>
                <button class="fnx-btn fnx-btn-ghost fnx-btn-lg" ng-click="c.goToPortalSelect()">{{c.t('learnMore')}}</button>
            </div>
        </div>
        <div class="fnx-hero-visual">
            <div class="fnx-hero-graphic">
                <div class="fnx-hero-circle c1"></div>
                <div class="fnx-hero-circle c2"></div>
                <div class="fnx-hero-circle c3"></div>
                <div class="fnx-hero-shield">
                    <svg width="80" height="80" viewBox="0 0 80 80"><path d="M40 8L12 22v18c0 16.6 11.9 32.1 28 36 16.1-3.9 28-19.4 28-36V22L40 8z" fill="none" stroke="#00B8D9" stroke-width="2.5"/><path d="M30 40l8 8 14-14" fill="none" stroke="#00B8D9" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
            </div>
        </div>
    </div>
    <div class="fnx-features">
        <div class="fnx-feature-card" ng-repeat="f in [{icon:'&#128274;',t:'Secure Reporting'},{icon:'&#128269;',t:'Case Tracking'},{icon:'&#128196;',t:'Evidence Chain'},{icon:'&#129302;',t:'AI Assistance'},{icon:'&#127974;',t:'Financial Intelligence'},{icon:'&#128737;',t:'Cyber Protection'}]">
            <div class="fnx-feature-icon">{{f.icon}}</div>
            <div class="fnx-feature-title">{{f.t}}</div>
        </div>
    </div>
</div>

<!-- ============ PORTAL SELECTION ============ -->
<div ng-if="c.currentView === 'portalSelect'" class="fnx-portal-select">
    <div class="fnx-portal-header">
        <button class="fnx-back-link" ng-click="c.currentView = 'landing'">&larr; Back</button>
        <div class="fnx-portal-title">
            <h2>Select Your Portal</h2>
            <p>Choose the portal that matches your role</p>
        </div>
    </div>
    <div class="fnx-portal-cards">
        <div class="fnx-portal-card fnx-portal-customer" ng-click="c.goToAuth()">
            <div class="fnx-portal-card-icon">&#128100;</div>
            <h3>{{c.t('customerPortal')}}</h3>
            <p>{{c.t('customerPortalDesc')}}</p>
            <ul><li>Report fraud securely</li><li>Track your cases</li><li>Submit evidence</li><li>Receive real-time updates</li><li>Get AI assistance</li></ul>
            <button class="fnx-btn fnx-btn-primary">{{c.t('enterPortal')}}</button>
        </div>
        <div class="fnx-portal-card fnx-portal-investigator">
            <div class="fnx-portal-card-icon">&#128373;</div>
            <h3>{{c.t('investigatorPortal')}}</h3>
            <p>{{c.t('investigatorPortalDesc')}}</p>
            <ul><li>Investigate fraud cases</li><li>Analyze intelligence</li><li>Manage compliance</li><li>Generate reports</li><li>Handle approvals</li></ul>
            <button class="fnx-btn fnx-btn-disabled">{{c.t('comingSoon')}}</button>
        </div>
    </div>
</div>

<!-- ============ AUTH ============ -->
<div ng-if="c.currentView === 'auth'" class="fnx-auth-page">
    <div class="fnx-auth-left">
        <div class="fnx-auth-brand" ng-click="c.currentView = 'landing'">
            <svg width="32" height="32" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="none" stroke="#00B8D9" stroke-width="2.5"/><path d="M13 15h14M13 20h10M13 25h7" stroke="#00B8D9" stroke-width="2" stroke-linecap="round"/></svg>
            <span>FRAUDNEXUS</span>
        </div>
        <h2>{{c.t('tagline')}}</h2>
        <p>Secure. Intelligent. Trusted.</p>
    </div>
    <div class="fnx-auth-right">
        <div class="fnx-auth-box">
            <div class="fnx-auth-tabs">
                <button ng-class="{'active': c.authMode === 'login'}" ng-click="c.authMode = 'login'; c.authError = ''">{{c.t('login')}}</button>
                <button ng-class="{'active': c.authMode === 'register'}" ng-click="c.authMode = 'register'; c.authError = ''">{{c.t('register')}}</button>
            </div>
            <div class="fnx-auth-error" ng-if="c.authError">{{c.authError}}</div>
            <!-- LOGIN -->
            <form ng-if="c.authMode === 'login'" ng-submit="c.doLogin()" class="fnx-auth-form">
                <div class="fnx-field"><label>{{c.t('email')}}</label><input type="email" ng-model="c.authForm.email" required placeholder="your@email.com"></div>
                <div class="fnx-field"><label>{{c.t('password')}}</label><input type="password" ng-model="c.authForm.password" required placeholder="Enter password"></div>
                <button type="submit" class="fnx-btn fnx-btn-primary fnx-btn-full" ng-disabled="c.authLoading">{{c.authLoading ? '...' : c.t('login')}}</button>
                <p class="fnx-auth-switch">{{c.t('noAccount')}} <a ng-click="c.authMode = 'register'">{{c.t('register')}}</a></p>
            </form>
            <!-- REGISTER -->
            <form ng-if="c.authMode === 'register'" ng-submit="c.doRegister()" class="fnx-auth-form">
                <div class="fnx-field"><label>{{c.t('fullName')}}</label><input type="text" ng-model="c.authForm.name" required placeholder="Full Name"></div>
                <div class="fnx-field"><label>{{c.t('email')}}</label><input type="email" ng-model="c.authForm.email" required placeholder="your@email.com"></div>
                <div class="fnx-field"><label>{{c.t('mobile')}}</label><input type="tel" ng-model="c.authForm.mobile" required placeholder="+91 XXXXX XXXXX"></div>
                <div class="fnx-field"><label>{{c.t('password')}}</label><input type="password" ng-model="c.authForm.password" required placeholder="Create password"></div>
                <div class="fnx-field"><label>{{c.t('confirmPassword')}}</label><input type="password" ng-model="c.authForm.confirmPassword" required placeholder="Confirm password"></div>
                <button type="submit" class="fnx-btn fnx-btn-primary fnx-btn-full" ng-disabled="c.authLoading">{{c.authLoading ? '...' : c.t('register')}}</button>
                <p class="fnx-auth-switch">{{c.t('hasAccount')}} <a ng-click="c.authMode = 'login'">{{c.t('login')}}</a></p>
            </form>
        </div>
    </div>
</div>

<!-- ============ MAIN APP LAYOUT (post-auth) ============ -->
<div ng-if="c.user && c.currentView !== 'landing' && c.currentView !== 'portalSelect' && c.currentView !== 'auth' && c.currentView !== 'submitSuccess'" class="fnx-main-layout">
    <!-- HEADER -->
    <header class="fnx-header">
        <div class="fnx-header-left">
            <button class="fnx-sidebar-toggle" ng-click="c.sidebarCollapsed = !c.sidebarCollapsed">&#9776;</button>
            <div class="fnx-header-brand" ng-click="c.navigate('dashboard')">
                <svg width="28" height="28" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="none" stroke="#00B8D9" stroke-width="2.5"/><path d="M13 15h14M13 20h10M13 25h7" stroke="#00B8D9" stroke-width="2" stroke-linecap="round"/></svg>
                <span>FRAUDNEXUS</span>
            </div>
        </div>
        <div class="fnx-header-right">
            <button class="fnx-lang-btn" ng-click="c.toggleLang()">{{c.lang === 'en' ? 'தமிழ்' : 'EN'}}</button>
            <button class="fnx-icon-btn" ng-click="c.showNotifications = !c.showNotifications" title="Notifications">&#128276;<span class="fnx-notif-dot" ng-if="c.cases.length > 0"></span></button>
            <div class="fnx-profile-pill">
                <span class="fnx-avatar">{{c.user.name.charAt(0)}}</span>
                <span class="fnx-profile-name">{{c.user.name}}</span>
                <button class="fnx-icon-btn fnx-logout-btn" ng-click="c.logout()" title="Logout">&#10148;</button>
            </div>
        </div>
        <!-- Notifications Dropdown -->
        <div class="fnx-notif-dropdown" ng-if="c.showNotifications">
            <div class="fnx-notif-header"><strong>Notifications</strong><button ng-click="c.showNotifications = false">&times;</button></div>
            <div class="fnx-notif-empty" ng-if="c.cases.length === 0">No notifications</div>
            <div class="fnx-notif-item" ng-repeat="cs in c.cases | limitTo:5" ng-click="c.viewCase(cs); c.showNotifications = false">
                <strong>{{cs.number}}</strong> - {{cs.type}}<br><small>Status: {{cs.status}}</small>
            </div>
        </div>
    </header>

    <!-- SIDEBAR -->
    <aside class="fnx-sidebar" ng-class="{'collapsed': c.sidebarCollapsed}">
        <nav class="fnx-nav">
            <a class="fnx-nav-item" ng-class="{'active': c.currentView === 'dashboard'}" ng-click="c.navigate('dashboard')"><span class="fnx-nav-icon">&#127968;</span><span class="fnx-nav-label">{{c.t('dashboard')}}</span></a>
            <a class="fnx-nav-item" ng-class="{'active': c.currentView === 'reportFraud'}" ng-click="c.navigate('reportFraud')"><span class="fnx-nav-icon">&#128680;</span><span class="fnx-nav-label">{{c.t('reportFraud')}}</span></a>
            <a class="fnx-nav-item" ng-class="{'active': c.currentView === 'trackCases'}" ng-click="c.navigate('trackCases')"><span class="fnx-nav-icon">&#128270;</span><span class="fnx-nav-label">{{c.t('trackCases')}}</span></a>
            <a class="fnx-nav-item" ng-class="{'active': c.currentView === 'evidenceVault'}" ng-click="c.navigate('evidenceVault')"><span class="fnx-nav-icon">&#128451;</span><span class="fnx-nav-label">{{c.t('evidence')}}</span></a>
            <a class="fnx-nav-item" ng-class="{'active': c.currentView === 'help'}" ng-click="c.navigate('help')"><span class="fnx-nav-icon">&#10067;</span><span class="fnx-nav-label">{{c.t('helpSupport')}}</span></a>
        </nav>
    </aside>

    <!-- CONTENT -->
    <main class="fnx-content" ng-class="{'sidebar-collapsed': c.sidebarCollapsed}">

        <!-- DASHBOARD -->
        <div ng-if="c.currentView === 'dashboard'" class="fnx-dashboard">
            <div class="fnx-welcome">
                <h2>{{c.t('welcome')}}, {{c.user.name}}!</h2>
                <p ng-if="c.customer.customer_id">Customer ID: <strong>{{c.customer.customer_id}}</strong></p>
            </div>
            <div class="fnx-stats-row">
                <div class="fnx-stat-card"><div class="fnx-stat-icon si-total">&#128202;</div><div class="fnx-stat-val">{{c.stats.total}}</div><div class="fnx-stat-label">{{c.t('totalCases')}}</div></div>
                <div class="fnx-stat-card"><div class="fnx-stat-icon si-active">&#128308;</div><div class="fnx-stat-val">{{c.stats.active}}</div><div class="fnx-stat-label">{{c.t('activeCases')}}</div></div>
                <div class="fnx-stat-card"><div class="fnx-stat-icon si-resolved">&#9989;</div><div class="fnx-stat-val">{{c.stats.resolved}}</div><div class="fnx-stat-label">{{c.t('resolvedCases')}}</div></div>
            </div>
            <div class="fnx-action-row">
                <button class="fnx-btn fnx-btn-primary fnx-btn-lg fnx-cta" ng-click="c.navigate('reportFraud')">&#128680; {{c.t('reportFraud')}}</button>
                <button class="fnx-btn fnx-btn-outline fnx-btn-lg" ng-click="c.navigate('trackCases')">&#128270; {{c.t('trackCases')}}</button>
            </div>
            <div class="fnx-section">
                <h3>{{c.t('recentCases')}}</h3>
                <div class="fnx-empty" ng-if="c.cases.length === 0">{{c.t('noCases')}}</div>
                <table class="fnx-table" ng-if="c.cases.length > 0">
                    <thead><tr><th>{{c.t('caseId')}}</th><th>{{c.t('incidentType')}}</th><th>{{c.t('date')}}</th><th>{{c.t('severity')}}</th><th>{{c.t('status')}}</th><th></th></tr></thead>
                    <tbody><tr ng-repeat="cs in c.cases | limitTo:5">
                        <td><strong>{{cs.number}}</strong></td><td>{{cs.type}}</td><td>{{cs.incident_date}}</td>
                        <td><span class="fnx-badge" ng-class="c.getSeverityClass(cs.severity)">{{cs.severity}}</span></td>
                        <td><span class="fnx-badge" ng-class="c.getStatusClass(cs.status)">{{cs.status}}</span></td>
                        <td><button class="fnx-btn fnx-btn-sm" ng-click="c.viewCase(cs)">{{c.t('viewCase')}}</button></td>
                    </tr></tbody>
                </table>
            </div>
            <div class="fnx-section">
                <h3>{{c.t('fraudAwareness')}}</h3>
                <div class="fnx-awareness-grid">
                    <div class="fnx-awareness-card"><div class="fnx-aw-icon">&#127907;</div><h4>{{c.t('phishing')}}</h4><p>Learn to identify and avoid phishing attacks targeting your financial information.</p></div>
                    <div class="fnx-awareness-card"><div class="fnx-aw-icon">&#128179;</div><h4>{{c.t('paymentFraud')}}</h4><p>Protect yourself from unauthorized transactions and payment scams.</p></div>
                    <div class="fnx-awareness-card"><div class="fnx-aw-icon">&#128272;</div><h4>{{c.t('accountSecurity')}}</h4><p>Best practices to secure your online accounts and banking credentials.</p></div>
                    <div class="fnx-awareness-card"><div class="fnx-aw-icon">&#128100;</div><h4>{{c.t('identityTheft')}}</h4><p>Steps to protect your identity and what to do if it's compromised.</p></div>
                </div>
            </div>
        </div>

        <!-- REPORT FRAUD WIZARD -->
        <div ng-if="c.currentView === 'reportFraud'" class="fnx-report">
            <h2>&#128680; {{c.t('reportFraud')}}</h2>
            <div class="fnx-wizard-progress">
                <div class="fnx-wizard-step" ng-repeat="s in [1,2,3,4,5,6,7]" ng-class="{'active': c.wizardStep === s, 'done': c.wizardStep > s}" ng-click="c.goToStep(s)">
                    <div class="fnx-ws-num">{{s}}</div>
                    <div class="fnx-ws-label" ng-if="s===1">Type</div>
                    <div class="fnx-ws-label" ng-if="s===2">Details</div>
                    <div class="fnx-ws-label" ng-if="s===3">Date</div>
                    <div class="fnx-ws-label" ng-if="s===4">Financial</div>
                    <div class="fnx-ws-label" ng-if="s===5">Location</div>
                    <div class="fnx-ws-label" ng-if="s===6">Evidence</div>
                    <div class="fnx-ws-label" ng-if="s===7">Review</div>
                </div>
            </div>

            <!-- Step 1: Type -->
            <div class="fnx-wizard-body" ng-if="c.wizardStep === 1">
                <h3>{{c.t('selectType')}}</h3>
                <div class="fnx-type-grid">
                    <div class="fnx-type-card" ng-repeat="ft in c.fraudTypes" ng-class="{'selected': c.report.type === ft}" ng-click="c.report.type = ft">{{ft}}</div>
                </div>
                <div class="fnx-wizard-actions"><button class="fnx-btn fnx-btn-primary" ng-click="c.nextStep()" ng-disabled="!c.report.type">{{c.t('next')}}</button></div>
            </div>

            <!-- Step 2: Description -->
            <div class="fnx-wizard-body" ng-if="c.wizardStep === 2">
                <h3>{{c.t('whatHappened')}}</h3>
                <textarea class="fnx-textarea" ng-model="c.report.description" placeholder="{{c.t('describeIncident')}}" rows="6"></textarea>
                <div class="fnx-wizard-actions">
                    <button class="fnx-btn fnx-btn-outline" ng-click="c.prevStep()">{{c.t('back')}}</button>
                    <button class="fnx-btn fnx-btn-primary" ng-click="c.nextStep()" ng-disabled="!c.report.description">{{c.t('next')}}</button>
                </div>
            </div>

            <!-- Step 3: Date/Time -->
            <div class="fnx-wizard-body" ng-if="c.wizardStep === 3">
                <h3>{{c.t('incidentDate')}}</h3>
                <div class="fnx-form-row">
                    <div class="fnx-field"><label>{{c.t('incidentDate')}}</label><input type="date" ng-model="c.report.incident_date" required></div>
                    <div class="fnx-field"><label>{{c.t('incidentTime')}}</label><input type="time" ng-model="c.report.incident_time"></div>
                </div>
                <div class="fnx-wizard-actions">
                    <button class="fnx-btn fnx-btn-outline" ng-click="c.prevStep()">{{c.t('back')}}</button>
                    <button class="fnx-btn fnx-btn-primary" ng-click="c.nextStep()" ng-disabled="!c.report.incident_date">{{c.t('next')}}</button>
                </div>
            </div>

            <!-- Step 4: Financial -->
            <div class="fnx-wizard-body" ng-if="c.wizardStep === 4">
                <h3>{{c.t('financialInvolvement')}}</h3>
                <div class="fnx-choice-row">
                    <button class="fnx-choice-btn" ng-class="{'selected': c.report.financial_involvement === 'Yes'}" ng-click="c.report.financial_involvement = 'Yes'">{{c.t('yes')}}</button>
                    <button class="fnx-choice-btn" ng-class="{'selected': c.report.financial_involvement === 'No'}" ng-click="c.report.financial_involvement = 'No'">{{c.t('no')}}</button>
                    <button class="fnx-choice-btn" ng-class="{'selected': c.report.financial_involvement === 'Not Sure'}" ng-click="c.report.financial_involvement = 'Not Sure'">{{c.t('notSure')}}</button>
                </div>
                <div ng-if="c.report.financial_involvement === 'Yes'" class="fnx-financial-section">
                    <div class="fnx-form-row">
                        <div class="fnx-field"><label>{{c.t('paymentMode')}}</label><select ng-model="c.report.payment_mode"><option value="">-- Select --</option><option ng-repeat="pm in c.paymentModes" value="{{pm}}">{{pm}}</option></select></div>
                        <div class="fnx-field"><label>{{c.t('amountInvolved')}} (INR)</label><input type="number" ng-model="c.report.exposure" placeholder="e.g. 75000"></div>
                    </div>
                    <div class="fnx-form-row">
                        <div class="fnx-field"><label>{{c.t('institution')}}</label><input type="text" ng-model="c.report.institution_name" placeholder="e.g. Partner Bank A"></div>
                        <div class="fnx-field"><label>{{c.t('institutionType')}}</label><select ng-model="c.report.institution_type"><option value="">-- Select --</option><option ng-repeat="it in c.institutionTypes" value="{{it}}">{{it}}</option></select></div>
                    </div>
                    <div class="fnx-form-row">
                        <div class="fnx-field"><label>{{c.t('branch')}}</label><input type="text" ng-model="c.report.branch" placeholder="e.g. Anna Nagar Branch"></div>
                        <div class="fnx-field"><label>{{c.t('referenceType')}}</label><select ng-model="c.report.reference_type"><option ng-repeat="rt in c.referenceTypes" value="{{rt}}">{{rt}}</option></select></div>
                    </div>
                    <div class="fnx-form-row">
                        <div class="fnx-field"><label>{{c.t('referenceValue')}}</label><input type="text" ng-model="c.report.transaction_reference" placeholder="e.g. DEMO-UTR-001"></div>
                    </div>
                    <div class="fnx-form-row">
                        <div class="fnx-field"><label>{{c.t('suspectName')}}</label><input type="text" ng-model="c.report.suspect_name" placeholder="Name / identifier"></div>
                        <div class="fnx-field"><label>{{c.t('suspectContact')}}</label><input type="text" ng-model="c.report.suspect_contact" placeholder="Phone / Email / UPI"></div>
                    </div>
                    <div class="fnx-field"><label>{{c.t('channel')}}</label><input type="text" ng-model="c.report.communication_channel" placeholder="e.g. WhatsApp / Telegram / Phone Call"></div>
                </div>
                <div class="fnx-wizard-actions">
                    <button class="fnx-btn fnx-btn-outline" ng-click="c.prevStep()">{{c.t('back')}}</button>
                    <button class="fnx-btn fnx-btn-primary" ng-click="c.nextStep()" ng-disabled="!c.report.financial_involvement">{{c.t('next')}}</button>
                </div>
            </div>

            <!-- Step 5: Location -->
            <div class="fnx-wizard-body" ng-if="c.wizardStep === 5">
                <h3>{{c.t('location')}} & {{c.t('digitalPlatform')}}</h3>
                <div class="fnx-form-row">
                    <div class="fnx-field"><label>{{c.t('location')}}</label><input type="text" ng-model="c.report.location" placeholder="City / Town"></div>
                    <div class="fnx-field"><label>{{c.t('area')}}</label><input type="text" ng-model="c.report.area" placeholder="Area / Locality"></div>
                </div>
                <div class="fnx-form-row">
                    <div class="fnx-field"><label>{{c.t('pincode')}}</label><input type="text" ng-model="c.report.pincode" placeholder="6-digit pincode"></div>
                    <div class="fnx-field"><label>{{c.t('digitalPlatform')}}</label><input type="text" ng-model="c.report.digital_platform" placeholder="App / Website / URL"></div>
                </div>
                <div class="fnx-wizard-actions">
                    <button class="fnx-btn fnx-btn-outline" ng-click="c.prevStep()">{{c.t('back')}}</button>
                    <button class="fnx-btn fnx-btn-primary" ng-click="c.nextStep()">{{c.t('next')}}</button>
                </div>
            </div>

            <!-- Step 6: Evidence -->
            <div class="fnx-wizard-body" ng-if="c.wizardStep === 6">
                <h3>{{c.t('evidence')}}</h3>
                <div class="fnx-form-row">
                    <div class="fnx-field"><label>{{c.t('evidenceType')}}</label><select ng-model="c.report.evidence_type"><option value="">-- Select --</option><option ng-repeat="et in c.evidenceTypes" value="{{et}}">{{et}}</option></select></div>
                </div>
                <div class="fnx-field"><label>{{c.t('evidenceDesc')}}</label><textarea class="fnx-textarea" ng-model="c.report.evidence_description" rows="3" placeholder="Describe your evidence..."></textarea></div>
                <div class="fnx-wizard-actions">
                    <button class="fnx-btn fnx-btn-outline" ng-click="c.prevStep()">{{c.t('back')}}</button>
                    <button class="fnx-btn fnx-btn-primary" ng-click="c.nextStep()">{{c.t('review')}}</button>
                </div>
            </div>

            <!-- Step 7: Review -->
            <div class="fnx-wizard-body" ng-if="c.wizardStep === 7">
                <h3>{{c.t('review')}}</h3>
                <div class="fnx-review-card">
                    <div class="fnx-review-row"><span>Incident Type:</span><strong>{{c.report.type}}</strong></div>
                    <div class="fnx-review-row"><span>Description:</span><span>{{c.report.description}}</span></div>
                    <div class="fnx-review-row"><span>Date:</span><span>{{c.report.incident_date}} {{c.report.incident_time}}</span></div>
                    <div class="fnx-review-row"><span>Financial:</span><span>{{c.report.financial_involvement}}</span></div>
                    <div class="fnx-review-row" ng-if="c.report.payment_mode"><span>Payment Mode:</span><span>{{c.report.payment_mode}}</span></div>
                    <div class="fnx-review-row" ng-if="c.report.exposure"><span>Amount:</span><span>INR {{c.report.exposure}}</span></div>
                    <div class="fnx-review-row" ng-if="c.report.institution_name"><span>Institution:</span><span>{{c.report.institution_name}} ({{c.report.institution_type}})</span></div>
                    <div class="fnx-review-row" ng-if="c.report.branch"><span>Branch:</span><span>{{c.report.branch}}</span></div>
                    <div class="fnx-review-row" ng-if="c.report.transaction_reference"><span>Reference:</span><span>{{c.report.reference_type}}: {{c.report.transaction_reference}}</span></div>
                    <div class="fnx-review-row" ng-if="c.report.suspect_name"><span>Suspect:</span><span>{{c.report.suspect_name}}</span></div>
                    <div class="fnx-review-row" ng-if="c.report.location"><span>Location:</span><span>{{c.report.location}} {{c.report.area}} {{c.report.pincode}}</span></div>
                    <div class="fnx-review-row" ng-if="c.report.digital_platform"><span>Platform:</span><span>{{c.report.digital_platform}}</span></div>
                    <div class="fnx-review-row" ng-if="c.report.evidence_type"><span>Evidence:</span><span>{{c.report.evidence_type}} - {{c.report.evidence_description}}</span></div>
                </div>
                <div class="fnx-wizard-actions">
                    <button class="fnx-btn fnx-btn-outline" ng-click="c.prevStep()">{{c.t('back')}}</button>
                    <button class="fnx-btn fnx-btn-primary fnx-btn-lg" ng-click="c.submitReport()" ng-disabled="c.isSubmitting">{{c.isSubmitting ? c.t('submitting') : c.t('submit')}}</button>
                </div>
            </div>
        </div>

        <!-- TRACK CASES -->
        <div ng-if="c.currentView === 'trackCases'" class="fnx-track">
            <h2>&#128270; {{c.t('trackCases')}}</h2>
            <div class="fnx-empty" ng-if="c.cases.length === 0">{{c.t('noCases')}}</div>
            <div class="fnx-case-list" ng-if="c.cases.length > 0">
                <div class="fnx-case-card" ng-repeat="cs in c.cases" ng-click="c.viewCase(cs)">
                    <div class="fnx-case-card-header">
                        <strong>{{cs.number}}</strong>
                        <span class="fnx-badge" ng-class="c.getStatusClass(cs.status)">{{cs.status}}</span>
                    </div>
                    <div class="fnx-case-card-body">
                        <div>{{cs.type}}</div>
                        <div class="fnx-case-meta"><span>{{cs.incident_date}}</span> <span class="fnx-badge" ng-class="c.getSeverityClass(cs.severity)">{{cs.severity}}</span></div>
                    </div>
                    <div class="fnx-mini-timeline">
                        <div class="fnx-mt-step" ng-repeat="st in ['New','Initial Review','Investigation','Resolved','Closed']" ng-class="{'reached': c.getStageIndex(cs.stage) >= $index}"></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- CASE DETAIL -->
        <div ng-if="c.currentView === 'caseDetail' && c.selectedCase" class="fnx-case-detail">
            <button class="fnx-back-link" ng-click="c.navigate('trackCases')">&larr; {{c.t('trackCases')}}</button>
            <div class="fnx-case-detail-header">
                <h2>{{c.selectedCase.number}}</h2>
                <span class="fnx-badge fnx-badge-lg" ng-class="c.getStatusClass(c.selectedCase.status)">{{c.selectedCase.status}}</span>
            </div>
            <div class="fnx-detail-grid">
                <div class="fnx-detail-item"><label>Type</label><span>{{c.selectedCase.type}}</span></div>
                <div class="fnx-detail-item"><label>Severity</label><span class="fnx-badge" ng-class="c.getSeverityClass(c.selectedCase.severity)">{{c.selectedCase.severity}}</span></div>
                <div class="fnx-detail-item"><label>Date</label><span>{{c.selectedCase.incident_date}}</span></div>
                <div class="fnx-detail-item"><label>Exposure</label><span>INR {{c.selectedCase.exposure}}</span></div>
                <div class="fnx-detail-item" ng-if="c.selectedCase.location"><label>Location</label><span>{{c.selectedCase.location}}</span></div>
                <div class="fnx-detail-item" ng-if="c.selectedCase.digital_platform"><label>Platform</label><span>{{c.selectedCase.digital_platform}}</span></div>
            </div>
            <div class="fnx-detail-desc"><label>Description</label><p>{{c.selectedCase.description}}</p></div>

            <!-- Transaction Details -->
            <div class="fnx-section" ng-if="c.selectedCase.transactions && c.selectedCase.transactions.length > 0">
                <h3>Transaction Details</h3>
                <div class="fnx-detail-grid" ng-repeat="txn in c.selectedCase.transactions">
                    <div class="fnx-detail-item" ng-if="txn.payment_mode"><label>Payment Mode</label><span>{{txn.payment_mode}}</span></div>
                    <div class="fnx-detail-item" ng-if="txn.institution_name"><label>Institution</label><span>{{txn.institution_name}}</span></div>
                    <div class="fnx-detail-item" ng-if="txn.branch"><label>Branch</label><span>{{txn.branch}}</span></div>
                    <div class="fnx-detail-item" ng-if="txn.reference_value"><label>{{txn.reference_type || 'Reference'}}</label><span>{{txn.reference_value}}</span></div>
                    <div class="fnx-detail-item" ng-if="txn.amount && txn.amount !== '0'"><label>Amount</label><span>{{txn.currency}} {{txn.amount}}</span></div>
                    <div class="fnx-detail-item" ng-if="txn.suspect_name"><label>Suspect</label><span>{{txn.suspect_name}}</span></div>
                </div>
            </div>

            <!-- Timeline -->
            <div class="fnx-section">
                <h3>{{c.t('caseTimeline')}}</h3>
                <div class="fnx-timeline">
                    <div class="fnx-tl-step" ng-repeat="st in [{l:'Submitted',k:'New'},{l:'Initial Review',k:'Initial Review'},{l:'Investigation',k:'Investigation'},{l:'Resolution',k:'Resolved'},{l:'Closed',k:'Closed'}]" ng-class="{'reached': c.getStageIndex(c.selectedCase.stage) >= $index, 'current': c.getStageIndex(c.selectedCase.stage) === $index}">
                        <div class="fnx-tl-dot"></div>
                        <div class="fnx-tl-label">{{st.l}}</div>
                    </div>
                </div>
            </div>

            <!-- Evidence -->
            <div class="fnx-section">
                <h3>{{c.t('evidence')}} ({{c.selectedCase.evidence.length}})</h3>
                <div class="fnx-evidence-list">
                    <div class="fnx-ev-item" ng-repeat="ev in c.selectedCase.evidence">
                        <div class="fnx-ev-icon">&#128196;</div>
                        <div class="fnx-ev-info"><strong>{{ev.number}}</strong><br>{{ev.type}} - {{ev.description}}<br><small>{{ev.uploaded_on}} | {{ev.status}}</small></div>
                    </div>
                </div>
                <div class="fnx-add-evidence">
                    <h4>{{c.t('addEvidence')}}</h4>
                    <div class="fnx-form-row">
                        <div class="fnx-field"><label>{{c.t('evidenceType')}}</label><select ng-model="c.addEvidenceForm.evidence_type"><option value="">-- Select --</option><option ng-repeat="et in c.evidenceTypes" value="{{et}}">{{et}}</option></select></div>
                    </div>
                    <div class="fnx-field"><label>{{c.t('evidenceDesc')}}</label><textarea class="fnx-textarea" ng-model="c.addEvidenceForm.evidence_description" rows="2"></textarea></div>
                    <button class="fnx-btn fnx-btn-primary" ng-click="c.submitAdditionalEvidence()" ng-disabled="c.addEvidenceLoading || !c.addEvidenceForm.evidence_type">{{c.addEvidenceLoading ? '...' : c.t('addEvidence')}}</button>
                </div>
            </div>
        </div>

        <!-- EVIDENCE VAULT -->
        <div ng-if="c.currentView === 'evidenceVault'" class="fnx-ev-vault">
            <h2>&#128451; {{c.t('evidence')}}</h2>
            <div class="fnx-empty" ng-if="c.cases.length === 0">No evidence found.</div>
            <div ng-repeat="cs in c.cases" ng-if="cs.evidence.length > 0" class="fnx-ev-case-group">
                <h4>{{cs.number}} - {{cs.type}}</h4>
                <div class="fnx-ev-item" ng-repeat="ev in cs.evidence">
                    <div class="fnx-ev-icon">&#128196;</div>
                    <div class="fnx-ev-info"><strong>{{ev.number}}</strong> | {{ev.type}}<br>{{ev.description}}<br><small>{{ev.uploaded_on}} | Status: {{ev.status}}</small></div>
                </div>
            </div>
        </div>

        <!-- HELP -->
        <div ng-if="c.currentView === 'help'" class="fnx-help">
            <h2>&#10067; {{c.t('helpSupport')}}</h2>
            <div class="fnx-help-cards">
                <div class="fnx-help-card"><h4>How do I report fraud?</h4><p>Click "Report Fraud" in the sidebar and follow the step-by-step wizard. Provide details about the incident, financial information, and any evidence you have.</p></div>
                <div class="fnx-help-card"><h4>What evidence should I submit?</h4><p>Screenshots, bank statements, transaction receipts, chat exports, emails, or any documents related to the fraud incident.</p></div>
                <div class="fnx-help-card"><h4>How do I track my case?</h4><p>Click "Track Cases" to view all your submitted cases, their current status, timeline, and evidence.</p></div>
                <div class="fnx-help-card"><h4>Is my data secure?</h4><p>Yes. Your data is stored securely in ServiceNow with role-based access controls. Only you can see your own cases and evidence.</p></div>
            </div>
        </div>
    </main>
</div>

<!-- ============ SUBMIT SUCCESS ============ -->
<div ng-if="c.currentView === 'submitSuccess'" class="fnx-success-page">
    <div class="fnx-success-card">
        <div class="fnx-success-icon">&#9989;</div>
        <h2>{{c.t('caseSubmitted')}}</h2>
        <div class="fnx-success-case-id">{{c.submitResult.number}}</div>
        <p>{{c.t('yourCaseId')}}: <strong>{{c.submitResult.number}}</strong></p>
        <p>Status: <span class="fnx-badge st-new">New</span></p>
        <div class="fnx-success-actions">
            <button class="fnx-btn fnx-btn-primary" ng-click="c.navigate('trackCases')">&#128270; {{c.t('trackYourCase')}}</button>
            <button class="fnx-btn fnx-btn-outline" ng-click="c.startNewReport()">{{c.t('reportAnother')}}</button>
            <button class="fnx-btn fnx-btn-outline" ng-click="c.navigate('dashboard')">{{c.t('dashboard')}}</button>
        </div>
    </div>
</div>

<!-- ============ AI ASSISTANT (Floating) ============ -->
<div ng-if="c.user" class="fnx-ai-fab" ng-click="c.showAI = !c.showAI">&#10024; {{c.t('askAI')}}</div>
<div ng-if="c.showAI" class="fnx-ai-panel">
    <div class="fnx-ai-header"><strong>&#10024; FRAUDNEXUS AI</strong><button ng-click="c.showAI = false">&times;</button></div>
    <div class="fnx-ai-body">
        <div class="fnx-ai-msg ai" ng-if="c.aiMessages.length === 0">Hello! I'm the FRAUDNEXUS AI Assistant. How can I help you today?</div>
        <div class="fnx-ai-msg" ng-repeat="m in c.aiMessages" ng-class="m.role">{{m.text}}</div>
    </div>
    <div class="fnx-ai-input">
        <input type="text" ng-model="c.aiInput" placeholder="{{c.t('aiPlaceholder')}}" ng-keypress="$event.keyCode === 13 && c.sendAIMessage()">
        <button ng-click="c.sendAIMessage()">&#10148;</button>
    </div>
</div>
</div>"""

# ============================================================
# CSS
# ============================================================
css = r"""
/* ============ ROOT VARIABLES ============ */
:root {
    --navy: #0B1F3A; --navy2: #123B63; --cyan: #00B8D9; --cyan-dark: #0093ad;
    --success: #16A34A; --warning: #F59E0B; --critical: #DC2626;
    --bg: #F5F7FA; --card: #FFFFFF; --border: #E2E8F0;
    --text1: #0F172A; --text2: #64748B;
    --font: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --sidebar-w: 240px; --header-h: 56px;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
.fnx-app { font-family: var(--font); color: var(--text1); background: var(--bg); min-height: 100vh; }

/* ============ LANDING ============ */
.fnx-landing { background: linear-gradient(135deg, var(--navy) 0%, #0d2847 50%, var(--navy2) 100%); min-height: 100vh; color: #fff; }
.fnx-landing-header { display: flex; justify-content: space-between; align-items: center; padding: 1rem 2.5rem; border-bottom: 1px solid rgba(255,255,255,0.08); }
.fnx-landing-brand { display: flex; align-items: center; gap: 0.7rem; }
.fnx-brand-text { font-size: 1.3rem; font-weight: 700; letter-spacing: 1.5px; }
.fnx-landing-actions { display: flex; gap: 0.75rem; align-items: center; }
.fnx-hero { display: flex; align-items: center; justify-content: space-between; padding: 5rem 4rem 3rem; max-width: 1200px; margin: 0 auto; gap: 3rem; }
.fnx-hero-content { flex: 1; }
.fnx-hero-badge { display: inline-block; background: rgba(0,184,217,0.15); color: var(--cyan); padding: 0.35rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600; letter-spacing: 2px; margin-bottom: 1.5rem; border: 1px solid rgba(0,184,217,0.3); }
.fnx-hero h1 { font-size: 2.8rem; font-weight: 800; line-height: 1.15; margin-bottom: 0.75rem; }
.fnx-hero-sub { font-size: 1.25rem; color: var(--cyan); font-weight: 500; margin-bottom: 1rem; }
.fnx-hero-desc { color: rgba(255,255,255,0.7); font-size: 1rem; line-height: 1.7; margin-bottom: 2rem; max-width: 520px; }
.fnx-hero-btns { display: flex; gap: 1rem; }
.fnx-hero-visual { flex: 0 0 320px; display: flex; justify-content: center; }
.fnx-hero-graphic { position: relative; width: 260px; height: 260px; }
.fnx-hero-circle { position: absolute; border-radius: 50%; border: 1.5px solid rgba(0,184,217,0.2); }
.fnx-hero-circle.c1 { width: 260px; height: 260px; top: 0; left: 0; animation: pulse-ring 3s ease-in-out infinite; }
.fnx-hero-circle.c2 { width: 200px; height: 200px; top: 30px; left: 30px; border-color: rgba(0,184,217,0.3); animation: pulse-ring 3s ease-in-out infinite 0.5s; }
.fnx-hero-circle.c3 { width: 140px; height: 140px; top: 60px; left: 60px; border-color: rgba(0,184,217,0.4); animation: pulse-ring 3s ease-in-out infinite 1s; }
.fnx-hero-shield { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }
@keyframes pulse-ring { 0%,100% { transform: scale(1); opacity: 0.6; } 50% { transform: scale(1.06); opacity: 1; } }

.fnx-features { display: grid; grid-template-columns: repeat(6, 1fr); gap: 1.25rem; padding: 2rem 4rem 4rem; max-width: 1200px; margin: 0 auto; }
.fnx-feature-card { text-align: center; padding: 1.5rem 1rem; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; transition: all 0.3s; }
.fnx-feature-card:hover { background: rgba(0,184,217,0.08); border-color: rgba(0,184,217,0.3); transform: translateY(-3px); }
.fnx-feature-icon { font-size: 1.8rem; margin-bottom: 0.5rem; }
.fnx-feature-title { font-size: 0.8rem; font-weight: 600; letter-spacing: 0.5px; }

/* ============ PORTAL SELECT ============ */
.fnx-portal-select { min-height: 100vh; background: var(--bg); padding: 2rem; }
.fnx-portal-header { text-align: center; margin-bottom: 3rem; }
.fnx-portal-title h2 { font-size: 1.8rem; color: var(--navy); margin-top: 1rem; }
.fnx-portal-title p { color: var(--text2); }
.fnx-portal-cards { display: flex; gap: 2rem; max-width: 800px; margin: 0 auto; justify-content: center; }
.fnx-portal-card { flex: 1; max-width: 360px; background: var(--card); border: 2px solid var(--border); border-radius: 16px; padding: 2.5rem 2rem; text-align: center; transition: all 0.3s; }
.fnx-portal-customer:hover { border-color: var(--cyan); box-shadow: 0 8px 30px rgba(0,184,217,0.15); transform: translateY(-4px); }
.fnx-portal-customer { cursor: pointer; }
.fnx-portal-investigator { opacity: 0.6; }
.fnx-portal-card-icon { font-size: 2.5rem; margin-bottom: 1rem; }
.fnx-portal-card h3 { color: var(--navy); margin-bottom: 0.5rem; font-size: 1.2rem; }
.fnx-portal-card p { color: var(--text2); font-size: 0.9rem; margin-bottom: 1rem; }
.fnx-portal-card ul { text-align: left; padding-left: 1.2rem; margin-bottom: 1.5rem; color: var(--text2); font-size: 0.85rem; }
.fnx-portal-card ul li { margin-bottom: 0.3rem; }

/* ============ AUTH ============ */
.fnx-auth-page { display: flex; min-height: 100vh; }
.fnx-auth-left { flex: 0 0 45%; background: linear-gradient(135deg, var(--navy), var(--navy2)); color: #fff; display: flex; flex-direction: column; justify-content: center; padding: 4rem; }
.fnx-auth-brand { display: flex; align-items: center; gap: 0.7rem; margin-bottom: 2rem; cursor: pointer; }
.fnx-auth-brand span { font-size: 1.3rem; font-weight: 700; letter-spacing: 1.5px; }
.fnx-auth-left h2 { font-size: 1.6rem; font-weight: 600; margin-bottom: 0.75rem; line-height: 1.4; }
.fnx-auth-left p { color: rgba(255,255,255,0.6); }
.fnx-auth-right { flex: 1; display: flex; align-items: center; justify-content: center; padding: 2rem; background: var(--bg); }
.fnx-auth-box { width: 100%; max-width: 420px; }
.fnx-auth-tabs { display: flex; margin-bottom: 1.5rem; border-bottom: 2px solid var(--border); }
.fnx-auth-tabs button { flex: 1; padding: 0.75rem; border: none; background: none; font-size: 1rem; font-weight: 600; color: var(--text2); cursor: pointer; border-bottom: 2px solid transparent; margin-bottom: -2px; }
.fnx-auth-tabs button.active { color: var(--navy); border-bottom-color: var(--cyan); }
.fnx-auth-error { background: #FEF2F2; color: var(--critical); padding: 0.75rem 1rem; border-radius: 8px; margin-bottom: 1rem; font-size: 0.85rem; border: 1px solid #FECACA; }
.fnx-auth-form { display: flex; flex-direction: column; gap: 1rem; }
.fnx-auth-switch { text-align: center; font-size: 0.85rem; color: var(--text2); margin-top: 1rem; }
.fnx-auth-switch a { color: var(--cyan); cursor: pointer; font-weight: 600; }

/* ============ FORM FIELDS ============ */
.fnx-field { display: flex; flex-direction: column; gap: 0.3rem; flex: 1; }
.fnx-field label { font-size: 0.8rem; font-weight: 600; color: var(--text2); text-transform: uppercase; letter-spacing: 0.5px; }
.fnx-field input, .fnx-field select { padding: 0.7rem 0.9rem; border: 1.5px solid var(--border); border-radius: 8px; font-size: 0.9rem; background: var(--card); color: var(--text1); transition: border-color 0.2s; }
.fnx-field input:focus, .fnx-field select:focus { outline: none; border-color: var(--cyan); box-shadow: 0 0 0 3px rgba(0,184,217,0.1); }
.fnx-textarea { width: 100%; padding: 0.7rem 0.9rem; border: 1.5px solid var(--border); border-radius: 8px; font-size: 0.9rem; font-family: var(--font); resize: vertical; }
.fnx-textarea:focus { outline: none; border-color: var(--cyan); }
.fnx-form-row { display: flex; gap: 1rem; }

/* ============ BUTTONS ============ */
.fnx-btn { padding: 0.6rem 1.4rem; border-radius: 8px; font-weight: 600; font-size: 0.85rem; cursor: pointer; border: none; transition: all 0.25s; display: inline-flex; align-items: center; gap: 0.4rem; }
.fnx-btn-primary { background: var(--cyan); color: #fff; }
.fnx-btn-primary:hover { background: var(--cyan-dark); transform: translateY(-1px); }
.fnx-btn-outline { background: transparent; color: var(--cyan); border: 1.5px solid var(--cyan); }
.fnx-btn-outline:hover { background: rgba(0,184,217,0.08); }
.fnx-btn-ghost { background: transparent; color: rgba(255,255,255,0.8); border: 1.5px solid rgba(255,255,255,0.3); }
.fnx-btn-ghost:hover { background: rgba(255,255,255,0.08); color: #fff; }
.fnx-btn-lg { padding: 0.8rem 2rem; font-size: 0.95rem; }
.fnx-btn-sm { padding: 0.35rem 0.8rem; font-size: 0.78rem; }
.fnx-btn-full { width: 100%; justify-content: center; }
.fnx-btn-disabled { background: var(--border); color: var(--text2); cursor: not-allowed; }
.fnx-btn:disabled { opacity: 0.5; cursor: not-allowed; }

/* ============ MAIN LAYOUT ============ */
.fnx-main-layout { display: grid; grid-template-columns: var(--sidebar-w) 1fr; grid-template-rows: var(--header-h) 1fr; grid-template-areas: "header header" "sidebar content"; min-height: 100vh; }

/* HEADER */
.fnx-header { grid-area: header; background: var(--navy); color: #fff; display: flex; align-items: center; justify-content: space-between; padding: 0 1.5rem; position: sticky; top: 0; z-index: 100; border-bottom: 2px solid var(--cyan); }
.fnx-header-left { display: flex; align-items: center; gap: 0.75rem; }
.fnx-header-brand { display: flex; align-items: center; gap: 0.5rem; cursor: pointer; }
.fnx-header-brand span { font-weight: 700; font-size: 1.1rem; letter-spacing: 1px; }
.fnx-header-right { display: flex; align-items: center; gap: 0.75rem; position: relative; }
.fnx-sidebar-toggle { background: none; border: none; color: #fff; font-size: 1.3rem; cursor: pointer; padding: 0.3rem; }
.fnx-icon-btn { background: none; border: none; color: #fff; font-size: 1.2rem; cursor: pointer; padding: 0.3rem 0.5rem; position: relative; border-radius: 6px; }
.fnx-icon-btn:hover { background: rgba(255,255,255,0.1); }
.fnx-notif-dot { position: absolute; top: 0; right: 0; width: 8px; height: 8px; background: var(--critical); border-radius: 50%; }
.fnx-lang-btn { background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: #fff; padding: 0.3rem 0.7rem; border-radius: 6px; font-size: 0.78rem; cursor: pointer; font-weight: 500; }
.fnx-lang-btn:hover { background: rgba(255,255,255,0.2); }
.fnx-profile-pill { display: flex; align-items: center; gap: 0.5rem; background: rgba(255,255,255,0.08); padding: 0.25rem 0.5rem 0.25rem 0.25rem; border-radius: 20px; }
.fnx-avatar { width: 28px; height: 28px; border-radius: 50%; background: var(--cyan); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.8rem; }
.fnx-profile-name { font-size: 0.82rem; font-weight: 500; }
.fnx-logout-btn { font-size: 0.9rem !important; }

/* Notifications */
.fnx-notif-dropdown { position: absolute; top: calc(var(--header-h) - 4px); right: 1rem; width: 300px; background: var(--card); border-radius: 12px; box-shadow: 0 12px 40px rgba(0,0,0,0.15); z-index: 200; color: var(--text1); overflow: hidden; }
.fnx-notif-header { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 1rem; border-bottom: 1px solid var(--border); }
.fnx-notif-header button { background: none; border: none; font-size: 1.2rem; cursor: pointer; color: var(--text2); }
.fnx-notif-item { padding: 0.75rem 1rem; border-bottom: 1px solid var(--border); cursor: pointer; font-size: 0.85rem; }
.fnx-notif-item:hover { background: var(--bg); }
.fnx-notif-empty { padding: 1.5rem; text-align: center; color: var(--text2); font-size: 0.85rem; }

/* SIDEBAR */
.fnx-sidebar { grid-area: sidebar; background: var(--navy); padding-top: 1rem; transition: width 0.3s; overflow: hidden; }
.fnx-sidebar.collapsed { width: 60px; }
.fnx-nav { display: flex; flex-direction: column; gap: 0.25rem; padding: 0 0.5rem; }
.fnx-nav-item { display: flex; align-items: center; gap: 0.75rem; padding: 0.7rem 0.9rem; color: rgba(255,255,255,0.65); text-decoration: none; border-radius: 8px; cursor: pointer; transition: all 0.2s; font-size: 0.88rem; font-weight: 500; }
.fnx-nav-item:hover { background: var(--navy2); color: #fff; }
.fnx-nav-item.active { background: rgba(0,184,217,0.15); color: var(--cyan); border-left: 3px solid var(--cyan); }
.fnx-nav-icon { font-size: 1.15rem; min-width: 24px; text-align: center; }
.fnx-sidebar.collapsed .fnx-nav-label { display: none; }

/* CONTENT */
.fnx-content { grid-area: content; padding: 1.5rem 2rem; overflow-y: auto; max-height: calc(100vh - var(--header-h)); }

/* ============ DASHBOARD ============ */
.fnx-welcome h2 { font-size: 1.5rem; color: var(--navy); margin-bottom: 0.25rem; }
.fnx-welcome p { color: var(--text2); margin-bottom: 1.5rem; }
.fnx-stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem; margin-bottom: 1.5rem; }
.fnx-stat-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1.25rem; display: flex; align-items: center; gap: 1rem; transition: box-shadow 0.2s; }
.fnx-stat-card:hover { box-shadow: 0 4px 15px rgba(0,0,0,0.06); }
.fnx-stat-icon { font-size: 1.8rem; }
.fnx-stat-val { font-size: 1.8rem; font-weight: 800; color: var(--navy); }
.fnx-stat-label { font-size: 0.78rem; color: var(--text2); font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
.fnx-action-row { display: flex; gap: 1rem; margin-bottom: 2rem; }
.fnx-cta { background: linear-gradient(135deg, var(--cyan), var(--cyan-dark)); }
.fnx-cta:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0,184,217,0.3); }

.fnx-section { margin-bottom: 2rem; }
.fnx-section h3 { font-size: 1.1rem; color: var(--navy); margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border); }
.fnx-empty { text-align: center; padding: 2rem; color: var(--text2); background: var(--card); border-radius: 12px; border: 1px dashed var(--border); }

/* TABLE */
.fnx-table { width: 100%; border-collapse: separate; border-spacing: 0; background: var(--card); border-radius: 12px; overflow: hidden; border: 1px solid var(--border); }
.fnx-table th { background: var(--bg); padding: 0.7rem 1rem; text-align: left; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text2); }
.fnx-table td { padding: 0.7rem 1rem; border-top: 1px solid var(--border); font-size: 0.85rem; }
.fnx-table tr:hover td { background: rgba(0,184,217,0.03); }

/* BADGES */
.fnx-badge { padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.3px; }
.fnx-badge-lg { font-size: 0.85rem; padding: 0.35rem 1rem; }
.sev-critical { background: #FEF2F2; color: var(--critical); }
.sev-high { background: #FFF7ED; color: #EA580C; }
.sev-medium { background: #FFFBEB; color: #D97706; }
.sev-low { background: #F0FDF4; color: var(--success); }
.st-new { background: #EFF6FF; color: #2563EB; }
.st-progress { background: #FFFBEB; color: #D97706; }
.st-resolved { background: #F0FDF4; color: var(--success); }

/* AWARENESS */
.fnx-awareness-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
.fnx-awareness-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1.25rem; text-align: center; transition: all 0.3s; }
.fnx-awareness-card:hover { border-color: var(--cyan); transform: translateY(-2px); }
.fnx-aw-icon { font-size: 1.8rem; margin-bottom: 0.5rem; }
.fnx-awareness-card h4 { color: var(--navy); margin-bottom: 0.4rem; font-size: 0.9rem; }
.fnx-awareness-card p { color: var(--text2); font-size: 0.78rem; line-height: 1.5; }

/* ============ REPORT WIZARD ============ */
.fnx-report h2 { color: var(--navy); margin-bottom: 1.5rem; }
.fnx-wizard-progress { display: flex; gap: 0.5rem; margin-bottom: 2rem; }
.fnx-wizard-step { display: flex; flex-direction: column; align-items: center; gap: 0.3rem; flex: 1; cursor: pointer; }
.fnx-ws-num { width: 32px; height: 32px; border-radius: 50%; background: var(--border); color: var(--text2); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.8rem; transition: all 0.3s; }
.fnx-wizard-step.active .fnx-ws-num { background: var(--cyan); color: #fff; box-shadow: 0 0 0 4px rgba(0,184,217,0.2); }
.fnx-wizard-step.done .fnx-ws-num { background: var(--success); color: #fff; }
.fnx-ws-label { font-size: 0.68rem; color: var(--text2); font-weight: 500; text-transform: uppercase; }
.fnx-wizard-body { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 2rem; }
.fnx-wizard-body h3 { color: var(--navy); margin-bottom: 1.25rem; font-size: 1.15rem; }
.fnx-wizard-actions { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid var(--border); }

/* Type Selection */
.fnx-type-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; }
.fnx-type-card { padding: 1rem; border: 2px solid var(--border); border-radius: 10px; text-align: center; cursor: pointer; font-weight: 500; font-size: 0.88rem; transition: all 0.2s; }
.fnx-type-card:hover { border-color: var(--cyan); background: rgba(0,184,217,0.04); }
.fnx-type-card.selected { border-color: var(--cyan); background: rgba(0,184,217,0.08); color: var(--navy); }

/* Financial choices */
.fnx-choice-row { display: flex; gap: 0.75rem; margin-bottom: 1.5rem; }
.fnx-choice-btn { padding: 0.8rem 2rem; border: 2px solid var(--border); border-radius: 10px; background: var(--card); cursor: pointer; font-weight: 600; font-size: 0.9rem; transition: all 0.2s; }
.fnx-choice-btn:hover { border-color: var(--cyan); }
.fnx-choice-btn.selected { border-color: var(--cyan); background: rgba(0,184,217,0.08); color: var(--navy); }
.fnx-financial-section { padding-top: 1rem; border-top: 1px solid var(--border); display: flex; flex-direction: column; gap: 1rem; }

/* Review */
.fnx-review-card { background: var(--bg); border-radius: 10px; padding: 1.5rem; }
.fnx-review-row { display: flex; gap: 1rem; padding: 0.5rem 0; border-bottom: 1px solid var(--border); font-size: 0.88rem; }
.fnx-review-row span:first-child { color: var(--text2); min-width: 140px; font-weight: 500; }
.fnx-review-row:last-child { border-bottom: none; }

/* ============ TRACK CASES ============ */
.fnx-track h2 { color: var(--navy); margin-bottom: 1.5rem; }
.fnx-case-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1rem; }
.fnx-case-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1.25rem; cursor: pointer; transition: all 0.2s; }
.fnx-case-card:hover { border-color: var(--cyan); box-shadow: 0 4px 15px rgba(0,0,0,0.06); transform: translateY(-2px); }
.fnx-case-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
.fnx-case-meta { display: flex; gap: 0.5rem; align-items: center; margin-top: 0.3rem; color: var(--text2); font-size: 0.82rem; }

/* Mini Timeline */
.fnx-mini-timeline { display: flex; gap: 4px; margin-top: 0.75rem; }
.fnx-mt-step { flex: 1; height: 4px; border-radius: 2px; background: var(--border); }
.fnx-mt-step.reached { background: var(--cyan); }

/* ============ CASE DETAIL ============ */
.fnx-back-link { background: none; border: none; color: var(--cyan); cursor: pointer; font-size: 0.88rem; font-weight: 500; padding: 0; margin-bottom: 1rem; display: inline-block; }
.fnx-back-link:hover { text-decoration: underline; }
.fnx-case-detail-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; }
.fnx-case-detail-header h2 { color: var(--navy); }
.fnx-detail-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.fnx-detail-item { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 0.75rem 1rem; }
.fnx-detail-item label { font-size: 0.72rem; font-weight: 600; text-transform: uppercase; color: var(--text2); letter-spacing: 0.5px; display: block; margin-bottom: 0.25rem; }
.fnx-detail-desc { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; margin-bottom: 1.5rem; }
.fnx-detail-desc label { font-size: 0.72rem; font-weight: 600; text-transform: uppercase; color: var(--text2); letter-spacing: 0.5px; }
.fnx-detail-desc p { margin-top: 0.5rem; font-size: 0.9rem; line-height: 1.6; white-space: pre-wrap; }

/* Timeline */
.fnx-timeline { display: flex; justify-content: space-between; position: relative; padding: 1rem 0; }
.fnx-timeline::before { content: ''; position: absolute; top: 50%; left: 5%; right: 5%; height: 3px; background: var(--border); transform: translateY(-50%); }
.fnx-tl-step { display: flex; flex-direction: column; align-items: center; gap: 0.5rem; position: relative; z-index: 1; }
.fnx-tl-dot { width: 18px; height: 18px; border-radius: 50%; background: var(--border); border: 3px solid var(--bg); transition: all 0.3s; }
.fnx-tl-step.reached .fnx-tl-dot { background: var(--cyan); }
.fnx-tl-step.current .fnx-tl-dot { background: var(--cyan); box-shadow: 0 0 0 4px rgba(0,184,217,0.25); }
.fnx-tl-label { font-size: 0.72rem; font-weight: 600; color: var(--text2); text-transform: uppercase; }
.fnx-tl-step.reached .fnx-tl-label { color: var(--navy); }

/* Evidence */
.fnx-evidence-list { display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1.5rem; }
.fnx-ev-item { display: flex; align-items: center; gap: 0.75rem; background: var(--bg); border-radius: 8px; padding: 0.75rem 1rem; }
.fnx-ev-icon { font-size: 1.3rem; }
.fnx-ev-info { font-size: 0.82rem; line-height: 1.5; }
.fnx-add-evidence { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 1.25rem; }
.fnx-add-evidence h4 { color: var(--navy); margin-bottom: 0.75rem; }

/* ============ SUCCESS ============ */
.fnx-success-page { display: flex; align-items: center; justify-content: center; min-height: 100vh; background: var(--bg); }
.fnx-success-card { text-align: center; background: var(--card); border-radius: 16px; padding: 3rem; box-shadow: 0 8px 30px rgba(0,0,0,0.08); max-width: 480px; }
.fnx-success-icon { font-size: 3rem; margin-bottom: 1rem; }
.fnx-success-card h2 { color: var(--navy); margin-bottom: 1rem; }
.fnx-success-case-id { font-size: 2rem; font-weight: 800; color: var(--cyan); margin-bottom: 1rem; letter-spacing: 1px; }
.fnx-success-actions { display: flex; flex-direction: column; gap: 0.75rem; margin-top: 1.5rem; }

/* ============ AI ASSISTANT ============ */
.fnx-ai-fab { position: fixed; bottom: 1.5rem; right: 1.5rem; background: linear-gradient(135deg, var(--cyan), var(--cyan-dark)); color: #fff; padding: 0.8rem 1.5rem; border-radius: 30px; cursor: pointer; font-weight: 600; font-size: 0.88rem; box-shadow: 0 4px 20px rgba(0,184,217,0.4); z-index: 300; transition: all 0.3s; }
.fnx-ai-fab:hover { transform: translateY(-2px); box-shadow: 0 6px 25px rgba(0,184,217,0.5); }
.fnx-ai-panel { position: fixed; bottom: 5rem; right: 1.5rem; width: 360px; height: 480px; background: var(--card); border-radius: 16px; box-shadow: 0 12px 40px rgba(0,0,0,0.15); z-index: 300; display: flex; flex-direction: column; overflow: hidden; border: 1px solid var(--border); }
.fnx-ai-header { display: flex; justify-content: space-between; align-items: center; padding: 0.8rem 1rem; background: var(--navy); color: #fff; }
.fnx-ai-header button { background: none; border: none; color: #fff; font-size: 1.2rem; cursor: pointer; }
.fnx-ai-body { flex: 1; overflow-y: auto; padding: 1rem; display: flex; flex-direction: column; gap: 0.5rem; }
.fnx-ai-msg { padding: 0.7rem 1rem; border-radius: 12px; font-size: 0.85rem; line-height: 1.5; max-width: 85%; }
.fnx-ai-msg.user { background: var(--cyan); color: #fff; align-self: flex-end; border-bottom-right-radius: 4px; }
.fnx-ai-msg.ai { background: var(--bg); color: var(--text1); align-self: flex-start; border-bottom-left-radius: 4px; }
.fnx-ai-input { display: flex; border-top: 1px solid var(--border); }
.fnx-ai-input input { flex: 1; padding: 0.75rem 1rem; border: none; font-size: 0.85rem; }
.fnx-ai-input input:focus { outline: none; }
.fnx-ai-input button { background: var(--cyan); color: #fff; border: none; padding: 0 1rem; cursor: pointer; font-size: 1.1rem; }

/* ============ HELP ============ */
.fnx-help h2 { color: var(--navy); margin-bottom: 1.5rem; }
.fnx-help-cards { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
.fnx-help-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; }
.fnx-help-card h4 { color: var(--navy); margin-bottom: 0.5rem; }
.fnx-help-card p { color: var(--text2); font-size: 0.85rem; line-height: 1.6; }

/* ============ EVIDENCE VAULT ============ */
.fnx-ev-vault h2 { color: var(--navy); margin-bottom: 1.5rem; }
.fnx-ev-case-group { margin-bottom: 1.5rem; }
.fnx-ev-case-group h4 { color: var(--navy); margin-bottom: 0.75rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border); }

/* ============ RESPONSIVE ============ */
@media (max-width: 768px) {
    .fnx-hero { flex-direction: column; padding: 3rem 1.5rem; text-align: center; }
    .fnx-hero-visual { display: none; }
    .fnx-hero-btns { justify-content: center; }
    .fnx-features { grid-template-columns: repeat(3, 1fr); padding: 2rem 1.5rem; }
    .fnx-portal-cards { flex-direction: column; }
    .fnx-auth-page { flex-direction: column; }
    .fnx-auth-left { display: none; }
    .fnx-main-layout { grid-template-columns: 1fr; grid-template-areas: "header" "content"; }
    .fnx-sidebar { display: none; }
    .fnx-stats-row { grid-template-columns: 1fr; }
    .fnx-type-grid { grid-template-columns: repeat(2, 1fr); }
    .fnx-form-row { flex-direction: column; }
    .fnx-awareness-grid { grid-template-columns: repeat(2, 1fr); }
    .fnx-detail-grid { grid-template-columns: 1fr; }
}
"""

# ============================================================
# DEPLOY TO SERVICENOW
# ============================================================
print("=" * 60)
print("PHASE 2 - STEP 4: DEPLOY CUSTOMER EXPERIENCE WIDGET")
print("=" * 60)

# Update widget
payload = {
    "template": template,
    "css": css,
    "client_script": client_script,
    "script": server_script
}

r = requests.patch(
    f"{url}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth, headers=headers, json=payload
)

if r.status_code == 200:
    print(f"[SUCCESS] Widget fnx_customer_experience updated: {r.status_code}")
else:
    print(f"[ERROR] Widget update failed: {r.status_code}")
    print(r.text[:500])

# Also update the UI Page for direct access
print("\n--- Updating UI Page (fnx_portal.do) ---")
ui_page_html = f"""<!DOCTYPE html>
<html>
<head>
<title>FRAUDNEXUS - Financial & Cyber Fraud Investigation Hub</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="FRAUDNEXUS - From Fraud Report to Resolution. Secure fraud reporting, case tracking, and intelligent investigation.">
<style>body{{margin:0;padding:0;}}iframe{{width:100%;height:100vh;border:none;}}</style>
</head>
<body>
<iframe src="/fnx" title="FRAUDNEXUS Customer Portal"></iframe>
</body>
</html>"""

r_ui = requests.get(
    f"{url}/api/now/table/sys_ui_page?sysparm_query=name=fnx_portal&sysparm_fields=sys_id",
    auth=auth, headers=headers
)
ui_pages = r_ui.json().get('result', [])
if ui_pages:
    requests.patch(
        f"{url}/api/now/table/sys_ui_page/{ui_pages[0]['sys_id']}",
        auth=auth, headers=headers,
        json={"html": ui_page_html}
    )
    print("[SUCCESS] UI Page fnx_portal updated")

print("\n" + "=" * 60)
print("STEP 4 COMPLETE: Customer Experience Widget Deployed")
print("=" * 60)
