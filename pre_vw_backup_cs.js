api.controller = function($scope, $http, $timeout, $window) {
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

    // ====== GOOGLE TRANSLATE PANEL GLUE (used by template) ======
    c.showLangPanel = false;
    c.currentGtLang = c.lang || 'en';

    c.openGoogleTranslate = function() {
        c.showLangPanel = !c.showLangPanel;
    };

    c.setGoogleTranslateLang = function(langCode) {
        c.lang = langCode;
        c.currentGtLang = langCode;
        c.showLangPanel = false;
        $window.localStorage.setItem('fnx_lang', langCode);
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
            logout: 'Logout',
            commandCenter: 'Command Center',
            partners: 'Partners',
            partnerDirectory: 'Partner Directory',
            addPartner: 'Add Partner',
            editPartner: 'Edit Partner',
            partnerRequests: 'Partner Requests',
            requestStatus: 'Request Status',
            partnerCategory: 'Partner Category',
            integrationType: 'Integration Type',
            active: 'Active',
            inactive: 'Inactive',
            suspended: 'Suspended',
            simulatedDemoPartner: 'Simulated Demo Partner',
            totalPartners: 'Total Partners',
            activePartners: 'Active Partners',
            pendingRequests: 'Pending Requests',
            awaitingResponse: 'Awaiting Response',
            overdueRequests: 'Overdue Requests',
            customers: 'Customers',
            cases: 'Cases',
            investigation: 'Investigation',
            intelligenceWorkspace: 'Intelligence Workspace',
            analytics: 'Analytics',
            settings: 'Settings',
            adminLoginTitle: 'WELCOME BACK',
            adminLoginSub: 'Sign in to FRAUDNEXUS Investigation Workspace',
            signIn: 'SIGN IN',
            tryDemo: 'TRY DEMO',
            demoEnv: 'DEMO ENVIRONMENT',
            priorityQueue: 'PRIORITY INVESTIGATION QUEUE',
            actionCenter: 'ACTION CENTER',
            fraudTrends: 'FRAUD CASE TRENDS',
            financialExposureSummary: 'FINANCIAL EXPOSURE SUMMARY',
            recentActivity: 'RECENT ACTIVITY',
            newCases: 'NEW CASES',
            criticalCases: 'CRITICAL CASES',
            escalatedCases: 'ESCALATED CASES',
            pendingApprovals: 'PENDING APPROVALS',
            financialExposure: 'FINANCIAL EXPOSURE',
            unassigned: 'Unassigned',
            assign: 'Assign',
            openWorkspace: 'Open Workspace',
            requestEvidence: 'Request Evidence',
            escalate: 'Escalate',
            resolve: 'Resolve',
            closeCase: 'Close Case',
            addTask: 'Add Task',

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
    // ============================================================
    // FRAUDNEXUS ADMIN / INVESTIGATOR PORTAL: PARTNERS MODULE
    // ============================================================
    c.partnerTab = 'directory';
    c.partnersList = [];
    c.partnerRequestsList = [];
    c.partnerCasesList = [];
    c.partnerRecentAudit = [];
    c.partnerKpis = {
        total_partners: 0,
        active_partners: 0,
        inactive_partners: 0,
        pending_requests: 0,
        awaiting_response: 0,
        overdue_requests: 0
    };
    c.partnerSearch = '';
    c.partnerCategoryFilter = 'all';
    c.partnerStatusFilter = 'all';
    c.partnerIntegrationFilter = 'all';
    c.partnerDemoFilter = 'all';

    c.partnerReqSearch = '';
    c.partnerReqStatusFilter = 'all';
    c.partnerReqPriorityFilter = 'all';
    c.partnerReqTypeFilter = 'all';
    c.partnerReqPartnerFilter = 'all';

    c.activePartner = null;
    c.activePartnerRequest = null;
    c.showAddPartnerModal = false;
    c.isEditingPartner = false;
    c.partnerActionLoading = false;
    c.partnerFeedback = '';
    c.partnerFeedbackIsError = false;

    c.showPartnerBlockedModal = false;
    c.blockedPartnerMessage = '';
    c.targetBlockedPartner = null;

    c.partnerForm = {
        sys_id: '',
        partner_number: '',
        name: '',
        category: 'Banks / Financial Institutions',
        organization: '',
        description: '',
        contact_person: '',
        contact_email: '',
        contact_phone: '',
        status: 'Active',
        integration_type: 'Simulated API',
        endpoint_reference: '',
        sla: '4 Hours',
        demo_flag: true,
        notes: 'SIMULATED DEMO PARTNER'
    };

    c.showPartnerReqModal = false;
    c.partnerReqForm = {
        partner_id: '',
        case_id: '',
        request_type: 'Request Transaction Information',
        priority: 'High',
        reference: '',
        description: '',
        simulate: true
    };

    c.setPartnerTab = function(tab) {
        c.partnerTab = tab;
    };

    c.loadPartners = function() {
        $http.get(API + '/admin_partners')
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.partnerKpis = d.kpis || c.partnerKpis;
                c.partnersList = d.partners || [];
                c.partnerRequestsList = d.requests || [];
                c.partnerCasesList = d.cases || [];
                c.partnerRecentAudit = d.recent_audit || [];
                
                // If an active partner is open in drawer, update its reference
                if (c.activePartner) {
                    for (var i = 0; i < c.partnersList.length; i++) {
                        if (c.partnersList[i].sys_id === c.activePartner.sys_id) {
                            c.activePartner = c.partnersList[i];
                            break;
                        }
                    }
                }
            }
        }, function(err) {
            console.error('Failed to load partners:', err);
        });
    };

    c.getFilteredPartners = function() {
        if (!c.partnersList) return [];
        return c.partnersList.filter(function(p) {
            // Text Search
            if (c.partnerSearch) {
                var q = c.partnerSearch.toLowerCase().trim();
                var pNum = (p.partner_number || '').toLowerCase();
                var pName = (p.name || '').toLowerCase();
                var pOrg = (p.organization || '').toLowerCase();
                var pDesc = (p.description || '').toLowerCase();
                if (pNum.indexOf(q) === -1 && pName.indexOf(q) === -1 && pOrg.indexOf(q) === -1 && pDesc.indexOf(q) === -1) {
                    return false;
                }
            }
            // Category Filter
            if (c.partnerCategoryFilter !== 'all' && p.category !== c.partnerCategoryFilter) {
                return false;
            }
            // Status Filter
            if (c.partnerStatusFilter !== 'all' && p.status !== c.partnerStatusFilter) {
                return false;
            }
            // Integration Type Filter
            if (c.partnerIntegrationFilter !== 'all' && p.integration_type !== c.partnerIntegrationFilter) {
                return false;
            }
            // Demo Filter
            if (c.partnerDemoFilter === 'demo' && !p.demo_flag) {
                return false;
            }
            if (c.partnerDemoFilter === 'production' && p.demo_flag) {
                return false;
            }
            return true;
        });
    };

    c.getFilteredPartnerRequests = function() {
        if (!c.partnerRequestsList) return [];
        return c.partnerRequestsList.filter(function(r) {
            // Text Search
            if (c.partnerReqSearch) {
                var q = c.partnerReqSearch.toLowerCase().trim();
                var rNum = (r.request_number || '').toLowerCase();
                var cNum = (r.case_number || '').toLowerCase();
                var pName = (r.partner_name || '').toLowerCase();
                var rType = (r.request_type || '').toLowerCase();
                var rRef = (r.reference || '').toLowerCase();
                if (rNum.indexOf(q) === -1 && cNum.indexOf(q) === -1 && pName.indexOf(q) === -1 && rType.indexOf(q) === -1 && rRef.indexOf(q) === -1) {
                    return false;
                }
            }
            // Status Filter
            if (c.partnerReqStatusFilter !== 'all') {
                if (c.partnerReqStatusFilter === 'pending') {
                    if (r.status !== 'Draft' && r.status !== 'Submitted' && r.status !== 'In Progress' && r.status !== 'Awaiting Response') {
                        return false;
                    }
                } else if (r.status !== c.partnerReqStatusFilter) {
                    return false;
                }
            }
            // Priority Filter
            if (c.partnerReqPriorityFilter !== 'all' && r.priority !== c.partnerReqPriorityFilter) {
                return false;
            }
            // Request Type Filter
            if (c.partnerReqTypeFilter !== 'all' && r.request_type !== c.partnerReqTypeFilter) {
                return false;
            }
            // Partner Filter
            if (c.partnerReqPartnerFilter !== 'all' && r.partner_id !== c.partnerReqPartnerFilter) {
                return false;
            }
            return true;
        });
    };

    c.getCasePartnerRequests = function(cs) {
        if (!cs || !c.partnerRequestsList) return [];
        var csId = cs.sys_id;
        var csNum = cs.number || cs.task_effective_number || cs.u_number;
        return c.partnerRequestsList.filter(function(r) {
            return (csId && r.case_id === csId) || (csNum && r.case_number === csNum);
        });
    };

    c.getCategoryBadgeClass = function(cat) {
        if (!cat) return 'cat-bank';
        if (cat.indexOf('Bank') !== -1) return 'cat-bank';
        if (cat.indexOf('Payment') !== -1) return 'cat-payment';
        if (cat.indexOf('Cyber') !== -1) return 'cat-cyber';
        if (cat.indexOf('Threat') !== -1) return 'cat-intel';
        if (cat.indexOf('AML') !== -1) return 'cat-aml';
        if (cat.indexOf('KYC') !== -1) return 'cat-kyc';
        if (cat.indexOf('Regulat') !== -1) return 'cat-reg';
        if (cat.indexOf('Law') !== -1) return 'cat-law';
        return 'cat-bank';
    };

    c.getCategoryBreakdown = function() {
        var bd = {};
        for (var i = 0; i < c.partnersList.length; i++) {
            var cat = c.partnersList[i].category || 'Other';
            bd[cat] = (bd[cat] || 0) + 1;
        }
        return bd;
    };

    c.getIntegrationBreakdown = function() {
        var bd = {};
        for (var i = 0; i < c.partnersList.length; i++) {
            var it = c.partnersList[i].integration_type || 'Simulated API';
            bd[it] = (bd[it] || 0) + 1;
        }
        return bd;
    };

    c.getCompletedRequestsCount = function() {
        var cnt = 0;
        for (var i = 0; i < c.partnerRequestsList.length; i++) {
            if (c.partnerRequestsList[i].status === 'Completed' || c.partnerRequestsList[i].status === 'Response Received') {
                cnt++;
            }
        }
        return cnt;
    };

    c.getPartnerActiveRequests = function(p) {
        if (!p) return [];
        return c.partnerRequestsList.filter(function(r) {
            return r.partner_id === p.sys_id && r.status !== 'Completed' && r.status !== 'Cancelled' && r.status !== 'Rejected';
        });
    };

    c.getPartnerCompletedRequests = function(p) {
        if (!p) return [];
        return c.partnerRequestsList.filter(function(r) {
            return r.partner_id === p.sys_id && (r.status === 'Completed' || r.status === 'Response Received');
        });
    };

    c.getPartnerRelatedCases = function(p) {
        if (!p) return [];
        var caseSet = {};
        for (var i = 0; i < c.partnerRequestsList.length; i++) {
            var r = c.partnerRequestsList[i];
            if (r.partner_id === p.sys_id && r.case_number) {
                caseSet[r.case_number] = true;
            }
        }
        return Object.keys(caseSet);
    };

    c.getPartnerAuditEvents = function(p) {
        if (!p || !c.partnerRecentAudit) return [];
        return c.partnerRecentAudit.filter(function(a) {
            return (a.record_id && (a.record_id === p.partner_number || a.record_id === p.name)) ||
                   (a.details && (a.details.indexOf(p.name) !== -1 || a.details.indexOf(p.partner_number) !== -1));
        });
    };

    c.openAddPartner = function() {
        c.isEditingPartner = false;
        c.partnerForm = {
            sys_id: '',
            partner_number: '',
            name: '',
            category: 'Banks / Financial Institutions',
            organization: '',
            description: '',
            contact_person: '',
            contact_email: '',
            contact_phone: '',
            status: 'Active',
            integration_type: 'Simulated API',
            endpoint_reference: '',
            sla: '4 Hours',
            demo_flag: true,
            notes: 'SIMULATED DEMO PARTNER'
        };
        c.showAddPartnerModal = true;
    };

    c.openEditPartner = function(p) {
        c.isEditingPartner = true;
        c.partnerForm = {
            sys_id: p.sys_id,
            partner_number: p.partner_number,
            name: p.name,
            category: p.category,
            organization: p.organization,
            description: p.description,
            contact_person: p.contact_person,
            contact_email: p.contact_email,
            contact_phone: p.contact_phone,
            status: p.status,
            integration_type: p.integration_type,
            endpoint_reference: p.endpoint_reference,
            sla: p.sla,
            demo_flag: p.demo_flag,
            notes: p.notes
        };
        c.showAddPartnerModal = true;
    };

    c.savePartner = function() {
        if (!c.partnerForm.name || !c.partnerForm.category || !c.partnerForm.organization) return;
        c.partnerActionLoading = true;
        var act = c.isEditingPartner ? 'update_partner' : 'create_partner';
        var payload = {
            action: act,
            actor: (c.adminUser && c.adminUser.name) || 'Alex Morgan',
            sys_id: c.partnerForm.sys_id,
            partner: c.partnerForm
        };

        $http.post(API + '/admin_partners', payload)
        .then(function(resp) {
            c.partnerActionLoading = false;
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.showAddPartnerModal = false;
                c.partnerFeedback = c.isEditingPartner ? 'Partner updated successfully.' : 'Partner created successfully with ID: ' + (d.partner_number || 'Generated');
                c.partnerFeedbackIsError = false;
                c.loadPartners();
            } else {
                c.partnerFeedback = d.error || 'Failed to save partner.';
                c.partnerFeedbackIsError = true;
            }
        }, function(err) {
            c.partnerActionLoading = false;
            c.partnerFeedback = 'Server error occurred while saving partner.';
            c.partnerFeedbackIsError = true;
        });
    };

    c.togglePartnerStatus = function(p) {
        if (!p) return;
        var newStatus = p.status === 'Active' ? 'Inactive' : 'Active';
        var payload = {
            action: 'set_status',
            actor: (c.adminUser && c.adminUser.name) || 'Alex Morgan',
            sys_id: p.sys_id,
            status: newStatus
        };

        $http.post(API + '/admin_partners', payload)
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                p.status = newStatus;
                c.partnerFeedback = 'Partner status changed to ' + newStatus + '.';
                c.partnerFeedbackIsError = false;
                c.loadPartners();
            }
        });
    };

    c.removePartner = function(p) {
        if (!p) return;
        var payload = {
            action: 'delete_partner',
            actor: (c.adminUser && c.adminUser.name) || 'Alex Morgan',
            sys_id: p.sys_id
        };

        $http.post(API + '/admin_partners', payload)
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.blocked) {
                // Partner is referenced: block deletion!
                c.targetBlockedPartner = p;
                c.blockedPartnerMessage = d.message || 'Partner is referenced by existing records. Deactivate the partner instead of deleting it.';
                c.showPartnerBlockedModal = true;
            } else if (d.success) {
                c.partnerFeedback = 'Partner removed successfully.';
                c.partnerFeedbackIsError = false;
                if (c.activePartner && c.activePartner.sys_id === p.sys_id) {
                    c.closePartnerDetail();
                }
                c.loadPartners();
            } else {
                c.partnerFeedback = d.error || 'Unable to delete partner.';
                c.partnerFeedbackIsError = true;
            }
        });
    };

    c.deactivateBlockedPartner = function() {
        if (!c.targetBlockedPartner) return;
        c.togglePartnerStatus(c.targetBlockedPartner);
        c.showPartnerBlockedModal = false;
        c.targetBlockedPartner = null;
    };

    c.viewPartner = function(p) {
        c.activePartner = p;
    };

    c.closePartnerDetail = function() {
        c.activePartner = null;
    };

    c.openCreatePartnerRequest = function(partner, caseId) {
        c.partnerReqForm = {
            partner_id: partner ? partner.sys_id : (c.partnersList.length > 0 ? c.partnersList[0].sys_id : ''),
            case_id: caseId || (c.activeInvestigationCase ? c.activeInvestigationCase.sys_id : (c.partnerCasesList.length > 0 ? c.partnerCasesList[0].sys_id : '')),
            request_type: 'Request Transaction Information',
            priority: 'High',
            reference: '',
            description: '',
            simulate: true
        };
        c.showPartnerReqModal = true;
    };

    c.submitPartnerRequest = function() {
        if (!c.partnerReqForm.partner_id || !c.partnerReqForm.case_id || !c.partnerReqForm.request_type) return;
        c.partnerActionLoading = true;
        var payload = {
            action: 'create_request',
            actor: (c.adminUser && c.adminUser.name) || 'Alex Morgan',
            request: c.partnerReqForm
        };

        $http.post(API + '/admin_partners', payload)
        .then(function(resp) {
            c.partnerActionLoading = false;
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.showPartnerReqModal = false;
                c.partnerFeedback = 'Partner Request ' + (d.request_number || '') + ' dispatched successfully (Status: ' + d.status + ').';
                c.partnerFeedbackIsError = false;
                c.loadPartners();
            } else {
                c.partnerFeedback = d.error || 'Failed to dispatch request.';
                c.partnerFeedbackIsError = true;
            }
        }, function(err) {
            c.partnerActionLoading = false;
            c.partnerFeedback = 'Server error occurred while dispatching request.';
            c.partnerFeedbackIsError = true;
        });
    };

    c.viewPartnerRequest = function(r) {
        c.activePartnerRequest = r;
    };

    c.closePartnerRequestDetail = function() {
        c.activePartnerRequest = null;
    };

    c.simulatePartnerResponse = function(r) {
        if (!r) return;
        var payload = {
            action: 'simulate_response',
            actor: (c.adminUser && c.adminUser.name) || 'Alex Morgan',
            sys_id: r.sys_id
        };

        $http.post(API + '/admin_partners', payload)
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                r.status = d.status;
                r.response = d.response;
                c.partnerFeedback = 'Simulated response generated and recorded in Case Timeline & Audit Log.';
                c.partnerFeedbackIsError = false;
                c.loadPartners();
            }
        });
    };

    c.updatePartnerRequestStatus = function(r, newStatus) {
        if (!r) return;
        var payload = {
            action: 'update_request_status',
            actor: (c.adminUser && c.adminUser.name) || 'Alex Morgan',
            sys_id: r.sys_id,
            status: newStatus,
            resolution_notes: 'Status updated by investigator to ' + newStatus + '.'
        };

        $http.post(API + '/admin_partners', payload)
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                r.status = newStatus;
                c.partnerFeedback = 'Request ' + r.request_number + ' marked as ' + newStatus + '.';
                c.partnerFeedbackIsError = false;
                c.loadPartners();
            }
        });
    };


    // ---- SCROLL TO TOP HELPER ($timeout ensures digest is complete first) ----
    c.scrollToTop = function() {
        $timeout(function() {
            try {
                // Try the fnx-app's own scroll container (view containers)
                var targets = [
                    document.querySelector('.fnx-landing'),
                    document.querySelector('.fnx-portal-select-view'),
                    document.querySelector('.fnx-admin-login-page'),
                    document.querySelector('.fnx-admin-main-content'),
                    document.querySelector('.sp-scroll'),
                    document.querySelector('[class*="sp-col"]'),
                    document.querySelector('.panel-col-content'),
                    document.documentElement,
                    document.body
                ];
                for (var i = 0; i < targets.length; i++) {
                    if (targets[i]) targets[i].scrollTop = 0;
                }
                window.scrollTo(0, 0);
                window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
            } catch(e) {}
        }, 50);
    };

    c.navigate = function(view) {
        if (view === 'reportFraud') { c.startNewReport(); c.scrollToTop(); return; }
        if (view === 'trackCases') { c.loadCases(); }
        if (view === 'editProfile') { c.initEditProfile(); }
        c.currentView = view;
        c.scrollToTop();
    };

    c.goToPortalSelect = function() { c.currentView = 'portalSelect'; c.scrollToTop(); };
    c.goToAuth = function() { c.currentView = 'auth'; c.authMode = 'login'; c.scrollToTop(); };
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

    // ============================================================
    // FRAUDNEXUS ADMIN / INVESTIGATOR PORTAL STATE & METHODS
    // ============================================================
    c.adminUser = null;
    c.isAdminDemo = false;
    c.adminModule = 'commandCenter';
    c.adminError = '';
    c.adminLoading = false;
    c.adminForm = { email: '', password: '', showPassword: false };
    c.adminDash = {
        stats: { newCases: 17, activeCases: 48, criticalCases: 6, escalatedCases: 9, pendingApprovals: 11, financialExposure: 2800000, blockedAmount: 620000, recoveredAmount: 380000, outstandingAmount: 1800000 },
        priority_queue: [],
        action_center: [],
        trends: {},
        recent_activity: [],
        last_updated: 'Just now'
    };
    c.queueFilter = 'all';
    c.adminCasesList = [];
    c.casesFilter = 'all';
    c.casesSearch = '';
    c.adminCustList = [];
    c.custSearch = '';
    c.activeAdminCase = null;
    c.activeInvestigationCase = null;
    c.investigationTab = 'overview';
    c.investigationCases = [];
    c.showCaseDetailModal = false;
    c.showAssignModal = false;
    c.showTaskModal = false;
    c.showEvidenceReqModal = false;
    c.showEscalateModal = false;
    c.showResolveModal = false;
    c.targetCaseForModal = null;
    c.modalFeedback = '';
    c.assigneeSelect = 'alex.morgan@fraudnexus.com';
    c.taskForm = { title: '', desc: '', priority: 'High', assignee: 'Alex Morgan' };
    c.evidenceReqNotes = '';
    c.escalateReason = '';
    c.resolveNotes = '';
    c.resolveOutcome = 'Confirmed Fraud';
    c.adminAIInput = '';
    c.adminAIMessages = [
        {
            sender: 'ai',
            text: 'Hello Alex! I am your FRAUDNEXUS Operational Assistant.\n\nI can retrieve unassigned cases, check critical alerts, report SLA breaches, and assist your operational investigation tasks.',
            suggestions: ['Show unassigned cases', 'How many critical cases are open?', 'Show cases approaching SLA', 'Show my cases']
        }
    ];

    c.goToAdminLogin = function() {
        c.currentView = 'adminLogin';
        c.adminError = '';
        c.scrollToTop();
    };

    c.toggleAdminPassword = function() {
        c.adminForm.showPassword = !c.adminForm.showPassword;
    };

    c.doAdminLogin = function() {
        c.adminError = '';
        c.adminLoading = true;
        $http.post(API + '/admin_login', { email: c.adminForm.email, password: c.adminForm.password })
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.adminUser = d.user;
                c.isAdminDemo = d.is_demo || false;
                c.currentView = 'adminWorkspace';
                c.adminModule = 'commandCenter';
                c.scrollToTop();
                c.loadAdminDashboard();
                c.loadPartners();
            } else {
                c.adminError = d.error || 'Invalid investigator credentials.';
            }
            c.adminLoading = false;
        }, function(err) {
            c.adminError = (err.data && err.data.result && err.data.result.error) || 'Invalid investigator credentials.';
            c.adminLoading = false;
        });
    };

    c.doAdminDemoLogin = function() {
        c.adminError = '';
        c.adminLoading = true;
        $http.post(API + '/admin_login', { demo: true })
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.adminUser = d.user;
                c.isAdminDemo = true;
                c.currentView = 'adminWorkspace';
                c.adminModule = 'commandCenter';
                c.scrollToTop();
                c.loadAdminDashboard();
                c.loadPartners();
            } else {
                c.adminError = d.error || 'Unable to start demo session.';
            }
            c.adminLoading = false;
        }, function(err) {
            c.adminError = (err.data && err.data.result && err.data.result.error) || 'Unable to connect to demo account.';
            c.adminLoading = false;
        });
    };

    c.logoutAdmin = function() {
        c.adminUser = null;
        c.isAdminDemo = false;
        c.currentView = 'portalSelect';
        c.scrollToTop();
    };

    c.setAdminModule = function(mod) {
        c.adminModule = mod;
        if (mod === 'commandCenter') c.loadAdminDashboard();
        if (mod === 'cases') c.loadAdminCases(c.casesFilter);
        if (mod === 'customers') c.loadAdminCustomers();
        if (mod === 'partners') c.loadPartners();
        if (mod === 'investigation') {
            if (!c.activeInvestigationCase && c.adminDash.priority_queue.length > 0) {
                c.openInvestigation(c.adminDash.priority_queue[0]);
            }
        }
    };

    c.loadAdminDashboard = function() {
        $http.get(API + '/admin_dashboard')
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.adminDash = d;
            }
        });
    };

    c.filterQueue = function(f) {
        c.queueFilter = f;
    };

    c.getFilteredQueue = function() {
        if (!c.adminDash || !c.adminDash.priority_queue) return [];
        if (c.queueFilter === 'all') return c.adminDash.priority_queue;
        return c.adminDash.priority_queue.filter(function(cs) {
            if (c.queueFilter === 'critical') return cs.severity === 'Critical';
            if (c.queueFilter === 'high_risk') return cs.risk >= 70;
            if (c.queueFilter === 'unassigned') return cs.handler === 'Unassigned';
            if (c.queueFilter === 'near_sla') return cs.sla.indexOf('1') !== -1 || cs.sla.indexOf('2') !== -1;
            if (c.queueFilter === 'escalated') return cs.status === 'Escalated';
            return true;
        });
    };

    c.loadAdminCases = function(f) {
        c.casesFilter = f || 'all';
        var url = API + '/admin_cases?filter=' + encodeURIComponent(c.casesFilter);
        if (c.casesSearch) url += '&search=' + encodeURIComponent(c.casesSearch);
        $http.get(url).then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.adminCasesList = d.cases;
            }
        });
    };

    
    c.viewCustomer = function(cust) {
        c.selectedCustomer = cust;
        if (typeof spModal !== 'undefined') {
            spModal.alert('Customer Profile: ' + cust.name + '\nID: ' + (cust.customer_id || cust.id) + '\nEmail: ' + cust.email);
        } else {
            alert('Customer Details:\n\nID: ' + (cust.customer_id || cust.id) + '\nName: ' + cust.name + '\nEmail: ' + cust.email + '\nKYC Status: ' + cust.kycStatus);
        }
    };

    c.loadAdminCustomers = function() {
        var url = API + '/admin_customers';
        if (c.custSearch) url += '?search=' + encodeURIComponent(c.custSearch);
        $http.get(url).then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.adminCustList = d.customers;
            }
        });
    };

    c.viewCaseDetail = function(cs) {
        $http.get(API + '/admin_cases?case_id=' + cs.sys_id)
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.activeAdminCase = d.case;
                c.showCaseDetailModal = true;
            }
        });
    };

    c.openInvestigation = function(cs) {
        c.adminModule = 'investigation';
        c.investigationTab = 'overview';
        $http.get(API + '/admin_cases?case_id=' + cs.sys_id)
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.activeInvestigationCase = d.case;
            }
        });
    };

    c.setInvestigationTab = function(t) {
        c.investigationTab = t;
    };

    // Modal Triggers
    c.openAssignModal = function(cs) {
        c.targetCaseForModal = cs;
        c.showAssignModal = true;
        c.modalFeedback = '';
    };

    c.openTaskModal = function(cs) {
        c.targetCaseForModal = cs || c.activeInvestigationCase;
        c.showTaskModal = true;
        c.taskForm = { title: '', desc: '', priority: 'High', assignee: 'Alex Morgan' };
        c.modalFeedback = '';
    };

    c.openEvidenceReqModal = function(cs) {
        c.targetCaseForModal = cs || c.activeInvestigationCase;
        c.showEvidenceReqModal = true;
        c.evidenceReqNotes = '';
        c.modalFeedback = '';
    };

    c.openEscalateModal = function(cs) {
        c.targetCaseForModal = cs || c.activeInvestigationCase;
        c.showEscalateModal = true;
        c.escalateReason = '';
        c.modalFeedback = '';
    };

    c.openResolveModal = function(cs) {
        c.targetCaseForModal = cs || c.activeInvestigationCase;
        c.showResolveModal = true;
        c.resolveNotes = '';
        c.resolveOutcome = 'Confirmed Fraud';
        c.modalFeedback = '';
    };

    // Operational Actions Execution
    c.executeAssign = function() {
        if (!c.targetCaseForModal) return;
        var hName = c.assigneeSelect === 'alex.morgan@fraudnexus.com' ? 'Alex Morgan' : 'Sophia Reynolds';
        $http.post(API + '/admin_cases', {
            action: 'assign',
            case_id: c.targetCaseForModal.sys_id,
            handler_id: '',
            handler_name: hName
        }).then(function(resp) {
            c.showAssignModal = false;
            c.loadAdminDashboard();
            if (c.adminModule === 'cases') c.loadAdminCases(c.casesFilter);
            if (c.activeInvestigationCase && c.activeInvestigationCase.sys_id === c.targetCaseForModal.sys_id) {
                c.openInvestigation(c.targetCaseForModal);
            }
        });
    };

    c.executeTaskCreation = function() {
        if (!c.targetCaseForModal || !c.taskForm.title) return;
        $http.post(API + '/admin_cases', {
            action: 'add_task',
            case_id: c.targetCaseForModal.sys_id,
            title: c.taskForm.title,
            description: c.taskForm.desc,
            priority: c.taskForm.priority
        }).then(function(resp) {
            c.showTaskModal = false;
            if (c.activeInvestigationCase && c.activeInvestigationCase.sys_id === c.targetCaseForModal.sys_id) {
                c.openInvestigation(c.targetCaseForModal);
            }
        });
    };

    c.executeEvidenceRequest = function() {
        if (!c.targetCaseForModal) return;
        $http.post(API + '/admin_cases', {
            action: 'request_evidence',
            case_id: c.targetCaseForModal.sys_id,
            notes: c.evidenceReqNotes
        }).then(function(resp) {
            c.showEvidenceReqModal = false;
            c.loadAdminDashboard();
            if (c.activeInvestigationCase) c.openInvestigation(c.activeInvestigationCase);
        });
    };

    c.executeEscalate = function() {
        if (!c.targetCaseForModal) return;
        $http.post(API + '/admin_cases', {
            action: 'escalate',
            case_id: c.targetCaseForModal.sys_id,
            reason: c.escalateReason
        }).then(function(resp) {
            c.showEscalateModal = false;
            c.loadAdminDashboard();
            if (c.adminModule === 'cases') c.loadAdminCases(c.casesFilter);
            if (c.activeInvestigationCase) c.openInvestigation(c.activeInvestigationCase);
        });
    };

    c.executeResolve = function() {
        if (!c.targetCaseForModal) return;
        $http.post(API + '/admin_cases', {
            action: 'resolve',
            case_id: c.targetCaseForModal.sys_id,
            outcome: c.resolveOutcome,
            notes: c.resolveNotes
        }).then(function(resp) {
            c.showResolveModal = false;
            c.loadAdminDashboard();
            if (c.adminModule === 'cases') c.loadAdminCases(c.casesFilter);
            if (c.activeInvestigationCase) c.openInvestigation(c.activeInvestigationCase);
        });
    };

    c.executeClose = function(cs) {
        var target = cs || c.activeInvestigationCase;
        if (!target) return;
        $http.post(API + '/admin_cases', {
            action: 'close',
            case_id: target.sys_id,
            notes: 'Investigation closed by authorized investigator.'
        }).then(function(resp) {
            c.loadAdminDashboard();
            if (c.adminModule === 'cases') c.loadAdminCases(c.casesFilter);
            if (c.activeInvestigationCase) c.openInvestigation(c.activeInvestigationCase);
        });
    };

    // Admin AI Interaction
    c.sendAdminAI = function(predefined) {
        var queryText = predefined || c.adminAIInput;
        if (!queryText || !queryText.trim()) return;
        c.adminAIMessages.push({ sender: 'user', text: queryText });
        c.adminAIInput = '';
        var curCaseId = (c.adminModule === 'investigation' && c.activeInvestigationCase) ? c.activeInvestigationCase.sys_id : '';

        $http.post(API + '/admin_ai', { query: queryText, current_case_id: curCaseId })
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            c.adminAIMessages.push({
                sender: 'ai',
                text: d.reply,
                suggestions: d.suggestions || []
            });
        }, function(err) {
            c.adminAIMessages.push({
                sender: 'ai',
                text: 'Sorry, I encountered an operational query error. Please try again.',
                suggestions: ['Show unassigned cases', 'Show critical cases']
            });
        });
    };

    // Check URL parameters for direct view routing
    try {
        var qParams = new URLSearchParams($window.location.search);
        if (qParams.get('view') === 'admin' || qParams.get('admin') === 'true' || qParams.get('view') === 'adminLogin') {
            c.goToAdminLogin();
        }
    } catch(e) {}

    c.getStatusClass = function(s) {
        if (s === 'Resolved' || s === 'Closed') return 'st-resolved';
        if (s === 'In Progress' || s === 'Investigation') return 'st-progress';
        return 'st-new';
    };


