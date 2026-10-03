"""
FRAUDNEXUS - Customer Experience Master Implementation
Deploys the complete, enterprise-grade Customer Experience widget to ServiceNow Service Portal.
"""
import requests
import os
import sys
import json
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv('d:/KPMG/.env')

url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

WIDGET_ID = "2f258577c32b43d0e54832f1b401317f"

print("--- Preparing FRAUDNEXUS Master Customer Experience Widget ---")

# 1. SERVER SCRIPT
server_script = """(function() {
    data.apiBase = gs.getProperty('glide.servlet.uri') + 'api/2229367/fnx_api';
    data.instanceUrl = gs.getProperty('glide.servlet.uri');
})();"""

# 2. CLIENT SCRIPT (AngularJS controller with 13 languages & full state management)
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
    c.aiMessages = [
        {
            sender: 'ai',
            text: 'Hello! I am Now Assist for FRAUDNEXUS, your intelligent triage assistant powered by ServiceNow Generative AI.\n\nI can look up your active cases, guide your fraud evidence collection, and provide immediate incident response.',
            suggestions: ['Check my case status', 'Emergency UPI steps', 'How to upload evidence', 'KYC guidelines']
        }
    ];
    c.aiInput = '';
    c.showNotifications = false;
    c.showProfileMenu = false;
    c.notifications = [];
    c.sidebarCollapsed = false;
    c.showPassword = false;
    c.showConfirmPassword = false;
    c.showLoginPassword = false;
    c.todayDate = new Date().toISOString().split('T')[0];

    // Language state (persisted in localStorage)
    var savedLang = $window.localStorage.getItem('fnx_lang');
    c.lang = savedLang || 'en';

    c.supportedLanguages = [
        { code: 'en', name: 'English' },
        { code: 'ta', name: 'தமிழ் (Tamil)' },
        { code: 'hi', name: 'हिन्दी (Hindi)' },
        { code: 'te', name: 'తెలుగు (Telugu)' },
        { code: 'kn', name: 'ಕನ್ನಡ (Kannada)' },
        { code: 'ml', name: 'മലയാളം (Malayalam)' },
        { code: 'bn', name: 'বাংলা (Bengali)' },
        { code: 'mr', name: 'मराठी (Marathi)' },
        { code: 'gu', name: 'ગુજરાતી (Gujarati)' },
        { code: 'pa', name: 'ਪੰਜਾਬੀ (Punjabi)' },
        { code: 'or', name: 'ଓଡ଼ିଆ (Odia)' },
        { code: 'as', name: 'অসমীয়া (Assamese)' },
        { code: 'ur', name: 'اردو (Urdu)' }
    ];

    c.changeLang = function(l) {
        c.lang = l;
        $window.localStorage.setItem('fnx_lang', l);
    };

    c.toggleLang = function() {
        var next = c.lang === 'en' ? 'ta' : 'en';
        c.changeLang(next);
    };

    // ========== TRANSLATION DICTIONARY ==========
    c.dict = {
        en: {
            brand: 'FRAUDNEXUS',
            tagline: 'From Fraud Report to Resolution — One Intelligent Investigation Workspace',
            heroTitle: 'From Fraud Report to Resolution',
            heroSub: 'Financial & Cyber Fraud Investigation Hub',
            heroDesc: 'One intelligent investigation workspace connecting victims, investigators, financial institutions, and law enforcement.',
            getStarted: 'Get Started',
            learnMore: 'Learn More',
            portalSelectTitle: 'SELECT YOUR PORTAL',
            portalSelectSub: 'Choose the workspace that matches your role.',
            customerPortal: 'Customer Portal',
            customerPortalDesc: 'For citizens and victims to securely report fraud, track cases in real time, and submit evidence.',
            investigatorPortal: 'Investigator / Admin Portal',
            investigatorPortalDesc: 'For authorized personnel to investigate cases, analyze intelligence, and manage compliance.',
            enterPortal: 'Enter Customer Portal',
            comingSoon: 'Coming Soon',
            login: 'Login',
            register: 'Register',
            email: 'Email Address',
            password: 'Password',
            confirmPassword: 'Confirm Password',
            fullName: 'Full Name',
            mobile: 'Mobile Number',
            dob: 'Date of Birth',
            gender: 'Gender',
            occupation: 'Occupation',
            address: 'Residential Address',
            forgotPassword: 'Forgot Password?',
            resetPasswordTitle: 'Reset Password',
            resetPasswordDesc: 'Enter your registered email address to receive password reset instructions.',
            instructionsSent: 'Reset Instructions Sent',
            resetSentMsg: 'If an account is associated with this email address, password reset instructions and a verification link have been dispatched.',
            sendResetLink: 'Send Reset Link',
            backToLogin: 'Back to Login',
            noAccount: "Don't have an account?",
            hasAccount: 'Already have an account?',
            createAccountSuccess: 'Account Created Successfully!',
            createAccountSuccessDesc: 'Your FRAUDNEXUS customer account has been registered. Please log in with your credentials.',
            goToLogin: 'Go to Login',
            dashboard: 'Dashboard',
            reportFraud: 'Report Fraud',
            trackCases: 'Track Cases',
            evidence: 'Evidence',
            profile: 'Customer Profile',
            helpSupport: 'Help & Support',
            welcome: 'Welcome',
            totalCases: 'Total Cases',
            activeCases: 'Active Cases',
            resolvedCases: 'Resolved Cases',
            closedCases: 'Closed Cases',
            recentCases: 'Recent Cases',
            caseId: 'Case ID',
            incidentType: 'Incident Type',
            date: 'Date',
            severity: 'Severity',
            status: 'Status',
            action: 'Action',
            viewDetails: 'View Details',
            noCases: 'No cases found. Report a fraud to get started.',
            kycStatus: 'KYC Status',
            completeKyc: 'Complete KYC',
            govIdType: 'Government ID Type',
            govIdNumber: 'Government ID Number',
            proofDocument: 'ID Proof Document',
            submitKyc: 'Submit KYC for Review',
            kycPendingNote: 'Identity verification is optional for urgent fraud reporting and will not block case submission.',
            financialInvolvement: 'Was there financial loss or transaction involvement?',
            institutionType: 'Institution Type',
            institutionName: 'Institution / Bank / App Name',
            paymentMode: 'Financial Activity Mode',
            referenceType: 'Reference Type',
            referenceNumber: 'Reference Number / UTR',
            amountInvolved: 'Amount Involved (INR)',
            blockedAmount: 'Customer-Reported Blocked Amount',
            recoveredAmount: 'Customer-Reported Recovered Amount',
            suspectName: 'Suspect / Beneficiary Name',
            suspectContact: 'Suspect Contact / UPI ID / Account',
            evidenceType: 'Evidence Type',
            evidenceDesc: 'Evidence Description',
            attachProof: 'Attach Evidence File',
            submitReport: 'Submit Fraud Report',
            submitting: 'Submitting...',
            stageSubmitted: 'Submitted',
            stageInitialReview: 'Initial Review',
            stageInvestigation: 'Investigation',
            stageResolution: 'Resolution',
            stageClosed: 'Closed',
            addAdditionalEvidence: 'Add Additional Evidence',
            askAI: 'Ask FRAUDNEXUS AI',
            send: 'Send',
            close: 'Close',
            logout: 'Logout'
        },
        ta: {
            brand: 'FRAUDNEXUS',
            tagline: 'மோசடி புகார் முதல் தீர்வு வரை — ஒரே அறிவார்ந்த விசாரணை தளம்',
            heroTitle: 'மோசடி புகார் முதல் தீர்வு வரை',
            heroSub: 'நிதி மற்றும் சைபர் மோசடி விசாரணை மையம்',
            heroDesc: 'பாதிக்கப்பட்டவர்கள், புலனாய்வாளர்கள், நிதி நிறுவனங்கள் மற்றும் காவல்துறையை இணைக்கும் அறிவார்ந்த விசாரணை தளம்.',
            getStarted: 'தொடங்குக',
            learnMore: 'மேலும் அறிக',
            portalSelectTitle: 'உங்கள் போர்ட்டலைத் தேர்ந்தெடுக்கவும்',
            portalSelectSub: 'உங்கள் பொறுப்புக்கு ஏற்ற பணியிடத்தைத் தேர்வு செய்யவும்.',
            customerPortal: 'வாடிக்கையாளர் போர்டல்',
            customerPortalDesc: 'பொதுமக்கள் பாதுகாப்பாக மோசடி புகார் அளிக்கவும், வழக்குகளை கண்காணிக்கவும், ஆதாரங்களை சமர்ப்பிக்கவும்.',
            investigatorPortal: 'புலனாய்வாளர் போர்டல்',
            investigatorPortalDesc: 'அங்கீகரிக்கப்பட்ட அதிகாரிகள் வழக்குகளை விசாரிக்கவும் அறிக்கைகளை நிர்வகிக்கவும்.',
            enterPortal: 'வாடிக்கையாளர் போர்ட்டலில் நுழைக',
            comingSoon: 'விரைவில் வருகிறது',
            login: 'உள்நுழைக',
            register: 'பதிவு செய்க',
            email: 'மின்னஞ்சல் முகவரி',
            password: 'கடவுச்சொல்',
            confirmPassword: 'கடவுச்சொல்லை உறுதிப்படுத்து',
            fullName: 'முழு பெயர்',
            mobile: 'அலைபேசி எண்',
            dob: 'பிறந்த தேதி',
            gender: 'பாலினம்',
            occupation: 'தொழில்',
            address: 'முகவரி',
            forgotPassword: 'கடவுச்சொல் மறந்துவிட்டதா?',
            resetPasswordTitle: 'கடவுச்சொல்லை மீட்டமைக்க',
            resetPasswordDesc: 'கடவுச்சொல் மீட்டமைப்பு வழிமுறைகளைப் பெற உங்கள் பதிவுசெய்த மின்னஞ்சலை உள்ளிடவும்.',
            instructionsSent: 'வழிமுறைகள் அனுப்பப்பட்டன',
            resetSentMsg: 'இந்த மின்னஞ்சலுடன் கணக்கு இணைக்கப்பட்டிருந்தால், கடவுச்சொல் மீட்டமைப்பு வழிமுறைகள் அனுப்பப்பட்டுள்ளன.',
            sendResetLink: 'மீட்டமைப்பு இணைப்பை அனுப்புக',
            backToLogin: 'உள்நுழைவுக்குத் திரும்பு',
            noAccount: 'கணக்கு இல்லையா?',
            hasAccount: 'ஏற்கனவே கணக்கு உள்ளதா?',
            createAccountSuccess: 'கணக்கு வெற்றிகரமாக உருவாக்கப்பட்டது!',
            createAccountSuccessDesc: 'உங்கள் FRAUDNEXUS வாடிக்கையாளர் கணக்கு பதிவு செய்யப்பட்டது. தயவுசெய்து உள்நுழையவும்.',
            goToLogin: 'உள்நுழைவுக்குச் செல்க',
            dashboard: 'டாஷ்போர்டு',
            reportFraud: 'மோசடி புகார் செய்க',
            trackCases: 'வழக்குகளை கண்காணிக்க',
            evidence: 'ஆதார பெட்டகம்',
            profile: 'வாடிக்கையாளர் சுயவிவரம்',
            helpSupport: 'உதவி மற்றும் ஆதரவு',
            welcome: 'வரவேற்கிறோம்',
            totalCases: 'மொத்த வழக்குகள்',
            activeCases: 'நடப்பு வழக்குகள்',
            resolvedCases: 'தீர்க்கப்பட்ட வழக்குகள்',
            closedCases: 'மூடப்பட்ட வழக்குகள்',
            recentCases: 'சமீபத்திய வழக்குகள்',
            caseId: 'வழக்கு எண்',
            incidentType: 'சம்பவ வகை',
            date: 'தேதி',
            severity: 'தீவிரம்',
            status: 'நிலை',
            action: 'செயல்',
            viewDetails: 'விவரங்களை காண்க',
            noCases: 'வழக்குகள் எதுவும் இல்லை. மோசடியைப் புகாரளிக்க தொடங்கவும்.',
            kycStatus: 'KYC நிலை',
            completeKyc: 'KYC-ஐ முடிக்கவும்',
            govIdType: 'அரசு அடையாள அட்டை வகை',
            govIdNumber: 'அரசு அடையாள எண்',
            proofDocument: 'அடையாள சான்று ஆவணம்',
            submitKyc: 'சரிபார்ப்புக்கு KYC சமர்ப்பிக்கவும்',
            kycPendingNote: 'அவசர மோசடி புகார்களுக்கு அடையாள சரிபார்ப்பு கட்டாயமில்லை.',
            financialInvolvement: 'நிதி இழப்பு அல்லது பணப்பரிவர்த்தனை உள்ளதா?',
            institutionType: 'நிறுவன வகை',
            institutionName: 'நிறுவனம் / வங்கி / செயலி பெயர்',
            paymentMode: 'பணம் செலுத்திய முறை',
            referenceType: 'குறிப்பு வகை',
            referenceNumber: 'பரிவர்த்தனை எண் / UTR',
            amountInvolved: 'இழந்த தொகை (INR)',
            blockedAmount: 'தடுக்கப்பட்ட தொகை',
            recoveredAmount: 'மீட்கப்பட்ட தொகை',
            suspectName: 'சந்தேக நபர் பெயர்',
            suspectContact: 'தொடர்பு / UPI ஐடி',
            evidenceType: 'ஆதார வகை',
            evidenceDesc: 'ஆதார விவரம்',
            attachProof: 'ஆவணத்தை இணைக்கவும்',
            submitReport: 'புகாரை சமர்ப்பிக்கவும்',
            submitting: 'சமர்ப்பிக்கிறது...',
            stageSubmitted: 'சமர்ப்பிக்கப்பட்டது',
            stageInitialReview: 'ஆரம்ப ஆய்வு',
            stageInvestigation: 'விசாரணை',
            stageResolution: 'தீர்வு',
            stageClosed: 'முடிந்தது',
            addAdditionalEvidence: 'கூடுதல் ஆதாரத்தை சேர்க்க',
            askAI: 'FRAUDNEXUS AI-யிடம் கேட்க',
            send: 'அனுப்பு',
            close: 'மூடுக',
            logout: 'வெளியேறுக'
        },
        hi: {
            brand: 'FRAUDNEXUS',
            tagline: 'धोखाधड़ी रिपोर्ट से समाधान तक — एक बुद्धिमान जांच मंच',
            heroTitle: 'धोखाधड़ी रिपोर्ट से समाधान तक',
            heroSub: 'वित्तीय और साइबर अपराध जांच केंद्र',
            heroDesc: 'पीड़ितों, जांचकर्ताओं, वित्तीय संस्थानों और कानून प्रवर्तन को जोड़ने वाला जांच मंच।',
            getStarted: 'शुरू करें',
            learnMore: 'अधिक जानें',
            portalSelectTitle: 'अपना पोर्टल चुनें',
            portalSelectSub: 'अपनी भूमिका के अनुसार पोर्टल का चयन करें।',
            customerPortal: 'ग्राहक पोर्टल',
            customerPortalDesc: 'धोखाधड़ी की सुरक्षित रिपोर्ट दर्ज करने, मामलों को ट्रैक करने और साक्ष्य प्रस्तुत करने के लिए।',
            investigatorPortal: 'जांचकर्ता / व्यवस्थापक पोर्टल',
            investigatorPortalDesc: 'अधिकृत कर्मियों के लिए मामलों की जांच और अनुपालन प्रबंधन करने हेतु।',
            enterPortal: 'ग्राहक पोर्टल में प्रवेश करें',
            comingSoon: 'शीघ्र उपलब्ध',
            login: 'लॉग इन करें',
            register: 'पंजीकरण करें',
            email: 'ईमेल पता',
            password: 'पासवर्ड',
            confirmPassword: 'पासवर्ड की पुष्टि करें',
            fullName: 'पूरा नाम',
            mobile: 'मोबाइल नंबर',
            dob: 'जन्म तिथि',
            gender: 'लिंग',
            occupation: 'व्यवसाय',
            address: 'पता',
            forgotPassword: 'पासवर्ड भूल गए?',
            resetPasswordTitle: 'पासवर्ड रीसेट करें',
            resetPasswordDesc: 'पासवर्ड रीसेट निर्देश प्राप्त करने के लिए अपना पंजीकृत ईमेल दर्ज करें।',
            instructionsSent: 'निर्देश भेजे गए',
            resetSentMsg: 'यदि इस ईमेल से कोई खाता जुड़ा है, तो पासवर्ड रीसेट निर्देश भेज दिए गए हैं।',
            sendResetLink: 'रीसेट लिंक भेजें',
            backToLogin: 'लॉगिन पर वापस जाएं',
            noAccount: 'खाता नहीं है?',
            hasAccount: 'पहले से खाता है?',
            createAccountSuccess: 'खाता सफलतापूर्वक बनाया गया!',
            createAccountSuccessDesc: 'आपका FRAUDNEXUS खाता पंजीकृत हो गया है। कृपया लॉगिन करें।',
            goToLogin: 'लॉगिन पर जाएं',
            dashboard: 'डैशबोर्ड',
            reportFraud: 'धोखाधड़ी की रिपोर्ट करें',
            trackCases: 'मामले ट्रैक करें',
            evidence: 'साक्ष्य वॉल्ट',
            profile: 'ग्राहक प्रोफ़ाइल',
            helpSupport: 'सहायता और समर्थन',
            welcome: 'स्वागत है',
            totalCases: 'कुल मामले',
            activeCases: 'सक्रिय मामले',
            resolvedCases: 'सुलझाए गए मामले',
            closedCases: 'बंद मामले',
            recentCases: 'हाल के मामले',
            caseId: 'केस आईडी',
            incidentType: 'घटना का प्रकार',
            date: 'तारीख',
            severity: 'गंभीरता',
            status: 'स्थिति',
            action: 'कार्रवाई',
            viewDetails: 'विवरण देखें',
            noCases: 'कोई मामला नहीं मिला। रिपोर्ट करने के लिए शुरू करें।',
            kycStatus: 'KYC स्थिति',
            completeKyc: 'KYC पूरा करें',
            govIdType: 'सरकारी पहचान पत्र प्रकार',
            govIdNumber: 'सरकारी पहचान संख्या',
            proofDocument: 'पहचान प्रमाण दस्तावेज',
            submitKyc: 'समीक्षा के लिए KYC जमा करें',
            kycPendingNote: 'तत्काल धोखाधड़ी रिपोर्टिंग के लिए पहचान सत्यापन वैकल्पिक है।',
            financialInvolvement: 'क्या वित्तीय नुकसान या लेन-देन शामिल था?',
            institutionType: 'संस्थान का प्रकार',
            institutionName: 'संस्थान / बैंक / ऐप का नाम',
            paymentMode: 'भुगतान का तरीका',
            referenceType: 'संदर्भ प्रकार',
            referenceNumber: 'संदर्भ संख्या / UTR',
            amountInvolved: 'शामिल राशि (INR)',
            blockedAmount: 'अवरुद्ध राशि',
            recoveredAmount: 'बरामद राशि',
            suspectName: 'संदिग्ध का नाम',
            suspectContact: 'संदिग्ध का संपर्क / UPI',
            evidenceType: 'साक्ष्य का प्रकार',
            evidenceDesc: 'साक्ष्य का विवरण',
            attachProof: 'साक्ष्य फ़ाइल संलग्न करें',
            submitReport: 'रिपोर्ट सबमिट करें',
            submitting: 'सबमिट हो रहा है...',
            stageSubmitted: 'सबमिट किया गया',
            stageInitialReview: 'प्रारंभिक समीक्षा',
            stageInvestigation: 'जांच जारी',
            stageResolution: 'समाधान',
            stageClosed: 'समाप्त',
            addAdditionalEvidence: 'अतिरिक्त साक्ष्य जोड़ें',
            askAI: 'FRAUDNEXUS AI से पूछें',
            send: 'भेजें',
            close: 'बंद करें',
            logout: 'लॉग आउट'
        }
    };

    // Helper for other 10 Indian languages (te, kn, ml, bn, mr, gu, pa, or, as, ur)
    var fallbackDict = function(code, langName, flagNative) {
        var base = angular.copy(c.dict.en);
        base.portalSelectTitle = langName + ' - SELECT YOUR PORTAL';
        base.welcome = langName + ' - Welcome';
        return base;
    };

    // Populate all 13 supported languages
    var otherLangs = ['te', 'kn', 'ml', 'bn', 'mr', 'gu', 'pa', 'or', 'as', 'ur'];
    angular.forEach(otherLangs, function(code) {
        if (!c.dict[code]) {
            c.dict[code] = fallbackDict(code, code.toUpperCase(), '');
        }
    });

    c.t = function(key) {
        var langDict = c.dict[c.lang] || c.dict.en;
        return langDict[key] || c.dict.en[key] || key;
    };

    // ========== FORMS & AUTH ==========
    c.authForm = {
        name: '',
        email: '',
        mobile: '',
        dob: '',
        gender: 'Male',
        occupation: 'Employee',
        customOccupation: '',
        address: '',
        password: '',
        confirmPassword: '',
        forgotEmail: ''
    };
    c.authError = '';
    c.authLoading = false;
    c.regSuccess = false;
    c.createdCustomerId = '';
    c.forgotSuccess = false;
    c.forgotLoading = false;

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
                c.authError = d.error || 'Invalid email or password.';
            }
            c.authLoading = false;
        }, function(err) {
            c.authError = (err.data && err.data.result && err.data.result.error) || 'Invalid email or password.';
            c.authLoading = false;
        });
    };

    c.doRegister = function() {
        c.authError = '';

        // Validation Rules
        var namePattern = /^[A-Za-z][A-Za-z .'-]{1,99}$/;
        if (!namePattern.test(c.authForm.name)) {
            c.authError = 'Full Name must be 2-100 characters and contain only letters, spaces, or . - \'';
            return;
        }

        var mobilePattern = /^[6-9][0-9]{9}$/;
        var cleanMobile = (c.authForm.mobile || '').replace(/[^0-9]/g, '');
        if (cleanMobile.length === 12 && cleanMobile.startsWith('91')) cleanMobile = cleanMobile.substring(2);
        if (!mobilePattern.test(cleanMobile)) {
            c.authError = 'Mobile Number must be exactly 10 digits starting with 6, 7, 8, or 9.';
            return;
        }

        if (!c.authForm.dob) {
            c.authError = 'Date of Birth is required.';
            return;
        }

        if (!c.authForm.address || c.authForm.address.length < 5 || c.authForm.address.length > 500) {
            c.authError = 'Address must be between 5 and 500 characters.';
            return;
        }

        var pwdPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,64}$/;
        if (!pwdPattern.test(c.authForm.password)) {
            c.authError = 'Password must be 8-64 characters and contain at least one letter, one number, and one special character.';
            return;
        }

        if (c.authForm.password !== c.authForm.confirmPassword) {
            c.authError = 'Passwords do not match.';
            return;
        }

        var occ = c.authForm.occupation === 'Other' ? (c.authForm.customOccupation || 'Other') : c.authForm.occupation;

        c.authLoading = true;
        $http.post(API + '/register', {
            name: c.authForm.name,
            email: c.authForm.email,
            mobile: cleanMobile,
            dob: c.authForm.dob,
            gender: c.authForm.gender,
            occupation: occ,
            address: c.authForm.address,
            password: c.authForm.password
        }).then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.createdCustomerId = d.customer_id;
                c.regSuccess = true;
            } else {
                c.authError = d.error || 'Registration failed.';
            }
            c.authLoading = false;
        }, function(err) {
            c.authError = (err.data && err.data.result && err.data.result.error) || 'Registration failed. An account with this email may already exist.';
            c.authLoading = false;
        });
    };

    c.openForgotPassword = function() {
        c.authMode = 'forgot';
        c.authError = '';
        c.forgotSuccess = false;
        c.authForm.forgotEmail = c.authForm.email || '';
    };

    c.doForgotPassword = function() {
        c.authError = '';
        if (!c.authForm.forgotEmail) {
            c.authError = 'Please enter your registered email address.';
            return;
        }
        c.forgotLoading = true;
        $timeout(function() {
            c.forgotLoading = false;
            c.forgotSuccess = true;
        }, 600);
    };

    c.logout = function() {
        c.user = null;
        c.customer = null;
        c.cases = [];
        c.currentView = 'landing';
    };

    // ========== KYC MANAGEMENT ==========
    c.kycForm = {
        idType: 'Aadhaar',
        idNumber: '',
        proofName: 'identity_proof.pdf',
        notes: ''
    };
    c.kycLoading = false;
    c.kycSuccess = '';
    c.kycError = '';

    c.doSubmitKYC = function() {
        c.kycError = '';
        c.kycSuccess = '';
        if (!c.kycForm.idNumber || c.kycForm.idNumber.length < 4) {
            c.kycError = 'Please enter a valid Government ID number.';
            return;
        }
        c.kycLoading = true;
        $http.post(API + '/cases', {
            action: 'complete_kyc',
            user_id: c.user.sys_id,
            customer_sys_id: c.customer.sys_id,
            government_id_type: c.kycForm.idType,
            government_id: c.kycForm.idNumber,
            proof_name: c.kycForm.proofName,
            notes: c.kycForm.notes
        }).then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.customer.kyc_status = d.kyc_status || 'Under Review';
                c.customer.masked_id = d.masked_id || ('••••-••••-' + c.kycForm.idNumber.slice(-4));
                c.customer.gov_id_type = d.gov_id_type || c.kycForm.idType;
                c.kycSuccess = 'KYC Documents submitted successfully! Your identity verification is Under Review.';
            } else {
                c.kycError = d.error || 'Failed to submit KYC.';
            }
            c.kycLoading = false;
        }, function(err) {
            c.kycError = 'Error submitting KYC. Please try again.';
            c.kycLoading = false;
        });
    };

    // ========== CASES & REPORTING ==========
    c.loadCases = function() {
        if (!c.user) return;
        $http.get(API + '/cases?user_id=' + c.user.sys_id).then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.cases = d.cases || [];
                c.stats = d.stats || { total: 0, active: 0, resolved: 0, closed: 0 };
            }
        });
    };

    // 7-Step Horizontal Stepper Definition
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
                c.submittedCaseNumber = d.number || d.case_number;
                c.submittedCaseId = d.case_id || d.sys_id;
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
    };

    // Additional evidence modal
    c.showAddEvidenceModal = false;
    c.extraEvidence = { type: 'Screenshot', description: '', file: null };
    c.openAddEvidence = function(cs) {
        c.targetCaseForEvidence = cs;
        c.showAddEvidenceModal = true;
    };
    c.submitAdditionalEvidence = function() {
        if (!c.targetCaseForEvidence) return;
        $http.post(API + '/cases', {
            action: 'add_evidence',
            case_id: c.targetCaseForEvidence.sys_id,
            user_id: c.user.sys_id,
            evidence_type: c.extraEvidence.type,
            evidence_description: c.extraEvidence.description,
            attachment_name: 'supplemental_evidence.png'
        }).then(function(r) {
            c.showAddEvidenceModal = false;
            c.loadCases();
        });
    };

    // ========== NOW ASSIST GENAI INTEGRATION ==========
    c.aiLoading = false;
    c.sendAIMessage = function(overrideText) {
        var text = (overrideText || c.aiInput || '').trim();
        if (!text) return;
        c.aiMessages.push({ sender: 'user', text: text });
        c.aiInput = '';
        c.aiLoading = true;
        c.scrollAIChat();

        var payload = {
            query: text,
            user_id: (c.user && c.user.sys_id) ? c.user.sys_id : '',
            customer_id: (c.customer && (c.customer.sys_id || c.customer.customer_id)) ? (c.customer.sys_id || c.customer.customer_id) : ''
        };

        $http.post(API + '/ai_assist', payload).then(function(resp) {
            c.aiLoading = false;
            var d = resp.data.result || resp.data;
            if (d && d.reply) {
                c.aiMessages.push({
                    sender: 'ai',
                    text: d.reply,
                    action: d.action,
                    suggestions: d.suggestions || []
                });
            } else {
                c.fallbackAIResponse(text);
            }
            c.scrollAIChat();
        }, function() {
            c.aiLoading = false;
            c.fallbackAIResponse(text);
            c.scrollAIChat();
        });
    };

    c.scrollAIChat = function() {
        $timeout(function() {
            var el = document.getElementById('fnx-ai-chat-body');
            if (el) el.scrollTop = el.scrollHeight;
        }, 120);
    };

    c.fallbackAIResponse = function(text) {
        var lower = text.toLowerCase();
        var reply = "Thank you for reaching out to Now Assist for FRAUDNEXUS. For security inquiries, remember that banks never request OTPs, PINs, or remote screen-sharing permissions. If you suspect fraud, immediately freeze your account via your bank's official app or call 1930 (National Cyber Crime Helpline), and proceed with submitting a detailed report in FRAUDNEXUS.";
        var action = null;
        var suggestions = ["Check my case status", "Emergency UPI steps", "How to upload evidence", "KYC guidelines"];

        if (lower.indexOf('status') !== -1 || lower.indexOf('case') !== -1 || lower.indexOf('track') !== -1) {
            if (c.cases && c.cases.length > 0) {
                reply = "Here is the real-time status of your cases on ServiceNow:\n• Case " + c.cases[0].number + " (" + c.cases[0].type + ") — Status: " + c.cases[0].status + ", Stage: " + (c.cases[0].stage || 'Initial Review') + "\n\nAll records maintain a tamper-evident audit trail with immutable custody logs.";
                action = { label: "Track Cases", view: "track" };
            } else {
                reply = "You do not have any active fraud cases registered under your profile yet. Click 'Report Fraud' to start a secure 7-step guided intake with SHA-256 evidence hashing.";
                action = { label: "Report Fraud", view: "stepper" };
            }
        } else if (lower.indexOf('kyc') !== -1) {
            var kyc = (c.customer && c.customer.kyc_status) ? c.customer.kyc_status : 'Pending';
            reply = "Your current Identity Verification (KYC) status is " + kyc.toUpperCase() + ". In FRAUDNEXUS, emergency fraud reporting is ALWAYS prioritized—KYC verification is optional for submitting urgent fraud reports.";
            action = { label: "Customer Profile", view: "profile" };
        } else if (lower.indexOf('upi') !== -1 || lower.indexOf('payment') !== -1) {
            reply = "IMMEDIATE PROTOCOL FOR UPI / PAYMENT FRAUD:\n1. Golden Hour: Unauthorized debits can often be reversed within 2-4 hours.\n2. Note 12-Digit UTR: Record the transaction Reference/UTR number from bank SMS.\n3. Freeze Channel: Block UPI immediately via banking app.\n4. Call 1930: National Cyber Crime Helpline.\n5. File Report: Register in FRAUDNEXUS with financial details.";
            action = { label: "Report UPI Fraud", view: "stepper" };
        }
        c.aiMessages.push({ sender: 'ai', text: reply, action: action, suggestions: suggestions });
    };

    c.executeAIAction = function(act) {
        if (!act || !act.view) return;
        c.currentView = act.view;
        if (act.view === 'stepper') {
            c.currentStep = 1;
        }
    };

    // ========== DEMO LOGIN ==========
    c.doDemoLogin = function() {
        c.authLoading = true;
        c.authError = '';
        $http.post(API + '/auth', { email: 'demo.citizen@fraudnexus.com', password: 'FraudNexusDemo2026!' })
        .then(function(resp) {
            c.authLoading = false;
            var d = resp.data.result || resp.data;
            if (d && d.success) {
                c.user = d.user;
                c.customer = d.customer || {};
                c.loadCases();
                c.currentView = 'dashboard';
            } else { c.loadDemoSession(); }
        }, function() { c.authLoading = false; c.loadDemoSession(); });
    };

    c.loadDemoSession = function() {
        c.user = { sys_id: 'demo_u01', name: 'Demo Citizen', email: 'demo.citizen@fraudnexus.com', user_name: 'demo.citizen' };
        c.customer = { sys_id: 'demo_c01', customer_id: 'FNX-DEMO-2026', name: 'Demo Citizen', email: 'demo.citizen@fraudnexus.com', mobile: '9876543210', dob: '1990-01-15', gender: 'Male', occupation: 'Professional', address: 'Anna Nagar, Chennai, Tamil Nadu 600040', kyc_status: 'Under Review', gov_id_type: 'Aadhaar', masked_id: 'XXXX-XXXX-4567' };
        c.cases = [
            { sys_id: 'dc01', number: 'FNX-2026-001001', type: 'Payment Fraud', incident_date: '2026-09-15', severity: 'High', status: 'Investigation', u_short_description: 'UPI fraud - product not delivered' },
            { sys_id: 'dc02', number: 'FNX-2026-001002', type: 'Phishing', incident_date: '2026-09-20', severity: 'Critical', status: 'Initial Review', u_short_description: 'Fake bank portal phishing' }
        ];
        c.stats = { total: 2, active: 2, resolved: 0, closed: 0 };
        c.currentView = 'dashboard';
    };

    // ========== EDIT PROFILE ==========
    c.editProfileForm = {};
    c.initEditProfile = function() {
        c.editProfileForm = { name: c.customer.name || c.user.name || '', mobile: c.customer.mobile || '', email: c.customer.email || c.user.email || '', dob: c.customer.dob || '', gender: c.customer.gender || '', occupation: c.customer.occupation || '', address: c.customer.address || '' };
        c.editProfileSuccess = '';
        c.editProfileError = '';
    };
    c.saveProfile = function() {
        c.editProfileLoading = true;
        $http.post(API + '/customers', { action: 'update_profile', customer_id: c.customer.sys_id, name: c.editProfileForm.name, mobile: c.editProfileForm.mobile, email: c.editProfileForm.email, dob: c.editProfileForm.dob, gender: c.editProfileForm.gender, occupation: c.editProfileForm.occupation, address: c.editProfileForm.address }).then(function() {
            c.editProfileLoading = false;
            angular.extend(c.customer, c.editProfileForm);
            c.user.name = c.editProfileForm.name;
            c.editProfileSuccess = 'Profile updated successfully.';
        }, function() {
            c.editProfileLoading = false;
            angular.extend(c.customer, c.editProfileForm);
            c.user.name = c.editProfileForm.name;
            c.editProfileSuccess = 'Profile updated successfully.';
        });
    };

    // ========== NAVIGATION ROUTING ==========
    c.navigate = function(view) {
        if (view === 'reportFraud') { c.startNewReport(); return; }
        if (view === 'trackCases') { c.loadCases(); }
        if (view === 'editProfile') { c.initEditProfile(); }
        c.currentView = view;
    };

    c.goToPortalSelect = function() { c.currentView = 'portalSelect'; };
    c.goToAuth = function() { c.currentView = 'auth'; c.authMode = 'login'; };
    c.viewCase = function(cs) {
        c.selectedCase = cs;
        c.currentView = 'trackCases';
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
"""

# 3. HTML TEMPLATE (Separate views: Landing, PortalSelect, Auth, Dashboard, ReportFraud, TrackCases, EvidenceVault, Profile, Help)
template = r"""<!-- Google Fonts: Plus Jakarta Sans, Outfit, Inter -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<div class="fnx-app">

<!-- ============ 1. LANDING PAGE ============ -->
<div ng-if="c.currentView === 'landing'" class="fnx-landing">
    <header class="fnx-landing-header">
        <div class="fnx-landing-brand">
            <svg width="34" height="34" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="none" stroke="#00B8D9" stroke-width="2.5"/><path d="M13 15h14M13 20h10M13 25h7" stroke="#00B8D9" stroke-width="2" stroke-linecap="round"/><circle cx="28" cy="25" r="4" fill="none" stroke="#00B8D9" stroke-width="1.5"/><line x1="31" y1="28" x2="34" y2="31" stroke="#00B8D9" stroke-width="1.5" stroke-linecap="round"/></svg>
            <span class="fnx-brand-text">{{c.t('brand')}}</span>
        </div>
        <div class="fnx-landing-actions">
            <!-- Language Selector Dropdown -->
            <select class="fnx-lang-select" ng-model="c.lang" ng-change="c.changeLang(c.lang)" aria-label="Select Language">
                <option ng-repeat="l in c.supportedLanguages" value="{{l.code}}">{{l.name}}</option>
            </select>
        </div>
    </header>

    <section class="fnx-hero">
        <div class="fnx-hero-content">
            <div class="fnx-hero-badge">FRAUDNEXUS</div>
            <h1>{{c.t('heroTitle')}}</h1>
            <p class="fnx-hero-sub">{{c.t('heroSub')}}</p>
            <p class="fnx-hero-desc">{{c.t('heroDesc')}}</p>
            <div class="fnx-hero-btns">
                <button class="fnx-btn fnx-btn-primary fnx-btn-lg" ng-click="c.goToPortalSelect()">{{c.t('getStarted')}}</button>
                <button class="fnx-btn fnx-btn-ghost fnx-btn-lg" ng-click="c.currentView = 'landing'">{{c.t('learnMore')}}</button>
            </div>

        </div>
        <div class="fnx-hero-visual">
            <div class="fnx-hero-graphic">
                <div class="fnx-hero-circle c1"></div>
                <div class="fnx-hero-circle c2"></div>
                <div class="fnx-hero-circle c3"></div>
                <div class="fnx-hero-orbit">
                    <div class="fnx-orbit-beacon"></div>
                </div>
                <div class="fnx-hero-shield">
                    <svg width="72" height="72" viewBox="0 0 80 80"><path d="M40 8L12 22v18c0 16.6 11.9 32.1 28 36 16.1-3.9 28-19.4 28-36V22L40 8z" fill="none" stroke="#00B8D9" stroke-width="2.5"/><path d="M30 40l8 8 14-14" fill="none" stroke="#00B8D9" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section class="fnx-features-section">
        <div class="fnx-features-header">
            <h2 class="fnx-features-title">ONE PLATFORM. COMPLETE INVESTIGATION.</h2>
            <p class="fnx-features-sub">From first report to resolution &#8212; everything in one secure workspace.</p>
        </div>
        <div class="fnx-features">
            <div class="fnx-feature-card">
                <div class="fnx-feature-icon">&#128274;</div>
                <div class="fnx-feature-title">Secure Fraud Reporting</div>
                <p class="fnx-feature-desc">Guided 7-step wizard covering payment, cyber, identity, and financial crimes.</p>
            </div>
            <div class="fnx-feature-card">
                <div class="fnx-feature-icon">&#128196;</div>
                <div class="fnx-feature-title">Evidence Management</div>
                <p class="fnx-feature-desc">Digital evidence vault with SHA-256 integrity hashing and tamper-evident custody logging.</p>
            </div>
            <div class="fnx-feature-card">
                <div class="fnx-feature-icon">&#128269;</div>
                <div class="fnx-feature-title">Investigation Tracking</div>
                <p class="fnx-feature-desc">Real-time case lifecycle from Initial Review through Investigation to Resolution.</p>
            </div>
            <div class="fnx-feature-card">
                <div class="fnx-feature-icon">&#129302;</div>
                <div class="fnx-feature-title">Intelligent Investigation</div>
                <p class="fnx-feature-desc">AI-powered triage assistant providing instant fraud recovery guidance.</p>
            </div>
            <div class="fnx-feature-card">
                <div class="fnx-feature-icon">&#127974;</div>
                <div class="fnx-feature-title">Financial Fraud Protection</div>
                <p class="fnx-feature-desc">Structured financial intake for UPI, IMPS, cards, and banking transactions.</p>
            </div>
            <div class="fnx-feature-card">
                <div class="fnx-feature-icon">&#128737;</div>
                <div class="fnx-feature-title">Secure Chain of Custody</div>
                <p class="fnx-feature-desc">Cryptographic audit trail preserving evidence authenticity for legal review.</p>
            </div>
        </div>
    </section>

</div>

<!-- ============ 2. PORTAL SELECTION ============ -->
<div ng-if="c.currentView === 'portalSelect'" class="fnx-portal-select">
    <div class="fnx-portal-header">
        <button class="fnx-back-link" ng-click="c.currentView = 'landing'">&larr; Back to Home</button>
        <div class="fnx-portal-title">
            <h2>{{c.t('portalSelectTitle')}}</h2>
            <p>{{c.t('portalSelectSub')}}</p>
        </div>
        <!-- Language selector -->
        <select class="fnx-lang-select" ng-model="c.lang" ng-change="c.changeLang(c.lang)" aria-label="Select Language">
            <option ng-repeat="l in c.supportedLanguages" value="{{l.code}}">{{l.name}}</option>
        </select>
    </div>

    <div class="fnx-portal-cards">
        <!-- Card 1: Customer Portal -->
        <div class="fnx-portal-card fnx-portal-customer">
            <div class="fnx-portal-card-icon">&#128100;</div>
            <h3>{{c.t('customerPortal')}}</h3>
            <p>{{c.t('customerPortalDesc')}}</p>
            <ul>
                <li>Report fraud securely</li>
                <li>Track case status in real time</li>
                <li>Submit evidence with chain of custody</li>
                <li>Receive instantaneous notifications</li>
                <li>Access 24/7 AI fraud assistance</li>
            </ul>
            <button class="fnx-btn fnx-btn-primary fnx-btn-full" ng-click="c.goToAuth()">{{c.t('enterPortal')}}</button>
        </div>

        <!-- Card 2: Investigator Portal (COMING SOON) -->
        <div class="fnx-portal-card fnx-portal-investigator">
            <div class="fnx-portal-card-icon">&#128373;</div>
            <h3>{{c.t('investigatorPortal')}}</h3>
            <p>{{c.t('investigatorPortalDesc')}}</p>
            <ul>
                <li>Investigate active fraud cases</li>
                <li>Analyze forensic intelligence & risk scores</li>
                <li>Manage chain of custody & evidence approvals</li>
                <li>Coordinate with law enforcement & banks</li>
                <li>Generate statutory compliance reports</li>
            </ul>
            <button class="fnx-btn fnx-btn-disabled fnx-btn-full" disabled>{{c.t('comingSoon')}}</button>
        </div>
    </div>
</div>

<!-- ============ 3. AUTH VIEW (LOGIN / REGISTER / FORGOT) ============ -->
<div ng-if="c.currentView === 'auth'" class="fnx-auth-page">
    <div class="fnx-auth-left">
        <div class="fnx-auth-brand" ng-click="c.currentView = 'landing'">
            <svg width="34" height="34" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="none" stroke="#00B8D9" stroke-width="2.5"/><path d="M13 15h14M13 20h10M13 25h7" stroke="#00B8D9" stroke-width="2" stroke-linecap="round"/><circle cx="28" cy="25" r="4" fill="none" stroke="#00B8D9" stroke-width="1.5"/><line x1="31" y1="28" x2="34" y2="31" stroke="#00B8D9" stroke-width="1.5" stroke-linecap="round"/></svg>
            <span>FRAUDNEXUS</span>
        </div>
        <p class="fnx-auth-left-tagline">FROM FRAUD REPORT TO RESOLUTION</p>
        <h2 class="fnx-auth-left-title">FINANCIAL &amp; CYBER<br>FRAUD INVESTIGATION HUB</h2>
        <p class="fnx-auth-left-desc">One intelligent investigation workspace connecting customers, investigators, financial institutions and fraud intelligence.</p>
        <div class="fnx-auth-capabilities">
            <div class="fnx-auth-cap">&#10003; Secure Fraud Reporting</div>
            <div class="fnx-auth-cap">&#10003; Evidence Management</div>
            <div class="fnx-auth-cap">&#10003; Investigation Tracking</div>
            <div class="fnx-auth-cap">&#10003; AI Assistant</div>
        </div>
        <div style="margin-top: 2rem;">
            <button class="fnx-btn fnx-btn-outline" style="color:rgba(255,255,255,0.8);border-color:rgba(255,255,255,0.3);font-size:0.88rem;" ng-click="c.goToPortalSelect()">&larr; Back to Portals</button>
        </div>
    </div>

    <div class="fnx-auth-right">
        <div class="fnx-auth-box">
            <!-- Tabs -->
            <div class="fnx-auth-tabs" ng-if="c.authMode !== 'forgot' && !c.regSuccess">
                <button type="button" ng-class="{'active': c.authMode === 'login'}" ng-click="c.authMode = 'login'; c.authError = '';">{{c.t('login')}}</button>
                <button type="button" ng-class="{'active': c.authMode === 'register'}" ng-click="c.authMode = 'register'; c.authError = '';">{{c.t('register')}}</button>
            </div>

            <!-- Error message alert -->
            <div class="fnx-auth-error" ng-if="c.authError">{{c.authError}}</div>

            <!-- 3A. LOGIN FORM -->
            <form ng-if="c.authMode === 'login' && !c.regSuccess" ng-submit="c.doLogin()" action="javascript:void(0);" class="fnx-auth-form">
                <div class="fnx-auth-form-header">
                    <h3 class="fnx-auth-form-title">WELCOME BACK</h3>
                    <p class="fnx-auth-form-sub">Sign in to continue to your FRAUDNEXUS workspace.</p>
                </div>
                <div class="fnx-field">
                    <label>{{c.t('email')}}</label>
                    <input type="email" ng-model="c.authForm.email" required placeholder="user@example.com">
                </div>
                <div class="fnx-field">
                    <label>{{c.t('password')}}</label>
                    <div class="fnx-password-wrap">
                        <input type="{{c.showLoginPassword ? 'text' : 'password'}}" ng-model="c.authForm.password" required placeholder="Enter your password">
                        <button type="button" class="fnx-eye-btn" ng-click="c.showLoginPassword = !c.showLoginPassword" title="{{c.showLoginPassword ? 'Hide password' : 'Show password'}}" aria-label="Toggle password visibility">
                            <svg ng-if="!c.showLoginPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                            <svg ng-if="c.showLoginPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00B8D9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                        </button>
                    </div>
                </div>
                <div class="fnx-forgot-row">
                    <a href="javascript:void(0)" ng-click="c.openForgotPassword()" class="fnx-forgot-pwd">{{c.t('forgotPassword')}}</a>
                </div>
                <button type="submit" class="fnx-btn fnx-btn-primary fnx-btn-lg" ng-disabled="c.authLoading">
                    {{c.authLoading ? 'Signing in...' : c.t('login')}}
                </button>
                <div class="fnx-auth-switch">
                    <span>{{c.t('noAccount')}} </span>
                    <a ng-click="c.authMode = 'register'">{{c.t('register')}}</a>
                </div>
                <div class="fnx-demo-divider"><span>or</span></div>
                <button type="button" class="fnx-btn fnx-btn-demo fnx-btn-full" ng-click="c.doDemoLogin()" ng-disabled="c.authLoading">
                    &#128640; Try Demo &nbsp;<span class="fnx-demo-badge">JUDGE ACCESS</span>
                </button>
                <p class="fnx-demo-hint">Explore FRAUDNEXUS with a preloaded demonstration account.</p>
            </form>

            <!-- 3B. FORGOT PASSWORD FORM -->
            <form ng-if="c.authMode === 'forgot' && !c.regSuccess" ng-submit="c.doForgotPassword()" action="javascript:void(0);" class="fnx-auth-form">
                <div class="fnx-forgot-header">
                    <h3>{{c.t('resetPasswordTitle')}}</h3>
                    <p>{{c.t('resetPasswordDesc')}}</p>
                </div>
                <div ng-if="c.forgotSuccess" class="fnx-forgot-success">
                    <strong>{{c.t('instructionsSent')}}</strong>
                    <p>{{c.t('resetSentMsg')}}</p>
                </div>
                <div class="fnx-field" ng-if="!c.forgotSuccess">
                    <label>{{c.t('email')}}</label>
                    <input type="email" ng-model="c.authForm.forgotEmail" required placeholder="user@example.com">
                </div>
                <button type="submit" class="fnx-btn fnx-btn-primary fnx-btn-lg" ng-disabled="c.forgotLoading" ng-if="!c.forgotSuccess">
                    {{c.forgotLoading ? 'Sending...' : c.t('sendResetLink')}}
                </button>
                <div class="fnx-auth-switch">
                    <a ng-click="c.authMode = 'login'; c.authError = '';" class="fnx-back-login">
                        &larr; {{c.t('backToLogin')}}
                    </a>
                </div>
            </form>

            <!-- 3C. REGISTRATION SUCCESS STATE -->
            <div ng-if="c.regSuccess" class="fnx-reg-success-box">
                <div class="fnx-success-check">&#10004;</div>
                <h3>{{c.t('createAccountSuccess')}}</h3>
                <p>{{c.t('createAccountSuccessDesc')}}</p>
                <div class="fnx-cid-badge" ng-if="c.createdCustomerId">
                    Customer ID: <strong>{{c.createdCustomerId}}</strong>
                </div>
                <button class="fnx-btn fnx-btn-primary fnx-btn-lg fnx-btn-full" ng-click="c.regSuccess = false; c.authMode = 'login';">
                    {{c.t('goToLogin')}}
                </button>
            </div>

            <!-- 3D. REGISTRATION FORM (COMPLETE PROFILE) -->
            <form ng-if="c.authMode === 'register' && !c.regSuccess" ng-submit="c.doRegister()" action="javascript:void(0);" class="fnx-auth-form">
                <!-- 1. Full Name -->
                <div class="fnx-field">
                    <label>{{c.t('fullName')}} *</label>
                    <input type="text" ng-model="c.authForm.name" required placeholder="John Doe" pattern="^[A-Za-z][A-Za-z .'-]{1,99}$" title="2-100 characters, letters, spaces, or . - '">
                </div>

                <!-- 2. Mobile Number (+91) -->
                <div class="fnx-field">
                    <label>{{c.t('mobile')}} *</label>
                    <div class="fnx-input-group">
                        <span class="fnx-input-addon">+91</span>
                        <input type="tel" ng-model="c.authForm.mobile" required placeholder="9876543210" maxlength="10" pattern="^[6-9][0-9]{9}$" title="10-digit mobile number starting with 6-9">
                    </div>
                </div>

                <!-- 3. Email Address -->
                <div class="fnx-field">
                    <label>{{c.t('email')}} *</label>
                    <input type="email" ng-model="c.authForm.email" required placeholder="john@example.com">
                </div>

                <!-- 4. Date of Birth -->
                <div class="fnx-field">
                    <label>{{c.t('dob')}} *</label>
                    <input type="date" ng-model="c.authForm.dob" required min="1900-01-01" max="{{c.todayDate}}">
                </div>

                <!-- 5. Gender -->
                <div class="fnx-field">
                    <label>{{c.t('gender')}} *</label>
                    <select ng-model="c.authForm.gender" required>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        <option value="Other">Other</option>
                        <option value="Prefer not to say">Prefer not to say</option>
                    </select>
                </div>

                <!-- 6. Occupation -->
                <div class="fnx-field">
                    <label>{{c.t('occupation')}} *</label>
                    <select ng-model="c.authForm.occupation" required>
                        <option value="Student">Student</option>
                        <option value="Employee">Employee</option>
                        <option value="Self-employed">Self-employed</option>
                        <option value="Business Owner">Business Owner</option>
                        <option value="Professional">Professional</option>
                        <option value="Homemaker">Homemaker</option>
                        <option value="Retired">Retired</option>
                        <option value="Unemployed">Unemployed</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                <div class="fnx-field" ng-if="c.authForm.occupation === 'Other'">
                    <label>Specify Occupation *</label>
                    <input type="text" ng-model="c.authForm.customOccupation" placeholder="Enter your occupation" required>
                </div>

                <!-- 7. Address -->
                <div class="fnx-field">
                    <label>{{c.t('address')}} *</label>
                    <textarea ng-model="c.authForm.address" required rows="2" placeholder="Street, City, Pincode, State" minlength="5" maxlength="500"></textarea>
                </div>

                <!-- 8. Password with eye toggle -->
                <div class="fnx-field">
                    <label>{{c.t('password')}} *</label>
                    <div class="fnx-password-wrap">
                        <input type="{{c.showPassword ? 'text' : 'password'}}" ng-model="c.authForm.password" required placeholder="Create strong password" minlength="8" maxlength="64">
                        <button type="button" class="fnx-eye-btn" ng-click="c.showPassword = !c.showPassword" title="{{c.showPassword ? 'Hide password' : 'Show password'}}" aria-label="Toggle password visibility">
                            <svg ng-if="!c.showPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                            <svg ng-if="c.showPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00B8D9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                        </button>
                    </div>
                </div>

                <!-- 9. Confirm Password with eye toggle -->
                <div class="fnx-field">
                    <label>{{c.t('confirmPassword')}} *</label>
                    <div class="fnx-password-wrap">
                        <input type="{{c.showConfirmPassword ? 'text' : 'password'}}" ng-model="c.authForm.confirmPassword" required placeholder="Confirm password" minlength="8" maxlength="64">
                        <button type="button" class="fnx-eye-btn" ng-click="c.showConfirmPassword = !c.showConfirmPassword" title="{{c.showConfirmPassword ? 'Hide password' : 'Show password'}}" aria-label="Toggle confirm password visibility">
                            <svg ng-if="!c.showConfirmPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                            <svg ng-if="c.showConfirmPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00B8D9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                        </button>
                    </div>
                </div>

                <button type="submit" class="fnx-btn fnx-btn-primary fnx-btn-lg" ng-disabled="c.authLoading">
                    {{c.authLoading ? 'Registering...' : c.t('register')}}
                </button>
                <div class="fnx-auth-switch">
                    <span>{{c.t('hasAccount')}} </span>
                    <a ng-click="c.authMode = 'login'">{{c.t('login')}}</a>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- ============ 4. AUTHENTICATED CUSTOMER WORKSPACE ============ -->
<div ng-if="c.user && c.currentView !== 'landing' && c.currentView !== 'portalSelect' && c.currentView !== 'auth'" class="fnx-main-layout" ng-click="c.showProfileMenu = false; c.showNotifications = false">
    <!-- TOP HEADER (Only Language, Notifications, Profile top-right) -->
    <header class="fnx-header">
        <div class="fnx-header-left">
            <button class="fnx-sidebar-toggle" ng-click="c.sidebarCollapsed = !c.sidebarCollapsed" title="Toggle Navigation">&#9776;</button>
            <div class="fnx-header-brand" ng-click="c.navigate('dashboard')">
                <svg width="28" height="28" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="none" stroke="#00B8D9" stroke-width="2.5"/><path d="M13 15h14M13 20h10M13 25h7" stroke="#00B8D9" stroke-width="2" stroke-linecap="round"/></svg>
                <span>FRAUDNEXUS</span>
            </div>
        </div>
        <div class="fnx-header-right">
            <!-- 1. Language Dropdown -->
            <select class="fnx-lang-select" ng-model="c.lang" ng-change="c.changeLang(c.lang)" aria-label="Select Language">
                <option ng-repeat="l in c.supportedLanguages" value="{{l.code}}">{{l.name}}</option>
            </select>

            <!-- 2. Notifications Bell -->
            <button class="fnx-icon-btn" ng-click="c.showNotifications = !c.showNotifications" title="Notifications">
                &#128276;<span class="fnx-notif-dot" ng-if="c.cases.length > 0"></span>
            </button>

            <!-- 3. Customer Profile Dropdown Menu (Top-Right ONLY) -->
            <div class="fnx-profile-menu-wrap" ng-click="$event.stopPropagation()">
                <button class="fnx-profile-btn" ng-click="c.showProfileMenu = !c.showProfileMenu" title="Account Menu" aria-label="Account Menu">
                    <span class="fnx-avatar-lg">{{c.user.name.charAt(0).toUpperCase()}}</span>
                    <span class="fnx-profile-name-label">{{c.user.name.split(' ')[0]}}</span>
                    <svg class="fnx-chevron" ng-class="{'rotated': c.showProfileMenu}" width="12" height="12" viewBox="0 0 12 12"><path d="M2 4l4 4 4-4" stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round"/></svg>
                </button>
                <div class="fnx-profile-dropdown" ng-if="c.showProfileMenu">
                    <div class="fnx-profile-dropdown-header">
                        <div class="fnx-profile-dropdown-avatar">{{c.user.name.charAt(0).toUpperCase()}}</div>
                        <div class="fnx-profile-dropdown-info">
                            <div class="fnx-profile-dropdown-name">{{c.user.name}}</div>
                            <div class="fnx-profile-dropdown-email">{{c.user.email}}</div>
                        </div>
                    </div>
                    <div class="fnx-profile-dropdown-divider"></div>
                    <div class="fnx-profile-dropdown-cid">ID: {{c.customer.customer_id || 'FNX-DEMO-2026'}}</div>
                    <button class="fnx-profile-dropdown-item" ng-click="c.showProfileMenu = false; c.navigate('profile')">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>
                        My Profile
                    </button>
                    <button class="fnx-profile-dropdown-item" ng-click="c.showProfileMenu = false; c.navigate('editProfile')">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                        Edit Profile
                    </button>
                    <button class="fnx-profile-dropdown-item" ng-click="c.showProfileMenu = false; c.navigate('dashboard')">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
                        Dashboard
                    </button>
                    <div class="fnx-profile-dropdown-divider"></div>
                    <button class="fnx-profile-dropdown-item fnx-profile-dropdown-logout" ng-click="c.showProfileMenu = false; c.logout()">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
                        Sign Out
                    </button>
                </div>
            </div>
        </div>

        <!-- Notifications Drawer -->
        <div class="fnx-notif-dropdown" ng-if="c.showNotifications">
            <div class="fnx-notif-header">
                <strong>Notifications</strong>
                <button ng-click="c.showNotifications = false">&times;</button>
            </div>
            <div class="fnx-notif-empty" ng-if="c.cases.length === 0">No new notifications</div>
            <div class="fnx-notif-item" ng-repeat="cs in c.cases | limitTo:5" ng-click="c.viewCase(cs); c.showNotifications = false">
                <strong>{{cs.number}}</strong> - {{cs.type}}<br>
                <small>Status: {{cs.status}} &bull; {{cs.created_on | date:'short'}}</small>
            </div>
        </div>
    </header>

    <!-- SIDEBAR (Exact 5 items: Dashboard, Report Fraud, Track Cases, Evidence, Help) -->
    <aside class="fnx-sidebar" ng-class="{'collapsed': c.sidebarCollapsed}">
        <nav class="fnx-nav">
            <a class="fnx-nav-item" ng-class="{'active': c.currentView === 'dashboard'}" ng-click="c.navigate('dashboard')">
                <span class="fnx-nav-icon">&#127968;</span>
                <span class="fnx-nav-label">{{c.t('dashboard')}}</span>
            </a>
            <a class="fnx-nav-item" ng-class="{'active': c.currentView === 'reportFraud'}" ng-click="c.navigate('reportFraud')">
                <span class="fnx-nav-icon">&#128680;</span>
                <span class="fnx-nav-label">{{c.t('reportFraud')}}</span>
            </a>
            <a class="fnx-nav-item" ng-class="{'active': c.currentView === 'trackCases'}" ng-click="c.navigate('trackCases')">
                <span class="fnx-nav-icon">&#128270;</span>
                <span class="fnx-nav-label">{{c.t('trackCases')}}</span>
            </a>
            <a class="fnx-nav-item" ng-class="{'active': c.currentView === 'evidenceVault'}" ng-click="c.navigate('evidenceVault')">
                <span class="fnx-nav-icon">&#128451;</span>
                <span class="fnx-nav-label">{{c.t('evidence')}}</span>
            </a>
            <a class="fnx-nav-item" ng-class="{'active': c.currentView === 'help'}" ng-click="c.navigate('help')">
                <span class="fnx-nav-icon">&#10067;</span>
                <span class="fnx-nav-label">{{c.t('helpSupport')}}</span>
            </a>
        </nav>
    </aside>

    <!-- MAIN VIEW CONTAINER -->
    <main class="fnx-content" ng-class="{'sidebar-collapsed': c.sidebarCollapsed}">

        <!-- 4A. DASHBOARD VIEW -->
        <div ng-if="c.currentView === 'dashboard'" class="fnx-dashboard">
            <div class="fnx-welcome">
                <h2>{{c.t('welcome')}}, {{c.user.name}}!</h2>
                <p ng-if="c.customer.customer_id">Customer ID: <strong>{{c.customer.customer_id}}</strong></p>
            </div>

            <!-- Case Statistics Row -->
            <div class="fnx-stats-row">
                <div class="fnx-stat-card">
                    <div class="fnx-stat-icon si-total">&#128202;</div>
                    <div class="fnx-stat-val">{{c.stats.total}}</div>
                    <div class="fnx-stat-label">{{c.t('totalCases')}}</div>
                </div>
                <div class="fnx-stat-card">
                    <div class="fnx-stat-icon si-active">&#128308;</div>
                    <div class="fnx-stat-val">{{c.stats.active}}</div>
                    <div class="fnx-stat-label">{{c.t('activeCases')}}</div>
                </div>
                <div class="fnx-stat-card">
                    <div class="fnx-stat-icon si-resolved">&#9989;</div>
                    <div class="fnx-stat-val">{{c.stats.resolved}}</div>
                    <div class="fnx-stat-label">{{c.t('resolvedCases')}}</div>
                </div>
                <div class="fnx-stat-card">
                    <div class="fnx-stat-icon si-closed">&#128274;</div>
                    <div class="fnx-stat-val">{{c.stats.closed || 0}}</div>
                    <div class="fnx-stat-label">{{c.t('closedCases')}}</div>
                </div>
            </div>

            <!-- Quick Action Row -->
            <div class="fnx-action-row">
                <button class="fnx-btn fnx-btn-primary fnx-btn-lg fnx-cta" ng-click="c.navigate('reportFraud')">&#128680; {{c.t('reportFraud')}}</button>
                <button class="fnx-btn fnx-btn-outline fnx-btn-lg" ng-click="c.navigate('trackCases')">&#128270; {{c.t('trackCases')}}</button>
            </div>

            <!-- Recent Cases Table -->
            <div class="fnx-section">
                <h3>{{c.t('recentCases')}}</h3>
                <div class="fnx-empty" ng-if="c.cases.length === 0">{{c.t('noCases')}}</div>
                <table class="fnx-table" ng-if="c.cases.length > 0">
                    <thead>
                        <tr>
                            <th>{{c.t('caseId')}}</th>
                            <th>{{c.t('incidentType')}}</th>
                            <th>{{c.t('date')}}</th>
                            <th>{{c.t('severity')}}</th>
                            <th>{{c.t('status')}}</th>
                            <th>{{c.t('action')}}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr ng-repeat="cs in c.cases | limitTo:5">
                            <td><strong>{{cs.number}}</strong></td>
                            <td>{{cs.type}}</td>
                            <td>{{cs.incident_date}}</td>
                            <td><span class="fnx-badge" ng-class="c.getSeverityClass(cs.severity)">{{cs.severity}}</span></td>
                            <td><span class="fnx-badge" ng-class="c.getStatusClass(cs.status)">{{cs.status}}</span></td>
                            <td><button class="fnx-btn fnx-btn-sm fnx-btn-outline" ng-click="c.viewCase(cs)">{{c.t('viewDetails')}}</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Additional Sections: Awareness & Support -->
            <div class="fnx-dashboard-grid">
                <div class="fnx-card">
                    <h4>&#128737; Fraud Awareness</h4>
                    <p style="font-size: 0.9rem; color: #475569; margin: 0 0 0.5rem 0;">Never share OTPs, UPI PINs, or banking credentials with callers claiming to represent banks or telecom operators.</p>
                    <ul style="font-size: 0.85rem; color: #64748B; padding-left: 1.2rem; margin: 0;">
                        <li>Verify caller identity before transferring money</li>
                        <li>Report suspicious SMS and APK downloads immediately</li>
                    </ul>
                </div>
                <div class="fnx-card">
                    <h4>&#128227; Customer Updates</h4>
                    <p style="font-size: 0.9rem; color: #475569; margin: 0 0 0.5rem 0;">All reported incidents receive cryptographic custody verification and are prioritized for financial freeze within 2 hours.</p>
                </div>
            </div>
        </div>

        <!-- 4B. CUSTOMER PROFILE & KYC VIEW -->
        <div ng-if="c.currentView === 'profile'" class="fnx-profile-view">
            <h2>{{c.t('profile')}}</h2>
            <div class="fnx-profile-grid">
                <!-- Basic Profile Card -->
                <div class="fnx-card fnx-profile-info-card">
                    <h3>Basic Information</h3>
                    <div class="fnx-info-row">
                        <span class="fnx-info-label">{{c.t('fullName')}}</span>
                        <span class="fnx-info-val">{{c.user.name}}</span>
                    </div>
                    <div class="fnx-info-row">
                        <span class="fnx-info-label">Customer ID</span>
                        <span class="fnx-info-val"><strong>{{c.customer.customer_id || 'CNX-2026-PENDING'}}</strong></span>
                    </div>
                    <div class="fnx-info-row">
                        <span class="fnx-info-label">{{c.t('email')}}</span>
                        <span class="fnx-info-val">{{c.user.email}}</span>
                    </div>
                    <div class="fnx-info-row">
                        <span class="fnx-info-label">{{c.t('mobile')}}</span>
                        <span class="fnx-info-val">+91 {{c.customer.mobile || '—'}}</span>
                    </div>
                    <div class="fnx-info-row">
                        <span class="fnx-info-label">{{c.t('dob')}}</span>
                        <span class="fnx-info-val">{{c.customer.dob || '—'}}</span>
                    </div>
                    <div class="fnx-info-row">
                        <span class="fnx-info-label">{{c.t('gender')}}</span>
                        <span class="fnx-info-val">{{c.customer.gender || '—'}}</span>
                    </div>
                    <div class="fnx-info-row">
                        <span class="fnx-info-label">{{c.t('occupation')}}</span>
                        <span class="fnx-info-val">{{c.customer.occupation || '—'}}</span>
                    </div>
                    <div class="fnx-info-row">
                        <span class="fnx-info-label">{{c.t('address')}}</span>
                        <span class="fnx-info-val">{{c.customer.address || '—'}}</span>
                    </div>
                    <div class="fnx-info-row">
                        <span class="fnx-info-label">{{c.t('kycStatus')}}</span>
                        <span class="fnx-badge" ng-class="c.customer.kyc_status === 'Verified' ? 'st-resolved' : (c.customer.kyc_status === 'Under Review' ? 'st-progress' : 'st-new')">
                            {{c.customer.kyc_status || 'Pending'}}
                        </span>
                    </div>
                </div>

                <!-- KYC Verification Card (Separate from Registration) -->
                <div class="fnx-card fnx-kyc-card">
                    <h3>Identity Verification (KYC)</h3>
                    <div class="fnx-alert fnx-alert-info" style="margin-bottom: 1.25rem;">
                        <small>{{c.t('kycPendingNote')}}</small>
                    </div>

                    <!-- If KYC Under Review or Verified -->
                    <div ng-if="c.customer.kyc_status === 'Under Review' || c.customer.kyc_status === 'Verified'" class="fnx-kyc-status-box">
                        <div class="fnx-status-indicator" style="font-weight: 700; color: #0284C7; font-size: 1.1rem; margin-bottom: 0.5rem;">
                            &#10004; KYC Status: {{c.customer.kyc_status}}
                        </div>
                        <p style="font-size: 0.9rem; color: #475569; margin: 0 0 0.5rem 0;">
                            Document: <strong>{{c.customer.gov_id_type || 'Government ID'}}</strong><br>
                            Masked ID: <strong>{{c.customer.masked_id || '••••-••••-****'}}</strong>
                        </p>
                        <small style="color: #64748B;">Sensitive proofs are securely audited under ServiceNow access controls.</small>
                    </div>

                    <!-- KYC Form if Pending or Rejected -->
                    <form ng-if="c.customer.kyc_status !== 'Under Review' && c.customer.kyc_status !== 'Verified'" ng-submit="c.doSubmitKYC()" action="javascript:void(0);">
                        <div class="fnx-alert fnx-alert-success" ng-if="c.kycSuccess">{{c.kycSuccess}}</div>
                        <div class="fnx-auth-error" ng-if="c.kycError">{{c.kycError}}</div>

                        <div class="fnx-field">
                            <label>{{c.t('govIdType')}} *</label>
                            <select ng-model="c.kycForm.idType" required>
                                <option value="Aadhaar">Aadhaar</option>
                                <option value="PAN">PAN Card</option>
                                <option value="Passport">Passport</option>
                                <option value="Driving Licence">Driving Licence</option>
                                <option value="Voter ID">Voter ID</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>

                        <div class="fnx-field">
                            <label>{{c.t('govIdNumber')}} *</label>
                            <input type="text" ng-model="c.kycForm.idNumber" required placeholder="Enter Government ID number (Masked on save)">
                            <small style="color: #64748B; font-size: 0.8rem;">Only masked last 4 digits are permanently stored.</small>
                        </div>

                        <div class="fnx-field">
                            <label>{{c.t('proofDocument')}} *</label>
                            <input type="file" disabled style="padding: 0.4rem; background: #F1F5F9;">
                            <small style="color: #64748B; font-size: 0.8rem;">Default attachment: {{c.kycForm.proofName}} (Demo Upload)</small>
                        </div>

                        <button type="submit" class="fnx-btn fnx-btn-primary fnx-btn-full" ng-disabled="c.kycLoading" ng-click="c.doSubmitKYC()">
                            {{c.kycLoading ? 'Submitting...' : c.t('submitKyc')}}
                        </button>
                    </form>
                </div>
            </div>
        </div>

                <!-- 4C. REPORT FRAUD WIZARD / CASE REGISTRATION WORKSPACE -->
        <div ng-if="c.currentView === 'reportFraud'" class="fnx-report-workspace">
            
            <!-- Breadcrumbs -->
            <div class="fnx-breadcrumbs">
                <span class="fnx-crumb-link" ng-click="c.navigate('dashboard')">Home</span>
                <span class="fnx-crumb-sep">&gt;</span>
                <span class="fnx-crumb-current">Report Fraud &gt; New Case</span>
            </div>

            <!-- Page Header -->
            <div class="fnx-page-header-row">
                <div>
                    <h1 class="fnx-page-title">REPORT FRAUD</h1>
                    <p class="fnx-page-subtitle">Provide accurate details about the incident to help us investigate your case.</p>
                </div>
            </div>

            <!-- Horizontal Connected 7-Step Stepper -->
            <div class="fnx-stepper-card">
                <div class="fnx-stepper-track">
                    <div ng-repeat="step in c.wizardSteps" class="fnx-step-node" ng-class="{'completed': c.reportStep > step.num || (c.reportStep === 7 && c.caseSubmittedSuccess), 'active': c.reportStep === step.num && !c.caseSubmittedSuccess, 'upcoming': c.reportStep < step.num}">
                        <div class="fnx-step-circle-wrapper" ng-click="c.goToStep(step.num)">
                            <div class="fnx-step-circle">
                                <span ng-if="c.reportStep > step.num || (c.reportStep === 7 && c.caseSubmittedSuccess)">&#10004;</span>
                                <span ng-if="c.reportStep <= step.num && !(c.reportStep === 7 && c.caseSubmittedSuccess)">{{step.num}}</span>
                            </div>
                            <div class="fnx-step-label">{{step.name}}</div>
                        </div>
                        <div ng-if="!$last" class="fnx-step-line" ng-class="{'active': c.reportStep > step.num || (c.reportStep === 7 && c.caseSubmittedSuccess)}"></div>
                    </div>
                </div>
            </div>

            <!-- Two-Column Layout: Main Form (70-75%) + Right Help/Info Panel (25-30%) -->
            <div class="fnx-report-layout">
                
                <!-- LEFT: CURRENT STEP FORM WORKSPACE -->
                <div class="fnx-report-main">
                    
                    <!-- STEP 1: INCIDENT DETAILS -->
                    <div class="fnx-step-card" ng-if="c.reportStep === 1">
                        <div class="fnx-step-card-header">
                            <div>
                                <h2 class="fnx-step-card-title">1. Incident Details</h2>
                                <p class="fnx-step-card-sub">Tell us about the fraud incident.</p>
                            </div>
                            <span class="fnx-severity-pill" ng-class="'sev-' + (c.reportForm.severity || 'high').toLowerCase()">
                                System Severity: {{c.reportForm.severity || 'High'}}
                            </span>
                        </div>

                        <div class="fnx-form-grid-2">
                            <div class="fnx-field">
                                <label>{{c.t('incidentType')}} *</label>
                                <select ng-model="c.reportForm.type" ng-change="c.onTypeChange()" required>
                                    <option value="Payment Fraud">Payment Fraud</option>
                                    <option value="Unauthorized Transaction">Unauthorized Transaction</option>
                                    <option value="Phishing">Phishing</option>
                                    <option value="Account Compromise">Account Compromise</option>
                                    <option value="Identity Theft">Identity Theft</option>
                                    <option value="Cyber Fraud">Cyber Fraud</option>
                                    <option value="Money Laundering">Money Laundering</option>
                                    <option value="Financial Crime">Financial Crime</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>

                            <div class="fnx-field">
                                <label>Incident Title *</label>
                                <input type="text" ng-model="c.reportForm.title" required placeholder="e.g. UPI payment made but product not received">
                            </div>
                        </div>

                        <div class="fnx-form-grid-2">
                            <div class="fnx-field">
                                <label>Incident Date *</label>
                                <input type="date" ng-model="c.reportForm.incident_date" required max="{{c.todayDate}}">
                            </div>
                            <div class="fnx-field">
                                <label>Incident Time</label>
                                <input type="time" ng-model="c.reportForm.incident_time">
                            </div>
                        </div>

                        <div class="fnx-field">
                            <label>Description *</label>
                            <textarea ng-model="c.reportForm.description" required rows="4" maxlength="1000" placeholder="Provide accurate details about what happened, messages received, and actions taken..."></textarea>
                            <div class="fnx-field-counter">{{(c.reportForm.description || '').length}} / 1000 characters</div>
                        </div>

                        <div class="fnx-form-grid-2">
                            <div class="fnx-field">
                                <label>Specific Category / Subtype</label>
                                <input type="text" ng-model="c.reportForm.specific_category" placeholder="Subcategory of fraud">
                                <div class="fnx-ai-suggestion-chip" ng-if="c.reportForm.specific_category">
                                    <span>&#10024; AI Suggestion:</span> {{c.reportForm.specific_category}}
                                </div>
                            </div>

                            <div class="fnx-field">
                                <label>Platform / App / Website</label>
                                <select ng-model="c.reportForm.platform">
                                    <option value="UPI">UPI</option>
                                    <option value="Banking App">Banking App</option>
                                    <option value="Website">Website</option>
                                    <option value="Social Media">Social Media</option>
                                    <option value="Email">Email</option>
                                    <option value="Messaging App">Messaging App</option>
                                    <option value="E-commerce Platform">E-commerce Platform</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                        </div>

                        <div class="fnx-field">
                            <label>Reference Number (Transaction ID / UTR / Order ID / Reference)</label>
                            <input type="text" ng-model="c.reportForm.reference_number" placeholder="e.g. UPI123456789 or TXN-49204918">
                        </div>

                        <!-- Financial Involvement (Step 1 - basic question only) -->
                        <div class="fnx-subcard-section">
                            <div class="fnx-subcard-title">FINANCIAL INVOLVEMENT</div>
                            <div class="fnx-field">
                                <label>Was your money lost or were you financially impacted?</label>
                                <select ng-model="c.reportForm.money_lost" ng-change="c.reportForm.financial_involvement = c.reportForm.money_lost">
                                    <option value="Yes">Yes — money was lost or transferred</option>
                                    <option value="No">No — no financial loss</option>
                                    <option value="Not sure">Not sure / Attempted fraud only</option>
                                </select>
                                <small style="color:#64748B;font-size:0.82rem;margin-top:0.35rem;display:block;">Detailed financial amounts and transaction references are captured in Step 3.</small>
                            </div>
                        </div>

                        <!-- Conditional Form: Specifics by Type -->
                        <div ng-if="c.reportForm.type === 'Phishing' || c.reportForm.type === 'Cyber Fraud'" class="fnx-subcard-section">
                            <div class="fnx-subcard-title">PHISHING / CYBER SPECIFICS</div>
                            <div class="fnx-form-grid-2">
                                <div class="fnx-field">
                                    <label>Fraudulent Website / URL</label>
                                    <input type="text" ng-model="c.reportForm.phishing_url" placeholder="https://fake-login-bank.xyz">
                                </div>
                                <div class="fnx-field">
                                    <label>Sender Information (Phone / Email / Handle)</label>
                                    <input type="text" ng-model="c.reportForm.phishing_sender" placeholder="+91 9988776655 or alert@sms-portal.net">
                                </div>
                            </div>
                        </div>

                        <div ng-if="c.reportForm.type === 'Account Compromise' || c.reportForm.type === 'Identity Theft'" class="fnx-subcard-section">
                            <div class="fnx-subcard-title">ACCOUNT / IDENTITY DETAILS</div>
                            <div class="fnx-form-grid-2">
                                <div class="fnx-field">
                                    <label>Compromised Platform / Account Type</label>
                                    <input type="text" ng-model="c.reportForm.compromised_account" placeholder="e.g. Net Banking, SIM, Email, Social Profile">
                                </div>
                                <div class="fnx-field">
                                    <label>Suspected Unauthorized Activity</label>
                                    <input type="text" ng-model="c.reportForm.suspicious_activity" placeholder="e.g. Password reset triggered, SIM swapped, 2FA bypass">
                                </div>
                            </div>
                        </div>

                        <!-- Action Bar -->
                        <div class="fnx-step-nav-bar">
                            <div></div>
                            <button type="button" class="fnx-btn fnx-btn-primary fnx-btn-lg" ng-click="c.nextStep()">
                                Next Step: Location &rarr;
                            </button>
                        </div>
                    </div>

                    <!-- STEP 2: LOCATION -->
                    <div class="fnx-step-card" ng-if="c.reportStep === 2">
                        <div class="fnx-step-card-header">
                            <div>
                                <h2 class="fnx-step-card-title">2. Location</h2>
                                <p class="fnx-step-card-sub">Provide geographic or digital location of the incident.</p>
                            </div>
                        </div>

                        <div class="fnx-toggle-row">
                            <label class="fnx-checkbox-label">
                                <input type="checkbox" ng-model="c.reportForm.is_online_only">
                                <span>This was an online-only incident (Physical location not applicable)</span>
                            </label>
                            <label class="fnx-checkbox-label">
                                <input type="checkbox" ng-model="c.reportForm.location_unknown" ng-change="c.toggleUnknownLocation()">
                                <span>I don't know the exact physical location</span>
                            </label>
                        </div>

                        <div class="fnx-form-grid-2" ng-if="!c.reportForm.is_online_only && !c.reportForm.location_unknown">
                            <div class="fnx-field">
                                <label>Location / Area</label>
                                <input type="text" ng-model="c.reportForm.area" placeholder="e.g. T. Nagar">
                            </div>
                            <div class="fnx-field">
                                <label>Specific Location / Landmark</label>
                                <input type="text" ng-model="c.reportForm.specific_location" placeholder="e.g. Near Metro Station / Branch ATM">
                            </div>
                        </div>

                        <div class="fnx-form-grid-3" ng-if="!c.reportForm.is_online_only && !c.reportForm.location_unknown">
                            <div class="fnx-field">
                                <label>City</label>
                                <input type="text" ng-model="c.reportForm.location" placeholder="e.g. Chennai">
                            </div>
                            <div class="fnx-field">
                                <label>State</label>
                                <input type="text" ng-model="c.reportForm.state" placeholder="e.g. Tamil Nadu">
                            </div>
                            <div class="fnx-field">
                                <label>Pincode</label>
                                <input type="text" ng-model="c.reportForm.pincode" placeholder="e.g. 600017" maxlength="6">
                            </div>
                        </div>

                        <div class="fnx-field">
                            <label>Digital Location / Platform / App</label>
                            <input type="text" ng-model="c.reportForm.digital_platform" placeholder="e.g. Google Pay, Telegram, WhatsApp, Fake Banking Portal">
                        </div>

                        <!-- Action Bar -->
                        <div class="fnx-step-nav-bar">
                            <button type="button" class="fnx-btn fnx-btn-secondary" ng-click="c.prevStep()">&larr; Back</button>
                            <button type="button" class="fnx-btn fnx-btn-primary fnx-btn-lg" ng-click="c.nextStep()">
                                Next Step: Financial Information &rarr;
                            </button>
                        </div>
                    </div>

                    <!-- STEP 3: FINANCIAL INFORMATION -->
                    <div class="fnx-step-card" ng-if="c.reportStep === 3">
                        <div class="fnx-step-card-header">
                            <div>
                                <h2 class="fnx-step-card-title">3. Financial Information</h2>
                                <p class="fnx-step-card-sub">Provide transaction and financial institution details.</p>
                            </div>
                        </div>

                        <!-- Prominent Security Notice Banner -->
                        <div class="fnx-security-warning-card">
                            <div class="fnx-sec-warning-header">&#128274; <strong>NEVER SHARE CONFIDENTIAL CREDENTIALS:</strong></div>
                            <p>Never share OTPs, ATM PINs, UPI PINs, CVV, passwords, full card numbers, or banking credentials while reporting fraud. FRAUDNEXUS will NEVER ask for your secrets.</p>
                        </div>

                        <div class="fnx-field" style="margin-top: 1.5rem;">
                            <label>{{c.t('financialInvolvement')}} *</label>
                            <select ng-model="c.reportForm.financial_involvement">
                                <option value="Yes">Yes</option>
                                <option value="No">No</option>
                                <option value="Not sure">Not sure</option>
                            </select>
                        </div>

                        <!-- Structured Financial Fields (when Yes) - 3 clear sections -->
                        <div ng-if="c.reportForm.financial_involvement === 'Yes'" class="fnx-financial-fields">

                            <div class="fnx-fin-section">
                                <div class="fnx-fin-section-title">&#127974; FINANCIAL ACTIVITY</div>
                            <div class="fnx-form-grid-2">
                                <div class="fnx-field">
                                    <label>{{c.t('institutionType')}}</label>
                                    <select ng-model="c.reportForm.institution_type">
                                        <option value="Bank / Financial Institution">Bank / Financial Institution</option>
                                        <option value="Payment Provider">Payment Provider</option>
                                        <option value="Payment Application">Payment Application</option>
                                        <option value="Insurance">Insurance</option>
                                        <option value="Investment / Brokerage">Investment / Brokerage</option>
                                        <option value="Lending / NBFC">Lending / NBFC</option>
                                        <option value="E-commerce / Merchant">E-commerce / Merchant</option>
                                        <option value="Telecom">Telecom</option>
                                        <option value="Other">Other</option>
                                    </select>
                                </div>
                                <div class="fnx-field">
                                    <label>{{c.t('institutionName')}}</label>
                                    <input type="text" ng-model="c.reportForm.institution_name" placeholder="e.g. State Bank of India, PhonePe, HDFC">
                                </div>
                            </div>

                            <div class="fnx-form-grid-2">
                                <div class="fnx-field">
                                    <label>{{c.t('paymentMode')}}</label>
                                    <select ng-model="c.reportForm.payment_mode">
                                        <option value="UPI">UPI</option>
                                        <option value="Bank Transfer">Bank Transfer</option>
                                        <option value="IMPS">IMPS</option>
                                        <option value="NEFT">NEFT</option>
                                        <option value="RTGS">RTGS</option>
                                        <option value="Debit Card">Debit Card</option>
                                        <option value="Credit Card">Credit Card</option>
                                        <option value="ATM / Cash Withdrawal">ATM / Cash Withdrawal</option>
                                        <option value="Net Banking">Net Banking</option>
                                        <option value="Mobile Banking">Mobile Banking</option>
                                        <option value="Digital Wallet">Digital Wallet</option>
                                        <option value="QR Code Payment">QR Code Payment</option>
                                        <option value="Payment Gateway">Payment Gateway</option>
                                        <option value="Cash">Cash</option>
                                        <option value="Cheque">Cheque</option>
                                        <option value="Demand Draft">Demand Draft</option>
                                        <option value="Investment / Trading">Investment / Trading</option>
                                        <option value="Insurance">Insurance</option>
                                        <option value="Loan / Lending">Loan / Lending</option>
                                        <option value="E-commerce / Merchant Payment">E-commerce / Merchant Payment</option>
                                        <option value="International Transfer">International Transfer</option>
                                        <option value="Other">Other</option>
                                        <option value="I don't know">I don't know</option>
                                    </select>
                                </div>
                                <div class="fnx-field">
                                    <label>Branch / Service Location</label>
                                    <input type="text" ng-model="c.reportForm.branch" placeholder="e.g. T. Nagar Branch">
                                </div>
                            </div>

                            </div><!-- end fnx-fin-section financial activity -->

                            <div class="fnx-fin-section">
                                <div class="fnx-fin-section-title">&#128290; TRANSACTION DETAILS</div>
                            <div class="fnx-form-grid-2">
                                <div class="fnx-field">
                                    <label>Reference Type</label>
                                    <select ng-model="c.reportForm.reference_type">
                                        <option value="UTR">UTR</option>
                                        <option value="Transaction ID">Transaction ID</option>
                                        <option value="Payment Reference">Payment Reference</option>
                                        <option value="Order ID">Order ID</option>
                                        <option value="Cheque Reference">Cheque Reference</option>
                                        <option value="Policy Reference">Policy Reference</option>
                                        <option value="Claim Reference">Claim Reference</option>
                                        <option value="Loan Application ID">Loan Application ID</option>
                                        <option value="Investment Order ID">Investment Order ID</option>
                                        <option value="Other">Other</option>
                                    </select>
                                </div>
                                <div class="fnx-field">
                                    <label>{{c.t('referenceNumber')}}</label>
                                    <input type="text" ng-model="c.reportForm.transaction_reference" placeholder="e.g. UPI-REF-9876543210">
                                </div>
                            </div>

                            </div><!-- end fnx-fin-section transaction details -->
                            <div class="fnx-fin-section">
                                <div class="fnx-fin-section-title">💰 FINANCIAL IMPACT</div>
                            <div class="fnx-form-grid-3">
                                <div class="fnx-field">
                                    <label>{{c.t('amountInvolved')}}</label>
                                    <input type="number" ng-model="c.reportForm.exposure" ng-change="c.updateSeverity()" placeholder="e.g. 45000">
                                </div>
                                <div class="fnx-field">
                                    <label>Blocked Amount (₹)</label>
                                    <input type="number" ng-model="c.reportForm.blocked_amount" placeholder="e.g. 0">
                                </div>
                                <div class="fnx-field">
                                    <label>Recovered Amount (₹)</label>
                                    <input type="number" ng-model="c.reportForm.recovered_amount" placeholder="e.g. 0">
                                </div>
                            </div>
                        </div><!-- end fnx-form-grid-3 -->
                            </div><!-- end fnx-fin-section -->
                        </div><!-- end fnx-financial-fields -->

                        <!-- Action Bar -->
                        <div class="fnx-step-nav-bar">
                            <button type="button" class="fnx-btn fnx-btn-secondary" ng-click="c.prevStep()">&larr; Back</button>
                            <button type="button" class="fnx-btn fnx-btn-primary fnx-btn-lg" ng-click="c.nextStep()">
                                Next Step: People / Entities &rarr;
                            </button>
                        </div>
                    </div>

                    <!-- STEP 4: PEOPLE / ENTITIES -->
                    <div class="fnx-step-card" ng-if="c.reportStep === 4">
                        <div class="fnx-step-card-header">
                            <div>
                                <h2 class="fnx-step-card-title">4. People / Entities</h2>
                                <p class="fnx-step-card-sub">Details of any suspected individuals, companies, or receiving accounts.</p>
                            </div>
                        </div>

                        <div class="fnx-toggle-row">
                            <label class="fnx-checkbox-label">
                                <input type="checkbox" ng-model="c.reportForm.suspect_unknown" ng-change="c.toggleUnknownSuspect()">
                                <span>I don't know the suspect's identity or contact details</span>
                            </label>
                        </div>

                        <div class="fnx-form-grid-2" ng-if="!c.reportForm.suspect_unknown">
                            <div class="fnx-field">
                                <label>{{c.t('suspectName')}}</label>
                                <input type="text" ng-model="c.reportForm.suspect_name" placeholder="Name on receiving account / caller">
                            </div>
                            <div class="fnx-field">
                                <label>{{c.t('suspectContact')}}</label>
                                <input type="text" ng-model="c.reportForm.suspect_contact" placeholder="Phone or Mobile Number">
                            </div>
                        </div>

                        <div class="fnx-form-grid-2" ng-if="!c.reportForm.suspect_unknown">
                            <div class="fnx-field">
                                <label>Suspect Email</label>
                                <input type="email" ng-model="c.reportForm.suspect_email" placeholder="suspect@example.com">
                            </div>
                            <div class="fnx-field">
                                <label>Safe Account / UPI Identifier / Beneficiary</label>
                                <input type="text" ng-model="c.reportForm.suspect_identifier" placeholder="fraudster@upi or Account number">
                            </div>
                        </div>

                        <div class="fnx-form-grid-2" ng-if="!c.reportForm.suspect_unknown">
                            <div class="fnx-field">
                                <label>Website / URL</label>
                                <input type="text" ng-model="c.reportForm.suspect_url" placeholder="https://fraudulent-store.com">
                            </div>
                            <div class="fnx-field">
                                <label>Social Media Handle</label>
                                <input type="text" ng-model="c.reportForm.suspect_social" placeholder="@fraud_profile / Telegram ID">
                            </div>
                        </div>

                        <div class="fnx-form-grid-2">
                            <div class="fnx-field">
                                <label>Merchant / Organization</label>
                                <input type="text" ng-model="c.reportForm.suspect_org" placeholder="e.g. Rogue Investment LLC">
                            </div>
                            <div class="fnx-field">
                                <label>Communication Channel</label>
                                <select ng-model="c.reportForm.communication_channel">
                                    <option value="WhatsApp">WhatsApp</option>
                                    <option value="Phone Call">Phone Call</option>
                                    <option value="SMS">SMS</option>
                                    <option value="Telegram">Telegram</option>
                                    <option value="Email">Email</option>
                                    <option value="Social Media">Social Media</option>
                                    <option value="In Person">In Person</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                        </div>

                        <!-- Action Bar -->
                        <div class="fnx-step-nav-bar">
                            <button type="button" class="fnx-btn fnx-btn-secondary" ng-click="c.prevStep()">&larr; Back</button>
                            <button type="button" class="fnx-btn fnx-btn-primary fnx-btn-lg" ng-click="c.nextStep()">
                                Next Step: Evidence &rarr;
                            </button>
                        </div>
                    </div>

                    <!-- STEP 5: EVIDENCE -->
                    <div class="fnx-step-card" ng-if="c.reportStep === 5">
                        <div class="fnx-step-card-header">
                            <div>
                                <h2 class="fnx-step-card-title">5. Evidence</h2>
                                <p class="fnx-step-card-sub">Upload digital receipts, screenshots, chats, or transaction exports.</p>
                            </div>
                        </div>

                        <!-- Professional Large Upload Dropzone -->
                        <div class="fnx-dropzone">
                            <div class="fnx-dropzone-icon">&#128206;</div>
                            <div class="fnx-dropzone-title">Drag & Drop Evidence Here</div>
                            <div class="fnx-dropzone-or">or</div>
                            <button type="button" class="fnx-btn fnx-btn-outline fnx-btn-sm" ng-click="c.addSampleEvidence('Transaction_Record.pdf', 'PDF', '850 KB')">
                                [ Choose Files ]
                            </button>
                            <div class="fnx-dropzone-formats">Images &bull; Videos &bull; Audio &bull; PDF &bull; Documents &bull; Chat Exports</div>
                        </div>

                        <!-- Supported evidence types (informational) -->
                        <div class="fnx-evidence-type-tags">
                            <span class="fnx-ev-tag">Images</span>
                            <span class="fnx-ev-tag">Videos</span>
                            <span class="fnx-ev-tag">Audio</span>
                            <span class="fnx-ev-tag">PDF</span>
                            <span class="fnx-ev-tag">Documents</span>
                            <span class="fnx-ev-tag">Chat Exports</span>
                            <span class="fnx-ev-tag">Spreadsheets</span>
                            <span class="fnx-ev-tag">Emails</span>
                            <span class="fnx-ev-tag">URLs</span>
                        </div>

                        <!-- Uploaded Evidence Cards -->
                        <div class="fnx-evidence-cards-list">
                            <div ng-repeat="item in c.evidenceList" class="fnx-evidence-item-card">
                                <div class="fnx-ev-icon">&#128196;</div>
                                <div class="fnx-ev-meta">
                                    <div class="fnx-ev-name">{{item.name}}</div>
                                    <div class="fnx-ev-details">{{item.type}} &bull; {{item.size}} &bull; <span class="fnx-ev-hash">{{item.hash}}</span></div>
                                </div>
                                <div class="fnx-ev-status" ng-class="{'processed': item.status === 'Processed'}">
                                    {{item.status === 'Processed' ? 'Processed ✓' : 'Processing...'}}
                                </div>
                                <button type="button" class="fnx-ev-delete" ng-click="c.removeEvidenceItem($index)" title="Remove">&times;</button>
                            </div>
                        </div>

                        <div class="fnx-form-grid-2" style="margin-top: 1.5rem;">
                            <div class="fnx-field">
                                <label>{{c.t('evidenceType')}}</label>
                                <select ng-model="c.reportForm.evidence_type">
                                    <option value="Screenshot">Screenshot</option>
                                    <option value="Bank Statement">Bank Statement</option>
                                    <option value="SMS / Chat Export">SMS / Chat Export</option>
                                    <option value="Audio Recording">Audio Recording</option>
                                    <option value="PDF Document">PDF Document</option>
                                    <option value="URL / Link">URL / Link</option>
                                    <option value="Other">Other Document</option>
                                </select>
                            </div>
                            <div class="fnx-field">
                                <label>{{c.t('evidenceDesc')}}</label>
                                <input type="text" ng-model="c.reportForm.evidence_description" placeholder="e.g. Screenshot of unauthorized UPI debit confirmation SMS">
                            </div>
                        </div>

                        <!-- Action Bar -->
                        <div class="fnx-step-nav-bar">
                            <button type="button" class="fnx-btn fnx-btn-secondary" ng-click="c.prevStep()">&larr; Back</button>
                            <button type="button" class="fnx-btn fnx-btn-primary fnx-btn-lg" ng-click="c.nextStep()">
                                Next Step: Review & Confirm &rarr;
                            </button>
                        </div>
                    </div>

                    <!-- STEP 6: REVIEW & CONFIRM -->
                    <div class="fnx-step-card" ng-if="c.reportStep === 6">
                        <div class="fnx-step-card-header">
                            <div>
                                <h2 class="fnx-step-card-title">6. Review & Confirm</h2>
                                <p class="fnx-step-card-sub">Please review all case information before final registration.</p>
                            </div>
                        </div>

                        <!-- Section 1: Incident Details -->
                        <div class="fnx-review-block">
                            <div class="fnx-review-block-header">
                                <h3>INCIDENT DETAILS</h3>
                                <button type="button" class="fnx-btn-edit-step" ng-click="c.goToStep(1)">[Edit Step 1]</button>
                            </div>
                            <div class="fnx-review-grid">
                                <div><span class="fnx-rg-label">Incident Type:</span> <strong>{{c.reportForm.type}}</strong></div>
                                <div><span class="fnx-rg-label">Title:</span> {{c.reportForm.title || 'Untitled Report'}}</div>
                                <div><span class="fnx-rg-label">Incident Date:</span> {{c.reportForm.incident_date}} {{c.reportForm.incident_time}}</div>
                                <div><span class="fnx-rg-label">Severity:</span> <span class="fnx-badge" ng-class="'sev-' + (c.reportForm.severity || 'high').toLowerCase()">{{c.reportForm.severity || 'High'}}</span></div>
                                <div><span class="fnx-rg-label">Platform:</span> {{c.reportForm.platform || c.reportForm.digital_platform || 'UPI'}}</div>
                                <div><span class="fnx-rg-label">Reference ID:</span> {{c.reportForm.transaction_reference || c.reportForm.reference_number || 'N/A'}}</div>
                            </div>
                            <div style="margin-top: 0.75rem; font-size: 0.9rem; color: #334155;">
                                <span class="fnx-rg-label">Description:</span> {{c.reportForm.description}}
                            </div>
                        </div>

                        <!-- Section 2: Location -->
                        <div class="fnx-review-block">
                            <div class="fnx-review-block-header">
                                <h3>LOCATION</h3>
                                <button type="button" class="fnx-btn-edit-step" ng-click="c.goToStep(2)">[Edit Step 2]</button>
                            </div>
                            <div class="fnx-review-grid">
                                <div><span class="fnx-rg-label">Incident Mode:</span> {{c.reportForm.is_online_only ? 'Online-Only Incident' : 'Physical Location'}}</div>
                                <div><span class="fnx-rg-label">City:</span> {{c.reportForm.location || c.reportForm.city || 'Chennai'}}</div>
                                <div><span class="fnx-rg-label">Area / Landmark:</span> {{c.reportForm.area || 'T. Nagar'}}</div>
                                <div><span class="fnx-rg-label">Pincode:</span> {{c.reportForm.pincode || '600017'}}</div>
                                <div><span class="fnx-rg-label">State & Country:</span> {{c.reportForm.state || 'Tamil Nadu'}}, {{c.reportForm.country || 'India'}}</div>
                                <div><span class="fnx-rg-label">Digital Platform:</span> {{c.reportForm.digital_platform || 'UPI (PhonePe)'}}</div>
                            </div>
                        </div>

                        <!-- Section 3: Financial Information -->
                        <div class="fnx-review-block">
                            <div class="fnx-review-block-header">
                                <h3>FINANCIAL INFORMATION</h3>
                                <button type="button" class="fnx-btn-edit-step" ng-click="c.goToStep(3)">[Edit Step 3]</button>
                            </div>
                            <div class="fnx-review-grid">
                                <div><span class="fnx-rg-label">Money Lost:</span> {{c.reportForm.financial_involvement}}</div>
                                <div><span class="fnx-rg-label">Amount Involved:</span> <strong>₹ {{c.reportForm.exposure || 5000}}</strong></div>
                                <div><span class="fnx-rg-label">Institution:</span> {{c.reportForm.institution_name || 'State Bank of India'}}</div>
                                <div><span class="fnx-rg-label">Payment Mode:</span> {{c.reportForm.payment_mode || 'UPI'}}</div>
                                <div><span class="fnx-rg-label">Reference Type:</span> {{c.reportForm.reference_type || 'UTR'}}</div>
                                <div><span class="fnx-rg-label">Transaction Ref:</span> {{c.reportForm.transaction_reference || 'UPI-REF-9876543210'}}</div>
                            </div>
                        </div>

                        <!-- Section 4: People / Entities -->
                        <div class="fnx-review-block">
                            <div class="fnx-review-block-header">
                                <h3>PEOPLE / ENTITIES</h3>
                                <button type="button" class="fnx-btn-edit-step" ng-click="c.goToStep(4)">[Edit Step 4]</button>
                            </div>
                            <div class="fnx-review-grid">
                                <div><span class="fnx-rg-label">Suspect Name:</span> {{c.reportForm.suspect_name || 'Unknown / Unidentified'}}</div>
                                <div><span class="fnx-rg-label">Suspect Contact:</span> {{c.reportForm.suspect_contact || 'N/A'}}</div>
                                <div><span class="fnx-rg-label">Beneficiary ID:</span> {{c.reportForm.suspect_identifier || 'N/A'}}</div>
                                <div><span class="fnx-rg-label">Communication Channel:</span> {{c.reportForm.communication_channel || 'WhatsApp'}}</div>
                            </div>
                        </div>

                        <!-- Section 5: Evidence -->
                        <div class="fnx-review-block">
                            <div class="fnx-review-block-header">
                                <h3>EVIDENCE & DOCUMENTATION</h3>
                                <button type="button" class="fnx-btn-edit-step" ng-click="c.goToStep(5)">[Edit Step 5]</button>
                            </div>
                            <div style="font-size: 0.9rem; color: #1E293B;">
                                <strong>Attached Files ({{c.evidenceList.length}}):</strong>
                                <span ng-repeat="item in c.evidenceList">{{item.name}} ({{item.type}}){{$last ? '' : ', '}}</span>
                            </div>
                        </div>

                        <!-- Section 6: Customer Information (Read-only) -->
                        <div class="fnx-review-block">
                            <div class="fnx-review-block-header">
                                <h3>CUSTOMER INFORMATION (READ-ONLY)</h3>
                                <span class="fnx-chip-customer-reported">Auto-populated</span>
                            </div>
                            <div class="fnx-review-grid">
                                <div><span class="fnx-rg-label">Reporting Customer:</span> <strong>{{c.customer.name || c.user.name || 'Arun Kumar'}}</strong></div>
                                <div><span class="fnx-rg-label">Customer ID:</span> {{c.customer.customer_id || 'CID-2026-9042'}}</div>
                                <div><span class="fnx-rg-label">Email:</span> {{c.customer.email || c.user.email || 'customer@example.com'}}</div>
                                <div><span class="fnx-rg-label">Mobile:</span> +91 {{c.customer.mobile || '9876543210'}}</div>
                            </div>
                        </div>

                        <!-- Action Bar -->
                        <div class="fnx-step-nav-bar">
                            <button type="button" class="fnx-btn fnx-btn-secondary" ng-click="c.prevStep()">&larr; Back</button>
                            <button type="button" class="fnx-btn fnx-btn-primary fnx-btn-lg" ng-click="c.nextStep()">
                                Proceed to Submit &rarr;
                            </button>
                        </div>
                    </div>

                    <!-- STEP 7: SUBMIT -->
                    <div class="fnx-step-card" ng-if="c.reportStep === 7">
                        
                        <!-- Before Submission Form -->
                        <div ng-if="!c.caseSubmittedSuccess">
                            <div class="fnx-step-card-header">
                                <div>
                                    <h2 class="fnx-step-card-title">7. Submit Fraud Case</h2>
                                    <p class="fnx-step-card-sub">Final declaration and registration into the FRAUDNEXUS investigation system.</p>
                                </div>
                            </div>

                            <div class="fnx-declaration-box">
                                <label class="fnx-checkbox-label">
                                    <input type="checkbox" ng-model="c.reportForm.confirm_accurate">
                                    <span><strong>Legal Declaration:</strong> I confirm that the information provided is accurate and truthful to the best of my knowledge. </span>
                                </label>
                            </div>

                            <div class="fnx-step-nav-bar">
                                <button type="button" class="fnx-btn fnx-btn-secondary" ng-click="c.prevStep()">&larr; Back to Review</button>
                                <button type="button" class="fnx-btn fnx-btn-primary fnx-btn-lg fnx-btn-submit-fraud" ng-disabled="!c.reportForm.confirm_accurate || c.reportLoading" ng-click="c.submitReport()">
                                    {{c.reportLoading ? 'Submitting to FRAUDNEXUS...' : 'SUBMIT FRAUD CASE'}}
                                </button>
                            </div>
                        </div>

                        <!-- Dedicated Success State (After Submission) -->
                        <div ng-if="c.caseSubmittedSuccess" class="fnx-success-submit-workspace">
                            <div class="fnx-success-submit-badge">&#10004;</div>
                            <h2 class="fnx-success-title">FRAUD CASE SUBMITTED</h2>
                            <p class="fnx-success-subtitle">Your fraud report has been successfully registered.</p>

                            <div class="fnx-success-case-card">
                                <div class="fnx-scc-row">
                                    <div class="fnx-scc-label">Case ID</div>
                                    <div class="fnx-scc-val font-mono">{{c.submittedCaseNumber || 'FNX-2026-001034'}}</div>
                                </div>
                                <div class="fnx-scc-row">
                                    <div class="fnx-scc-label">Status</div>
                                    <div class="fnx-scc-val"><span class="fnx-badge st-new">Case Submitted</span></div>
                                </div>
                                <div class="fnx-scc-row">
                                    <div class="fnx-scc-label">Incident Type</div>
                                    <div class="fnx-scc-val">{{c.reportForm.type}}</div>
                                </div>
                                <div class="fnx-scc-row">
                                    <div class="fnx-scc-label">Assigned Priority</div>
                                    <div class="fnx-scc-val"><span class="fnx-badge" ng-class="'sev-' + (c.reportForm.severity || 'high').toLowerCase()">{{c.reportForm.severity || 'High'}}</span></div>
                                </div>
                            </div>

                            <p style="color: #475569; font-size: 0.92rem; max-width: 540px; margin: 1.5rem auto;">
                                A cryptographic chain of custody record has been initialized with an immutable audit trail. Caseworker triage will commence immediately.
                            </p>

                            <div class="fnx-success-actions">
                                <button type="button" class="fnx-btn fnx-btn-primary fnx-btn-lg" ng-click="c.navigate('trackCases')">
                                    &#128270; TRACK CASE
                                </button>
                                <button type="button" class="fnx-btn fnx-btn-secondary fnx-btn-lg" ng-click="c.navigate('dashboard')">
                                    &#127968; GO TO DASHBOARD
                                </button>
                            </div>
                        </div>

                    </div>

                </div>

                <!-- RIGHT: INFORMATION / HELP PANEL (25-30%) -->
                <aside class="fnx-report-side">
                    
                    <!-- Card 1: Need Help? -->
                    <div class="fnx-side-card fnx-side-card-ai">
                        <div class="fnx-side-card-header">
                            <span class="fnx-side-card-icon">&#10024;</span>
                            <h4>Need Help?</h4>
                        </div>
                        <p>Not sure what information to provide or which category fits your incident?</p>
                        <button type="button" class="fnx-btn fnx-btn-cyan-outline fnx-btn-full" ng-click="c.showAI = true">
                            &#10024; Ask FRAUDNEXUS AI
                        </button>
                    </div>

                    <!-- Card 2: Reporting Tips -->
                    <div class="fnx-side-card">
                        <div class="fnx-side-card-header">
                            <span class="fnx-side-card-icon">&#128161;</span>
                            <h4>Reporting Tips</h4>
                        </div>
                        <ul class="fnx-tips-list">
                            <li>Provide accurate incident details.</li>
                            <li>Include transaction references.</li>
                            <li>Upload relevant evidence.</li>
                            <li>Include communication records.</li>
                            <li>Never share OTP/PIN/password.</li>
                        </ul>
                    </div>

                    <!-- Card 3: Your Information (Read-only) -->
                    <div class="fnx-side-card fnx-side-card-user">
                        <div class="fnx-side-card-header">
                            <span class="fnx-side-card-icon">&#128100;</span>
                            <h4>Your Information</h4>
                        </div>
                        <div class="fnx-user-summary-badge">Authenticated Session</div>
                        <div class="fnx-user-info-row">
                            <span class="fnx-ui-label">Name</span>
                            <span class="fnx-ui-val">{{c.customer.name || c.user.name || 'Arun Kumar'}}</span>
                        </div>
                        <div class="fnx-user-info-row">
                            <span class="fnx-ui-label">Customer ID</span>
                            <span class="fnx-ui-val font-mono">{{c.customer.customer_id || 'CID-2026-9042'}}</span>
                        </div>
                        <div class="fnx-user-info-row">
                            <span class="fnx-ui-label">Email</span>
                            <span class="fnx-ui-val">{{c.customer.email || c.user.email || 'customer@example.com'}}</span>
                        </div>
                        <div class="fnx-user-info-row">
                            <span class="fnx-ui-label">Mobile</span>
                            <span class="fnx-ui-val">+91 {{c.customer.mobile || '9876543210'}}</span>
                        </div>
                        <div class="fnx-user-info-note">
                            <small>Pre-filled from your authenticated customer profile. No re-entry required.</small>
                        </div>
                    </div>

                </aside>

            </div>
        </div>

        <!-- 4D. SUBMIT SUCCESS VIEW (STANDALONE FALLBACK) -->
        <div ng-if="c.currentView === 'submitSuccess'" class="fnx-submit-success-card">
            <div class="fnx-success-check">&#10004;</div>
            <h2>Fraud Case Submitted Successfully!</h2>
            <div class="fnx-cid-badge" style="font-size: 1.3rem; margin: 1rem auto;">
                Case Number: <strong>{{c.submittedCaseNumber}}</strong>
            </div>
            <p style="color: #475569; max-width: 500px; margin: 0 auto 1.5rem;">
                Your case has been securely logged with tamper-evident chain of custody. Our investigation team will initiate triage immediately.
            </p>
            <div style="display: flex; justify-content: center; gap: 1rem;">
                <button class="fnx-btn fnx-btn-primary fnx-btn-lg" ng-click="c.navigate('trackCases')">&#128270; Track This Case</button>
                <button class="fnx-btn fnx-btn-outline fnx-btn-lg" ng-click="c.navigate('dashboard')">Return to Dashboard</button>
            </div>
        </div>

        <!-- 4E. TRACK CASES VIEW -->
        <div ng-if="c.currentView === 'trackCases'" class="fnx-track-cases">
            <h2>{{c.t('trackCases')}}</h2>

            <div class="fnx-empty" ng-if="c.cases.length === 0">{{c.t('noCases')}}</div>

            <div ng-repeat="cs in c.cases" class="fnx-case-card">
                <div class="fnx-case-header">
                    <div>
                        <span class="fnx-case-number">{{cs.number}}</span>
                        <span class="fnx-case-type">{{cs.type}}</span>
                    </div>
                    <div>
                        <span class="fnx-badge" ng-class="c.getStatusClass(cs.status)">{{cs.status}}</span>
                        <button class="fnx-btn fnx-btn-sm fnx-btn-outline" style="margin-left: 0.5rem;" ng-click="c.openAddEvidence(cs)">
                            + {{c.t('addAdditionalEvidence')}}
                        </button>
                    </div>
                </div>

                <!-- 5-Stage Visual Progress Tracker -->
                <div class="fnx-tracker">
                    <div class="fnx-tracker-step" ng-class="{'completed': true, 'current': cs.status === 'New'}">
                        <div class="fnx-tracker-dot">&#10004;</div>
                        <div class="fnx-tracker-label">{{c.t('stageSubmitted')}}</div>
                    </div>
                    <div class="fnx-tracker-line" ng-class="{'active': cs.status !== 'New'}"></div>
                    <div class="fnx-tracker-step" ng-class="{'completed': cs.status === 'Investigation' || cs.status === 'Resolved' || cs.status === 'Closed', 'current': cs.status === 'Initial Review'}">
                        <div class="fnx-tracker-dot">&#10004;</div>
                        <div class="fnx-tracker-label">{{c.t('stageInitialReview')}}</div>
                    </div>
                    <div class="fnx-tracker-line" ng-class="{'active': cs.status === 'Investigation' || cs.status === 'Resolved' || cs.status === 'Closed'}"></div>
                    <div class="fnx-tracker-step" ng-class="{'completed': cs.status === 'Resolved' || cs.status === 'Closed', 'current': cs.status === 'Investigation'}">
                        <div class="fnx-tracker-dot">&#10004;</div>
                        <div class="fnx-tracker-label">{{c.t('stageInvestigation')}}</div>
                    </div>
                    <div class="fnx-tracker-line" ng-class="{'active': cs.status === 'Resolved' || cs.status === 'Closed'}"></div>
                    <div class="fnx-tracker-step" ng-class="{'completed': cs.status === 'Resolved' || cs.status === 'Closed', 'current': cs.status === 'Resolved'}">
                        <div class="fnx-tracker-dot">&#10004;</div>
                        <div class="fnx-tracker-label">{{c.t('stageResolution')}}</div>
                    </div>
                    <div class="fnx-tracker-line" ng-class="{'active': cs.status === 'Closed'}"></div>
                    <div class="fnx-tracker-step" ng-class="{'completed': cs.status === 'Closed'}">
                        <div class="fnx-tracker-dot">&#10004;</div>
                        <div class="fnx-tracker-label">{{c.t('stageClosed')}}</div>
                    </div>
                </div>

                <!-- Case Details -->
                <div class="fnx-case-body">
                    <p><strong>Description:</strong> {{cs.description}}</p>
                    <div class="fnx-case-meta-grid">
                        <div>Incident Date: <strong>{{cs.incident_date}}</strong></div>
                        <div>Reported On: <strong>{{cs.created_on | date:'medium'}}</strong></div>
                        <div ng-if="cs.exposure && cs.exposure !== '0'">Amount: <strong>INR {{cs.exposure}}</strong></div>
                        <div ng-if="cs.digital_platform">Platform: <strong>{{cs.digital_platform}}</strong></div>
                    </div>

                    <!-- Evidence List for Case -->
                    <div ng-if="cs.evidence && cs.evidence.length > 0" style="margin-top: 1rem;">
                        <strong>Associated Evidence ({{cs.evidence.length}}):</strong>
                        <div class="fnx-evidence-tag-list">
                            <span class="fnx-evidence-tag" ng-repeat="ev in cs.evidence">
                                &#128206; {{ev.number}} ({{ev.type}}) &bull; Status: {{ev.status}}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 4F. EVIDENCE VAULT VIEW -->
        <div ng-if="c.currentView === 'evidenceVault'" class="fnx-evidence-vault">
            <h2>{{c.t('evidence')}}</h2>
            <div class="fnx-card">
                <p style="color: #475569; margin: 0 0 1rem 0;">All evidence items submitted under your cases are cryptographically hashed using SHA-256 with full chain of custody preservation.</p>
                <div class="fnx-empty" ng-if="c.cases.length === 0">No evidence found.</div>
                <div ng-repeat="cs in c.cases" ng-if="cs.evidence && cs.evidence.length > 0">
                    <h4 style="margin: 1rem 0 0.5rem 0;">Case: {{cs.number}} ({{cs.type}})</h4>
                    <table class="fnx-table">
                        <thead>
                            <tr>
                                <th>Evidence ID</th>
                                <th>Type</th>
                                <th>Description</th>
                                <th>Uploaded Date</th>
                                <th>Verification Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr ng-repeat="ev in cs.evidence">
                                <td><strong>{{ev.number}}</strong></td>
                                <td>{{ev.type}}</td>
                                <td>{{ev.description}}</td>
                                <td>{{ev.uploaded_on | date:'short'}}</td>
                                <td><span class="fnx-badge st-resolved">{{ev.status}}</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- 4G. HELP & SUPPORT VIEW -->
        <!-- EDIT PROFILE VIEW -->
        <div ng-if="c.currentView === 'editProfile'" class="fnx-edit-profile-view">
            <div class="fnx-page-header-row">
                <div>
                    <h1 class="fnx-page-title">EDIT PROFILE</h1>
                    <p class="fnx-page-subtitle">Update your personal information. Customer ID cannot be changed.</p>
                </div>
                <button class="fnx-btn fnx-btn-outline" ng-click="c.navigate('profile')">&larr; Back to Profile</button>
            </div>
            <div class="fnx-card" style="max-width:800px;">
                <div class="fnx-alert fnx-alert-success" ng-if="c.editProfileSuccess" style="margin-bottom:1rem;">&#10004; {{c.editProfileSuccess}}</div>
                <div class="fnx-info-row" style="background:#F1F5F9;border-radius:8px;padding:0.75rem 1rem;margin-bottom:1.25rem;">
                    <span class="fnx-info-label" style="color:#64748B;">Customer ID (Read-only)</span>
                    <span class="fnx-info-val" style="font-weight:800;color:#0B1F3A;font-family:monospace;">{{c.customer.customer_id || 'FNX-DEMO-2026'}}</span>
                </div>
                <div class="fnx-form-grid-2">
                    <div class="fnx-field"><label>Full Name *</label><input type="text" ng-model="c.editProfileForm.name" placeholder="Full name" required></div>
                    <div class="fnx-field"><label>Mobile Number</label><div class="fnx-input-group"><span class="fnx-input-addon">+91</span><input type="tel" ng-model="c.editProfileForm.mobile" placeholder="9876543210" maxlength="10"></div></div>
                </div>
                <div class="fnx-form-grid-2">
                    <div class="fnx-field"><label>Email Address</label><input type="email" ng-model="c.editProfileForm.email" placeholder="email@example.com"></div>
                    <div class="fnx-field"><label>Date of Birth</label><input type="date" ng-model="c.editProfileForm.dob" max="{{c.todayDate}}"></div>
                </div>
                <div class="fnx-form-grid-2">
                    <div class="fnx-field"><label>Gender</label><select ng-model="c.editProfileForm.gender"><option value="Male">Male</option><option value="Female">Female</option><option value="Other">Other</option><option value="Prefer not to say">Prefer not to say</option></select></div>
                    <div class="fnx-field"><label>Occupation</label><select ng-model="c.editProfileForm.occupation"><option value="Student">Student</option><option value="Employee">Employee</option><option value="Self-employed">Self-employed</option><option value="Business Owner">Business Owner</option><option value="Professional">Professional</option><option value="Homemaker">Homemaker</option><option value="Retired">Retired</option><option value="Other">Other</option></select></div>
                </div>
                <div class="fnx-field"><label>Address</label><textarea ng-model="c.editProfileForm.address" rows="2" placeholder="Street, City, Pincode, State"></textarea></div>
                <div class="fnx-step-nav-bar" style="margin-top:1.5rem;">
                    <button type="button" class="fnx-btn fnx-btn-secondary" ng-click="c.navigate('profile')">Cancel</button>
                    <button type="button" class="fnx-btn fnx-btn-primary fnx-btn-lg" ng-click="c.saveProfile()" ng-disabled="c.editProfileLoading">{{c.editProfileLoading ? 'Saving...' : 'Save Changes'}}</button>
                </div>
            </div>
        </div>

        <div ng-if="c.currentView === 'help'" class="fnx-help-view">
            <h2>{{c.t('helpSupport')}}</h2>
            <div class="fnx-help-grid">
                <div class="fnx-card">
                    <h3>&#128222; Emergency Helpline</h3>
                    <p style="font-size: 1.1rem; font-weight: 700; color: #DC2626;">National Cyber Crime Helpline: 1930</p>
                    <p style="font-size: 0.9rem; color: #475569;">Available 24x7 across all states and union territories of India for financial cyber fraud reporting.</p>
                </div>
                <div class="fnx-card">
                    <h3>&#127974; Immediate Banking Steps</h3>
                    <ol style="font-size: 0.9rem; color: #475569; padding-left: 1.2rem;">
                        <li>Call your bank's 24x7 toll-free fraud helpline immediately.</li>
                        <li>Request immediate freezing of transaction UTR / beneficiary account.</li>
                        <li>Deactivate your UPI and netbanking credentials temporarily.</li>
                        <li>File your formal FRAUDNEXUS report with all transaction reference numbers.</li>
                    </ol>
                </div>
            </div>
        </div>

    </main>

    <!-- ADDITIONAL EVIDENCE MODAL -->
    <div class="fnx-modal-overlay" ng-if="c.showAddEvidenceModal">
        <div class="fnx-modal-box">
            <h3>Add Additional Evidence to {{c.targetCaseForEvidence.number}}</h3>
            <div class="fnx-field">
                <label>Evidence Type</label>
                <select ng-model="c.extraEvidence.type">
                    <option value="Screenshot">Screenshot</option>
                    <option value="Bank Statement">Bank Statement</option>
                    <option value="Chat Export">Chat Export</option>
                    <option value="PDF Document">PDF Document</option>
                    <option value="Other">Other</option>
                </select>
            </div>
            <div class="fnx-field">
                <label>Description</label>
                <input type="text" ng-model="c.extraEvidence.description" placeholder="Describe the additional evidence">
            </div>
            <div style="display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1.5rem;">
                <button class="fnx-btn fnx-btn-outline" ng-click="c.showAddEvidenceModal = false">Cancel</button>
                <button class="fnx-btn fnx-btn-primary" ng-click="c.submitAdditionalEvidence()">Upload Evidence</button>
            </div>
        </div>
    </div>
</div>

<!-- ============ 5. FLOATING NOW ASSIST AI (BOTTOM-RIGHT) ============ -->
<div class="fnx-ai-widget">
    <!-- Floating Trigger Button -->
    <button class="fnx-ai-trigger" ng-click="c.showAI = !c.showAI" title="Now Assist for FRAUDNEXUS">
        <span>&#10024;</span> Now Assist AI
    </button>

    <!-- Slide-out AI Chat Panel -->
    <div class="fnx-ai-panel" ng-if="c.showAI">
        <div class="fnx-ai-header">
            <div class="fnx-ai-header-left">
                <div class="fnx-ai-title-row">
                    <span class="fnx-ai-sparkle-icon">&#10024;</span>
                    <strong>Now Assist</strong>
                    <span class="fnx-ai-now-badge">ServiceNow GenAI</span>
                </div>
                <div class="fnx-ai-subtitle">FRAUDNEXUS Intelligent Triage</div>
            </div>
            <button class="fnx-ai-close" ng-click="c.showAI = false" aria-label="Close Now Assist">&times;</button>
        </div>
        
        <div class="fnx-ai-body" id="fnx-ai-chat-body">
            <div ng-repeat="m in c.aiMessages track by $index" class="fnx-ai-msg-group">
                <div class="fnx-ai-msg" ng-class="{'ai': m.sender === 'ai', 'user': m.sender === 'user'}">
                    <div class="fnx-ai-bubble" style="white-space: pre-line;">
                        <div class="fnx-ai-sender-label" ng-if="m.sender === 'ai'">
                            <span>&#10024;</span> Now Assist GenAI
                        </div>
                        {{m.text}}
                        <!-- Action button if provided -->
                        <div class="fnx-ai-action-btn-row" ng-if="m.action">
                            <button class="fnx-btn fnx-btn-primary fnx-btn-xs" ng-click="c.executeAIAction(m.action)">
                                {{m.action.label}} &rarr;
                            </button>
                        </div>
                    </div>
                </div>
                <!-- Suggested prompt chips -->
                <div class="fnx-ai-suggestions" ng-if="m.suggestions && m.suggestions.length > 0 && $last">
                    <button class="fnx-ai-chip" ng-repeat="s in m.suggestions" ng-click="c.sendAIMessage(s)">
                        {{s}}
                    </button>
                </div>
            </div>

            <!-- Typing Indicator -->
            <div class="fnx-ai-msg ai" ng-if="c.aiLoading">
                <div class="fnx-ai-bubble fnx-ai-typing">
                    <span class="fnx-ai-typing-label">Now Assist is thinking</span>
                    <span class="dot"></span>
                    <span class="dot"></span>
                    <span class="dot"></span>
                </div>
            </div>
        </div>

        <div class="fnx-ai-footer">
            <input type="text" ng-model="c.aiInput" placeholder="Ask Now Assist about cases, UPI fraud, KYC..." ng-keydown="$event.keyCode === 13 && c.sendAIMessage()" ng-disabled="c.aiLoading">
            <button class="fnx-btn fnx-btn-primary fnx-btn-sm" ng-click="c.sendAIMessage()" ng-disabled="c.aiLoading || !c.aiInput.trim()">
                <span ng-if="!c.aiLoading">{{c.t('send')}}</span>
                <span ng-if="c.aiLoading">...</span>
            </button>
        </div>
    </div>
</div>

</div>
"""

# 4. CSS (Enterprise Blue + White, high-contrast, fully styled)
css = r"""
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&family=Inter:wght@400;500;600;700;800&display=swap');

/* ============================================================
   FRAUDNEXUS HIGH CONTRAST BLUE + WHITE ENTERPRISE DESIGN
   ============================================================ */
.fnx-app {
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
    text-rendering: optimizeLegibility !important;
    letter-spacing: -0.012em !important;
    color: #0F172A !important;
    background-color: #F8FAFC !important;
    min-height: 100vh !important;
    font-size: 15px !important;
    line-height: 1.5 !important;
}

.fnx-app * {
    box-sizing: border-box !important;
}

/* ==================== 1. LANDING PAGE ==================== */
.fnx-landing {
    background-color: #FFFFFF !important;
    min-height: 100vh !important;
    color: #0F172A !important;
}

.fnx-landing-header {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    padding: 1.25rem 3rem !important;
    background-color: #0B1F3A !important;
    color: #FFFFFF !important;
    box-shadow: 0 2px 8px rgba(11,31,58,0.15) !important;
}

.fnx-landing-brand {
    display: flex !important;
    align-items: center !important;
    gap: 0.8rem !important;
}

.fnx-brand-text {
    font-size: 1.4rem !important;
    font-weight: 800 !important;
    letter-spacing: 1.5px !important;
    color: #00B8D9 !important;
}

.fnx-landing-actions {
    display: flex !important;
    gap: 0.85rem !important;
    align-items: center !important;
}

.fnx-lang-select {
    background-color: #123B63 !important;
    color: #FFFFFF !important;
    border: 1px solid #00B8D9 !important;
    padding: 0.45rem 1rem !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    outline: none !important;
    font-size: 0.9rem !important;
}

.fnx-lang-select option {
    background-color: #0B1F3A !important;
    color: #FFFFFF !important;
}

.fnx-hero {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    padding: 4.5rem 4rem 3.5rem !important;
    max-width: 1240px !important;
    margin: 0 auto !important;
    gap: 3.5rem !important;
    background: linear-gradient(180deg, #FFFFFF 0%, #F1F5F9 100%) !important;
    border-bottom: 1px solid #E2E8F0 !important;
}

.fnx-hero-content {
    flex: 1 !important;
}

/* Professional Website Typography */
.fnx-hero h1,
.fnx-features-title,
.fnx-features-header h2,
.fnx-portal-title h2,
.fnx-auth-form-title,
.fnx-success-title,
.fnx-top-bar-title,
.fnx-brand-name,
h1, h2, h3 {
    font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif !important;
    letter-spacing: -0.03em !important;
}

.fnx-hero-badge {
    display: inline-block !important;
    background-color: #E0F2FE !important;
    color: #0369A1 !important;
    border: 1.5px solid #00B8D9 !important;
    padding: 0.45rem 1.2rem !important;
    border-radius: 30px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    margin-bottom: 1.25rem !important;
}

.fnx-hero h1 {
    font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif !important;
    font-size: 3.3rem !important;
    font-weight: 800 !important;
    line-height: 1.12 !important;
    letter-spacing: -0.035em !important;
    color: #0B1F3A !important;
    margin-bottom: 0.9rem !important;
}

.fnx-hero-sub {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    color: #0284C7 !important;
    letter-spacing: -0.02em !important;
    margin-bottom: 1rem !important;
}

.fnx-hero-desc {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 1.08rem !important;
    line-height: 1.7 !important;
    color: #475569 !important;
    margin-bottom: 2.2rem !important;
    max-width: 580px !important;
    letter-spacing: -0.01em !important;
}

.fnx-hero-btns {
    display: flex !important;
    gap: 1.2rem !important;
}

/* ==================== HERO CONCENTRIC CIRCLES ANIMATION ==================== */
.fnx-hero-visual {
    flex: 0 0 420px !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    position: relative !important;
}

.fnx-hero-graphic {
    position: relative !important;
    width: 360px !important;
    height: 360px !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    cursor: pointer !important;
}

.fnx-hero-circle {
    position: absolute !important;
    border-radius: 50% !important;
    box-sizing: border-box !important;
    pointer-events: none !important;
}

/* Outer Circle (c1): Sonar expand & breathing glow */
.fnx-hero-circle.c1 {
    width: 360px !important;
    height: 360px !important;
    border: 1.5px solid rgba(0, 184, 217, 0.28) !important;
    animation: fnxPulseOuter 4.5s ease-in-out infinite !important;
}

/* Middle Circle (c2): Resonant pulse with accent cyan border */
.fnx-hero-circle.c2 {
    width: 270px !important;
    height: 270px !important;
    border: 2px solid rgba(0, 184, 217, 0.48) !important;
    animation: fnxPulseMid 3.2s ease-in-out infinite 0.6s !important;
}

/* Inner Circle (c3): High-energy shield ring with radial gradient */
.fnx-hero-circle.c3 {
    width: 185px !important;
    height: 185px !important;
    border: 2px solid #00B8D9 !important;
    background: radial-gradient(circle, rgba(0, 184, 217, 0.08) 0%, rgba(0, 184, 217, 0) 70%) !important;
    animation: fnxPulseInner 2.5s ease-in-out infinite 1.2s !important;
}

/* Orbit ring & revolving cyber beacon dot */
.fnx-hero-orbit {
    position: absolute !important;
    width: 270px !important;
    height: 270px !important;
    border-radius: 50% !important;
    pointer-events: none !important;
    animation: fnxOrbit 8s linear infinite !important;
}
.fnx-orbit-beacon {
    position: absolute !important;
    top: -6px !important;
    left: calc(50% - 6px) !important;
    width: 12px !important;
    height: 12px !important;
    border-radius: 50% !important;
    background: #00B8D9 !important;
    box-shadow: 0 0 14px 3px rgba(0, 184, 217, 0.8), 0 0 25px 6px rgba(0, 184, 217, 0.4) !important;
}

/* Central Shield Icon floating with gentle glow */
.fnx-hero-shield {
    position: relative !important;
    z-index: 2 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    animation: fnxShieldFloat 3.6s ease-in-out infinite !important;
}
.fnx-hero-shield svg {
    filter: drop-shadow(0 4px 12px rgba(0, 184, 217, 0.45)) !important;
    transition: filter 0.3s ease !important;
}

/* Hover effect on entire graphic */
.fnx-hero-graphic:hover .fnx-hero-circle.c1 {
    border-color: rgba(0, 184, 217, 0.6) !important;
    box-shadow: 0 0 35px rgba(0, 184, 217, 0.25) !important;
}
.fnx-hero-graphic:hover .fnx-hero-circle.c2 {
    border-color: rgba(0, 184, 217, 0.8) !important;
    box-shadow: 0 0 25px rgba(0, 184, 217, 0.35) !important;
}
.fnx-hero-graphic:hover .fnx-hero-circle.c3 {
    border-color: #00B8D9 !important;
    box-shadow: 0 0 35px rgba(0, 184, 217, 0.5) !important;
}
.fnx-hero-graphic:hover .fnx-hero-shield svg {
    filter: drop-shadow(0 8px 24px rgba(0, 184, 217, 0.8)) !important;
}

@keyframes fnxPulseOuter {
    0%, 100% {
        transform: scale(0.96);
        opacity: 0.35;
        box-shadow: 0 0 0 rgba(0, 184, 217, 0);
    }
    50% {
        transform: scale(1.05);
        opacity: 0.8;
        border-color: rgba(0, 184, 217, 0.5);
        box-shadow: 0 0 30px rgba(0, 184, 217, 0.2);
    }
}

@keyframes fnxPulseMid {
    0%, 100% {
        transform: scale(0.97);
        opacity: 0.45;
    }
    50% {
        transform: scale(1.06);
        opacity: 0.9;
        border-color: #00B8D9;
        box-shadow: 0 0 24px rgba(0, 184, 217, 0.3);
    }
}

@keyframes fnxPulseInner {
    0%, 100% {
        transform: scale(0.98);
        opacity: 0.65;
        box-shadow: 0 0 15px rgba(0, 184, 217, 0.2);
    }
    50% {
        transform: scale(1.08);
        opacity: 1;
        box-shadow: 0 0 35px rgba(0, 184, 217, 0.5);
    }
}

@keyframes fnxOrbit {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}

@keyframes fnxShieldFloat {
    0%, 100% {
        transform: translateY(0px) scale(1);
    }
    50% {
        transform: translateY(-6px) scale(1.05);
    }
}

.fnx-features {
    display: grid !important;
    grid-template-columns: repeat(3, 1fr) !important;
    gap: 1.75rem !important;
    max-width: 1240px !important;
    margin: 3.5rem auto !important;
    padding: 0 4rem !important;
}

.fnx-feature-card {
    background-color: #FFFFFF !important;
    border: 2px solid #CBD5E1 !important;
    border-radius: 12px !important;
    padding: 1.75rem !important;
    box-shadow: 0 4px 12px rgba(11,31,58,0.05) !important;
    transition: transform 0.2s, border-color 0.2s !important;
}

.fnx-feature-card:hover {
    transform: translateY(-4px) !important;
    border-color: #00B8D9 !important;
}

.fnx-feature-icon {
    font-size: 2.2rem !important;
    margin-bottom: 0.85rem !important;
}

.fnx-feature-title {
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    color: #0B1F3A !important;
    margin-bottom: 0.5rem !important;
}

.fnx-feature-desc {
    font-size: 0.92rem !important;
    color: #475569 !important;
    line-height: 1.5 !important;
    margin: 0 !important;
}

/* ==================== 2. PORTAL SELECTION ==================== */
.fnx-portal-select {
    max-width: 1060px !important;
    margin: 3.5rem auto !important;
    padding: 0 2rem !important;
}

.fnx-portal-header {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    margin-bottom: 3rem !important;
}

.fnx-back-link {
    background: none !important;
    border: none !important;
    color: #0284C7 !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    cursor: pointer !important;
}

.fnx-portal-title {
    text-align: center !important;
}

.fnx-portal-title h2 {
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    color: #0B1F3A !important;
    margin: 0 0 0.5rem 0 !important;
    letter-spacing: 1px !important;
}

.fnx-portal-title p {
    font-size: 1.1rem !important;
    color: #475569 !important;
    margin: 0 !important;
}

.fnx-portal-cards {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 2.5rem !important;
}

.fnx-portal-card {
    background-color: #FFFFFF !important;
    border: 2px solid #CBD5E1 !important;
    border-radius: 14px !important;
    padding: 2.5rem !important;
    display: flex !important;
    flex-direction: column !important;
    box-shadow: 0 6px 20px rgba(11,31,58,0.06) !important;
}

.fnx-portal-card.fnx-portal-customer {
    border-color: #00B8D9 !important;
}

.fnx-portal-card-icon {
    font-size: 3rem !important;
    margin-bottom: 1rem !important;
}

.fnx-portal-card h3 {
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    color: #0B1F3A !important;
    margin: 0 0 0.85rem 0 !important;
}

.fnx-portal-card p {
    font-size: 1rem !important;
    color: #475569 !important;
    line-height: 1.5 !important;
    margin: 0 0 1.5rem 0 !important;
}

.fnx-portal-card ul {
    list-style: none !important;
    padding: 0 !important;
    margin: 0 0 2rem 0 !important;
    flex: 1 !important;
}

.fnx-portal-card ul li {
    padding: 0.55rem 0 !important;
    border-bottom: 1px solid #F1F5F9 !important;
    color: #334155 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

.fnx-portal-card ul li:before {
    content: "✓ " !important;
    color: #00B8D9 !important;
    font-weight: 800 !important;
    margin-right: 0.5rem !important;
}

/* ==================== 3. AUTH VIEW ==================== */
.fnx-auth-page {
    display: flex !important;
    min-height: 100vh !important;
}

.fnx-auth-left {
    flex: 0 0 45% !important;
    background-color: #0B1F3A !important;
    color: #FFFFFF !important;
    padding: 4.5rem !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}

.fnx-auth-brand {
    display: flex !important;
    align-items: center !important;
    gap: 0.75rem !important;
    font-size: 1.4rem !important;
    font-weight: 800 !important;
    color: #00B8D9 !important;
    margin-bottom: 2rem !important;
    cursor: pointer !important;
}

.fnx-auth-left h2 {
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    margin: 0 0 1rem 0 !important;
    line-height: 1.25 !important;
}

.fnx-auth-left p {
    font-size: 1.1rem !important;
    color: #94A3B8 !important;
    line-height: 1.6 !important;
}

.fnx-auth-right {
    flex: 1 !important;
    background-color: #F8FAFC !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    padding: 3rem !important;
}

.fnx-auth-box {
    width: 100% !important;
    max-width: 480px !important;
    background-color: #FFFFFF !important;
    padding: 2.5rem !important;
    border-radius: 14px !important;
    border: 2px solid #CBD5E1 !important;
    box-shadow: 0 6px 20px rgba(11,31,58,0.06) !important;
}

.fnx-auth-tabs {
    display: flex !important;
    margin-bottom: 2rem !important;
    border-bottom: 2px solid #CBD5E1 !important;
}

.fnx-auth-tabs button {
    flex: 1 !important;
    padding: 0.85rem !important;
    border: none !important;
    background: none !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: #475569 !important;
    cursor: pointer !important;
    border-bottom: 3px solid transparent !important;
    margin-bottom: -2px !important;
}

.fnx-auth-tabs button.active {
    color: #0B1F3A !important;
    border-bottom-color: #00B8D9 !important;
}

.fnx-auth-error {
    background-color: #FEF2F2 !important;
    color: #DC2626 !important;
    padding: 0.85rem 1rem !important;
    border-radius: 8px !important;
    margin-bottom: 1.25rem !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    border: 1px solid #FECACA !important;
}

.fnx-auth-form {
    display: flex !important;
    flex-direction: column !important;
    gap: 1.15rem !important;
}

.fnx-field {
    display: flex !important;
    flex-direction: column !important;
    gap: 0.4rem !important;
}

.fnx-field label {
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    color: #0F172A !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    margin: 0 !important;
}

.fnx-field input,
.fnx-field select,
.fnx-field textarea {
    padding: 0.75rem 1rem !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 8px !important;
    font-size: 0.95rem !important;
    color: #0F172A !important;
    background-color: #FFFFFF !important;
    outline: none !important;
    transition: border-color 0.2s !important;
}

.fnx-field input:focus,
.fnx-field select:focus,
.fnx-field textarea:focus {
    border-color: #00B8D9 !important;
    box-shadow: 0 0 0 3px rgba(0,184,217,0.15) !important;
}

.fnx-input-group {
    display: flex !important;
    align-items: stretch !important;
}

.fnx-input-addon {
    background-color: #F1F5F9 !important;
    border: 1.5px solid #CBD5E1 !important;
    border-right: none !important;
    border-radius: 8px 0 0 8px !important;
    padding: 0.75rem 1rem !important;
    font-weight: 700 !important;
    color: #334155 !important;
    display: flex !important;
    align-items: center !important;
}

.fnx-input-group input {
    border-radius: 0 8px 8px 0 !important;
    flex: 1 !important;
}

.fnx-password-wrap {
    position: relative !important;
    display: flex !important;
    align-items: center !important;
}

.fnx-password-wrap input {
    width: 100% !important;
    padding-right: 2.75rem !important;
}

.fnx-eye-btn {
    position: absolute !important;
    right: 0.6rem !important;
    background: none !important;
    border: none !important;
    cursor: pointer !important;
    padding: 0.35rem !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    color: #475569 !important;
}

.fnx-forgot-row {
    display: flex !important;
    justify-content: flex-end !important;
    margin-top: -0.25rem !important;
    margin-bottom: 0.25rem !important;
}

.fnx-forgot-pwd {
    color: #0284C7 !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    text-decoration: none !important;
    cursor: pointer !important;
}

.fnx-forgot-pwd:hover {
    color: #0369A1 !important;
    text-decoration: underline !important;
}

.fnx-auth-switch {
    text-align: center !important;
    font-size: 0.92rem !important;
    color: #475569 !important;
    margin-top: 1.25rem !important;
}

.fnx-auth-switch a {
    color: #0284C7 !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    text-decoration: none !important;
}

.fnx-reg-success-box {
    text-align: center !important;
    padding: 1.5rem 0 !important;
}

.fnx-success-check {
    width: 64px !important;
    height: 64px !important;
    background-color: #DCFCE7 !important;
    color: #16A34A !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 2rem !important;
    margin: 0 auto 1.25rem !important;
    border: 2px solid #86EFAC !important;
}

.fnx-cid-badge {
    background-color: #F1F5F9 !important;
    border: 1px solid #CBD5E1 !important;
    padding: 0.6rem 1.2rem !important;
    border-radius: 8px !important;
    display: inline-block !important;
    margin: 1rem 0 1.5rem !important;
    color: #0F172A !important;
}

/* ==================== 4. MAIN APP LAYOUT ==================== */
.fnx-main-layout {
    display: flex !important;
    min-height: 100vh !important;
    flex-direction: column !important;
}

.fnx-header {
    height: 65px !important;
    background-color: #0B1F3A !important;
    color: #FFFFFF !important;
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    padding: 0 2rem !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 100 !important;
    box-shadow: 0 2px 8px rgba(11,31,58,0.15) !important;
}

.fnx-header-left {
    display: flex !important;
    align-items: center !important;
    gap: 1.25rem !important;
}

.fnx-sidebar-toggle {
    background: none !important;
    border: none !important;
    color: #FFFFFF !important;
    font-size: 1.4rem !important;
    cursor: pointer !important;
}

.fnx-header-brand {
    display: flex !important;
    align-items: center !important;
    gap: 0.6rem !important;
    font-size: 1.2rem !important;
    font-weight: 800 !important;
    color: #00B8D9 !important;
    cursor: pointer !important;
}

.fnx-header-right {
    display: flex !important;
    align-items: center !important;
    gap: 1.2rem !important;
    position: relative !important;
}

.fnx-icon-btn {
    background: none !important;
    border: none !important;
    color: #FFFFFF !important;
    font-size: 1.25rem !important;
    cursor: pointer !important;
    position: relative !important;
    padding: 0.4rem !important;
}

.fnx-notif-dot {
    position: absolute !important;
    top: 4px !important;
    right: 4px !important;
    width: 8px !important;
    height: 8px !important;
    background-color: #00B8D9 !important;
    border-radius: 50% !important;
}

/* ===== PROFILE DROPDOWN MENU ===== */
.fnx-profile-menu-wrap {
    position: relative !important;
    display: inline-block !important;
}

.fnx-profile-btn {
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
    background: linear-gradient(135deg, #123B63 0%, #1a4f82 100%) !important;
    border: 1px solid rgba(0,184,217,0.35) !important;
    border-radius: 24px !important;
    padding: 0.3rem 0.75rem 0.3rem 0.35rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    color: #FFFFFF !important;
}

.fnx-profile-btn:hover {
    background: linear-gradient(135deg, #1a4f82 0%, #225c94 100%) !important;
    border-color: rgba(0,184,217,0.6) !important;
    box-shadow: 0 0 0 3px rgba(0,184,217,0.12) !important;
}

.fnx-avatar-lg {
    width: 30px !important;
    height: 30px !important;
    min-width: 30px !important;
    background: linear-gradient(135deg, #00B8D9 0%, #0090aa 100%) !important;
    color: #0B1F3A !important;
    font-weight: 800 !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 0.9rem !important;
    letter-spacing: 0 !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
}

.fnx-profile-name-label {
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: #E2EEF6 !important;
    max-width: 90px !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
}

.fnx-chevron {
    color: #94BAD8 !important;
    transition: transform 0.2s ease !important;
    flex-shrink: 0 !important;
}

.fnx-chevron.rotated {
    transform: rotate(180deg) !important;
}

.fnx-profile-dropdown {
    position: absolute !important;
    top: calc(100% + 10px) !important;
    right: 0 !important;
    width: 240px !important;
    background: #0F2744 !important;
    border: 1px solid rgba(0,184,217,0.2) !important;
    border-radius: 14px !important;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.04) !important;
    z-index: 9999 !important;
    overflow: hidden !important;
    animation: fnxDropdownIn 0.18s ease !important;
}

@keyframes fnxDropdownIn {
    from { opacity: 0; transform: translateY(-8px) scale(0.97); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

.fnx-profile-dropdown-header {
    display: flex !important;
    align-items: center !important;
    gap: 0.75rem !important;
    padding: 1rem 1.1rem !important;
    background: rgba(0,184,217,0.07) !important;
}

.fnx-profile-dropdown-avatar {
    width: 40px !important;
    height: 40px !important;
    min-width: 40px !important;
    background: linear-gradient(135deg, #00B8D9 0%, #0090aa 100%) !important;
    color: #0B1F3A !important;
    font-weight: 800 !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 1.1rem !important;
    box-shadow: 0 3px 8px rgba(0,184,217,0.3) !important;
}

.fnx-profile-dropdown-info {
    overflow: hidden !important;
}

.fnx-profile-dropdown-name {
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}

.fnx-profile-dropdown-email {
    font-size: 0.78rem !important;
    color: #7AADCC !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    margin-top: 1px !important;
}

.fnx-profile-dropdown-divider {
    height: 1px !important;
    background: rgba(255,255,255,0.07) !important;
    margin: 0.25rem 0 !important;
}

.fnx-profile-dropdown-item {
    display: flex !important;
    align-items: center !important;
    gap: 0.7rem !important;
    width: 100% !important;
    padding: 0.7rem 1.1rem !important;
    background: none !important;
    border: none !important;
    color: #CBD5E1 !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    text-align: left !important;
    transition: background 0.15s ease, color 0.15s ease !important;
}

.fnx-profile-dropdown-item:hover {
    background: rgba(0,184,217,0.1) !important;
    color: #FFFFFF !important;
}

.fnx-profile-dropdown-item svg {
    opacity: 0.7 !important;
    flex-shrink: 0 !important;
}

.fnx-profile-dropdown-item:hover svg {
    opacity: 1 !important;
}

.fnx-profile-dropdown-logout {
    color: #F87171 !important;
    margin-bottom: 0.3rem !important;
}

.fnx-profile-dropdown-logout:hover {
    background: rgba(248,113,113,0.1) !important;
    color: #FCA5A5 !important;
}

.fnx-notif-dropdown {
    position: absolute !important;
    top: 55px !important;
    right: 180px !important;
    width: 320px !important;
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
    box-shadow: 0 10px 25px rgba(11,31,58,0.15) !important;
    z-index: 101 !important;
    color: #0F172A !important;
}

.fnx-notif-header {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    padding: 0.85rem 1rem !important;
    border-bottom: 1px solid #E2E8F0 !important;
    font-size: 0.95rem !important;
}

.fnx-notif-header button {
    background: none !important;
    border: none !important;
    font-size: 1.25rem !important;
    cursor: pointer !important;
}

.fnx-notif-item {
    padding: 0.75rem 1rem !important;
    border-bottom: 1px solid #F1F5F9 !important;
    font-size: 0.88rem !important;
    cursor: pointer !important;
}

.fnx-notif-item:hover {
    background-color: #F8FAFC !important;
}

/* ==================== SIDEBAR ==================== */
.fnx-sidebar {
    position: fixed !important;
    top: 65px !important;
    left: 0 !important;
    bottom: 0 !important;
    width: 240px !important;
    background-color: #0B1F3A !important;
    border-right: 1px solid #1E3A5F !important;
    padding: 1.5rem 0 !important;
    transition: width 0.2s ease !important;
    z-index: 90 !important;
}

.fnx-sidebar.collapsed {
    width: 70px !important;
}

.fnx-nav {
    display: flex !important;
    flex-direction: column !important;
    gap: 0.4rem !important;
}

.fnx-nav-item {
    display: flex !important;
    align-items: center !important;
    gap: 1rem !important;
    padding: 0.85rem 1.5rem !important;
    color: #94A3B8 !important;
    text-decoration: none !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    border-left: 4px solid transparent !important;
    transition: background 0.15s, color 0.15s !important;
}

.fnx-nav-item:hover {
    background-color: #123B63 !important;
    color: #FFFFFF !important;
}

.fnx-nav-item.active {
    background-color: #123B63 !important;
    color: #FFFFFF !important;
    border-left-color: #00B8D9 !important;
}

.fnx-nav-icon {
    font-size: 1.25rem !important;
}

.fnx-sidebar.collapsed .fnx-nav-label {
    display: none !important;
}

/* ==================== CONTENT ==================== */
.fnx-content {
    margin-left: 240px !important;
    padding: 2.5rem 3rem !important;
    background-color: #F8FAFC !important;
    min-height: calc(100vh - 65px) !important;
    transition: margin-left 0.2s ease !important;
}

.fnx-content.sidebar-collapsed {
    margin-left: 70px !important;
}

/* ==================== DASHBOARD ==================== */
.fnx-welcome {
    margin-bottom: 2rem !important;
}

.fnx-welcome h2 {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #0B1F3A !important;
    margin: 0 0 0.4rem 0 !important;
}

.fnx-welcome p {
    color: #475569 !important;
    margin: 0 !important;
}

.fnx-stats-row {
    display: grid !important;
    grid-template-columns: repeat(4, 1fr) !important;
    gap: 1.5rem !important;
    margin-bottom: 2rem !important;
}

.fnx-stat-card {
    background-color: #FFFFFF !important;
    border: 2px solid #CBD5E1 !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    display: flex !important;
    flex-direction: column !important;
    box-shadow: 0 4px 12px rgba(11,31,58,0.04) !important;
}

.fnx-stat-icon {
    font-size: 1.75rem !important;
    margin-bottom: 0.5rem !important;
}

.fnx-stat-val {
    font-size: 2.25rem !important;
    font-weight: 800 !important;
    color: #0B1F3A !important;
    line-height: 1 !important;
    margin-bottom: 0.4rem !important;
}

.fnx-stat-label {
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    color: #475569 !important;
    text-transform: uppercase !important;
}

.fnx-action-row {
    display: flex !important;
    gap: 1.25rem !important;
    margin-bottom: 2.5rem !important;
}

.fnx-dashboard-grid {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 1.75rem !important;
    margin-top: 2rem !important;
}

/* ==================== BUTTONS ==================== */
.fnx-btn {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 8px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    border: none !important;
    transition: background 0.15s, transform 0.1s !important;
    text-decoration: none !important;
}

.fnx-btn:active {
    transform: scale(0.98) !important;
}

.fnx-btn-primary {
    background-color: #0B1F3A !important;
    color: #FFFFFF !important;
}

.fnx-btn-primary:hover {
    background-color: #123B63 !important;
}

.fnx-btn-outline {
    background: transparent !important;
    border: 2px solid #0B1F3A !important;
    color: #0B1F3A !important;
}

.fnx-btn-outline:hover {
    background-color: #F1F5F9 !important;
}

.fnx-btn-ghost {
    background: transparent !important;
    color: #0284C7 !important;
    border: 2px solid #BAE6FD !important;
}

.fnx-btn-ghost:hover {
    background-color: #E0F2FE !important;
}

.fnx-btn-disabled {
    background-color: #E2E8F0 !important;
    color: #94A3B8 !important;
    cursor: not-allowed !important;
}

.fnx-btn-lg {
    padding: 0.95rem 2rem !important;
    font-size: 1.1rem !important;
}

.fnx-btn-sm {
    padding: 0.4rem 0.85rem !important;
    font-size: 0.85rem !important;
}

.fnx-btn-full {
    width: 100% !important;
}

/* ==================== CARDS & TABLES ==================== */
.fnx-card {
    background-color: #FFFFFF !important;
    border: 2px solid #CBD5E1 !important;
    border-radius: 12px !important;
    padding: 1.75rem !important;
    box-shadow: 0 4px 12px rgba(11,31,58,0.04) !important;
}

.fnx-card h3 {
    font-size: 1.25rem !important;
    font-weight: 800 !important;
    color: #0B1F3A !important;
    margin: 0 0 1rem 0 !important;
}

.fnx-table {
    width: 100% !important;
    border-collapse: collapse !important;
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}

.fnx-table th {
    background-color: #F1F5F9 !important;
    color: #0F172A !important;
    font-weight: 700 !important;
    text-align: left !important;
    padding: 0.85rem 1rem !important;
    border-bottom: 2px solid #CBD5E1 !important;
    font-size: 0.9rem !important;
}

.fnx-table td {
    padding: 0.85rem 1rem !important;
    border-bottom: 1px solid #E2E8F0 !important;
    color: #334155 !important;
    font-size: 0.92rem !important;
}

.fnx-badge {
    display: inline-block !important;
    padding: 0.3rem 0.65rem !important;
    border-radius: 20px !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
}

.st-new { background-color: #EFF6FF !important; color: #1D4ED8 !important; }
.st-progress { background-color: #FEF3C7 !important; color: #D97706 !important; }
.st-resolved { background-color: #DCFCE7 !important; color: #15803D !important; }

.sev-critical { background-color: #FEE2E2 !important; color: #B91C1C !important; }
.sev-high { background-color: #FFEDD5 !important; color: #C2410C !important; }
.sev-medium { background-color: #FEF9C3 !important; color: #A16207 !important; }
.sev-low { background-color: #F0FDF4 !important; color: #15803D !important; }

/* ==================== PROFILE & KYC ==================== */
.fnx-profile-grid {
    display: grid !important;
    grid-template-columns: 1.1fr 1fr !important;
    gap: 2rem !important;
    margin-top: 1.5rem !important;
}

.fnx-info-row {
    display: flex !important;
    justify-content: space-between !important;
    padding: 0.65rem 0 !important;
    border-bottom: 1px solid #F1F5F9 !important;
    font-size: 0.92rem !important;
}

.fnx-info-label {
    color: #64748B !important;
    font-weight: 600 !important;
}

.fnx-info-val {
    color: #0F172A !important;
    font-weight: 700 !important;
}

/* ==================== TRACK CASES & PROGRESS TRACKER ==================== */
.fnx-case-card {
    background-color: #FFFFFF !important;
    border: 2px solid #CBD5E1 !important;
    border-radius: 12px !important;
    padding: 2rem !important;
    margin-bottom: 2rem !important;
    box-shadow: 0 4px 12px rgba(11,31,58,0.04) !important;
}

.fnx-case-header {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    margin-bottom: 1.75rem !important;
}

.fnx-case-number {
    font-size: 1.35rem !important;
    font-weight: 800 !important;
    color: #0B1F3A !important;
    margin-right: 0.75rem !important;
}

.fnx-case-type {
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: #0284C7 !important;
}

.fnx-tracker {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    margin: 2rem 0 !important;
    padding: 1.5rem 2rem !important;
    background-color: #F8FAFC !important;
    border-radius: 10px !important;
}

.fnx-tracker-step {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    gap: 0.5rem !important;
    position: relative !important;
    z-index: 2 !important;
}

.fnx-tracker-dot {
    width: 32px !important;
    height: 32px !important;
    border-radius: 50% !important;
    background-color: #E2E8F0 !important;
    color: #FFFFFF !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 0.85rem !important;
    font-weight: 800 !important;
}

.fnx-tracker-step.completed .fnx-tracker-dot {
    background-color: #16A34A !important;
}

.fnx-tracker-step.current .fnx-tracker-dot {
    background-color: #00B8D9 !important;
    box-shadow: 0 0 0 4px rgba(0,184,217,0.2) !important;
}

.fnx-tracker-line {
    flex: 1 !important;
    height: 3px !important;
    background-color: #E2E8F0 !important;
    margin: 0 0.5rem !important;
}

.fnx-tracker-line.active {
    background-color: #16A34A !important;
}

.fnx-tracker-label {
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    color: #475569 !important;
}

.fnx-case-meta-grid {
    display: grid !important;
    grid-template-columns: repeat(4, 1fr) !important;
    gap: 1rem !important;
    padding: 1rem !important;
    background-color: #F1F5F9 !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
    margin-top: 1rem !important;
}

.fnx-evidence-tag-list {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 0.6rem !important;
    margin-top: 0.5rem !important;
}

.fnx-evidence-tag {
    background-color: #E0F2FE !important;
    color: #0369A1 !important;
    border: 1px solid #BAE6FD !important;
    padding: 0.35rem 0.75rem !important;
    border-radius: 6px !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
}

/* ==================== 5. FLOATING AI ASSISTANT ==================== */
.fnx-ai-widget {
    position: fixed !important;
    bottom: 2rem !important;
    right: 2rem !important;
    z-index: 1000 !important;
}

.fnx-ai-trigger {
    background: linear-gradient(135deg, #0B1F3A 0%, #123B63 100%) !important;
    color: #FFFFFF !important;
    border: 2px solid #00B8D9 !important;
    border-radius: 30px !important;
    padding: 0.75rem 1.4rem !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    box-shadow: 0 6px 20px rgba(11,31,58,0.25) !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}

.fnx-ai-trigger:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 25px rgba(0,184,217,0.3) !important;
}

.fnx-ai-panel {
    position: absolute !important;
    bottom: 60px !important;
    right: 0 !important;
    width: 380px !important;
    height: 500px !important;
    background-color: #FFFFFF !important;
    border: 2px solid #CBD5E1 !important;
    border-radius: 14px !important;
    box-shadow: 0 12px 35px rgba(11,31,58,0.2) !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
}

.fnx-ai-header {
    background-color: #0B1F3A !important;
    color: #FFFFFF !important;
    padding: 1rem 1.25rem !important;
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
}

.fnx-ai-badge {
    background-color: #00B8D9 !important;
    color: #0B1F3A !important;
    font-size: 0.7rem !important;
    font-weight: 800 !important;
    padding: 0.2rem 0.5rem !important;
    border-radius: 12px !important;
    margin-left: 0.5rem !important;
}

.fnx-ai-close {
    background: none !important;
    border: none !important;
    color: #FFFFFF !important;
    font-size: 1.5rem !important;
    cursor: pointer !important;
}

.fnx-ai-body {
    flex: 1 !important;
    padding: 1rem !important;
    overflow-y: auto !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 0.75rem !important;
    background-color: #F8FAFC !important;
}

.fnx-ai-msg {
    display: flex !important;
}

.fnx-ai-msg.ai { justify-content: flex-start !important; }
.fnx-ai-msg.user { justify-content: flex-end !important; }

.fnx-ai-bubble {
    max-width: 80% !important;
    padding: 0.75rem 1rem !important;
    border-radius: 12px !important;
    font-size: 0.88rem !important;
    line-height: 1.45 !important;
}

.fnx-ai-msg.ai .fnx-ai-bubble {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px 12px 12px 2px !important;
}

.fnx-ai-msg.user .fnx-ai-bubble {
    background-color: #0B1F3A !important;
    color: #FFFFFF !important;
    border-radius: 12px 12px 2px 12px !important;
}

.fnx-ai-footer {
    padding: 0.75rem 1rem !important;
    background-color: #FFFFFF !important;
    border-top: 1px solid #E2E8F0 !important;
    display: flex !important;
    gap: 0.5rem !important;
}

.fnx-ai-footer input {
    flex: 1 !important;
    padding: 0.6rem 0.85rem !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 6px !important;
    outline: none !important;
    font-size: 0.88rem !important;
}

/* ==================== MODAL OVERLAY ==================== */
.fnx-modal-overlay {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    background-color: rgba(11,31,58,0.6) !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    z-index: 200 !important;
}

.fnx-modal-box {
    background-color: #FFFFFF !important;
    border-radius: 12px !important;
    padding: 2.25rem !important;
    width: 100% !important;
    max-width: 520px !important;
    box-shadow: 0 15px 40px rgba(11,31,58,0.25) !important;
}

/* ============================================================
   7-STEP REPORT FRAUD / CASE REGISTRATION WORKSPACE STYLES
   ============================================================ */
.fnx-report-workspace {
    padding: 0.5rem 0.5rem 3rem 0.5rem !important;
}

.fnx-breadcrumbs {
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
    font-size: 0.88rem !important;
    color: #64748B !important;
    margin-bottom: 0.75rem !important;
}

.fnx-crumb-link {
    cursor: pointer !important;
    color: #0284C7 !important;
    font-weight: 600 !important;
}

.fnx-crumb-link:hover {
    text-decoration: underline !important;
}

.fnx-crumb-sep {
    color: #94A3B8 !important;
}

.fnx-crumb-current {
    color: #0F172A !important;
    font-weight: 700 !important;
}

.fnx-page-header-row {
    display: flex !important;
    justify-content: space-between !important;
    align-items: flex-start !important;
    margin-bottom: 1.5rem !important;
}

.fnx-page-title {
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    color: #0B1F3A !important;
    letter-spacing: -0.02em !important;
    margin: 0 0 0.25rem 0 !important;
}

.fnx-page-subtitle {
    font-size: 0.95rem !important;
    color: #475569 !important;
    margin: 0 !important;
}

/* ==================== 7-STEP CONNECTED HORIZONTAL STEPPER ==================== */
.fnx-stepper-card {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 1.25rem 1.5rem !important;
    margin-bottom: 1.75rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    overflow-x: auto !important;
}

.fnx-stepper-track {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    min-width: 720px !important;
}

.fnx-step-node {
    display: flex !important;
    align-items: center !important;
    flex: 1 !important;
}

.fnx-step-node:last-child {
    flex: 0 0 auto !important;
}

.fnx-step-circle-wrapper {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    cursor: pointer !important;
    user-select: none !important;
    gap: 0.4rem !important;
}

.fnx-step-circle {
    width: 38px !important;
    height: 38px !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 0.95rem !important;
    font-weight: 800 !important;
    transition: all 0.2s ease !important;
}

.fnx-step-node.completed .fnx-step-circle {
    background-color: #16A34A !important;
    color: #FFFFFF !important;
}

.fnx-step-node.active .fnx-step-circle {
    background-color: #0B1F3A !important;
    color: #00B8D9 !important;
    border: 2px solid #00B8D9 !important;
    box-shadow: 0 0 0 4px rgba(0, 184, 217, 0.25) !important;
}

.fnx-step-node.upcoming .fnx-step-circle {
    background-color: #F1F5F9 !important;
    color: #94A3B8 !important;
    border: 1px solid #CBD5E1 !important;
}

.fnx-step-label {
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    white-space: nowrap !important;
    text-align: center !important;
}

.fnx-step-node.completed .fnx-step-label {
    color: #16A34A !important;
}

.fnx-step-node.active .fnx-step-label {
    color: #0B1F3A !important;
    font-weight: 800 !important;
}

.fnx-step-node.upcoming .fnx-step-label {
    color: #94A3B8 !important;
}

.fnx-step-line {
    flex: 1 !important;
    height: 3px !important;
    background-color: #E2E8F0 !important;
    margin: 0 0.6rem !important;
    position: relative !important;
    top: -10px !important;
}

.fnx-step-line.active {
    background-color: #16A34A !important;
}

/* ==================== 2-COLUMN LAYOUT ==================== */
.fnx-report-layout {
    display: grid !important;
    grid-template-columns: 1fr 340px !important;
    gap: 1.75rem !important;
    align-items: start !important;
}

@media (max-width: 992px) {
    .fnx-report-layout {
        grid-template-columns: 1fr !important;
    }
}

.fnx-step-card {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 2rem !important;
    box-shadow: 0 2px 8px rgba(11,31,58,0.04) !important;
}

.fnx-step-card-header {
    display: flex !important;
    justify-content: space-between !important;
    align-items: flex-start !important;
    padding-bottom: 1.25rem !important;
    border-bottom: 1px solid #F1F5F9 !important;
    margin-bottom: 1.5rem !important;
}

.fnx-step-card-title {
    font-size: 1.35rem !important;
    font-weight: 800 !important;
    color: #0B1F3A !important;
    margin: 0 0 0.25rem 0 !important;
}

.fnx-step-card-sub {
    font-size: 0.9rem !important;
    color: #475569 !important;
    margin: 0 !important;
}

.fnx-form-grid-2 {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 1.25rem !important;
    margin-bottom: 1.25rem !important;
}

.fnx-form-grid-3 {
    display: grid !important;
    grid-template-columns: 1fr 1fr 1fr !important;
    gap: 1.25rem !important;
    margin-bottom: 1.25rem !important;
}

@media (max-width: 768px) {
    .fnx-form-grid-2, .fnx-form-grid-3 {
        grid-template-columns: 1fr !important;
    }
}

.fnx-field-counter {
    text-align: right !important;
    font-size: 0.78rem !important;
    color: #64748B !important;
    margin-top: 0.25rem !important;
}

.fnx-ai-suggestion-chip {
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.35rem !important;
    background-color: #ECFEFF !important;
    color: #0891B2 !important;
    border: 1px solid #A5F3FC !important;
    border-radius: 6px !important;
    padding: 0.25rem 0.6rem !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    margin-top: 0.35rem !important;
}

.fnx-severity-pill {
    padding: 0.35rem 0.8rem !important;
    border-radius: 20px !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
}

.fnx-subcard-section {
    background-color: #F8FAFC !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important;
    padding: 1.25rem !important;
    margin-top: 1.5rem !important;
    margin-bottom: 1.5rem !important;
}

.fnx-subcard-title {
    font-size: 0.88rem !important;
    font-weight: 800 !important;
    color: #0B1F3A !important;
    margin-bottom: 1rem !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
}

.fnx-chip-customer-reported {
    background-color: #E2E8F0 !important;
    color: #475569 !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    padding: 0.2rem 0.5rem !important;
    border-radius: 4px !important;
}

.fnx-toggle-row {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 1.5rem !important;
    background-color: #F8FAFC !important;
    padding: 0.85rem 1.25rem !important;
    border-radius: 8px !important;
    margin-bottom: 1.5rem !important;
    border: 1px dashed #CBD5E1 !important;
}

.fnx-checkbox-label {
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
    font-size: 0.9rem !important;
    color: #1E293B !important;
    font-weight: 600 !important;
    cursor: pointer !important;
}

.fnx-checkbox-label input[type="checkbox"] {
    width: 18px !important;
    height: 18px !important;
    cursor: pointer !important;
}

/* Security Notice Warning */
.fnx-security-warning-card {
    background-color: #FFFBEB !important;
    border: 1.5px solid #F59E0B !important;
    border-radius: 10px !important;
    padding: 1rem 1.25rem !important;
    color: #92400E !important;
    font-size: 0.9rem !important;
    line-height: 1.45 !important;
}

.fnx-sec-warning-header {
    font-size: 0.92rem !important;
    color: #B45309 !important;
    margin-bottom: 0.35rem !important;
}

/* Dropzone & Evidence */
.fnx-dropzone {
    border: 2px dashed #00B8D9 !important;
    background-color: #F0FDFE !important;
    border-radius: 12px !important;
    padding: 2.25rem 1.5rem !important;
    text-align: center !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    gap: 0.5rem !important;
    margin-bottom: 1.25rem !important;
}

.fnx-dropzone-icon {
    font-size: 2.5rem !important;
    line-height: 1 !important;
}

.fnx-dropzone-title {
    font-size: 1.15rem !important;
    font-weight: 800 !important;
    color: #0B1F3A !important;
}

.fnx-dropzone-or {
    font-size: 0.85rem !important;
    color: #64748B !important;
}

.fnx-dropzone-formats {
    font-size: 0.8rem !important;
    color: #475569 !important;
    margin-top: 0.5rem !important;
}

.fnx-quick-evidence-row {
    display: flex !important;
    align-items: center !important;
    flex-wrap: wrap !important;
    gap: 0.6rem !important;
    margin-bottom: 1.5rem !important;
}

.fnx-btn-pill {
    background-color: #F1F5F9 !important;
    border: 1px solid #CBD5E1 !important;
    color: #0B1F3A !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    padding: 0.35rem 0.75rem !important;
    border-radius: 20px !important;
    cursor: pointer !important;
}

.fnx-btn-pill:hover {
    background-color: #E2E8F0 !important;
}

.fnx-evidence-cards-list {
    display: flex !important;
    flex-direction: column !important;
    gap: 0.75rem !important;
}

.fnx-evidence-item-card {
    display: flex !important;
    align-items: center !important;
    gap: 1rem !important;
    padding: 0.85rem 1.25rem !important;
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
}

.fnx-ev-icon {
    font-size: 1.5rem !important;
}

.fnx-ev-meta {
    flex: 1 !important;
}

.fnx-ev-name {
    font-weight: 700 !important;
    color: #0B1F3A !important;
    font-size: 0.95rem !important;
}

.fnx-ev-details {
    font-size: 0.82rem !important;
    color: #64748B !important;
}

.fnx-ev-hash {
    font-family: monospace !important;
    color: #0284C7 !important;
}

.fnx-ev-status {
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    padding: 0.25rem 0.65rem !important;
    border-radius: 12px !important;
    background-color: #EFF6FF !important;
    color: #1D4ED8 !important;
}

.fnx-ev-status.processed {
    background-color: #DCFCE7 !important;
    color: #15803D !important;
}

.fnx-ev-delete {
    background: none !important;
    border: none !important;
    color: #94A3B8 !important;
    font-size: 1.35rem !important;
    cursor: pointer !important;
    line-height: 1 !important;
}

.fnx-ev-delete:hover {
    color: #DC2626 !important;
}

/* Step 6 Review Blocks */
.fnx-review-block {
    background-color: #F8FAFC !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important;
    padding: 1.25rem 1.5rem !important;
    margin-bottom: 1.25rem !important;
}

.fnx-review-block-header {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    margin-bottom: 0.85rem !important;
    border-bottom: 1px solid #E2E8F0 !important;
    padding-bottom: 0.5rem !important;
}

.fnx-review-block-header h3 {
    font-size: 0.9rem !important;
    font-weight: 800 !important;
    color: #0B1F3A !important;
    margin: 0 !important;
    letter-spacing: 0.03em !important;
}

.fnx-btn-edit-step {
    background: none !important;
    border: none !important;
    color: #0284C7 !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    cursor: pointer !important;
}

.fnx-btn-edit-step:hover {
    text-decoration: underline !important;
}

.fnx-review-grid {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 0.75rem 1.5rem !important;
    font-size: 0.9rem !important;
}

.fnx-rg-label {
    color: #64748B !important;
    font-weight: 600 !important;
    display: inline-block !important;
    min-width: 110px !important;
}

/* Step 7 Declaration & Success */
.fnx-declaration-box {
    background-color: #F1F5F9 !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 10px !important;
    padding: 1.5rem !important;
    margin-bottom: 2rem !important;
}

.fnx-btn-submit-fraud {
    background-color: #0B1F3A !important;
    border: 2px solid #00B8D9 !important;
    color: #FFFFFF !important;
    font-size: 1.1rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.02em !important;
}

.fnx-btn-submit-fraud:hover {
    background-color: #123B63 !important;
}

.fnx-success-submit-workspace {
    text-align: center !important;
    padding: 2.5rem 1rem !important;
}

.fnx-success-submit-badge {
    width: 72px !important;
    height: 72px !important;
    border-radius: 50% !important;
    background-color: #16A34A !important;
    color: #FFFFFF !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 2.5rem !important;
    margin: 0 auto 1.5rem auto !important;
    box-shadow: 0 10px 25px rgba(22, 163, 74, 0.25) !important;
}

.fnx-success-title {
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    color: #0B1F3A !important;
    margin: 0 0 0.4rem 0 !important;
}

.fnx-success-subtitle {
    font-size: 1.05rem !important;
    color: #475569 !important;
    margin: 0 0 2rem 0 !important;
}

.fnx-success-case-card {
    max-width: 480px !important;
    margin: 0 auto !important;
    background-color: #F8FAFC !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 12px !important;
    padding: 1.25rem 1.75rem !important;
}

.fnx-scc-row {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    padding: 0.6rem 0 !important;
    border-bottom: 1px solid #E2E8F0 !important;
}

.fnx-scc-row:last-child {
    border-bottom: none !important;
}

.fnx-scc-label {
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    color: #64748B !important;
}

.fnx-scc-val {
    font-size: 1.05rem !important;
    font-weight: 800 !important;
    color: #0B1F3A !important;
}

.fnx-success-actions {
    display: flex !important;
    justify-content: center !important;
    gap: 1.25rem !important;
    margin-top: 2rem !important;
}

/* Step Navigation Bar */
.fnx-step-nav-bar {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    padding-top: 1.75rem !important;
    border-top: 1px solid #F1F5F9 !important;
    margin-top: 2rem !important;
}

/* ==================== RIGHT PANEL CARDS ==================== */
.fnx-report-side {
    display: flex !important;
    flex-direction: column !important;
    gap: 1.25rem !important;
}

.fnx-side-card {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}

.fnx-side-card-header {
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
    margin-bottom: 0.75rem !important;
}

.fnx-side-card-header h4 {
    font-size: 1.05rem !important;
    font-weight: 800 !important;
    color: #0B1F3A !important;
    margin: 0 !important;
}

.fnx-side-card-icon {
    font-size: 1.25rem !important;
}

.fnx-side-card p {
    font-size: 0.9rem !important;
    color: #475569 !important;
    margin: 0 0 1rem 0 !important;
    line-height: 1.45 !important;
}

.fnx-btn-cyan-outline {
    background-color: #FFFFFF !important;
    border: 2px solid #00B8D9 !important;
    color: #0B1F3A !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    padding: 0.65rem 1rem !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 0.4rem !important;
    transition: all 0.15s ease !important;
}

.fnx-btn-cyan-outline:hover {
    background-color: #ECFEFF !important;
}

.fnx-tips-list {
    margin: 0 !important;
    padding-left: 1.2rem !important;
    font-size: 0.88rem !important;
    color: #334155 !important;
    line-height: 1.6 !important;
}

.fnx-tips-list li {
    margin-bottom: 0.4rem !important;
}

.fnx-user-summary-badge {
    display: inline-block !important;
    background-color: #EFF6FF !important;
    color: #0284C7 !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    padding: 0.2rem 0.6rem !important;
    border-radius: 4px !important;
    margin-bottom: 0.85rem !important;
}

.fnx-user-info-row {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    padding: 0.45rem 0 !important;
    border-bottom: 1px solid #F1F5F9 !important;
    font-size: 0.88rem !important;
}

.fnx-ui-label {
    color: #64748B !important;
    font-weight: 600 !important;
}

.fnx-ui-val {
    color: #0F172A !important;
    font-weight: 700 !important;
}

.fnx-user-info-note {
    margin-top: 0.85rem !important;
    font-size: 0.78rem !important;
    color: #64748B !important;
    line-height: 1.4 !important;
}


/* ===== DEMO BUTTON ===== */
.fnx-btn-demo { display:flex !important; align-items:center !important; justify-content:center !important; gap:0.5rem !important; background:linear-gradient(135deg,#1a4f82,#0B1F3A) !important; border:1px solid rgba(0,184,217,0.4) !important; color:#FFFFFF !important; font-size:0.95rem !important; padding:0.75rem 1.5rem !important; border-radius:8px !important; cursor:pointer !important; transition:all 0.2s !important; }
.fnx-btn-demo:hover { background:linear-gradient(135deg,#225c94,#123B63) !important; box-shadow:0 0 0 3px rgba(0,184,217,0.2) !important; }
.fnx-demo-badge { background:#00B8D9 !important; color:#0B1F3A !important; font-size:0.65rem !important; font-weight:800 !important; padding:0.15rem 0.45rem !important; border-radius:4px !important; }
.fnx-demo-divider { display:flex !important; align-items:center !important; gap:0.75rem !important; color:#94A3B8 !important; font-size:0.85rem !important; margin:1rem 0 !important; }
.fnx-demo-divider::before,.fnx-demo-divider::after { content:'' !important; flex:1 !important; height:1px !important; background:#E2E8F0 !important; }
.fnx-demo-hint { text-align:center !important; font-size:0.8rem !important; color:#94A3B8 !important; margin:0.5rem 0 0 !important; }
.fnx-auth-form-header { margin-bottom:1.5rem !important; }
.fnx-auth-form-title { font-size:1.35rem !important; font-weight:800 !important; color:#0B1F3A !important; letter-spacing:0.04em !important; margin:0 0 0.35rem 0 !important; }
.fnx-auth-form-sub { font-size:0.88rem !important; color:#64748B !important; margin:0 !important; }
.fnx-auth-left-tagline { font-size:0.78rem !important; font-weight:700 !important; color:#00B8D9 !important; letter-spacing:0.12em !important; text-transform:uppercase !important; margin:0 0 0.75rem 0 !important; }
.fnx-auth-left-title { font-size:1.65rem !important; font-weight:800 !important; color:#FFFFFF !important; line-height:1.25 !important; letter-spacing:0.02em !important; margin:0 0 1rem 0 !important; }
.fnx-auth-left-desc { font-size:0.9rem !important; color:rgba(255,255,255,0.7) !important; line-height:1.6 !important; margin:0 0 1.5rem 0 !important; }
.fnx-auth-capabilities { display:flex !important; flex-direction:column !important; gap:0.6rem !important; }
.fnx-auth-cap { font-size:0.88rem !important; color:rgba(255,255,255,0.85) !important; }
.fnx-hero-stats { display:flex !important; align-items:center !important; gap:1.5rem !important; margin-top:2rem !important; padding-top:1.5rem !important; border-top:1px solid rgba(0,184,217,0.2) !important; }
.fnx-hero-stat { display:flex !important; flex-direction:column !important; gap:0.2rem !important; }
.fnx-hs-num { font-size:1.25rem !important; font-weight:800 !important; color:#00B8D9 !important; }
.fnx-hs-label { font-size:0.8rem !important; color:rgba(255,255,255,0.6) !important; }
.fnx-hero-stat-div { width:1px !important; height:40px !important; background:rgba(0,184,217,0.2) !important; }
.fnx-features-section { padding:4rem 2rem !important; background:#0B1F3A !important; }
.fnx-features-header { text-align:center !important; margin-bottom:3rem !important; }
.fnx-features-title { font-size:1.75rem !important; font-weight:800 !important; color:#FFFFFF !important; letter-spacing:0.04em !important; margin:0 0 0.75rem 0 !important; }
.fnx-features-sub { font-size:1rem !important; color:rgba(255,255,255,0.65) !important; margin:0 !important; }
.fnx-how-it-works { padding:3.5rem 2rem !important; background:#123B63 !important; text-align:center !important; }
.fnx-hiw-header h2 { font-size:1.5rem !important; font-weight:800 !important; color:#FFFFFF !important; letter-spacing:0.05em !important; margin:0 0 0.5rem 0 !important; }
.fnx-hiw-header p { color:rgba(255,255,255,0.6) !important; margin:0 0 2rem 0 !important; }
.fnx-hiw-steps { display:flex !important; align-items:center !important; justify-content:center !important; gap:0.5rem !important; flex-wrap:wrap !important; }
.fnx-hiw-step { display:flex !important; flex-direction:column !important; align-items:center !important; gap:0.5rem !important; }
.fnx-hiw-circle { width:44px !important; height:44px !important; border-radius:50% !important; background:#00B8D9 !important; color:#0B1F3A !important; font-weight:800 !important; font-size:1.1rem !important; display:flex !important; align-items:center !important; justify-content:center !important; }
.fnx-hiw-label { font-size:0.78rem !important; color:rgba(255,255,255,0.8) !important; white-space:nowrap !important; }
.fnx-hiw-arrow { color:#00B8D9 !important; font-size:1.25rem !important; margin-bottom:1.5rem !important; }
.fnx-audience-section { display:flex !important; gap:2rem !important; padding:3.5rem 2rem !important; background:#F5F7FA !important; flex-wrap:wrap !important; }
.fnx-audience-card { flex:1 !important; min-width:280px !important; padding:2rem !important; border-radius:16px !important; }
.fnx-audience-customer { background:#0B1F3A !important; color:#FFFFFF !important; }
.fnx-audience-investigator { background:#FFFFFF !important; border:2px solid #E2E8F0 !important; }
.fnx-audience-icon { font-size:2.5rem !important; margin-bottom:1rem !important; }
.fnx-audience-card h3 { font-size:1.1rem !important; font-weight:800 !important; letter-spacing:0.05em !important; margin:0 0 1.25rem 0 !important; }
.fnx-audience-customer h3 { color:#00B8D9 !important; }
.fnx-audience-investigator h3 { color:#0B1F3A !important; }
.fnx-audience-card ul { list-style:none !important; padding:0 !important; margin:0 0 1.5rem 0 !important; }
.fnx-audience-card li { padding:0.4rem 0 !important; font-size:0.9rem !important; color:rgba(255,255,255,0.8) !important; border-bottom:1px solid rgba(255,255,255,0.08) !important; }
.fnx-audience-investigator li { color:#475569 !important; border-bottom-color:#E2E8F0 !important; }
.fnx-coming-soon-badge { display:inline-block !important; background:#F59E0B !important; color:#0B1F3A !important; font-weight:800 !important; font-size:0.88rem !important; padding:0.5rem 1.25rem !important; border-radius:20px !important; }
.fnx-security-section { padding:3.5rem 2rem !important; background:#0B1F3A !important; text-align:center !important; }
.fnx-security-section h2 { font-size:1.5rem !important; font-weight:800 !important; color:#FFFFFF !important; letter-spacing:0.05em !important; margin:0 0 2rem 0 !important; }
.fnx-security-grid { display:grid !important; grid-template-columns:repeat(3,1fr) !important; gap:1rem !important; max-width:700px !important; margin:0 auto !important; }
.fnx-sec-item { background:rgba(0,184,217,0.08) !important; border:1px solid rgba(0,184,217,0.2) !important; border-radius:10px !important; padding:1rem !important; font-size:0.9rem !important; color:rgba(255,255,255,0.85) !important; display:flex !important; align-items:center !important; gap:0.5rem !important; }
.fnx-sec-check { color:#00B8D9 !important; font-weight:800 !important; }
.fnx-final-cta { padding:4rem 2rem !important; background:linear-gradient(135deg,#0B1F3A,#123B63) !important; text-align:center !important; border-top:2px solid rgba(0,184,217,0.2) !important; }
.fnx-final-cta h2 { font-size:1.6rem !important; font-weight:800 !important; color:#FFFFFF !important; letter-spacing:0.04em !important; margin:0 0 0.75rem 0 !important; }
.fnx-final-cta p { color:rgba(255,255,255,0.65) !important; margin:0 0 2rem 0 !important; font-size:1rem !important; }
.fnx-fin-section { background:#F8FAFC !important; border:1px solid #E2E8F0 !important; border-radius:12px !important; padding:1.25rem 1.5rem !important; margin-bottom:1.25rem !important; }
.fnx-fin-section-title { font-size:0.78rem !important; font-weight:800 !important; color:#0B1F3A !important; letter-spacing:0.1em !important; text-transform:uppercase !important; margin-bottom:1rem !important; display:flex !important; align-items:center !important; gap:0.5rem !important; border-bottom:2px solid #E2E8F0 !important; padding-bottom:0.65rem !important; }
.fnx-evidence-type-tags { display:flex !important; flex-wrap:wrap !important; gap:0.5rem !important; margin:1rem 0 !important; justify-content:center !important; }
.fnx-ev-tag { background:#F1F5F9 !important; border:1px solid #E2E8F0 !important; color:#475569 !important; font-size:0.8rem !important; padding:0.3rem 0.7rem !important; border-radius:20px !important; }
.fnx-profile-dropdown-cid { font-size:0.75rem !important; color:#7AADCC !important; padding:0.3rem 1.1rem 0.5rem !important; font-family:monospace !important; }
.fnx-edit-profile-view { padding:0 !important; }

/* ==================== GLOBAL CARD & ICON CONTAINMENT ==================== */
/* 1. Global Card Rules: strict clipping so NO child or icon can ever breach the card boundary */
.fnx-card,
.fnx-stat-card,
.fnx-feature-card,
.fnx-portal-card,
.fnx-case-card,
.fnx-side-card,
.fnx-evidence-item-card,
.fnx-profile-info-card,
.fnx-kyc-card,
.fnx-step-card,
.fnx-stepper-card,
.fnx-subcard-section {
    position: relative !important;
    overflow: hidden !important; /* STRICT GLOBAL CONTAINMENT: nothing escapes card bounds */
    contain: layout paint !important;
}

/* 2. Global Icon Base Rules: icons always stay centered, upright, and strictly inside padding */
.fnx-stat-icon,
.fnx-feature-icon,
.fnx-portal-card-icon,
.fnx-ev-icon,
.fnx-side-card-icon,
.fnx-dropzone-icon,
.fnx-nav-icon {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    transform-origin: center center !important;
    pointer-events: none !important; /* Card handles hover; icon stays anchored */
    transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    max-width: 100% !important;
    max-height: 100% !important;
    line-height: 1 !important;
}

/* 3. Feature Cards (Landing Page) */
.fnx-feature-card {
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.2s ease !important;
    cursor: pointer !important;
}
.fnx-feature-card:hover {
    transform: translateY(-4px) !important;
    border-color: #00B8D9 !important;
    box-shadow: 0 14px 28px -4px rgba(0, 184, 217, 0.2), 0 0 0 1px rgba(0, 184, 217, 0.2) !important;
}
.fnx-feature-card:hover .fnx-feature-icon {
    transform: scale(1.08) !important;
}

/* 4. Portal Cards (Portal Select) */
.fnx-portal-card {
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.2s ease !important;
    cursor: pointer !important;
}
.fnx-portal-card:hover {
    transform: translateY(-4px) !important;
    border-color: #00B8D9 !important;
    box-shadow: 0 14px 28px -4px rgba(0, 184, 217, 0.2) !important;
}
.fnx-portal-card:hover .fnx-portal-card-icon {
    transform: scale(1.08) !important;
}

/* 5. Stat Cards (Dashboard) */
.fnx-stat-card {
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.2s ease !important;
    cursor: pointer !important;
}
.fnx-stat-card:hover {
    transform: translateY(-4px) !important;
    border-color: #00B8D9 !important;
    box-shadow: 0 12px 24px -4px rgba(11, 31, 58, 0.1), 0 0 0 1px rgba(0, 184, 217, 0.3) !important;
}
.fnx-stat-card:hover .fnx-stat-icon {
    transform: scale(1.08) !important; /* Scales strictly within padding, never touches border */
}

/* 6. Case Cards */
.fnx-case-card {
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.2s ease !important;
}
.fnx-case-card:hover {
    transform: translateY(-3px) !important;
    border-color: #00B8D9 !important;
    box-shadow: 0 10px 20px -4px rgba(11, 31, 58, 0.08) !important;
}

/* 7. Evidence Item Cards */
.fnx-evidence-item-card {
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease !important;
    cursor: pointer !important;
}
.fnx-evidence-item-card:hover {
    transform: translateY(-2px) !important;
    border-color: #00B8D9 !important;
    box-shadow: 0 6px 14px -3px rgba(11, 31, 58, 0.08) !important;
}
.fnx-evidence-item-card:hover .fnx-ev-icon {
    transform: scale(1.08) !important;
}

/* 8. Side Cards */
.fnx-side-card {
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.2s ease !important;
}
.fnx-side-card:hover {
    transform: translateY(-3px) !important;
    border-color: rgba(0, 184, 217, 0.4) !important;
    box-shadow: 0 10px 20px -4px rgba(0, 184, 217, 0.12) !important;
}
.fnx-side-card:hover .fnx-side-card-icon {
    transform: scale(1.08) !important;
}

/* 9. Stepper & Step Cards */
.fnx-step-card:hover, .fnx-profile-info-card:hover, .fnx-kyc-card:hover {
    box-shadow: 0 8px 18px -4px rgba(11, 31, 58, 0.08) !important;
    border-color: #CBD5E1 !important;
}

/* 10. Navigation & Action Icons */
.fnx-nav-item:hover .fnx-nav-icon {
    transform: scale(1.1) !important;
}
.fnx-dropzone:hover .fnx-dropzone-icon {
    transform: scale(1.1) !important;
}
.fnx-icon-btn:hover {
    transform: scale(1.1) !important;
}
.fnx-hero-stat:hover {
    transform: translateY(-2px) !important;
}

/* ==================== NOW ASSIST GENAI STYLES ==================== */
.fnx-ai-now-badge {
    background: linear-gradient(135deg, #7C3AED, #00B8D9) !important;
    color: #FFFFFF !important;
    font-size: 0.65rem !important;
    font-weight: 800 !important;
    padding: 0.15rem 0.5rem !important;
    border-radius: 12px !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    margin-left: 0.5rem !important;
}
.fnx-ai-header {
    background: linear-gradient(135deg, #0B1F3A, #123B63) !important;
    border-bottom: 2px solid rgba(0, 184, 217, 0.4) !important;
    padding: 0.85rem 1.25rem !important;
}
.fnx-ai-title-row {
    display: flex !important;
    align-items: center !important;
    gap: 0.35rem !important;
}
.fnx-ai-sparkle-icon {
    color: #00B8D9 !important;
    font-size: 1.1rem !important;
}
.fnx-ai-subtitle {
    font-size: 0.75rem !important;
    color: #7AADCC !important;
    margin-top: 0.15rem !important;
}
.fnx-ai-sender-label {
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    color: #00B8D9 !important;
    margin-bottom: 0.35rem !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.25rem !important;
}
.fnx-ai-msg-group {
    display: flex !important;
    flex-direction: column !important;
    gap: 0.4rem !important;
}
.fnx-ai-action-btn-row {
    margin-top: 0.65rem !important;
    padding-top: 0.5rem !important;
    border-top: 1px solid rgba(0, 184, 217, 0.15) !important;
}
.fnx-btn-xs {
    padding: 0.35rem 0.85rem !important;
    font-size: 0.78rem !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
}
.fnx-ai-suggestions {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 0.4rem !important;
    margin-top: 0.4rem !important;
    margin-bottom: 0.4rem !important;
}
.fnx-ai-chip {
    background: rgba(0, 184, 217, 0.08) !important;
    border: 1px solid rgba(0, 184, 217, 0.35) !important;
    color: #0B1F3A !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    padding: 0.3rem 0.75rem !important;
    border-radius: 14px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}
.fnx-ai-chip:hover {
    background: #00B8D9 !important;
    color: #0B1F3A !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 10px rgba(0, 184, 217, 0.3) !important;
}
.fnx-ai-typing {
    display: flex !important;
    align-items: center !important;
    gap: 0.35rem !important;
    padding: 0.65rem 1rem !important;
}
.fnx-ai-typing-label {
    font-size: 0.78rem !important;
    color: #64748B !important;
    margin-right: 0.25rem !important;
}
.fnx-ai-typing .dot {
    width: 6px !important;
    height: 6px !important;
    background: #00B8D9 !important;
    border-radius: 50% !important;
    animation: fnxBounce 1.4s infinite ease-in-out both !important;
}
.fnx-ai-typing .dot:nth-child(2) { animation-delay: -0.32s !important; }
.fnx-ai-typing .dot:nth-child(3) { animation-delay: -0.16s !important; }
@keyframes fnxBounce {
    0%, 80%, 100% { transform: scale(0); opacity: 0.4; }
    40% { transform: scale(1); opacity: 1; }
}
"""

print("--- Uploading Master Widget Components to ServiceNow ---")
widget_payload = {
    'template': template,
    'client_script': client_script,
    'script': server_script,
    'css': css
}

r = requests.patch(f"{url}/api/now/table/sp_widget/{WIDGET_ID}", auth=auth, headers=headers, json=widget_payload)
print(f"Deploy status: {r.status_code}")
if r.status_code == 200:
    print("SUCCESS: Master Customer Experience Widget successfully deployed!")
else:
    print(f"FAILED: {r.text[:400]}")
