var api = {};
api.controller = function($scope, $http, $timeout, $window) {
    var c = this;
var API = '/api/2229367/fnx_api';
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
            enterPortal: 'Enter Customer Portal',
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
            viewCase: 'View Details',
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
institution: 'Institution / Organization Name',
            institutionType: 'Institution Type',
branch: 'Branch / Location Identifier',
            referenceType: 'Reference Type',
referenceValue: 'Transaction Reference / UTR',
            amountInvolved: 'Estimated Amount Lost (INR)',
            currency: 'Currency',
suspectName: 'Suspect / Beneficiary Name or Phone',
            suspectContact: 'Suspect Contact Information',
            channel: 'Communication Channel',
            location: 'Location',
            area: 'Area',
            pincode: 'Pincode',
digitalPlatform: 'Digital Platform / App / Website',
            evidenceType: 'Evidence Type',
            evidenceDesc: 'Evidence Description',
            next: 'Next Step',
            back: 'Back',
            review: 'Review & Submit',
            submit: 'Submit Fraud Report',
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
            reportAnother: 'Report Another Case',
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
            enterPortal: 'வாடிக்கையாளர் போர்டல் நுழை',
            comingSoon: 'விரைவில்',
            login: 'உள்நுழை',
            register: 'பதிவு செய்',
            email: 'மின்னஞ்சல் முகவரி',
            password: 'கடவுச்சொல்',
            confirmPassword: 'கடவுச்சொல்லை உறுதிப்படுத்து',
            fullName: 'முழு பெயர்',
            mobile: 'அலைபேசி எண்',
            forgotPassword: 'கடவுச்சொல் மறந்துவிட்டதா?',
            noAccount: 'கணக்கு இல்லையா?',
            hasAccount: 'ஏற்கனவே கணக்கு உள்ளதா?',
            dashboard: 'டாஷ்போர்டு',
            reportFraud: 'மோசடி புகார் செய்',
            trackCases: 'வழக்குகளைக் காண்க',
            evidence: 'ஆதாரப் பெட்டகம்',
            helpSupport: 'உதவி & ஆதரவு',
            welcome: 'வணக்கம்',
            totalCases: 'மொத்த வழக்குகள்',
            activeCases: 'செயலில் உள்ள வழக்குகள்',
            resolvedCases: 'தீர்க்கப்பட்ட வழக்குகள்',
            recentCases: 'சமீபத்திய வழக்குகள்',
            caseId: 'வழக்கு எண்',
            incidentType: 'சம்பவ வகை',
            date: 'தேதி',
            severity: 'தீவிரம்',
            status: 'நிலை',
            viewCase: 'விவரம்',
            noCases: 'வழக்குகள் இல்லை. மோசடி புகார் செய்ய தொடங்கவும்.',
            whatHappened: 'என்ன நடந்தது?',
            describeIncident: 'சம்பவத்தை விரிவாக விவரிக்கவும்...',
            incidentDate: 'சம்பவ தேதி',
            incidentTime: 'சம்பவ நேரம் (விருப்பம்)',
            financialInvolvement: 'நிதி இழப்பு உள்ளதா?',
            yes: 'ஆம்',
            no: 'இல்லை',
            notSure: 'தெரியவில்லை',
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
    c.navigate = function(view) {
        c.currentView = view;
        c.showNotifications = false;
        c.showAI = false;
        if (view === 'dashboard' || view === 'trackCases') {
            c.loadCases();
        }
    };
    c.goToPortalSelect = function() {
        c.currentView = 'portalSelect';
    };
    c.goToAuth = function(mode) {
        c.authMode = mode || 'login';
        c.currentView = 'auth';
    };
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
                c.authError = d.error || 'Login failed. Please check your credentials.';
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
    c.wizardStep = 1;
    c.fraudTypes = [
'Payment Fraud', 'UPI Fraud', 'Credit/Debit Card Fraud', 'Identity Theft',
        'Phishing Scam', 'Investment Fraud', 'Cryptocurrency Fraud', 'Loan Scam',
        'Job Scam', 'Lottery Scam', 'Social Media Impersonation', 'Account Takeover',
        'SIM Swap Fraud', 'Other Financial Fraud', 'Other Cyber Fraud'
    ];
c.paymentModes = ['UPI', 'Credit/Debit Card', 'Net Banking', 'Cryptocurrency', 'Wire Transfer', 'Cash', 'Other'];
c.institutionTypes = ['Bank', 'Payment Gateway / Wallet', 'Crypto Exchange', 'Telecom / ISP', 'E-Commerce', 'Other'];
    c.referenceTypes = ['UTR Number', 'Transaction ID', 'Reference Number', 'Order ID', 'Wallet Txn ID', 'Hash'];
c.evidenceTypes = ['Screenshot', 'Bank Statement', 'Transaction Receipt', 'Chat Export', 'Email Header', 'Audio Recording', 'Video', 'Document/PDF', 'Other'];
    c.severities = ['Low', 'Medium', 'High', 'Critical'];
    c.report = {
        type: '', description: '', incident_date: '', incident_time: '',
        financial_involvement: 'No', payment_mode: '', institution_name: '',
        institution_type: '', branch: '', platform: '', reference_type: 'UTR Number',
        transaction_reference: '', exposure: '', currency: 'INR', transaction_date: '',
        direction: 'Debited (Money Lost)', transaction_status: 'Completed', number_of_transactions: 1,
        suspect_name: '', suspect_contact: '', suspect_identifier: '', communication_channel: '',
        location: '', area: '', pincode: '', digital_platform: '',
        evidence_type: '', evidence_description: '', attachment_name: '', severity: 'Medium'
    };
    c.isSubmitting = false;
    c.submitResult = null;
    c.nextStep = function() {
        if (c.wizardStep === 1 && !c.report.type) {
            alert('Please select an incident type.');
            return;
        }
        if (c.wizardStep === 2 && !c.report.description) {
            alert('Please describe what happened.');
            return;
        }
        if (c.wizardStep === 3 && c.report.financial_involvement !== 'Yes') {
            c.wizardStep = 5;
            return;
        }
        if (c.wizardStep < 7) {
            c.wizardStep++;
        }
    };
    c.prevStep = function() {
        if (c.wizardStep === 5 && c.report.financial_involvement !== 'Yes') {
            c.wizardStep = 3;
            return;
        }
        if (c.wizardStep > 1) {
            c.wizardStep--;
        }
    };
    c.goToStep = function(step) {
        c.wizardStep = step;
    };
    c.submitReport = function() {
        c.isSubmitting = true;
        var payload = angular.copy(c.report);
        payload.user_id = c.user.sys_id;
        payload.customer_id = (c.customer && c.customer.sys_id) || '';
$http.post(API + '/cases', payload)
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.submitResult = d;
                c.currentView = 'submitSuccess';
                c.loadCases();
            } else {
                alert('Submission failed: ' + (d.error || 'Please try again.'));
            }
            c.isSubmitting = false;
        }, function(err) {
            alert('Submission error. Please try again.');
            c.isSubmitting = false;
        });
    };
    c.startNewReport = function() {
        c.wizardStep = 1;
        c.report = {
            type: '', description: '', incident_date: '', incident_time: '',
            financial_involvement: 'No', payment_mode: '', institution_name: '',
            institution_type: '', branch: '', platform: '', reference_type: 'UTR Number',
            transaction_reference: '', exposure: '', currency: 'INR', transaction_date: '',
            direction: 'Debited (Money Lost)', transaction_status: 'Completed', number_of_transactions: 1,
            suspect_name: '', suspect_contact: '', suspect_identifier: '', communication_channel: '',
            location: '', area: '', pincode: '', digital_platform: '',
            evidence_type: '', evidence_description: '', attachment_name: '', severity: 'Medium'
        };
        c.submitResult = null;
        c.currentView = 'reportFraud';
    };