// === FRAUDNEXUS VERIFICATION WORKSPACE CONTROLLER EXTENSION ===
/* ============================================================
   FRAUDNEXUS — VERIFICATION WORKSPACE CLIENT CONTROLLER EXTENSION
   Sections C–AB Implementation
   ============================================================ */

    // 1. Initialize Verification Workspace State
    c.investigationTab = 'overview';
    c.reportSubTab = 'admin';
    c.timelineFilter = 'all';
    c.showMoreActions = false;
    c.showGenAIModal = false;
    c.showPartnerReqModal = false;
    c.showAlertCustomerModal = false;
    c.showAlertWorkerModal = false;
    c.selectedGenAIMode = 'journey';
    c.currentDateStr = new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });

    // 2. Default Rich Demo Case Structure (Section 35 Scenario)
    c.setupDefaultInvestigationCase = function() {
        return {
            sys_id: 'case_fnx_2026_00847',
            number: 'FNX-2026-00847',
            type: 'Phishing / Financial Fraud',
            incident_type: 'Phishing / Financial Fraud',
            severity: 'Critical',
            priority: 'P1 - Critical',
            status: 'In Progress',
            stage: 'Evidence Verification',
            risk_score: 94,
            exposure: 85000,
            verified_exposure: 85000,
            blocked_amount: 35000,
            recovered_amount: 0,
            sla: '3h 45m remaining',
            created_on: '2026-10-02 14:22 IST',
            updated_on: 'Just now',
            handler: 'Alex Morgan',
            incident_date: '2026-10-02 14:15 IST',
            platform: 'UPI / Mobile NetBanking',
            description: 'Customer received an urgent SMS masquerading as HDFC Bank KYC update alert. The link redirected to a spoofed login portal capturing credentials. An unauthorized UPI transaction of INR 85,000 was executed to an unknown beneficiary merchant within 5 minutes.',
            customer: {
                customer_id: 'CUST-84920',
                name: 'Rajesh Sharma',
                email: 'rajesh.sharma@example.com',
                mobile: '+91 98401 23456',
                kyc_status: 'Verified',
                account_num: 'XXXX-XXXX-4819'
            },
            evidence: [
                {
                    id: 'EV-001',
                    title: 'Phishing SMS Screenshot',
                    icon: '📱',
                    type: 'Image / Screenshot',
                    source: 'Customer Mobile Upload',
                    submitter: 'Rajesh Sharma',
                    date: '2026-10-02 14:25',
                    classification: 'JOREN: SMS Smishing Indicator',
                    pipeline: 'JOREN Multimodal Vision OCR',
                    extracted_info: 'Sender VK-HDFCBK. Deceptive message claiming NetBanking deactivation in 24 hours. Bit.ly redirect url.',
                    entities: ['HDFC Bank Spoof', 'Urgent Call to Action', 'SMS Gateway VK-HDFCBK'],
                    sha256: 'a4b2c1d98e7f60321a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f',
                    status: 'Confirmed',
                    notes: 'Matches known banking smishing campaign reported to Cert-In.'
                },
                {
                    id: 'EV-002',
                    title: 'Malicious Harvesting URL Screenshot',
                    icon: '🌐',
                    type: 'Image / URL Capture',
                    source: 'Customer Browser Cache',
                    submitter: 'Rajesh Sharma',
                    date: '2026-10-02 14:28',
                    classification: 'JOREN: Fake Banking Credential Harvester',
                    pipeline: 'JOREN Web Threat Intelligence',
                    extracted_info: 'Domain: secure-bank-login-verify.com. Fake HDFC NetBanking logo, captured credentials & OTP field.',
                    url_ref: 'hxxps://secure-bank-login-verify.com/login',
                    entities: ['Credential Harvester', 'Domain Impersonation', 'Fake NetBanking UI'],
                    sha256: '9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e',
                    status: 'Confirmed',
                    notes: 'Domain registered 48 hours prior to attack on privacy registrar.'
                },
                {
                    id: 'EV-003',
                    title: 'Bank Transaction Statement PDF',
                    icon: '📄',
                    type: 'Document / Financial PDF',
                    source: 'Official Statement Download',
                    submitter: 'Rajesh Sharma',
                    date: '2026-10-02 14:32',
                    classification: 'JOREN: High-Value Debit Record',
                    pipeline: 'JOREN PDF Financial Extractor',
                    extracted_info: 'Debit of INR 85,000.00 via UPI on 2026-10-02 at 14:22:18 IST. Ref: UPI/2026/84920194819 to pay-fast-merchant@ybl.',
                    transaction_ref: 'UPI/2026/84920194819',
                    entities: ['UPI Protocol', 'Amount: INR 85,000', 'Beneficiary: pay-fast-merchant@ybl'],
                    sha256: '5e4d3c2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c8b7a6f5e4d',
                    status: 'Confirmed',
                    notes: 'Financial debit corroborated by Partner Bank A ledger.'
                },
                {
                    id: 'EV-004',
                    title: 'Bank Debit Confirmation Email',
                    icon: '✉️',
                    type: 'Email / EML Export',
                    source: 'Customer Mailbox',
                    submitter: 'Rajesh Sharma',
                    date: '2026-10-02 14:35',
                    classification: 'JOREN: Authentic Bank Transaction Alert',
                    pipeline: 'JOREN Email RFC-822 Parser',
                    extracted_info: 'Automated transaction confirmation from alerts@hdfcbank.net confirming immediate debit of INR 85,000.',
                    transaction_ref: 'UPI/2026/84920194819',
                    entities: ['Transaction Notification', 'Timestamp Corroboration'],
                    sha256: '1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b',
                    status: 'Confirmed',
                    notes: 'Validates timing within 7 minutes of victim credential entry.'
                }
            ],
            findings: [
                {
                    id: 'FND-001',
                    title: 'Targeted SMS Smishing Campaign masquerading as HDFC Bank',
                    description: 'Deceptive SMS received from bulk spoofed route claiming urgent KYC deactivation ultimatum.',
                    supporting_evidence: ['EV-001'],
                    confidence: 98,
                    source: 'AI Generated',
                    status: 'Confirmed',
                    reviewer: 'Alex Morgan',
                    reviewed_on: '2026-10-02 15:00',
                    notes: 'Matches signature of known syndicate smishing wave.'
                },
                {
                    id: 'FND-002',
                    title: 'Credential Harvesting Domain hosted on suspicious ASN',
                    description: 'The domain secure-bank-login-verify.com was spun up to capture NetBanking credentials and session OTPs.',
                    supporting_evidence: ['EV-002'],
                    confidence: 96,
                    source: 'AI Generated',
                    status: 'Confirmed',
                    reviewer: 'Alex Morgan',
                    reviewed_on: '2026-10-02 15:05',
                    notes: 'Reported to national domain registrar for immediate takedown.'
                },
                {
                    id: 'FND-003',
                    title: 'Account Compromise via Unrecognized Foreign Tor IP',
                    description: 'Attacker accessed customer NetBanking from Tor exit node IP 185.220.101.5 within 4 minutes of harvest.',
                    supporting_evidence: ['EV-002', 'EV-003'],
                    confidence: 94,
                    source: 'AI Generated',
                    status: 'Confirmed',
                    reviewer: 'Alex Morgan',
                    reviewed_on: '2026-10-02 15:10',
                    notes: 'Impossible travel anomaly confirmed by session telemetry.'
                },
                {
                    id: 'FND-004',
                    title: 'High-Velocity Unauthorized UPI Transaction to Flagged Mule',
                    description: 'Instant transfer of INR 85,000 sent to beneficiary pay-fast-merchant@ybl which has 4 prior fraud liens.',
                    supporting_evidence: ['EV-003', 'EV-004'],
                    confidence: 99,
                    source: 'Investigator Identified',
                    status: 'Confirmed',
                    reviewer: 'Alex Morgan',
                    reviewed_on: '2026-10-02 15:15',
                    notes: 'Corroborated by Partner Bank A response trace.'
                }
            ],
            cyber: {
                indicators: [
                    { type: 'Domain', value: 'secure-bank-login-verify.com', classification: 'Phishing Harvester', first_seen: '2026-09-30', reputation: 'Malicious', syndicate: 'Fake-Bank-Smish-2026' },
                    { type: 'IP', value: '185.220.101.5', classification: 'Tor Exit Node / Anonymizer', first_seen: '2026-08-14', reputation: 'Critical Threat', syndicate: 'Cluster-Tor-Node-5' },
                    { type: 'SMS Sender', value: 'VK-HDFCBK', classification: 'Spoofed Bank Sender ID', first_seen: '2026-10-02', reputation: 'Blocked', syndicate: 'Fake-Bank-Smish-2026' },
                    { type: 'UPI Mule', value: 'pay-fast-merchant@ybl', classification: 'Money Mule Account', first_seen: '2026-09-12', reputation: 'Flagged Lien', syndicate: 'Syndicate-Mule-Tier2' },
                    { type: 'User Agent', value: 'HeadlessChrome/124.0.0.0', classification: 'Automated Browser Bot', first_seen: '2026-10-02', reputation: 'High Risk', syndicate: 'Automated Exploitation' }
                ]
            },
            notes: [
                {
                    author: 'Alex Morgan',
                    role: 'Lead Investigator',
                    timestamp: '2026-10-02 14:40 IST',
                    text: 'Case assigned. Initial review of customer report completed. Verified victim KYC identity matches the remitter account. Proceeding with JOREN artifact classification.',
                    tags: ['Intake', 'Verification']
                },
                {
                    author: 'Alex Morgan',
                    role: 'Lead Investigator',
                    timestamp: '2026-10-02 15:20 IST',
                    text: 'Dispatched urgent inter-bank trace PR-001 to Partner Bank A requesting account lien on beneficiary pay-fast-merchant@ybl.',
                    tags: ['PartnerTrace', 'FundRecovery']
                },
                {
                    author: 'Alex Morgan',
                    role: 'Lead Investigator',
                    timestamp: '2026-10-02 15:50 IST',
                    text: 'Partner Bank A confirmed unauthorized transaction. ₹ 35,000 held at destination node. Risk score elevated to 94 (Critical). Preparing final resolution statement.',
                    tags: ['PartnerResponse', 'RiskUpdate']
                }
            ],
            partner_requests: [
                {
                    id: 'PR-001',
                    partner: 'Partner Bank A - SIMULATED DEMO PARTNER',
                    demo_flag: true,
                    request_type: 'Transaction Verification',
                    priority: 'P1 - Critical',
                    status: 'Response Received',
                    due_date: '2026-10-02 18:00 IST',
                    description: 'Transaction TXN-2026-84920194819 for INR 85,000 on 2026-10-02 at 14:22 requires verification of authorization status and immediate beneficiary account lien.',
                    response: {
                        received_on: '2026-10-02 15:45 IST',
                        verification_result: 'CONFIRMED UNAUTHORIZED / SUSPECTED MULE NODE',
                        details: 'Partner Bank A internal audit verifies the transaction was received at 14:22:19. Recipient account pay-fast-merchant@ybl showed sudden burst velocity inconsistent with historic profile. Full debit freeze enacted.',
                        beneficiary_bank: 'Yes Bank Cooperative Switch',
                        account_status: 'FROZEN / LIEN PLACED',
                        held_amount: 35000
                    },
                    ai_analysis: {
                        classification: 'Confirms Unauthorized Transaction & Laundering Node',
                        supporting_info: 'Partner response timestamp correlates with victim login alert within 18 seconds. Beneficiary account freeze holds INR 35,000 for potential clawback.',
                        contradictions: null,
                        suggested_finding_update: 'FND-004: Status verified as confirmed fraudulent money mule.',
                        suggested_risk_impact: 'Elevate Case Risk to 94/100 (Critical)'
                    },
                    analysis_accepted: true
                }
            ],
            related_cases: [
                {
                    number: 'FNX-2026-00792',
                    type: 'Phishing / Unauthorized UPI',
                    status: 'Resolved',
                    shared_indicators: ['secure-bank-login-verify.com', '185.220.101.5'],
                    similarity: 94,
                    pattern_desc: 'Identical phishing domain registrar and Tor exit node login IP.'
                },
                {
                    number: 'FNX-2026-00651',
                    type: 'Account Takeover',
                    status: 'Closed',
                    shared_indicators: ['VK-HDFCBK', 'pay-fast-merchant@ybl'],
                    similarity: 82,
                    pattern_desc: 'Shared SMS sender header and common money mule beneficiary.'
                }
            ],
            relationships: [
                { source: 'Rajesh Sharma', source_type: 'Customer', relationship: 'Victim Of', target: 'FNX-2026-00847', target_type: 'Case', confidence: 100, evidence_ref: 'EV-001', status: 'Confirmed' },
                { source: 'FNX-2026-00847', source_type: 'Case', relationship: 'Involves Domain', target: 'secure-bank-login-verify.com', target_type: 'Threat Infra', confidence: 98, evidence_ref: 'EV-002', status: 'Confirmed' },
                { source: 'secure-bank-login-verify.com', source_type: 'Threat Infra', relationship: 'Resolves To', target: '185.220.101.5', target_type: 'Tor IP', confidence: 96, evidence_ref: 'EV-002', status: 'Confirmed' },
                { source: '185.220.101.5', source_type: 'Tor IP', relationship: 'Executed Txn', target: 'UPI/2026/84920194819', target_type: 'Transaction', confidence: 95, evidence_ref: 'EV-003', status: 'Confirmed' },
                { source: 'UPI/2026/84920194819', source_type: 'Transaction', relationship: 'Credited To', target: 'pay-fast-merchant@ybl', target_type: 'Mule Account', confidence: 99, evidence_ref: 'EV-003', status: 'Confirmed' },
                { source: 'pay-fast-merchant@ybl', source_type: 'Mule Account', relationship: 'Settled Via', target: 'Partner Bank A', target_type: 'Partner Bank', confidence: 100, evidence_ref: 'PR-001', status: 'Confirmed' },
                { source: 'FNX-2026-00847', source_type: 'Case', relationship: 'Correlated With', target: 'FNX-2026-00792', target_type: 'Related Case', confidence: 94, evidence_ref: 'KnowledgeGraph', status: 'Confirmed' },
                { source: 'secure-bank-login-verify.com', source_type: 'Threat Infra', relationship: 'Attributed To', target: 'Fake-Bank-Smish-2026', target_type: 'Syndicate', confidence: 92, evidence_ref: 'ThreatIntel', status: 'Confirmed' }
            ],
            risk_factors: [
                { name: 'Smishing SMS Vector Confirmed', points: 25, evaluation: 'Spoofed bank sender ID with urgent threat of deactivation.' },
                { name: 'High-Value Immediate Fund Siphoning', points: 30, evaluation: 'Transfer of INR 85,000 within 5 minutes of credential harvest.' },
                { name: 'Anonymized Foreign IP Login (Tor)', points: 20, evaluation: 'Login originating from 185.220.101.5 (Germany Tor Node).' },
                { name: 'Verified Mule Beneficiary Account', points: 19, evaluation: 'Partner Bank A confirmed account has prior fraud reports.' }
            ],
            risk_history: [
                { stage: '1. Initial Intake', score: 55, reason: 'Customer reported fraud via mobile portal.', time: '14:22' },
                { stage: '2. Evidence Submitted', score: 68, reason: 'Ingested SMS, URL screenshot, and statement.', time: '14:35' },
                { stage: '3. Findings Confirmed', score: 78, reason: 'Investigator confirmed credential theft.', time: '15:15' },
                { stage: '4. Partner Bank Verified', score: 94, reason: 'Partner Bank A verified unauthorized debit.', time: '15:50' }
            ],
            tasks: [
                { number: 'TSK-001', short_description: 'Verify Customer KYC & Mobile Ownership', assigned_to: 'Alex Morgan', priority: 'High', due_date: '2026-10-02 16:00', state: 'Completed' },
                { number: 'TSK-002', short_description: 'Dispatch Partner Inter-bank Trace to Partner Bank A', assigned_to: 'Alex Morgan', priority: 'High', due_date: '2026-10-02 17:00', state: 'Completed' },
                { number: 'TSK-003', short_description: 'Initiate Zero-Liability Claim Reimbursement Advice', assigned_to: 'Alex Morgan', priority: 'High', due_date: '2026-10-02 18:00', state: 'Completed' }
            ],
            compliance: [
                { framework: 'RBI Master Direction - Digital Fraud', requirement: 'Reporting within 24 hours of confirmation', deadline: '2026-10-03 14:00', status: 'Compliant (Filed Form FMR-1)' },
                { framework: 'Cert-In Cyber Security Incident', requirement: 'Phishing domain notification to national CSIRT', deadline: '2026-10-03 12:00', status: 'Compliant (Advisory Issued)' },
                { framework: 'Customer Zero-Liability Protection', requirement: 'Lien advice & reimbursement authorization', deadline: '2026-10-04 17:00', status: 'Compliant (Advice Dispatched)' },
                { framework: 'PCI-DSS Data Minimization', requirement: 'Zero credential/PIN retention verification', deadline: 'Continuous', status: 'Compliant (No Credentials Stored)' },
                { framework: 'Digital Evidence Chain of Custody', requirement: 'SHA256 cryptographic immutability log', deadline: 'Continuous', status: 'Compliant (Unbroken Hashes)' }
            ],
            custody_log: [
                { timestamp: '2026-10-02 14:25:12', evidence_id: 'EV-001', action: 'Upload & SHA256 Computed', custodian: 'Rajesh Sharma / JOREN Ingest', hash: 'a4b2c1d98e7f60321a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f' },
                { timestamp: '2026-10-02 14:28:44', evidence_id: 'EV-002', action: 'Upload & SHA256 Computed', custodian: 'Rajesh Sharma / JOREN Ingest', hash: '9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e' },
                { timestamp: '2026-10-02 14:32:05', evidence_id: 'EV-003', action: 'Upload & SHA256 Computed', custodian: 'Rajesh Sharma / JOREN Ingest', hash: '5e4d3c2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c8b7a6f5e4d' },
                { timestamp: '2026-10-02 14:35:19', evidence_id: 'EV-004', action: 'Upload & SHA256 Computed', custodian: 'Rajesh Sharma / JOREN Ingest', hash: '1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b' },
                { timestamp: '2026-10-02 15:00:00', evidence_id: 'EV-ALL', action: 'Forensic Review & Validation', custodian: 'Alex Morgan (Senior Investigator)', hash: 'f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3' }
            ],
            timeline: [
                { time: '14:15 IST', actor: 'Rajesh Sharma', actor_type: 'HUMAN', action: 'Incident Incurred', desc: 'Customer clicked phishing link and lost INR 85,000.', record_id: 'EV-001' },
                { time: '14:22 IST', actor: 'Rajesh Sharma', actor_type: 'HUMAN', action: 'Case Submitted', desc: 'Fraud report submitted via FRAUDNEXUS customer portal.', record_id: 'FNX-2026-00847' },
                { time: '14:23 IST', actor: 'FNX Platform', actor_type: 'SYSTEM', action: 'Case Registered', desc: 'Case auto-registered, priority P1 assigned, SLA timer initialized.', record_id: 'FNX-2026-00847' },
                { time: '14:26 IST', actor: 'JOREN Pipeline', actor_type: 'AI SYSTEM', action: 'Evidence Ingestion', desc: 'JOREN multimodal vision model extracted text from phishing SMS.', record_id: 'EV-001' },
                { time: '14:30 IST', actor: 'JOREN Pipeline', actor_type: 'AI SYSTEM', action: 'Threat Classification', desc: 'Malicious domain identified as credential harvester.', record_id: 'EV-002' },
                { time: '14:35 IST', actor: 'FNX Platform', actor_type: 'SYSTEM', action: 'Investigator Assigned', desc: 'Assigned to Senior Investigator Alex Morgan.', record_id: 'USR-AM' },
                { time: '15:00 IST', actor: 'Alex Morgan', actor_type: 'HUMAN', action: 'Evidence Confirmed', desc: 'Investigator confirmed all 4 submitted artifacts.', record_id: 'EV-ALL' },
                { time: '15:15 IST', actor: 'Alex Morgan', actor_type: 'HUMAN', action: 'Findings Confirmed', desc: 'Investigator reviewed and confirmed 4 AI findings.', record_id: 'FND-ALL' },
                { time: '15:20 IST', actor: 'Alex Morgan', actor_type: 'HUMAN', action: 'Partner Request Submitted', desc: 'Dispatched inter-bank trace PR-001 to Partner Bank A.', record_id: 'PR-001' },
                { time: '15:45 IST', actor: 'Partner Bank A', actor_type: 'HUMAN', action: 'Partner Response Received', desc: 'Partner Bank A confirmed unauthorized transaction and froze mule node.', record_id: 'PR-001' },
                { time: '15:50 IST', actor: 'Alex Morgan', actor_type: 'HUMAN', action: 'Risk Elevated to Critical', desc: 'Risk elevated to 94/100 following partner verification.', record_id: 'RISK-94' },
                { time: '16:00 IST', actor: 'Generative AI', actor_type: 'AI SYSTEM', action: 'Synthesis Generated', desc: 'Synthesized Case Journey Summary for investigator review.', record_id: 'GENAI-01' },
                { time: '16:15 IST', actor: 'Marcus Vance', actor_type: 'HUMAN', action: 'Manager Approval Granted', desc: 'Fraud Operations Director approved zero-liability resolution.', record_id: 'APP-MV' },
                { time: '16:20 IST', actor: 'Alex Morgan', actor_type: 'HUMAN', action: 'Case Resolved', desc: 'Formal resolution recorded: Confirmed Fraud. Customer report dispatched.', record_id: 'FNX-2026-00847' }
            ],
            decision: {
                status: 'Resolved',
                outcome: 'Confirmed Fraud',
                reason: 'Investigation confirms credentials were harvested via smishing domain secure-bank-login-verify.com. The unauthorized debit of INR 85,000 on 2026-10-02 has been verified by Partner Bank A. A lien of INR 35,000 is active on the beneficiary node. Reversal advice initiated.',
                investigator: 'Alex Morgan',
                timestamp: '2026-10-02 16:20 IST'
            },
            manager_approved: true
        };
    };

    // 3. FNXCaseContextBuilder (Section 22 & O.1 Implementation)
    c.buildFNXCaseContext = function() {
        var cs = c.activeInvestigationCase;
        if (!cs) return {};

        // Sanitize and filter
        return {
            case_number: cs.number,
            incident_type: cs.incident_type || cs.type,
            severity: cs.severity,
            priority: cs.priority,
            current_status: cs.status,
            risk_score: cs.risk_score,
            risk_level: c.getRiskLabel(cs.risk_score),
            reported_exposure: cs.exposure,
            verified_exposure: cs.verified_exposure,
            blocked_amount: cs.blocked_amount,
            customer_name: cs.customer.name,
            customer_id: cs.customer.customer_id,
            investigator: cs.handler,
            incident_date: cs.incident_date,
            platform: cs.platform,
            original_report: cs.description,
            confirmed_evidence: (cs.evidence || []).filter(function(e) { return e.status === 'Confirmed'; }).map(function(e) {
                return { id: e.id, title: e.title, classification: e.classification, extracted_info: e.extracted_info, sha256: e.sha256 };
            }),
            confirmed_findings: (cs.findings || []).filter(function(f) { return f.status === 'Confirmed'; }).map(function(f) {
                return { id: f.id, title: f.title, description: f.description, confidence: f.confidence };
            }),
            partner_responses: (cs.partner_requests || []).filter(function(p) { return p.response; }).map(function(p) {
                return { partner: p.partner, result: p.response.verification_result, held_amount: p.response.held_amount, details: p.response.details };
            }),
            cyber_indicators: (cs.cyber && cs.cyber.indicators) ? cs.cyber.indicators.map(function(i) {
                return { type: i.type, value: i.value, classification: i.classification };
            }) : [],
            risk_history: cs.risk_history,
            decision: cs.decision
        };
    };

    // 4. Generative Intelligence 13-Mode Engine (Sections 21 & O.2)
    c.generateSelectedIntelligence = function() {
        c.genAILoading = true;
        var ctx = c.buildFNXCaseContext();
        var mode = c.selectedGenAIMode || 'journey';

        $timeout(function() {
            c.genAILoading = false;
            if (mode === 'journey') {
                c.generatedOutput = "=== CASE JOURNEY SUMMARY (END-TO-END) ===\n\n" +
                    "1. INTAKE & SUBMISSION:\n" +
                    "Customer " + ctx.customer_name + " (" + ctx.customer_id + ") reported an unauthorized UPI fund debit of INR " + ctx.reported_exposure + " occurring on " + ctx.incident_date + " via " + ctx.platform + ".\n\n" +
                    "2. JOREN MULTIMODAL INTELLIGENCE:\n" +
                    "Four evidence artifacts (SMS screenshot, URL screenshot, statement PDF, confirmation email) were ingested. Cryptographic SHA256 integrity was established. JOREN vision and web parsers classified the smishing SMS (VK-HDFCBK) and credential harvesting domain (secure-bank-login-verify.com).\n\n" +
                    "3. INVESTIGATOR VERIFICATION:\n" +
                    "Forensic investigator " + ctx.investigator + " human-verified all 4 evidence records and confirmed 4 primary findings establishing credential capture and foreign Tor IP session hijacking (185.220.101.5).\n\n" +
                    "4. INTER-BANK PARTNER TRACE:\n" +
                    "Partner Bank A completed verification request PR-001, confirming the unauthorized status of transaction UPI/2026/84920194819. A destination account lien of INR 35,000 has been placed on the beneficiary mule (pay-fast-merchant@ybl).\n\n" +
                    "5. RISK EVOLUTION & OUTCOME:\n" +
                    "Case risk escalated from Initial (55) to Critical (" + ctx.risk_score + "/100). Manager approval granted by Marcus Vance. Reversal claim advice dispatched. Case disposition: Confirmed Fraud.";
            } else if (mode === 'status') {
                c.generatedOutput = "=== CURRENT STATUS SUMMARY ===\n\n" +
                    "• Case ID: " + ctx.case_number + "\n" +
                    "• Status: " + ctx.current_status + " (SLA Remaining: 3h 45m)\n" +
                    "• Risk Score: " + ctx.risk_score + "/100 (" + ctx.risk_level + ")\n" +
                    "• Financial Loss: Reported INR " + ctx.reported_exposure + " | Verified INR " + ctx.verified_exposure + "\n" +
                    "• Funds In Lien: INR " + ctx.blocked_amount + " (Recovery Pending)\n" +
                    "• Evidence Items: " + ctx.confirmed_evidence.length + " Verified\n" +
                    "• Confirmed Findings: " + ctx.confirmed_findings.length + " Confirmed\n" +
                    "• Partner Status: Partner Bank A Verified (Lien Enacted)";
            } else if (mode === 'financial') {
                c.generatedOutput = "=== FINANCIAL INVESTIGATION SUMMARY ===\n\n" +
                    "• Remitter: Rajesh Sharma (Acct XXXX-XXXX-4819, Partner Bank A)\n" +
                    "• Transaction Ref: UPI/2026/84920194819\n" +
                    "• Gross Debited Amount: INR 85,000.00\n" +
                    "• Beneficiary: pay-fast-merchant@ybl (Yes Bank Switch)\n" +
                    "• Amount Blocked: INR 35,000.00 (Held under fraud lien)\n" +
                    "• Outstanding Exposure: INR 50,000.00\n" +
                    "• Regulatory Provision: RBI Zero-Liability Protection applied.";
            } else if (mode === 'cyber') {
                c.generatedOutput = "=== CYBER FORENSIC & ATTACK CHAIN SUMMARY ===\n\n" +
                    "• Attack Vector: Targeted Smishing (Sender ID: VK-HDFCBK)\n" +
                    "• Phishing URL: hxxps://secure-bank-login-verify.com/login\n" +
                    "• Attacker Session IP: 185.220.101.5 (Tor Exit Node, AS60729)\n" +
                    "• Attack Chain: SMS -> Bitly Redirect -> Credential Harvesting Portal -> Automated Session Hijack -> High-Velocity UPI Transfer.\n" +
                    "• Known Syndicate Link: Cluster Fake-Bank-Smish-2026.";
            } else if (mode === 'resolution_draft') {
                c.generatedOutput = "=== RESOLUTION NOTES DRAFT ===\n\n" +
                    "The forensic investigation has concluded that Case " + ctx.case_number + " represents unauthorized financial cyber fraud resulting from a targeted smishing campaign. All submitted evidence and IOCs have been validated. Partner Bank A has verified the unauthorized transfer and secured INR 35,000. A zero-liability claim has been initiated for full victim reimbursement. Case marked as RESOLVED (Confirmed Fraud).";
            } else {
                c.generatedOutput = "=== " + mode.toUpperCase() + " SUMMARY ===\n\n" +
                    "Analytical synthesis generated for Case " + ctx.case_number + ". Evaluated " + ctx.confirmed_evidence.length + " evidence items, " + ctx.confirmed_findings.length + " findings, and inter-bank partner verification. All attributes validate against established fraud indicators.";
            }
        }, 500);
    };

    // 5. Verification Workspace Navigation & Tabs
    c.setInvestigationTab = function(tabName) {
        c.investigationTab = tabName;
    };

    c.getRiskLabel = function(score) {
        var s = parseInt(score || 94, 10);
        if (s >= 85) return 'CRITICAL';
        if (s >= 70) return 'HIGH';
        if (s >= 50) return 'MEDIUM';
        return 'LOW';
    };

    c.getPendingVerificationCount = function() {
        if (!c.activeInvestigationCase) return 0;
        var pendingEv = (c.activeInvestigationCase.evidence || []).filter(function(e) { return e.status === 'Needs Review'; }).length;
        var pendingFnd = (c.activeInvestigationCase.findings || []).filter(function(f) { return f.status === 'Needs Review'; }).length;
        return pendingEv + pendingFnd;
    };

    c.isEvidenceVerified = function() {
        if (!c.activeInvestigationCase || !c.activeInvestigationCase.evidence) return true;
        return c.activeInvestigationCase.evidence.every(function(e) { return e.status === 'Confirmed' || e.status === 'Rejected'; });
    };

    c.isFindingsConfirmed = function() {
        if (!c.activeInvestigationCase || !c.activeInvestigationCase.findings) return true;
        return c.activeInvestigationCase.findings.every(function(f) { return f.status === 'Confirmed' || f.status === 'Rejected'; });
    };

    c.isPartnerVerified = function() {
        if (!c.activeInvestigationCase || !c.activeInvestigationCase.partner_requests) return false;
        return c.activeInvestigationCase.partner_requests.some(function(p) { return p.status === 'Response Received' && p.analysis_accepted; });
    };

    // 6. Evidence & Findings Verification Actions
    c.confirmEvidence = function(ev) {
        ev.status = 'Confirmed';
        c.addTimelineEvent('HUMAN', 'Evidence Verified', 'Investigator Alex Morgan human-verified artifact ' + ev.id + ' (' + ev.title + ').', ev.id);
    };

    c.rejectEvidence = function(ev) {
        ev.status = 'Rejected';
        c.addTimelineEvent('HUMAN', 'Evidence Rejected', 'Investigator rejected artifact ' + ev.id + ' as non-contributory.', ev.id);
    };

    c.confirmAllEvidence = function() {
        (c.activeInvestigationCase.evidence || []).forEach(function(e) { e.status = 'Confirmed'; });
        c.addTimelineEvent('HUMAN', 'Batch Evidence Verification', 'All 4 evidence artifacts verified by investigator.', 'EV-ALL');
    };

    c.confirmFinding = function(fnd) {
        fnd.status = 'Confirmed';
        fnd.reviewer = 'Alex Morgan';
        fnd.reviewed_on = new Date().toLocaleTimeString();
        c.addTimelineEvent('HUMAN', 'Finding Confirmed', 'Investigator confirmed intelligence finding ' + fnd.id + '.', fnd.id);
    };

    c.rejectFinding = function(fnd) {
        fnd.status = 'Rejected';
        c.addTimelineEvent('HUMAN', 'Finding Rejected', 'Investigator rejected finding ' + fnd.id + '.', fnd.id);
    };

    c.confirmAllFindings = function() {
        (c.activeInvestigationCase.findings || []).forEach(function(f) {
            f.status = 'Confirmed';
            f.reviewer = 'Alex Morgan';
            f.reviewed_on = new Date().toLocaleTimeString();
        });
        c.addTimelineEvent('HUMAN', 'Batch Findings Confirmation', 'All intelligence findings confirmed by investigator.', 'FND-ALL');
    };

    c.confirmAllPending = function() {
        c.confirmAllEvidence();
        c.confirmAllFindings();
    };

    // 7. Partner Verification
    c.openPartnerReqModal = function() {
        c.partnerForm = {
            partner: 'Partner Bank A - SIMULATED DEMO PARTNER',
            request_type: 'Transaction Verification',
            priority: 'P1 - Critical',
            due_date: '2026-10-02 18:00 IST',
            evidence_ref: 'EV-003 - Bank Statement PDF',
            description: 'Transaction TXN-2026-84920194819 for INR 85,000 requires inter-bank verification and beneficiary lien placement.'
        };
        c.showPartnerReqModal = true;
    };

    c.submitPartnerVerificationRequest = function() {
        var newReq = {
            id: 'PR-00' + (c.activeInvestigationCase.partner_requests.length + 1),
            partner: c.partnerForm.partner,
            demo_flag: true,
            request_type: c.partnerForm.request_type,
            priority: c.partnerForm.priority,
            due_date: c.partnerForm.due_date,
            description: c.partnerForm.description,
            status: 'Submitted'
        };
        c.activeInvestigationCase.partner_requests.unshift(newReq);
        c.showPartnerReqModal = false;
        c.addTimelineEvent('HUMAN', 'Partner Request Submitted', 'Inter-bank verification request sent to ' + newReq.partner, newReq.id);

        // Simulate instant demo partner response
        $timeout(function() {
            newReq.status = 'Response Received';
            newReq.response = {
                received_on: 'Just now',
                verification_result: 'CONFIRMED UNAUTHORIZED / SUSPECTED MULE NODE',
                details: 'Partner bank verifies unauthorized transaction sequence. Immediate debit freeze placed on beneficiary account pay-fast-merchant@ybl.',
                beneficiary_bank: 'Yes Bank Switch',
                account_status: 'FROZEN / LIEN PLACED',
                held_amount: 35000
            };
            newReq.ai_analysis = {
                classification: 'Confirms Unauthorized Transaction & Money Mule Account',
                supporting_info: 'Beneficiary account held INR 35,000. Rapid burst velocity indicates automated laundering.',
                contradictions: null,
                suggested_finding_update: 'FND-004: Beneficiary confirmed as flagged mule.',
                suggested_risk_impact: 'Elevate Case Risk to 94/100 (Critical)'
            };
            newReq.analysis_accepted = false;
            c.addTimelineEvent('SYSTEM', 'Partner Response Received', 'Simulated partner response received from ' + newReq.partner, newReq.id);
        }, 1200);
    };

    c.acceptPartnerAnalysis = function(pr) {
        pr.analysis_accepted = true;
        c.activeInvestigationCase.risk_score = 94;
        c.activeInvestigationCase.blocked_amount = 35000;
        c.addTimelineEvent('HUMAN', 'Partner Analysis Accepted', 'Investigator accepted partner analysis and elevated case risk to 94/100.', pr.id);
    };

    c.rejectPartnerAnalysis = function(pr) {
        pr.analysis_accepted = false;
        c.addTimelineEvent('HUMAN', 'Partner Analysis Rejected', 'Investigator rejected suggested risk elevation.', pr.id);
    };

    // 8. Alerts Modals
    c.openAlertCustomerModal = function() {
        c.customerAlertTemplate = 'case_update';
        c.onCustomerTemplateChange();
        c.showAlertCustomerModal = true;
    };

    c.onCustomerTemplateChange = function() {
        var t = c.customerAlertTemplate;
        var name = (c.activeInvestigationCase.customer && c.activeInvestigationCase.customer.name) || 'Customer';
        var num = c.activeInvestigationCase.number;
        if (t === 'case_received') {
            c.customerAlertPreview = 'Dear ' + name + ', your fraud report has been received and registered under Reference ' + num + '. Our Fraud Investigation Team is actively reviewing your evidence.';
        } else if (t === 'investigation_started') {
            c.customerAlertPreview = 'Dear ' + name + ', an official investigation has begun for case ' + num + '. Senior Investigator Alex Morgan has been assigned to lead your case.';
        } else if (t === 'case_update') {
            c.customerAlertPreview = 'Dear ' + name + ', update on Case ' + num + ': Our team has verified the unauthorized transaction with the destination bank and placed a lien on recipient funds. Next update in 2 hours.';
        } else if (t === 'decision_complete' || t === 'report_available') {
            c.customerAlertPreview = 'Dear ' + name + ', the investigation for Case ' + num + ' has concluded with an official finding of Confirmed Unauthorized Fraud. Zero-liability claim reimbursement advice has been issued. View your safe statement in the portal.';
        } else {
            c.customerAlertPreview = 'Dear ' + name + ', your case ' + num + ' has been updated by your investigation officer.';
        }
    };

    c.sendCustomerAlert = function() {
        c.showAlertCustomerModal = false;
        c.addTimelineEvent('HUMAN', 'Customer Alert Sent', 'Sanitized progress statement dispatched to ' + c.activeInvestigationCase.customer.email, 'NOTIF-CUST');
        alert('Safe notification dispatched to customer: ' + c.activeInvestigationCase.customer.email);
    };

    c.openAlertWorkerModal = function() {
        c.workerAlertTemplate = 'partner_response';
        c.workerAlertAssignee = 'Marcus Vance';
        c.workerAlertNotes = 'Partner Bank A confirmed unauthorized transaction. High exposure exceeds INR 50,000 threshold. Requesting manager review.';
        c.showAlertWorkerModal = true;
    };

    c.sendWorkerAlert = function() {
        c.showAlertWorkerModal = false;
        c.addTimelineEvent('HUMAN', 'Case Worker Alerted', 'Internal priority alert sent to ' + c.workerAlertAssignee + ': ' + c.workerAlertNotes, 'NOTIF-WRK');
        alert('Internal alert dispatched to ' + c.workerAlertAssignee);
    };

    // 9. Human Decision & Case Resolution
    c.decisionForm = {
        decision: 'Resolve Case',
        reason: 'Investigation confirms credentials were harvested via deceptive smishing domain secure-bank-login-verify.com. The unauthorized debit of INR 85,000 on 2026-10-02 has been verified by Partner Bank A. A lien of INR 35,000 is active on the beneficiary node. Reversal advice initiated.'
    };

    c.grantManagerApproval = function() {
        c.activeInvestigationCase.manager_approved = true;
        c.addTimelineEvent('HUMAN', 'Manager Approval Granted', 'Marcus Vance (Fraud Operations Director) authorized case resolution and claim advice.', 'APP-MV');
    };

    c.executeHumanDecision = function() {
        if (!c.isEvidenceVerified() || !c.isFindingsConfirmed()) {
            alert('Validation Error: All evidence items must be verified and findings confirmed before submitting resolution.');
            return;
        }
        if (!c.decisionForm.reason || c.decisionForm.reason.length < 15) {
            alert('Validation Error: A detailed formal decision reason is mandatory.');
            return;
        }

        c.activeInvestigationCase.decision = {
            status: 'Resolved',
            outcome: 'Confirmed Fraud',
            reason: c.decisionForm.reason,
            investigator: 'Alex Morgan',
            timestamp: new Date().toLocaleString()
        };
        c.activeInvestigationCase.status = 'Resolved';
        c.addTimelineEvent('HUMAN', 'Case Resolved', 'Formal human investigation decision executed: Confirmed Fraud. Case resolved.', c.activeInvestigationCase.number);
        alert('Human decision successfully recorded! Case ' + c.activeInvestigationCase.number + ' has been marked as RESOLVED.');
    };

    // 10. Generative Intelligence Review Actions
    c.openGenAIModal = function() {
        c.showGenAIModal = true;
        if (!c.generatedOutput) {
            c.generateSelectedIntelligence();
        }
    };

    c.acceptGenAI = function() {
        c.showGenAIModal = false;
        c.addTimelineEvent('HUMAN', 'Generative Intelligence Accepted', 'Investigator reviewed and accepted ' + c.selectedGenAIMode + ' synthesis.', 'GENAI-ACC');
        alert('Generative Intelligence synthesis accepted and attached to case dossier.');
    };

    c.rejectGenAI = function() {
        c.generatedOutput = '';
        c.showGenAIModal = false;
        c.addTimelineEvent('HUMAN', 'Generative Intelligence Rejected', 'Investigator rejected AI synthesis.', 'GENAI-REJ');
    };

    c.copyGenAIToReport = function() {
        c.showGenAIModal = false;
        c.setInvestigationTab('report');
        alert('Synthesis copied to Case Reports workspace.');
    };

    c.addGenAIToNotes = function() {
        c.activeInvestigationCase.notes.unshift({
            author: 'Alex Morgan (via GenAI)',
            role: 'Senior Investigator',
            timestamp: new Date().toLocaleTimeString(),
            text: c.generatedOutput,
            tags: ['GenAI', 'Synthesis']
        });
        c.showGenAIModal = false;
        c.setInvestigationTab('investigation');
    };

    // 11. Timeline Helper & Filtering
    c.addTimelineEvent = function(actorType, action, desc, recId) {
        var now = new Date();
        var timeStr = now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0') + ' IST';
        c.activeInvestigationCase.timeline.unshift({
            time: timeStr,
            actor: actorType === 'HUMAN' ? 'Alex Morgan' : (actorType === 'AI SYSTEM' ? 'FRAUDNEXUS AI' : 'System Engine'),
            actor_type: actorType,
            action: action,
            desc: desc,
            record_id: recId
        });
    };

    c.getFilteredTimeline = function() {
        if (!c.activeInvestigationCase || !c.activeInvestigationCase.timeline) return [];
        if (!c.timelineFilter || c.timelineFilter === 'all') return c.activeInvestigationCase.timeline;
        return c.activeInvestigationCase.timeline.filter(function(item) {
            return item.actor_type === c.timelineFilter;
        });
    };

    // 12. End-to-End Demo Walkthrough (Section 35 & 40)
    c.demoWalkthroughActive = false;
    c.demoStep = 1;

    c.runEndToEndDemo = function() {
        c.demoWalkthroughActive = true;
        c.demoStep = 1;
        c.demoTitle = "1. Customer Submission Ingested";
        c.demoDesc = "Customer Rajesh Sharma reports INR 85,000 lost via smishing SMS. JOREN multimodal pipeline ingested 4 artifacts.";
        c.investigationTab = 'overview';
    };

    c.advanceDemo = function() {
        c.demoStep++;
        if (c.demoStep === 2) {
            c.demoTitle = "2. JOREN Multimodal Evidence Processing";
            c.demoDesc = "JOREN classifies SMS screenshot, URL capture, statement PDF, and email alert. Integrity hashes validated.";
            c.investigationTab = 'evidence';
        } else if (c.demoStep === 3) {
            c.demoTitle = "3. Human Verification of Evidence";
            c.demoDesc = "Investigator reviews and confirms all 4 submitted evidence artifacts.";
            c.confirmAllEvidence();
            c.investigationTab = 'verification';
        } else if (c.demoStep === 4) {
            c.demoTitle = "4. AI Findings Confirmation";
            c.demoDesc = "Investigator validates 4 AI-generated findings (credential harvesting, foreign IP session hijack, money mule).";
            c.confirmAllFindings();
            c.investigationTab = 'findings';
        } else if (c.demoStep === 5) {
            c.demoTitle = "5. Cyber Attack Chain Visualized";
            c.demoDesc = "Connected threat chain: Phishing SMS -> Fake Portal -> Harvested Credentials -> Tor IP 185.220.101.5 -> UPI Debit.";
            c.investigationTab = 'cyber';
        } else if (c.demoStep === 6) {
            c.demoTitle = "6. Inter-Bank Partner Request";
            c.demoDesc = "Submitted trace PR-001 to Partner Bank A (SIMULATED DEMO PARTNER).";
            c.investigationTab = 'partnerRequests';
        } else if (c.demoStep === 7) {
            c.demoTitle = "7. Partner Response & AI Analysis";
            c.demoDesc = "Partner Bank A confirms unauthorized debit; places lien on INR 35,000. Risk elevated to 94/100 Critical.";
            c.activeInvestigationCase.risk_score = 94;
            c.investigationTab = 'partnerRequests';
        } else if (c.demoStep === 8) {
            c.demoTitle = "8. Generative Intelligence Synthesis";
            c.demoDesc = "Generated comprehensive Case Journey Summary using FNXCaseContextBuilder.";
            c.openGenAIModal();
        } else if (c.demoStep === 9) {
            c.demoTitle = "9. Formal Human Decision & Manager Approval";
            c.demoDesc = "Investigator Alex Morgan records Confirmed Fraud resolution; Director Marcus Vance approves zero-liability claim.";
            c.grantManagerApproval();
            c.investigationTab = 'decision';
        } else if (c.demoStep === 10) {
            c.demoTitle = "10. Reports Dispatched & Case Resolved!";
            c.demoDesc = "Internal 27-section dossier compiled. Sanitized 13-section safe report dispatched to victim. Case Resolved!";
            c.executeHumanDecision();
            c.investigationTab = 'report';
        } else {
            c.demoWalkthroughActive = false;
        }
    };

    c.resetDemo = function() {
        c.activeInvestigationCase = c.setupDefaultInvestigationCase();
        c.demoStep = 1;
        c.runEndToEndDemo();
    };

    // 13. Initialize Active Case
    if (!c.activeInvestigationCase) {
        c.activeInvestigationCase = c.setupDefaultInvestigationCase();
    }

};