c.evidenceForm = { case_id: '', evidence_type: 'Document/PDF', evidence_description: '', attachment_name: '' };
    c.evidenceSubmitting = false;
    c.submitAdditionalEvidence = function(caseId) {
        c.evidenceSubmitting = true;
        var payload = {
            action: 'add_evidence',
            case_id: caseId || c.evidenceForm.case_id || (c.selectedCase && c.selectedCase.sys_id),
            user_id: c.user.sys_id,
            evidence_type: c.evidenceForm.evidence_type,
            evidence_description: c.evidenceForm.evidence_description,
            attachment_name: c.evidenceForm.attachment_name || 'evidence_file.pdf'
        };
$http.post(API + '/cases', payload)
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                alert('Additional evidence registered successfully: ' + (d.evidence_number || 'EV-' + d.evidence_id.substring(0,6)));
c.evidenceForm = { case_id: '', evidence_type: 'Document/PDF', evidence_description: '', attachment_name: '' };
                c.loadCases();
            }
            c.evidenceSubmitting = false;
        }, function() {
            alert('Failed to upload additional evidence.');
            c.evidenceSubmitting = false;
        });
    };
    c.sendAIMessage = function() {
        if (!c.aiInput || !c.aiInput.trim()) return;
        var q = c.aiInput.trim();
        c.aiMessages.push({ role: 'user', text: q });
        c.aiInput = '';
        var qLower = q.toLowerCase();
        var reply = "Thank you for reaching out to FRAUDNEXUS AI. ";
        if (qLower.indexOf('upi') >= 0 || qLower.indexOf('qr') >= 0 || qLower.indexOf('gpay') >= 0 || qLower.indexOf('phonepe') >= 0) {
reply += "For UPI/QR fraud: Immediately call 1930 (Cyber Crime Helpline) and report the transaction reference / UTR to your bank to request an immediate freeze of the beneficiary account.";
        } else if (qLower.indexOf('card') >= 0 || qLower.indexOf('atm') >= 0 || qLower.indexOf('otp') >= 0) {
reply += "For unauthorized Card / OTP debits: Block your card immediately via your bank mobile app and file a dispute under RBI's zero liability guidelines within 72 hours.";
        } else if (qLower.indexOf('invest') >= 0 || qLower.indexOf('crypto') >= 0 || qLower.indexOf('telegram') >= 0) {
reply += "For Investment / Telegram trading scams: Preserve all chat transcripts, deposit addresses, bank receipts, and suspect profile links. Submit them through the Report Fraud wizard under 'Investment Fraud'.";
        } else if (qLower.indexOf('status') >= 0 || qLower.indexOf('track') >= 0) {
            reply += "You can track the live status and forensic audit timeline of all your cases anytime by clicking 'Track Cases' on the left navigation sidebar.";
        } else {
            reply += "To protect your case, ensure you report the exact financial institution, transaction reference, and attach receipts or chat screenshots in the Evidence step.";
        }
        $timeout(function() {
            c.aiMessages.push({ role: 'ai', text: reply });
        }, 400);
    };
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
};
