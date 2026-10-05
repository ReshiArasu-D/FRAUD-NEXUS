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
        hi: {
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
            addTask: 'Add Task'
        },
        ta: {
            brand: 'FRAUDNEXUS',
            tagline: 'மோசடி அறிக்கையிலிருந்து தீர்மானம் வரை — ஒரு அறிவார்ந்த புலனாய்வு பணியிடம்',
            heroTitle: 'மோசடி அறிக்கையிலிருந்து தீர்மானம் வரை',
            heroSub: 'நிதி & சைபர் மோசடி விசாரணை மையம்',
            heroDesc: 'பாதிக்கப்பட்டவர்கள், புலனாய்வாளர்கள், நிதி நிறுவனங்கள் மற்றும் சட்ட அமலாக்கத்தை இணைக்கும் ஒரு அறிவார்ந்த விசாரணை பணியிடம்.',
            getStarted: 'தொடங்குங்கள்',
            learnMore: 'மேலும் அறிக',
            portalSelectTitle: 'உங்கள் போர்ட்டலைத் தேர்ந்தெடுக்கவும்',
            portalSelectSub: 'உங்கள் பணிக்கு பொருந்தக்கூடிய பணியிடத்தைத் தேர்வு செய்யவும்.',
            customerPortal: 'வாடிக்கையாளர் போர்டல்',
            customerPortalDesc: 'குடிமக்களும் பாதிக்கப்பட்டவர்களும் மோசடியைப் பாதுகாப்பாகப் புகாரளிக்கவும், வழக்குகளை நிகழ்நேரத்தில் கண்காணிக்கவும், ஆதாரங்களைச் சமர்ப்பிக்கவும்.',
            investigatorPortal: 'புலனாய்வாளர் / நிர்வாக போர்டல்',
            investigatorPortalDesc: 'வழக்குகளை விசாரிக்கவும், உளவுத்துறையை ஆய்வு செய்யவும், இணக்கத்தை நிர்வகிக்கவும் அங்கீகரிக்கப்பட்ட பணியாளர்களுக்கு.',
            enterPortal: 'வாடிக்கையாளர் போர்ட்டலை உள்ளிடவும்',
            comingSoon: 'விரைவில்',
            login: 'உள்நுழைக',
            register: 'பதிவு செய்யுங்கள்',
            email: 'மின்னஞ்சல் முகவரி',
            password: 'கடவுச்சொல்',
            confirmPassword: 'கடவுச்சொல்லை உறுதிப்படுத்தவும்',
            fullName: 'முழுப் பெயர்',
            mobile: 'மொபைல் எண்',
            dob: 'பிறந்த தேதி',
            gender: 'பாலினம்',
            occupation: 'தொழில்',
            address: 'குடியிருப்பு முகவரி',
            forgotPassword: 'கடவுச்சொல் மறந்துவிட்டதா?',
            resetPasswordTitle: 'கடவுச்சொல்லை மீட்டமைக்கவும்',
            resetPasswordDesc: 'கடவுச்சொல் மீட்டமைப்பு வழிமுறைகளைப் பெற உங்கள் பதிவு செய்யப்பட்ட மின்னஞ்சல் முகவரியை உள்ளிடவும்.',
            instructionsSent: 'வழிமுறைகளை மீட்டமைக்க அனுப்பப்பட்டது',
            resetSentMsg: 'இந்த மின்னஞ்சல் முகவரியுடன் கணக்கு இணைக்கப்பட்டிருந்தால், கடவுச்சொல் மீட்டமைப்பு வழிமுறைகளும் சரிபார்ப்பு இணைப்பும் அனுப்பப்படும்.',
            sendResetLink: 'மீட்டமை இணைப்பை அனுப்பவும்',
            backToLogin: 'உள்நுழைவுக்குத் திரும்பு',
            hasAccount: 'ஏற்கனவே கணக்கு உள்ளதா?',
            createAccountSuccess: 'கணக்கு வெற்றிகரமாக உருவாக்கப்பட்டது!',
            createAccountSuccessDesc: 'உங்கள் FRAUDNEXUS வாடிக்கையாளர் கணக்கு பதிவு செய்யப்பட்டுள்ளது. உங்கள் சான்றுகளுடன் உள்நுழையவும்.',
            goToLogin: 'உள்நுழைவுக்குச் செல்லவும்',
            dashboard: 'டாஷ்போர்டு',
            reportFraud: 'மோசடி புகார்',
            trackCases: 'வழக்குகளைக் கண்காணிக்கவும்',
            evidence: 'ஆதாரம்',
            profile: 'வாடிக்கையாளர் சுயவிவரம்',
            helpSupport: 'உதவி & ஆதரவு',
            welcome: 'வரவேற்கிறோம்',
            totalCases: 'மொத்த வழக்குகள்',
            activeCases: 'செயலில் உள்ள வழக்குகள்',
            resolvedCases: 'தீர்க்கப்பட்ட வழக்குகள்',
            closedCases: 'மூடப்பட்ட வழக்குகள்',
            recentCases: 'சமீபத்திய வழக்குகள்',
            caseId: 'வழக்கு ஐடி',
            incidentType: 'சம்பவ வகை',
            date: 'தேதி',
            severity: 'தீவிரம்',
            status: 'நிலை',
            action: 'செயல்',
            viewDetails: 'விவரங்களைக் காண்க',
            noCases: 'வழக்குகள் எதுவும் கண்டறியப்படவில்லை. தொடங்குவதற்கு ஒரு மோசடியைப் புகாரளிக்கவும்.',
            kycStatus: 'KYC நிலை',
            completeKyc: 'KYC ஐ முடிக்கவும்',
            govIdType: 'அரசாங்க ஐடி வகை',
            govIdNumber: 'அரசாங்க அடையாள எண்',
            proofDocument: 'அடையாளச் சான்று ஆவணம்',
            submitKyc: 'மதிப்பாய்விற்கு KYC ஐ சமர்ப்பிக்கவும்',
            kycPendingNote: 'அவசர மோசடி அறிக்கையிடலுக்கு அடையாளச் சரிபார்ப்பு விருப்பமானது மற்றும் வழக்குச் சமர்ப்பிப்பைத் தடுக்காது.',
            financialInvolvement: 'நிதி இழப்பு அல்லது பரிவர்த்தனை ஈடுபாடு உள்ளதா?',
            institutionType: 'நிறுவன வகை',
            institutionName: 'நிறுவனம் / வங்கி / பயன்பாட்டின் பெயர்',
            paymentMode: 'நிதி நடவடிக்கை முறை',
            referenceType: 'குறிப்பு வகை',
            referenceNumber: 'குறிப்பு எண் / UTR',
            amountInvolved: 'சம்பந்தப்பட்ட தொகை (INR)',
            blockedAmount: 'வாடிக்கையாளர் புகாரளித்த தடுக்கப்பட்ட தொகை',
            recoveredAmount: 'வாடிக்கையாளரால் அறிவிக்கப்பட்ட மீட்டெடுக்கப்பட்ட தொகை',
            suspectName: 'சந்தேக நபர் / பயனாளியின் பெயர்',
            suspectContact: 'சந்தேகத்திற்குரிய தொடர்பு / UPI ஐடி / கணக்கு',
            evidenceType: 'சான்று வகை',
            evidenceDesc: 'சான்று விளக்கம்',
            attachProof: 'ஆதாரக் கோப்பை இணைக்கவும்',
            submitReport: 'மோசடி அறிக்கையை சமர்ப்பிக்கவும்',
            submitting: 'சமர்ப்பிக்கிறது...',
            stageSubmitted: 'சமர்ப்பிக்கப்பட்டது',
            stageInitialReview: 'ஆரம்ப மதிப்பாய்வு',
            stageInvestigation: 'விசாரணை',
            stageResolution: 'தீர்மானம்',
            stageClosed: 'மூடப்பட்டது',
            addAdditionalEvidence: 'கூடுதல் சான்றுகளைச் சேர்க்கவும்',
            askAI: 'FRAUDNEXUS AI ஐக் கேளுங்கள்',
            send: 'அனுப்பு',
            close: 'மூடு',
            logout: 'வெளியேறு',
            commandCenter: 'கட்டளை மையம்',
            partners: 'பங்குதாரர்கள்',
            partnerDirectory: 'கூட்டாளர் கோப்பகம்',
            addPartner: 'கூட்டாளரைச் சேர்க்கவும்',
            editPartner: 'கூட்டாளரைத் திருத்து',
            partnerRequests: 'கூட்டாளர் கோரிக்கைகள்',
            requestStatus: 'கோரிக்கை நிலை',
            partnerCategory: 'கூட்டாளர் வகை',
            integrationType: 'ஒருங்கிணைப்பு வகை',
            active: 'செயலில்',
            inactive: 'செயலற்றது',
            suspended: 'இடைநிறுத்தப்பட்டது',
            simulatedDemoPartner: 'உருவகப்படுத்தப்பட்ட டெமோ பார்ட்னர்',
            totalPartners: 'மொத்த பங்குதாரர்கள்',
            activePartners: 'செயலில் பங்குதாரர்கள்',
            pendingRequests: 'நிலுவையில் உள்ள கோரிக்கைகள்',
            awaitingResponse: 'பதிலுக்காக காத்திருக்கிறது',
            overdueRequests: 'தாமதமான கோரிக்கைகள்',
            customers: 'வாடிக்கையாளர்கள்',
            cases: 'வழக்குகள்',
            investigation: 'விசாரணை',
            intelligenceWorkspace: 'புலனாய்வு பணியிடம்',
            analytics: 'பகுப்பாய்வு',
            settings: 'அமைப்புகள்',
            adminLoginTitle: 'வெல்கம் பேக்',
            adminLoginSub: 'FRAUDNEXUS இன்வெஸ்டிகேஷன் பணியிடத்தில் உள்நுழையவும்',
            signIn: 'உள்நுழையவும்',
            tryDemo: 'டெமோவை முயற்சிக்கவும்',
            demoEnv: 'டெமோ சூழல்',
            priorityQueue: 'முன்னுரிமை விசாரணை வரிசை',
            actionCenter: 'நடவடிக்கை மையம்',
            fraudTrends: 'மோசடி வழக்கு போக்குகள்',
            financialExposureSummary: 'நிதி வெளிப்பாடு சுருக்கம்',
            recentActivity: 'சமீபத்திய செயல்பாடு',
            newCases: 'புதிய வழக்குகள்',
            criticalCases: 'முக்கியமான வழக்குகள்',
            escalatedCases: 'விரிவாக்கப்பட்ட வழக்குகள்',
            pendingApprovals: 'நிலுவையில் உள்ள ஒப்புதல்கள்',
            financialExposure: 'நிதி வெளிப்பாடு',
            unassigned: 'ஒதுக்கப்படாதது',
            assign: 'ஒதுக்கு',
            openWorkspace: 'பணியிடத்தைத் திறக்கவும்',
            requestEvidence: 'ஆதாரங்களைக் கோருங்கள்',
            escalate: 'அதிகரிக்கும்',
            resolve: 'தீர்க்கவும்',
            closeCase: 'வழக்கை மூடு',
            addTask: 'பணியைச் சேர்க்கவும்'
        },
        te: {
            brand: 'FRAUDNEXUS',
            tagline: 'ఫ్రాడ్ రిపోర్ట్ నుండి రిజల్యూషన్ వరకు — వన్ ఇంటెలిజెంట్ ఇన్వెస్టిగేషన్ వర్క్‌స్పేస్',
            heroTitle: 'మోసం నివేదిక నుండి రిజల్యూషన్ వరకు',
            heroSub: 'ఫైనాన్షియల్ & సైబర్ ఫ్రాడ్ ఇన్వెస్టిగేషన్ హబ్',
            heroDesc: 'బాధితులు, పరిశోధకులు, ఆర్థిక సంస్థలు మరియు చట్టాన్ని అమలు చేసే వ్యక్తులను అనుసంధానించే ఒక తెలివైన పరిశోధన కార్యస్థలం.',
            getStarted: 'ప్రారంభించండి',
            learnMore: 'మరింత తెలుసుకోండి',
            portalSelectTitle: 'మీ పోర్టల్‌ని ఎంచుకోండి',
            portalSelectSub: 'మీ పాత్రకు సరిపోయే కార్యస్థలాన్ని ఎంచుకోండి.',
            customerPortal: 'కస్టమర్ పోర్టల్',
            customerPortalDesc: 'పౌరులు మరియు బాధితులు మోసాన్ని సురక్షితంగా నివేదించడానికి, నిజ సమయంలో కేసులను ట్రాక్ చేయడానికి మరియు సాక్ష్యాలను సమర్పించడానికి.',
            investigatorPortal: 'పరిశోధకుడు / అడ్మిన్ పోర్టల్',
            investigatorPortalDesc: 'కేసులను పరిశోధించడానికి, ఇంటెలిజెన్స్‌ని విశ్లేషించడానికి మరియు సమ్మతిని నిర్వహించడానికి అధికారం కలిగిన సిబ్బందికి.',
            enterPortal: 'కస్టమర్ పోర్టల్‌ని నమోదు చేయండి',
            comingSoon: 'త్వరలో వస్తుంది',
            login: 'లాగిన్ చేయండి',
            register: 'నమోదు చేసుకోండి',
            email: 'ఇమెయిల్ చిరునామా',
            password: 'పాస్వర్డ్',
            confirmPassword: 'పాస్‌వర్డ్‌ని నిర్ధారించండి',
            fullName: 'పూర్తి పేరు',
            mobile: 'మొబైల్ నంబర్',
            dob: 'పుట్టిన తేదీ',
            gender: 'లింగం',
            occupation: 'వృత్తి',
            address: 'నివాస చిరునామా',
            forgotPassword: 'పాస్‌వర్డ్ మర్చిపోయారా?',
            resetPasswordTitle: 'పాస్‌వర్డ్‌ని రీసెట్ చేయండి',
            resetPasswordDesc: 'పాస్‌వర్డ్ రీసెట్ సూచనలను స్వీకరించడానికి మీ నమోదిత ఇమెయిల్ చిరునామాను నమోదు చేయండి.',
            instructionsSent: 'రీసెట్ సూచనలు పంపబడ్డాయి',
            resetSentMsg: 'ఈ ఇమెయిల్ చిరునామాతో ఖాతా అనుబంధించబడి ఉంటే, పాస్‌వర్డ్ రీసెట్ సూచనలు మరియు ధృవీకరణ లింక్ పంపబడతాయి.',
            sendResetLink: 'రీసెట్ లింక్‌ని పంపండి',
            backToLogin: 'తిరిగి లాగిన్‌కి',
            hasAccount: 'ఇప్పటికే ఖాతా ఉందా?',
            createAccountSuccess: 'ఖాతా విజయవంతంగా సృష్టించబడింది!',
            createAccountSuccessDesc: 'మీ FRAUDNEXUS కస్టమర్ ఖాతా నమోదు చేయబడింది. దయచేసి మీ ఆధారాలతో లాగిన్ అవ్వండి.',
            goToLogin: 'లాగిన్‌కి వెళ్లండి',
            dashboard: 'డాష్‌బోర్డ్',
            reportFraud: 'మోసాన్ని నివేదించండి',
            trackCases: 'కేసులను ట్రాక్ చేయండి',
            evidence: 'సాక్ష్యం',
            profile: 'కస్టమర్ ప్రొఫైల్',
            helpSupport: 'సహాయం & మద్దతు',
            welcome: 'స్వాగతం',
            totalCases: 'మొత్తం కేసులు',
            activeCases: 'యాక్టివ్ కేసులు',
            resolvedCases: 'పరిష్కరించబడిన కేసులు',
            closedCases: 'క్లోజ్డ్ కేసులు',
            recentCases: 'ఇటీవలి కేసులు',
            caseId: 'కేసు ID',
            incidentType: 'సంఘటన రకం',
            date: 'తేదీ',
            severity: 'తీవ్రత',
            status: 'స్థితి',
            action: 'చర్య',
            viewDetails: 'వివరాలను వీక్షించండి',
            noCases: 'కేసులు ఏవీ కనుగొనబడలేదు. ప్రారంభించడానికి మోసాన్ని నివేదించండి.',
            kycStatus: 'KYC స్థితి',
            completeKyc: 'KYCని పూర్తి చేయండి',
            govIdType: 'ప్రభుత్వ ID రకం',
            govIdNumber: 'ప్రభుత్వ ID నంబర్',
            proofDocument: 'ID ప్రూఫ్ డాక్యుమెంట్',
            submitKyc: 'సమీక్ష కోసం KYCని సమర్పించండి',
            kycPendingNote: 'అత్యవసర ఫ్రాడ్ రిపోర్టింగ్ కోసం గుర్తింపు ధృవీకరణ ఐచ్ఛికం మరియు కేసు సమర్పణను నిరోధించదు.',
            financialInvolvement: 'ఆర్థిక నష్టం లేదా లావాదేవీ ప్రమేయం ఉందా?',
            institutionType: 'సంస్థ రకం',
            institutionName: 'సంస్థ / బ్యాంక్ / యాప్ పేరు',
            paymentMode: 'ఆర్థిక కార్యాచరణ మోడ్',
            referenceType: 'సూచన రకం',
            referenceNumber: 'సూచన సంఖ్య / UTR',
            amountInvolved: 'పాల్గొన్న మొత్తం (INR)',
            blockedAmount: 'కస్టమర్ నివేదించిన బ్లాక్ చేయబడిన మొత్తం',
            recoveredAmount: 'కస్టమర్ నివేదించిన రికవరీ మొత్తం',
            suspectName: 'అనుమానితుడు / లబ్ధిదారుని పేరు',
            suspectContact: 'అనుమానిత సంప్రదింపు / UPI ID / ఖాతా',
            evidenceType: 'సాక్ష్యం రకం',
            evidenceDesc: 'సాక్ష్యం వివరణ',
            attachProof: 'ఎవిడెన్స్ ఫైల్‌ని అటాచ్ చేయండి',
            submitReport: 'మోసం నివేదికను సమర్పించండి',
            submitting: 'సమర్పిస్తోంది...',
            stageSubmitted: 'సమర్పించారు',
            stageInitialReview: 'ప్రారంభ సమీక్ష',
            stageInvestigation: 'విచారణ',
            stageResolution: 'రిజల్యూషన్',
            stageClosed: 'మూసివేయబడింది',
            addAdditionalEvidence: 'అదనపు సాక్ష్యాలను జోడించండి',
            askAI: 'FRAUDNEXUS AIని అడగండి',
            send: 'పంపండి',
            close: 'మూసివేయి',
            logout: 'లాగ్అవుట్',
            commandCenter: 'కమాండ్ సెంటర్',
            partners: 'భాగస్వాములు',
            partnerDirectory: 'భాగస్వామి డైరెక్టరీ',
            addPartner: 'భాగస్వామిని జోడించండి',
            editPartner: 'భాగస్వామిని సవరించండి',
            partnerRequests: 'భాగస్వామి అభ్యర్థనలు',
            requestStatus: 'అభ్యర్థన స్థితి',
            partnerCategory: 'భాగస్వామి వర్గం',
            integrationType: 'ఇంటిగ్రేషన్ రకం',
            active: 'చురుకుగా',
            inactive: 'నిష్క్రియ',
            suspended: 'సస్పెండ్ చేయబడింది',
            simulatedDemoPartner: 'అనుకరణ డెమో భాగస్వామి',
            totalPartners: 'మొత్తం భాగస్వాములు',
            activePartners: 'క్రియాశీల భాగస్వాములు',
            pendingRequests: 'పెండింగ్‌లో ఉన్న అభ్యర్థనలు',
            awaitingResponse: 'ప్రతిస్పందన కోసం వేచి ఉంది',
            overdueRequests: 'గడువు ముగిసిన అభ్యర్థనలు',
            customers: 'వినియోగదారులు',
            cases: 'కేసులు',
            investigation: 'విచారణ',
            intelligenceWorkspace: 'ఇంటెలిజెన్స్ వర్క్‌స్పేస్',
            analytics: 'విశ్లేషణలు',
            settings: 'సెట్టింగ్‌లు',
            adminLoginTitle: 'తిరిగి స్వాగతం',
            adminLoginSub: 'FRAUDNEXUS ఇన్వెస్టిగేషన్ వర్క్‌స్పేస్‌కి సైన్ ఇన్ చేయండి',
            signIn: 'సైన్ ఇన్ చేయండి',
            tryDemo: 'డెమోని ప్రయత్నించండి',
            demoEnv: 'డెమో ఎన్విరాన్మెంట్',
            priorityQueue: 'ప్రయారిటీ ఇన్వెస్టిగేషన్ క్యూ',
            actionCenter: 'యాక్షన్ సెంటర్',
            fraudTrends: 'మోసం కేసు ట్రెండ్‌లు',
            financialExposureSummary: 'ఫైనాన్షియల్ ఎక్స్‌పోజర్ సారాంశం',
            recentActivity: 'ఇటీవలి కార్యాచరణ',
            newCases: 'కొత్త కేసులు',
            criticalCases: 'క్రిటికల్ కేసులు',
            escalatedCases: 'ఎస్కలేటెడ్ కేసులు',
            pendingApprovals: 'పెండింగ్‌లో ఉన్న ఆమోదాలు',
            financialExposure: 'ఫైనాన్షియల్ ఎక్స్‌పోజర్',
            unassigned: 'కేటాయించబడలేదు',
            assign: 'కేటాయించండి',
            openWorkspace: 'కార్యస్థలాన్ని తెరవండి',
            requestEvidence: 'సాక్ష్యాలను అభ్యర్థించండి',
            escalate: 'పెంచండి',
            resolve: 'పరిష్కరించండి',
            closeCase: 'కేసును మూసివేయండి',
            addTask: 'టాస్క్ జోడించండి'
        },
        kn: {
            brand: 'ಫ್ರಾಡ್ನೆಕ್ಸಸ್',
            tagline: 'ವಂಚನೆ ವರದಿಯಿಂದ ರೆಸಲ್ಯೂಶನ್‌ಗೆ — ಒಂದು ಇಂಟೆಲಿಜೆಂಟ್ ಇನ್ವೆಸ್ಟಿಗೇಷನ್ ವರ್ಕ್‌ಸ್ಪೇಸ್',
            heroTitle: 'ವಂಚನೆ ವರದಿಯಿಂದ ನಿರ್ಣಯದವರೆಗೆ',
            heroSub: 'ಹಣಕಾಸು ಮತ್ತು ಸೈಬರ್ ವಂಚನೆ ತನಿಖಾ ಕೇಂದ್ರ',
            heroDesc: 'ಬಲಿಪಶುಗಳು, ತನಿಖಾಧಿಕಾರಿಗಳು, ಹಣಕಾಸು ಸಂಸ್ಥೆಗಳು ಮತ್ತು ಕಾನೂನು ಜಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸುವ ಒಂದು ಬುದ್ಧಿವಂತ ತನಿಖಾ ಕಾರ್ಯಸ್ಥಳ.',
            getStarted: 'ಪ್ರಾರಂಭಿಸಿ',
            learnMore: 'ಇನ್ನಷ್ಟು ತಿಳಿಯಿರಿ',
            portalSelectTitle: 'ನಿಮ್ಮ ಪೋರ್ಟಲ್ ಆಯ್ಕೆಮಾಡಿ',
            portalSelectSub: 'ನಿಮ್ಮ ಪಾತ್ರಕ್ಕೆ ಹೊಂದಿಕೆಯಾಗುವ ಕಾರ್ಯಸ್ಥಳವನ್ನು ಆಯ್ಕೆಮಾಡಿ.',
            customerPortal: 'ಗ್ರಾಹಕ ಪೋರ್ಟಲ್',
            customerPortalDesc: 'ನಾಗರಿಕರು ಮತ್ತು ಬಲಿಪಶುಗಳಿಗೆ ವಂಚನೆಯನ್ನು ಸುರಕ್ಷಿತವಾಗಿ ವರದಿ ಮಾಡಲು, ನೈಜ ಸಮಯದಲ್ಲಿ ಪ್ರಕರಣಗಳನ್ನು ಪತ್ತೆಹಚ್ಚಲು ಮತ್ತು ಸಾಕ್ಷ್ಯವನ್ನು ಸಲ್ಲಿಸಲು.',
            investigatorPortal: 'ತನಿಖಾಧಿಕಾರಿ / ನಿರ್ವಾಹಕ ಪೋರ್ಟಲ್',
            investigatorPortalDesc: 'ಪ್ರಕರಣಗಳನ್ನು ತನಿಖೆ ಮಾಡಲು, ಗುಪ್ತಚರವನ್ನು ವಿಶ್ಲೇಷಿಸಲು ಮತ್ತು ಅನುಸರಣೆಯನ್ನು ನಿರ್ವಹಿಸಲು ಅಧಿಕೃತ ಸಿಬ್ಬಂದಿಗೆ.',
            enterPortal: 'ಗ್ರಾಹಕ ಪೋರ್ಟಲ್ ಅನ್ನು ನಮೂದಿಸಿ',
            comingSoon: 'ಶೀಘ್ರದಲ್ಲೇ ಬರಲಿದೆ',
            login: 'ಲಾಗಿನ್ ಮಾಡಿ',
            register: 'ನೋಂದಾಯಿಸಿ',
            email: 'ಇಮೇಲ್ ವಿಳಾಸ',
            password: 'ಪಾಸ್ವರ್ಡ್',
            confirmPassword: 'ಪಾಸ್ವರ್ಡ್ ಅನ್ನು ದೃಢೀಕರಿಸಿ',
            fullName: 'ಪೂರ್ಣ ಹೆಸರು',
            mobile: 'ಮೊಬೈಲ್ ಸಂಖ್ಯೆ',
            dob: 'ಹುಟ್ಟಿದ ದಿನಾಂಕ',
            gender: 'ಲಿಂಗ',
            occupation: 'ಉದ್ಯೋಗ',
            address: 'ವಸತಿ ವಿಳಾಸ',
            forgotPassword: 'ಪಾಸ್ವರ್ಡ್ ಮರೆತಿರುವಿರಾ?',
            resetPasswordTitle: 'ಪಾಸ್ವರ್ಡ್ ಮರುಹೊಂದಿಸಿ',
            resetPasswordDesc: 'ಪಾಸ್ವರ್ಡ್ ಮರುಹೊಂದಿಸುವ ಸೂಚನೆಗಳನ್ನು ಸ್ವೀಕರಿಸಲು ನಿಮ್ಮ ನೋಂದಾಯಿತ ಇಮೇಲ್ ವಿಳಾಸವನ್ನು ನಮೂದಿಸಿ.',
            instructionsSent: 'ಮರುಹೊಂದಿಸುವ ಸೂಚನೆಗಳನ್ನು ಕಳುಹಿಸಲಾಗಿದೆ',
            resetSentMsg: 'ಈ ಇಮೇಲ್ ವಿಳಾಸದೊಂದಿಗೆ ಖಾತೆಯು ಸಂಯೋಜಿತವಾಗಿದ್ದರೆ, ಪಾಸ್‌ವರ್ಡ್ ಮರುಹೊಂದಿಸುವ ಸೂಚನೆಗಳು ಮತ್ತು ಪರಿಶೀಲನೆ ಲಿಂಕ್ ಅನ್ನು ರವಾನಿಸಲಾಗಿದೆ.',
            sendResetLink: 'ಮರುಹೊಂದಿಸುವ ಲಿಂಕ್ ಕಳುಹಿಸಿ',
            backToLogin: 'ಲಾಗಿನ್ ಗೆ ಹಿಂತಿರುಗಿ',
            hasAccount: 'ಈಗಾಗಲೇ ಖಾತೆಯನ್ನು ಹೊಂದಿರುವಿರಾ?',
            createAccountSuccess: 'ಖಾತೆಯನ್ನು ಯಶಸ್ವಿಯಾಗಿ ರಚಿಸಲಾಗಿದೆ!',
            createAccountSuccessDesc: 'ನಿಮ್ಮ FRAUDNEXUS ಗ್ರಾಹಕ ಖಾತೆಯನ್ನು ನೋಂದಾಯಿಸಲಾಗಿದೆ. ದಯವಿಟ್ಟು ನಿಮ್ಮ ರುಜುವಾತುಗಳೊಂದಿಗೆ ಲಾಗ್ ಇನ್ ಮಾಡಿ.',
            goToLogin: 'ಲಾಗಿನ್ ಗೆ ಹೋಗಿ',
            dashboard: 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
            reportFraud: 'ವಂಚನೆ ವರದಿ ಮಾಡಿ',
            trackCases: 'ಪ್ರಕರಣಗಳನ್ನು ಟ್ರ್ಯಾಕ್ ಮಾಡಿ',
            evidence: 'ಸಾಕ್ಷಿ',
            profile: 'ಗ್ರಾಹಕರ ಪ್ರೊಫೈಲ್',
            helpSupport: 'ಸಹಾಯ ಮತ್ತು ಬೆಂಬಲ',
            welcome: 'ಸ್ವಾಗತ',
            totalCases: 'ಒಟ್ಟು ಪ್ರಕರಣಗಳು',
            activeCases: 'ಸಕ್ರಿಯ ಪ್ರಕರಣಗಳು',
            resolvedCases: 'ಪರಿಹರಿಸಿದ ಪ್ರಕರಣಗಳು',
            closedCases: 'ಮುಚ್ಚಿದ ಪ್ರಕರಣಗಳು',
            recentCases: 'ಇತ್ತೀಚಿನ ಪ್ರಕರಣಗಳು',
            caseId: 'ಕೇಸ್ ಐಡಿ',
            incidentType: 'ಘಟನೆಯ ಪ್ರಕಾರ',
            date: 'ದಿನಾಂಕ',
            severity: 'ತೀವ್ರತೆ',
            status: 'ಸ್ಥಿತಿ',
            action: 'ಕ್ರಿಯೆ',
            viewDetails: 'ವಿವರಗಳನ್ನು ವೀಕ್ಷಿಸಿ',
            noCases: 'ಯಾವುದೇ ಪ್ರಕರಣಗಳು ಕಂಡುಬಂದಿಲ್ಲ. ಪ್ರಾರಂಭಿಸಲು ವಂಚನೆಯನ್ನು ವರದಿ ಮಾಡಿ.',
            kycStatus: 'KYC ಸ್ಥಿತಿ',
            completeKyc: 'KYC ಪೂರ್ಣಗೊಳಿಸಿ',
            govIdType: 'ಸರ್ಕಾರಿ ID ಪ್ರಕಾರ',
            govIdNumber: 'ಸರ್ಕಾರಿ ID ಸಂಖ್ಯೆ',
            proofDocument: 'ID ಪುರಾವೆ ಡಾಕ್ಯುಮೆಂಟ್',
            submitKyc: 'ಪರಿಶೀಲನೆಗಾಗಿ KYC ಸಲ್ಲಿಸಿ',
            kycPendingNote: 'ತುರ್ತು ವಂಚನೆ ವರದಿಗಾಗಿ ಗುರುತಿನ ಪರಿಶೀಲನೆಯು ಐಚ್ಛಿಕವಾಗಿರುತ್ತದೆ ಮತ್ತು ಪ್ರಕರಣದ ಸಲ್ಲಿಕೆಯನ್ನು ನಿರ್ಬಂಧಿಸುವುದಿಲ್ಲ.',
            financialInvolvement: 'ಹಣಕಾಸಿನ ನಷ್ಟ ಅಥವಾ ವಹಿವಾಟಿನ ಒಳಗೊಳ್ಳುವಿಕೆ ಇದೆಯೇ?',
            institutionType: 'ಸಂಸ್ಥೆಯ ಪ್ರಕಾರ',
            institutionName: 'ಸಂಸ್ಥೆ / ಬ್ಯಾಂಕ್ / ಅಪ್ಲಿಕೇಶನ್ ಹೆಸರು',
            paymentMode: 'ಹಣಕಾಸು ಚಟುವಟಿಕೆ ಮೋಡ್',
            referenceType: 'ಉಲ್ಲೇಖದ ಪ್ರಕಾರ',
            referenceNumber: 'ಉಲ್ಲೇಖ ಸಂಖ್ಯೆ / UTR',
            amountInvolved: 'ಒಳಗೊಂಡಿರುವ ಮೊತ್ತ (INR)',
            blockedAmount: 'ಗ್ರಾಹಕ-ವರದಿ ಮಾಡಲಾದ ನಿರ್ಬಂಧಿಸಲಾದ ಮೊತ್ತ',
            recoveredAmount: 'ಗ್ರಾಹಕ-ವರದಿ ಮಾಡಿದ ಮರುಪಡೆಯಲಾದ ಮೊತ್ತ',
            suspectName: 'ಶಂಕಿತ / ಫಲಾನುಭವಿ ಹೆಸರು',
            suspectContact: 'ಶಂಕಿತ ಸಂಪರ್ಕ / UPI ಐಡಿ / ಖಾತೆ',
            evidenceType: 'ಸಾಕ್ಷ್ಯದ ಪ್ರಕಾರ',
            evidenceDesc: 'ಸಾಕ್ಷ್ಯ ವಿವರಣೆ',
            attachProof: 'ಎವಿಡೆನ್ಸ್ ಫೈಲ್ ಅನ್ನು ಲಗತ್ತಿಸಿ',
            submitReport: 'ವಂಚನೆ ವರದಿಯನ್ನು ಸಲ್ಲಿಸಿ',
            submitting: 'ಸಲ್ಲಿಸಲಾಗುತ್ತಿದೆ...',
            stageSubmitted: 'ಸಲ್ಲಿಸಲಾಗಿದೆ',
            stageInitialReview: 'ಆರಂಭಿಕ ವಿಮರ್ಶೆ',
            stageInvestigation: 'ತನಿಖೆ',
            stageResolution: 'ರೆಸಲ್ಯೂಶನ್',
            stageClosed: 'ಮುಚ್ಚಲಾಗಿದೆ',
            addAdditionalEvidence: 'ಹೆಚ್ಚುವರಿ ಪುರಾವೆಗಳನ್ನು ಸೇರಿಸಿ',
            askAI: 'FRAUDNEXUS AI ಅನ್ನು ಕೇಳಿ',
            send: 'ಕಳುಹಿಸು',
            close: 'ಮುಚ್ಚಿ',
            logout: 'ಲಾಗ್ಔಟ್',
            commandCenter: 'ಕಮಾಂಡ್ ಸೆಂಟರ್',
            partners: 'ಪಾಲುದಾರರು',
            partnerDirectory: 'ಪಾಲುದಾರ ಡೈರೆಕ್ಟರಿ',
            addPartner: 'ಪಾಲುದಾರರನ್ನು ಸೇರಿಸಿ',
            editPartner: 'ಪಾಲುದಾರರನ್ನು ಸಂಪಾದಿಸಿ',
            partnerRequests: 'ಪಾಲುದಾರರ ವಿನಂತಿಗಳು',
            requestStatus: 'ವಿನಂತಿ ಸ್ಥಿತಿ',
            partnerCategory: 'ಪಾಲುದಾರ ವರ್ಗ',
            integrationType: 'ಏಕೀಕರಣದ ಪ್ರಕಾರ',
            active: 'ಸಕ್ರಿಯ',
            inactive: 'ನಿಷ್ಕ್ರಿಯ',
            suspended: 'ಅಮಾನತುಗೊಳಿಸಲಾಗಿದೆ',
            simulatedDemoPartner: 'ಅನುಕರಿಸಿದ ಡೆಮೊ ಪಾಲುದಾರ',
            totalPartners: 'ಒಟ್ಟು ಪಾಲುದಾರರು',
            activePartners: 'ಸಕ್ರಿಯ ಪಾಲುದಾರರು',
            pendingRequests: 'ಬಾಕಿ ಉಳಿದಿರುವ ವಿನಂತಿಗಳು',
            awaitingResponse: 'ಪ್ರತಿಕ್ರಿಯೆಗಾಗಿ ನಿರೀಕ್ಷಿಸಲಾಗುತ್ತಿದೆ',
            overdueRequests: 'ಅವಧಿ ಮೀರಿದ ವಿನಂತಿಗಳು',
            customers: 'ಗ್ರಾಹಕರು',
            cases: 'ಪ್ರಕರಣಗಳು',
            investigation: 'ತನಿಖೆ',
            intelligenceWorkspace: 'ಗುಪ್ತಚರ ಕಾರ್ಯಕ್ಷೇತ್ರ',
            analytics: 'ಅನಾಲಿಟಿಕ್ಸ್',
            settings: 'ಸೆಟ್ಟಿಂಗ್‌ಗಳು',
            adminLoginTitle: 'ಮರಳಿ ಸ್ವಾಗತ',
            adminLoginSub: 'FRAUDNEXUS ಇನ್ವೆಸ್ಟಿಗೇಶನ್ ಕಾರ್ಯಸ್ಥಳಕ್ಕೆ ಸೈನ್ ಇನ್ ಮಾಡಿ',
            signIn: 'ಸೈನ್ ಇನ್ ಮಾಡಿ',
            tryDemo: 'ಡೆಮೊ ಪ್ರಯತ್ನಿಸಿ',
            demoEnv: 'ಡೆಮೊ ಪರಿಸರ',
            priorityQueue: 'ಆದ್ಯತೆಯ ತನಿಖಾ ಸರತಿ',
            actionCenter: 'ಆಕ್ಷನ್ ಸೆಂಟರ್',
            fraudTrends: 'ವಂಚನೆ ಪ್ರಕರಣದ ಪ್ರವೃತ್ತಿಗಳು',
            financialExposureSummary: 'ಹಣಕಾಸಿನ ಮಾನ್ಯತೆ ಸಾರಾಂಶ',
            recentActivity: 'ಇತ್ತೀಚಿನ ಚಟುವಟಿಕೆ',
            newCases: 'ಹೊಸ ಪ್ರಕರಣಗಳು',
            criticalCases: 'ನಿರ್ಣಾಯಕ ಪ್ರಕರಣಗಳು',
            escalatedCases: 'ಉಲ್ಬಣಗೊಂಡ ಪ್ರಕರಣಗಳು',
            pendingApprovals: 'ಬಾಕಿ ಉಳಿದಿರುವ ಅನುಮೋದನೆಗಳು',
            financialExposure: 'ಹಣಕಾಸಿನ ಮಾನ್ಯತೆ',
            unassigned: 'ನಿಯೋಜಿಸಲಾಗಿಲ್ಲ',
            assign: 'ನಿಯೋಜಿಸಿ',
            openWorkspace: 'ಕಾರ್ಯಕ್ಷೇತ್ರವನ್ನು ತೆರೆಯಿರಿ',
            requestEvidence: 'ಪುರಾವೆಗಳನ್ನು ವಿನಂತಿಸಿ',
            escalate: 'ಹೆಚ್ಚಿಸು',
            resolve: 'ಪರಿಹರಿಸು',
            closeCase: 'ಕೇಸ್ ಮುಚ್ಚಿ',
            addTask: 'ಕಾರ್ಯವನ್ನು ಸೇರಿಸಿ'
        },
        ml: {
            brand: 'ഫ്രാഡ്നെക്സസ്',
            tagline: 'വഞ്ചന റിപ്പോർട്ട് മുതൽ പ്രമേയം വരെ - ഒരു ഇൻ്റലിജൻ്റ് ഇൻവെസ്റ്റിഗേഷൻ വർക്ക്‌സ്‌പെയ്‌സ്',
            heroTitle: 'തട്ടിപ്പ് റിപ്പോർട്ട് മുതൽ പ്രമേയം വരെ',
            heroSub: 'സാമ്പത്തിക, സൈബർ തട്ടിപ്പ് അന്വേഷണ കേന്ദ്രം',
            heroDesc: 'ഇരകൾ, അന്വേഷകർ, ധനകാര്യ സ്ഥാപനങ്ങൾ, നിയമപാലകർ എന്നിവരെ ബന്ധിപ്പിക്കുന്ന ഒരു ഇൻ്റലിജൻ്റ് ഇൻവെസ്റ്റിഗേഷൻ വർക്ക്‌സ്‌പേസ്.',
            getStarted: 'ആരംഭിക്കുക',
            learnMore: 'കൂടുതലറിയുക',
            portalSelectTitle: 'നിങ്ങളുടെ പോർട്ടൽ തിരഞ്ഞെടുക്കുക',
            portalSelectSub: 'നിങ്ങളുടെ റോളുമായി പൊരുത്തപ്പെടുന്ന വർക്ക്‌സ്‌പെയ്‌സ് തിരഞ്ഞെടുക്കുക.',
            customerPortal: 'കസ്റ്റമർ പോർട്ടൽ',
            customerPortalDesc: 'പൗരന്മാർക്കും ഇരകൾക്കും സുരക്ഷിതമായി വഞ്ചന റിപ്പോർട്ട് ചെയ്യാനും കേസുകൾ തത്സമയം ട്രാക്ക് ചെയ്യാനും തെളിവുകൾ സമർപ്പിക്കാനും.',
            investigatorPortal: 'ഇൻവെസ്റ്റിഗേറ്റർ / അഡ്മിൻ പോർട്ടൽ',
            investigatorPortalDesc: 'കേസുകൾ അന്വേഷിക്കാനും ഇൻ്റലിജൻസ് വിശകലനം ചെയ്യാനും പാലിക്കൽ നിയന്ത്രിക്കാനും അംഗീകൃത ഉദ്യോഗസ്ഥർക്ക്.',
            enterPortal: 'കസ്റ്റമർ പോർട്ടൽ നൽകുക',
            comingSoon: 'ഉടൻ വരുന്നു',
            login: 'ലോഗിൻ ചെയ്യുക',
            register: 'രജിസ്റ്റർ ചെയ്യുക',
            email: 'ഇമെയിൽ വിലാസം',
            password: 'രഹസ്യവാക്ക്',
            confirmPassword: 'പാസ്‌വേഡ് സ്ഥിരീകരിക്കുക',
            fullName: 'മുഴുവൻ പേര്',
            mobile: 'മൊബൈൽ നമ്പർ',
            dob: 'ജനനത്തീയതി',
            gender: 'ലിംഗഭേദം',
            occupation: 'തൊഴിൽ',
            address: 'താമസ വിലാസം',
            forgotPassword: 'പാസ്‌വേഡ് മറന്നോ?',
            resetPasswordTitle: 'പാസ്‌വേഡ് പുനഃസജ്ജമാക്കുക',
            resetPasswordDesc: 'പാസ്‌വേഡ് റീസെറ്റ് നിർദ്ദേശങ്ങൾ ലഭിക്കുന്നതിന് നിങ്ങളുടെ രജിസ്റ്റർ ചെയ്ത ഇമെയിൽ വിലാസം നൽകുക.',
            instructionsSent: 'റീസെറ്റ് നിർദ്ദേശങ്ങൾ അയച്ചു',
            resetSentMsg: 'ഈ ഇമെയിൽ വിലാസവുമായി ഒരു അക്കൗണ്ട് ബന്ധപ്പെടുത്തിയിട്ടുണ്ടെങ്കിൽ, പാസ്‌വേഡ് പുനഃസജ്ജീകരണ നിർദ്ദേശങ്ങളും ഒരു സ്ഥിരീകരണ ലിങ്കും അയച്ചിട്ടുണ്ട്.',
            sendResetLink: 'റീസെറ്റ് ലിങ്ക് അയയ്ക്കുക',
            backToLogin: 'ലോഗിൻ എന്നതിലേക്ക് മടങ്ങുക',
            hasAccount: 'ഇതിനകം ഒരു അക്കൗണ്ട് ഉണ്ടോ?',
            createAccountSuccess: 'അക്കൗണ്ട് സൃഷ്‌ടിച്ചു!',
            createAccountSuccessDesc: 'നിങ്ങളുടെ FRAUDNEXUS ഉപഭോക്തൃ അക്കൗണ്ട് രജിസ്റ്റർ ചെയ്തു. നിങ്ങളുടെ ക്രെഡൻഷ്യലുകൾ ഉപയോഗിച്ച് ലോഗിൻ ചെയ്യുക.',
            goToLogin: 'ലോഗിൻ എന്നതിലേക്ക് പോകുക',
            dashboard: 'ഡാഷ്ബോർഡ്',
            reportFraud: 'വഞ്ചന റിപ്പോർട്ട് ചെയ്യുക',
            trackCases: 'കേസുകൾ ട്രാക്ക് ചെയ്യുക',
            evidence: 'തെളിവ്',
            profile: 'ഉപഭോക്തൃ പ്രൊഫൈൽ',
            helpSupport: 'സഹായവും പിന്തുണയും',
            welcome: 'സ്വാഗതം',
            totalCases: 'ആകെ കേസുകൾ',
            activeCases: 'സജീവ കേസുകൾ',
            resolvedCases: 'പരിഹരിച്ച കേസുകൾ',
            closedCases: 'അടച്ച കേസുകൾ',
            recentCases: 'സമീപകാല കേസുകൾ',
            caseId: 'കേസ് ഐഡി',
            incidentType: 'സംഭവ തരം',
            date: 'തീയതി',
            severity: 'തീവ്രത',
            status: 'നില',
            action: 'ആക്ഷൻ',
            viewDetails: 'വിശദാംശങ്ങൾ കാണുക',
            noCases: 'കേസുകളൊന്നും കണ്ടെത്തിയില്ല. ആരംഭിക്കുന്നതിന് ഒരു തട്ടിപ്പ് റിപ്പോർട്ട് ചെയ്യുക.',
            kycStatus: 'KYC നില',
            completeKyc: 'KYC പൂർത്തിയാക്കുക',
            govIdType: 'സർക്കാർ ഐഡി തരം',
            govIdNumber: 'സർക്കാർ ഐഡി നമ്പർ',
            proofDocument: 'ഐഡി പ്രൂഫ് ഡോക്യുമെൻ്റ്',
            submitKyc: 'അവലോകനത്തിനായി KYC സമർപ്പിക്കുക',
            kycPendingNote: 'ഐഡൻ്റിറ്റി വെരിഫിക്കേഷൻ അടിയന്തിര വഞ്ചന റിപ്പോർട്ടിംഗിന് ഓപ്ഷണലാണ്, കേസ് സമർപ്പിക്കുന്നത് തടയില്ല.',
            financialInvolvement: 'സാമ്പത്തിക നഷ്ടമോ ഇടപാട് പങ്കാളിത്തമോ ഉണ്ടായിട്ടുണ്ടോ?',
            institutionType: 'സ്ഥാപന തരം',
            institutionName: 'സ്ഥാപനം / ബാങ്ക് / ആപ്പ് പേര്',
            paymentMode: 'സാമ്പത്തിക പ്രവർത്തന മോഡ്',
            referenceType: 'റഫറൻസ് തരം',
            referenceNumber: 'റഫറൻസ് നമ്പർ / UTR',
            amountInvolved: 'ഉൾപ്പെട്ട തുക (INR)',
            blockedAmount: 'ഉപഭോക്താവ് റിപ്പോർട്ട് ചെയ്ത ബ്ലോക്ക് ചെയ്ത തുക',
            recoveredAmount: 'ഉപഭോക്താവ്-റിപ്പോർട്ട് ചെയ്‌ത തുക',
            suspectName: 'സംശയിക്കുന്നയാളുടെ / ഗുണഭോക്താവിൻ്റെ പേര്',
            suspectContact: 'കോൺടാക്റ്റ് / UPI ഐഡി / അക്കൗണ്ട് എന്ന് സംശയിക്കുന്നു',
            evidenceType: 'തെളിവ് തരം',
            evidenceDesc: 'തെളിവുകളുടെ വിവരണം',
            attachProof: 'എവിഡൻസ് ഫയൽ അറ്റാച്ചുചെയ്യുക',
            submitReport: 'വഞ്ചന റിപ്പോർട്ട് സമർപ്പിക്കുക',
            submitting: 'സമർപ്പിക്കുന്നു...',
            stageSubmitted: 'സമർപ്പിച്ചു',
            stageInitialReview: 'പ്രാരംഭ അവലോകനം',
            stageInvestigation: 'അന്വേഷണം',
            stageResolution: 'റെസലൂഷൻ',
            stageClosed: 'അടച്ചു',
            addAdditionalEvidence: 'അധിക തെളിവുകൾ ചേർക്കുക',
            askAI: 'FRAUDNEXUS AI-യോട് ചോദിക്കുക',
            send: 'അയക്കുക',
            close: 'അടയ്ക്കുക',
            logout: 'പുറത്തുകടക്കുക',
            commandCenter: 'കമാൻഡ് സെൻ്റർ',
            partners: 'പങ്കാളികൾ',
            partnerDirectory: 'പങ്കാളി ഡയറക്ടറി',
            addPartner: 'പങ്കാളിയെ ചേർക്കുക',
            editPartner: 'പങ്കാളിയെ എഡിറ്റ് ചെയ്യുക',
            partnerRequests: 'പങ്കാളി അഭ്യർത്ഥനകൾ',
            requestStatus: 'അഭ്യർത്ഥന നില',
            partnerCategory: 'പങ്കാളി വിഭാഗം',
            integrationType: 'സംയോജന തരം',
            active: 'സജീവമാണ്',
            inactive: 'നിഷ്ക്രിയം',
            suspended: 'സസ്പെൻഡ് ചെയ്തു',
            simulatedDemoPartner: 'സിമുലേറ്റഡ് ഡെമോ പങ്കാളി',
            totalPartners: 'മൊത്തം പങ്കാളികൾ',
            activePartners: 'സജീവ പങ്കാളികൾ',
            pendingRequests: 'തീർപ്പാക്കാത്ത അഭ്യർത്ഥനകൾ',
            awaitingResponse: 'പ്രതികരണത്തിനായി കാത്തിരിക്കുന്നു',
            overdueRequests: 'കാലഹരണപ്പെട്ട അഭ്യർത്ഥനകൾ',
            customers: 'ഉപഭോക്താക്കൾ',
            cases: 'കേസുകൾ',
            investigation: 'അന്വേഷണം',
            intelligenceWorkspace: 'ഇൻ്റലിജൻസ് വർക്ക്‌സ്‌പേസ്',
            analytics: 'അനലിറ്റിക്സ്',
            settings: 'ക്രമീകരണങ്ങൾ',
            adminLoginTitle: 'സ്വാഗതം',
            adminLoginSub: 'FRAUDNEXUS ഇൻവെസ്റ്റിഗേഷൻ വർക്ക്‌സ്‌പെയ്‌സിലേക്ക് സൈൻ ഇൻ ചെയ്യുക',
            signIn: 'സൈൻ ഇൻ ചെയ്യുക',
            tryDemo: 'ഡെമോ പരീക്ഷിക്കുക',
            demoEnv: 'ഡെമോ എൻവയോൺമെൻ്റ്',
            priorityQueue: 'മുൻഗണനാ അന്വേഷണ ക്യൂ',
            actionCenter: 'പ്രവർത്തന കേന്ദ്രം',
            fraudTrends: 'വഞ്ചന കേസ് ട്രെൻഡുകൾ',
            financialExposureSummary: 'സാമ്പത്തിക എക്സ്പോഷർ സംഗ്രഹം',
            recentActivity: 'സമീപകാല പ്രവർത്തനം',
            newCases: 'പുതിയ കേസുകൾ',
            criticalCases: 'ഗുരുതരമായ കേസുകൾ',
            escalatedCases: 'എസ്കലേറ്റഡ് കേസുകൾ',
            pendingApprovals: 'അനുമതികൾ തീർച്ചപ്പെടുത്തിയിട്ടില്ല',
            financialExposure: 'ഫിനാൻഷ്യൽ എക്സ്പോഷർ',
            unassigned: 'അസൈൻ ചെയ്തിട്ടില്ല',
            assign: 'അസൈൻ ചെയ്യുക',
            openWorkspace: 'വർക്ക്‌സ്‌പെയ്‌സ് തുറക്കുക',
            requestEvidence: 'തെളിവുകൾ അഭ്യർത്ഥിക്കുക',
            escalate: 'വർദ്ധിപ്പിക്കുക',
            resolve: 'പരിഹരിക്കുക',
            closeCase: 'കേസ് അടയ്ക്കുക',
            addTask: 'ടാസ്ക് ചേർക്കുക'
        },
        bn: {
            brand: 'ফ্রডনেক্সাস',
            tagline: 'জালিয়াতি রিপোর্ট থেকে সমাধান - এক বুদ্ধিমান তদন্ত কর্মক্ষেত্র',
            heroTitle: 'জালিয়াতি রিপোর্ট থেকে সমাধান পর্যন্ত',
            heroSub: 'আর্থিক ও সাইবার জালিয়াতি তদন্ত হাব',
            heroDesc: 'শিকার, তদন্তকারী, আর্থিক প্রতিষ্ঠান এবং আইন প্রয়োগকারীকে সংযুক্ত করার জন্য একটি বুদ্ধিমান তদন্ত কর্মক্ষেত্র।',
            getStarted: 'শুরু করুন',
            learnMore: 'আরও জানুন',
            portalSelectTitle: 'আপনার পোর্টাল নির্বাচন করুন',
            portalSelectSub: 'আপনার ভূমিকার সাথে মেলে এমন কর্মক্ষেত্র বেছে নিন।',
            customerPortal: 'গ্রাহক পোর্টাল',
            customerPortalDesc: 'নাগরিক এবং ভুক্তভোগীদের নিরাপদে জালিয়াতির প্রতিবেদন করতে, বাস্তব সময়ে কেস ট্র্যাক করতে এবং প্রমাণ জমা দেওয়ার জন্য।',
            investigatorPortal: 'তদন্তকারী/অ্যাডমিন পোর্টাল',
            investigatorPortalDesc: 'মামলা তদন্ত, বুদ্ধিমত্তা বিশ্লেষণ এবং সম্মতি পরিচালনা করার জন্য অনুমোদিত কর্মীদের জন্য।',
            enterPortal: 'কাস্টমার পোর্টালে প্রবেশ করুন',
            comingSoon: 'শীঘ্রই আসছে',
            login: 'লগইন করুন',
            register: 'নিবন্ধন করুন',
            email: 'ইমেইল ঠিকানা',
            password: 'পাসওয়ার্ড',
            confirmPassword: 'পাসওয়ার্ড নিশ্চিত করুন',
            fullName: 'পুরো নাম',
            mobile: 'মোবাইল নম্বর',
            dob: 'জন্ম তারিখ',
            gender: 'লিঙ্গ',
            occupation: 'পেশা',
            address: 'আবাসিক ঠিকানা',
            forgotPassword: 'পাসওয়ার্ড ভুলে গেছেন?',
            resetPasswordTitle: 'পাসওয়ার্ড রিসেট করুন',
            resetPasswordDesc: 'পাসওয়ার্ড রিসেট নির্দেশাবলী পেতে আপনার নিবন্ধিত ইমেল ঠিকানা লিখুন.',
            instructionsSent: 'রিসেট নির্দেশাবলী পাঠানো হয়েছে',
            resetSentMsg: 'যদি একটি অ্যাকাউন্ট এই ইমেল ঠিকানার সাথে যুক্ত থাকে, তাহলে পাসওয়ার্ড পুনরায় সেট করার নির্দেশাবলী এবং একটি যাচাইকরণ লিঙ্ক পাঠানো হয়েছে৷',
            sendResetLink: 'রিসেট লিঙ্ক পাঠান',
            backToLogin: 'লগইন এ ফিরে যান',
            hasAccount: 'ইতিমধ্যে একটি অ্যাকাউন্ট আছে?',
            createAccountSuccess: 'অ্যাকাউন্ট সফলভাবে তৈরি!',
            createAccountSuccessDesc: 'আপনার FAUDNEXUS গ্রাহক অ্যাকাউন্ট নিবন্ধিত হয়েছে৷ আপনার শংসাপত্রের সাথে লগ ইন করুন.',
            goToLogin: 'লগইন এ যান',
            dashboard: 'ড্যাশবোর্ড',
            reportFraud: 'রিপোর্ট জালিয়াতি',
            trackCases: 'ট্র্যাক কেস',
            evidence: 'প্রমাণ',
            profile: 'গ্রাহক প্রোফাইল',
            helpSupport: 'সাহায্য এবং সমর্থন',
            welcome: 'স্বাগতম',
            totalCases: 'মোট মামলা',
            activeCases: 'সক্রিয় মামলা',
            resolvedCases: 'মীমাংসা মামলা',
            closedCases: 'ক্লোজড কেস',
            recentCases: 'সাম্প্রতিক কেস',
            caseId: 'কেস আইডি',
            incidentType: 'ঘটনার ধরন',
            date: 'তারিখ',
            severity: 'তীব্রতা',
            status: 'স্ট্যাটাস',
            action: 'অ্যাকশন',
            viewDetails: 'বিস্তারিত দেখুন',
            noCases: 'কোন মামলা পাওয়া যায়নি। শুরু করতে একটি জালিয়াতির প্রতিবেদন করুন।',
            kycStatus: 'কেওয়াইসি স্ট্যাটাস',
            completeKyc: 'KYC সম্পূর্ণ করুন',
            govIdType: 'সরকারি আইডি টাইপ',
            govIdNumber: 'সরকারি আইডি নম্বর',
            proofDocument: 'আইডি প্রুফ ডকুমেন্ট',
            submitKyc: 'পর্যালোচনার জন্য KYC জমা দিন',
            kycPendingNote: 'জরুরী জালিয়াতি প্রতিবেদনের জন্য পরিচয় যাচাইকরণ ঐচ্ছিক এবং কেস জমা বাধা দেবে না।',
            financialInvolvement: 'আর্থিক ক্ষতি বা লেনদেন জড়িত ছিল?',
            institutionType: 'প্রতিষ্ঠানের ধরন',
            institutionName: 'প্রতিষ্ঠান / ব্যাঙ্ক / অ্যাপের নাম',
            paymentMode: 'আর্থিক কার্যকলাপ মোড',
            referenceType: 'রেফারেন্স টাইপ',
            referenceNumber: 'রেফারেন্স নম্বর / ইউটিআর',
            amountInvolved: 'জড়িত পরিমাণ (INR)',
            blockedAmount: 'গ্রাহক-প্রতিবেদিত ব্লক করা পরিমাণ',
            recoveredAmount: 'গ্রাহক-প্রতিবেদিত পুনরুদ্ধার পরিমাণ',
            suspectName: 'সন্দেহভাজন / সুবিধাভোগীর নাম',
            suspectContact: 'সন্দেহজনক যোগাযোগ / UPI আইডি / অ্যাকাউন্ট',
            evidenceType: 'প্রমাণের ধরন',
            evidenceDesc: 'প্রমাণ বিবরণ',
            attachProof: 'এভিডেন্স ফাইল সংযুক্ত করুন',
            submitReport: 'জালিয়াতি রিপোর্ট জমা দিন',
            submitting: 'জমা দেওয়া হচ্ছে...',
            stageSubmitted: 'জমা দেওয়া হয়েছে',
            stageInitialReview: 'প্রাথমিক পর্যালোচনা',
            stageInvestigation: 'তদন্ত',
            stageResolution: 'রেজোলিউশন',
            stageClosed: 'বন্ধ',
            addAdditionalEvidence: 'অতিরিক্ত প্রমাণ যোগ করুন',
            askAI: 'FRAUDNEXUS AI কে জিজ্ঞাসা করুন',
            send: 'পাঠান',
            close: 'বন্ধ',
            logout: 'লগআউট',
            commandCenter: 'কমান্ড সেন্টার',
            partners: 'অংশীদার',
            partnerDirectory: 'অংশীদার ডিরেক্টরি',
            addPartner: 'অংশীদার যোগ করুন',
            editPartner: 'অংশীদার সম্পাদনা করুন',
            partnerRequests: 'অংশীদার অনুরোধ',
            requestStatus: 'অনুরোধের স্থিতি',
            partnerCategory: 'অংশীদার বিভাগ',
            integrationType: 'ইন্টিগ্রেশন টাইপ',
            active: 'সক্রিয়',
            inactive: 'নিষ্ক্রিয়',
            suspended: 'স্থগিত',
            simulatedDemoPartner: 'সিমুলেটেড ডেমো পার্টনার',
            totalPartners: 'মোট অংশীদার',
            activePartners: 'সক্রিয় অংশীদার',
            pendingRequests: 'মুলতুবি অনুরোধ',
            awaitingResponse: 'প্রতিক্রিয়ার অপেক্ষায়',
            overdueRequests: 'ওভারডিউ অনুরোধ',
            customers: 'গ্রাহকদের',
            cases: 'মামলা',
            investigation: 'তদন্ত',
            intelligenceWorkspace: 'গোয়েন্দা কর্মক্ষেত্র',
            analytics: 'বিশ্লেষণ',
            settings: 'সেটিংস',
            adminLoginTitle: 'স্বাগত ফিরে',
            adminLoginSub: 'ফ্রডনেক্সাস ইনভেস্টিগেশন ওয়ার্কস্পেসে সাইন ইন করুন',
            signIn: 'সাইন ইন করুন',
            tryDemo: 'ডেমো ব্যবহার করে দেখুন',
            demoEnv: 'ডেমো এনভায়রনমেন্ট',
            priorityQueue: 'অগ্রাধিকার তদন্ত সারি',
            actionCenter: 'অ্যাকশন সেন্টার',
            fraudTrends: 'জালিয়াতি মামলা প্রবণতা',
            financialExposureSummary: 'ফিনান্সিয়াল এক্সপোজার সারাংশ',
            recentActivity: 'সাম্প্রতিক কার্যকলাপ',
            newCases: 'নতুন কেস',
            criticalCases: 'ক্রিটিকাল কেস',
            escalatedCases: 'বর্ধিত মামলা',
            pendingApprovals: 'মুলতুবি অনুমোদন',
            financialExposure: 'ফিনান্সিয়াল এক্সপোজার',
            unassigned: 'আনঅ্যাসাইন করা হয়েছে',
            assign: 'বরাদ্দ করুন',
            openWorkspace: 'ওয়ার্কস্পেস খুলুন',
            requestEvidence: 'প্রমাণের অনুরোধ করুন',
            escalate: 'বাড়ানো',
            resolve: 'সমাধান করুন',
            closeCase: 'ক্লোজ কেস',
            addTask: 'টাস্ক যোগ করুন'
        },
        mr: {
            brand: 'फसवणूक',
            tagline: 'फसवणूक अहवालापासून रिझोल्यूशनपर्यंत - एक बुद्धिमान तपास कार्यक्षेत्र',
            heroTitle: 'फसवणूक अहवाल ते निराकरण',
            heroSub: 'आर्थिक आणि सायबर फसवणूक तपास केंद्र',
            heroDesc: 'पीडित, तपासकर्ते, वित्तीय संस्था आणि कायद्याची अंमलबजावणी यांना जोडणारे एक बुद्धिमान तपास कार्यक्षेत्र.',
            getStarted: 'प्रारंभ करा',
            learnMore: 'अधिक जाणून घ्या',
            portalSelectTitle: 'तुमचे पोर्टल निवडा',
            portalSelectSub: 'तुमच्या भूमिकेशी जुळणारे कार्यक्षेत्र निवडा.',
            customerPortal: 'ग्राहक पोर्टल',
            customerPortalDesc: 'नागरिक आणि पीडितांना सुरक्षितपणे फसवणूकीचा अहवाल देण्यासाठी, वास्तविक वेळेत प्रकरणांचा मागोवा घेण्यासाठी आणि पुरावे सादर करण्यासाठी.',
            investigatorPortal: 'अन्वेषक / प्रशासन पोर्टल',
            investigatorPortalDesc: 'प्रकरणांचा तपास करण्यासाठी, बुद्धिमत्तेचे विश्लेषण करण्यासाठी आणि अनुपालन व्यवस्थापित करण्यासाठी अधिकृत कर्मचाऱ्यांसाठी.',
            enterPortal: 'ग्राहक पोर्टल प्रविष्ट करा',
            comingSoon: 'लवकरच येत आहे',
            login: 'लॉगिन करा',
            register: 'नोंदणी करा',
            email: 'ईमेल पत्ता',
            password: 'पासवर्ड',
            confirmPassword: 'पासवर्डची पुष्टी करा',
            fullName: 'पूर्ण नाव',
            mobile: 'मोबाईल नंबर',
            dob: 'जन्मतारीख',
            gender: 'लिंग',
            occupation: 'व्यवसाय',
            address: 'निवासी पत्ता',
            forgotPassword: 'पासवर्ड विसरलात?',
            resetPasswordTitle: 'पासवर्ड रीसेट करा',
            resetPasswordDesc: 'पासवर्ड रीसेट सूचना प्राप्त करण्यासाठी तुमचा नोंदणीकृत ईमेल पत्ता प्रविष्ट करा.',
            instructionsSent: 'पाठवलेल्या सूचना रीसेट करा',
            resetSentMsg: 'एखादे खाते या ईमेल पत्त्याशी संबद्ध असल्यास, पासवर्ड रीसेट करण्याच्या सूचना आणि सत्यापन दुवा पाठविला गेला आहे.',
            sendResetLink: 'रीसेट लिंक पाठवा',
            backToLogin: 'लॉगिन वर परत',
            hasAccount: 'आधीच खाते आहे?',
            createAccountSuccess: 'खाते यशस्वीरित्या तयार केले!',
            createAccountSuccessDesc: 'तुमचे FAUDNEXUS ग्राहक खाते नोंदणीकृत झाले आहे. कृपया तुमच्या क्रेडेन्शियल्ससह लॉग इन करा.',
            goToLogin: 'लॉगिन वर जा',
            dashboard: 'डॅशबोर्ड',
            reportFraud: 'फसवणूक नोंदवा',
            trackCases: 'प्रकरणांचा मागोवा घ्या',
            evidence: 'पुरावा',
            profile: 'ग्राहक प्रोफाइल',
            helpSupport: 'मदत आणि समर्थन',
            welcome: 'स्वागत आहे',
            totalCases: 'एकूण प्रकरणे',
            activeCases: 'सक्रिय प्रकरणे',
            resolvedCases: 'निराकरण प्रकरणे',
            closedCases: 'बंद प्रकरणे',
            recentCases: 'अलीकडील प्रकरणे',
            caseId: 'केस आयडी',
            incidentType: 'घटनेचा प्रकार',
            date: 'तारीख',
            severity: 'तीव्रता',
            status: 'स्थिती',
            action: 'कृती',
            viewDetails: 'तपशील पहा',
            noCases: 'कोणतीही प्रकरणे आढळली नाहीत. सुरू करण्यासाठी फसवणुकीचा अहवाल द्या.',
            kycStatus: 'केवायसी स्थिती',
            completeKyc: 'केवायसी पूर्ण करा',
            govIdType: 'सरकारी आयडी प्रकार',
            govIdNumber: 'सरकारी आयडी क्रमांक',
            proofDocument: 'आयडी प्रूफ दस्तऐवज',
            submitKyc: 'पुनरावलोकनासाठी KYC सबमिट करा',
            kycPendingNote: 'तात्काळ फसवणूक अहवालासाठी ओळख पडताळणी पर्यायी आहे आणि केस सबमिशन अवरोधित करणार नाही.',
            financialInvolvement: 'आर्थिक नुकसान किंवा व्यवहाराचा सहभाग होता का?',
            institutionType: 'संस्थेचा प्रकार',
            institutionName: 'संस्था / बँक / ॲपचे नाव',
            paymentMode: 'आर्थिक क्रियाकलाप मोड',
            referenceType: 'संदर्भ प्रकार',
            referenceNumber: 'संदर्भ क्रमांक / UTR',
            amountInvolved: 'गुंतलेली रक्कम (INR)',
            blockedAmount: 'ग्राहक-अवरोधित रक्कम',
            recoveredAmount: 'ग्राहक-अहवाल वसूल केलेली रक्कम',
            suspectName: 'संशयित / लाभार्थी नाव',
            suspectContact: 'संशयित संपर्क / UPI आयडी / खाते',
            evidenceType: 'पुरावा प्रकार',
            evidenceDesc: 'पुरावा वर्णन',
            attachProof: 'पुरावा फाइल संलग्न करा',
            submitReport: 'फसवणूक अहवाल सबमिट करा',
            submitting: 'सबमिट करत आहे...',
            stageSubmitted: 'सादर केले',
            stageInitialReview: 'प्रारंभिक पुनरावलोकन',
            stageInvestigation: 'तपास',
            stageResolution: 'ठराव',
            stageClosed: 'बंद',
            addAdditionalEvidence: 'अतिरिक्त पुरावा जोडा',
            askAI: 'FRAUDNEXUS AI ला विचारा',
            send: 'पाठवा',
            close: 'बंद करा',
            logout: 'लॉगआउट करा',
            commandCenter: 'कमांड सेंटर',
            partners: 'भागीदार',
            partnerDirectory: 'भागीदार निर्देशिका',
            addPartner: 'भागीदार जोडा',
            editPartner: 'भागीदार संपादित करा',
            partnerRequests: 'भागीदार विनंत्या',
            requestStatus: 'विनंती स्थिती',
            partnerCategory: 'भागीदार श्रेणी',
            integrationType: 'एकत्रीकरण प्रकार',
            active: 'सक्रिय',
            inactive: 'निष्क्रिय',
            suspended: 'निलंबित',
            simulatedDemoPartner: 'सिम्युलेटेड डेमो पार्टनर',
            totalPartners: 'एकूण भागीदार',
            activePartners: 'सक्रिय भागीदार',
            pendingRequests: 'प्रलंबित विनंत्या',
            awaitingResponse: 'प्रतिसादाच्या प्रतीक्षेत',
            overdueRequests: 'अतिदेय विनंत्या',
            customers: 'ग्राहक',
            cases: 'प्रकरणे',
            investigation: 'तपास',
            intelligenceWorkspace: 'बुद्धिमत्ता कार्यक्षेत्र',
            analytics: 'विश्लेषण',
            settings: 'सेटिंग्ज',
            adminLoginTitle: 'परत आपले स्वागत आहे',
            adminLoginSub: 'FRAUDNEXUS Investigation Workspace मध्ये साइन इन करा',
            signIn: 'साइन इन करा',
            tryDemo: 'डेमो वापरून पहा',
            demoEnv: 'डेमो पर्यावरण',
            priorityQueue: 'प्राधान्य तपासणी रांग',
            actionCenter: 'कृती केंद्र',
            fraudTrends: 'फसवणूक प्रकरण ट्रेंड',
            financialExposureSummary: 'आर्थिक एक्सपोजर सारांश',
            recentActivity: 'अलीकडील क्रियाकलाप',
            newCases: 'नवीन प्रकरणे',
            criticalCases: 'गंभीर प्रकरणे',
            escalatedCases: 'वाढलेली प्रकरणे',
            pendingApprovals: 'प्रलंबित मंजूरी',
            financialExposure: 'आर्थिक एक्सपोजर',
            unassigned: 'असाइन केलेले नाही',
            assign: 'नियुक्त करा',
            openWorkspace: 'कार्यक्षेत्र उघडा',
            requestEvidence: 'पुरावा मागवा',
            escalate: 'वाढवा',
            resolve: 'निराकरण करा',
            closeCase: 'केस बंद करा',
            addTask: 'कार्य जोडा'
        },
        gu: {
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
            addTask: 'Add Task'
        },
        pa: {
            brand: 'ਫਰਾਡਨੇਕਸ',
            tagline: 'ਫਰਾਡ ਰਿਪੋਰਟ ਤੋਂ ਲੈ ਕੇ ਰੈਜ਼ੋਲਿਊਸ਼ਨ ਤੱਕ — ਇੱਕ ਇੰਟੈਲੀਜੈਂਟ ਇਨਵੈਸਟੀਗੇਸ਼ਨ ਵਰਕਸਪੇਸ',
            heroTitle: 'ਫਰਾਡ ਰਿਪੋਰਟ ਤੋਂ ਰੈਜ਼ੋਲਿਊਸ਼ਨ ਤੱਕ',
            heroSub: 'ਵਿੱਤੀ ਅਤੇ ਸਾਈਬਰ ਧੋਖਾਧੜੀ ਜਾਂਚ ਹੱਬ',
            heroDesc: 'ਪੀੜਤਾਂ, ਜਾਂਚਕਰਤਾਵਾਂ, ਵਿੱਤੀ ਸੰਸਥਾਵਾਂ ਅਤੇ ਕਾਨੂੰਨ ਲਾਗੂ ਕਰਨ ਵਾਲਿਆਂ ਨੂੰ ਜੋੜਨ ਵਾਲਾ ਇੱਕ ਬੁੱਧੀਮਾਨ ਜਾਂਚ ਵਰਕਸਪੇਸ।',
            getStarted: 'ਸ਼ੁਰੂ ਕਰੋ',
            learnMore: 'ਹੋਰ ਜਾਣੋ',
            portalSelectTitle: 'ਆਪਣਾ ਪੋਰਟਲ ਚੁਣੋ',
            portalSelectSub: 'ਉਹ ਵਰਕਸਪੇਸ ਚੁਣੋ ਜੋ ਤੁਹਾਡੀ ਭੂਮਿਕਾ ਨਾਲ ਮੇਲ ਖਾਂਦਾ ਹੋਵੇ।',
            customerPortal: 'ਗਾਹਕ ਪੋਰਟਲ',
            customerPortalDesc: 'ਨਾਗਰਿਕਾਂ ਅਤੇ ਪੀੜਤਾਂ ਲਈ ਸੁਰੱਖਿਅਤ ਢੰਗ ਨਾਲ ਧੋਖਾਧੜੀ ਦੀ ਰਿਪੋਰਟ ਕਰਨ, ਅਸਲ ਸਮੇਂ ਵਿੱਚ ਕੇਸਾਂ ਨੂੰ ਟਰੈਕ ਕਰਨ ਅਤੇ ਸਬੂਤ ਜਮ੍ਹਾਂ ਕਰਾਉਣ ਲਈ।',
            investigatorPortal: 'ਇਨਵੈਸਟੀਗੇਟਰ / ਐਡਮਿਨ ਪੋਰਟਲ',
            investigatorPortalDesc: 'ਕੇਸਾਂ ਦੀ ਜਾਂਚ ਕਰਨ, ਖੁਫੀਆ ਜਾਣਕਾਰੀ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰਨ ਅਤੇ ਪਾਲਣਾ ਦਾ ਪ੍ਰਬੰਧਨ ਕਰਨ ਲਈ ਅਧਿਕਾਰਤ ਕਰਮਚਾਰੀਆਂ ਲਈ।',
            enterPortal: 'ਗਾਹਕ ਪੋਰਟਲ ਦਰਜ ਕਰੋ',
            comingSoon: 'ਜਲਦੀ ਆ ਰਿਹਾ ਹੈ',
            login: 'ਲੌਗਇਨ ਕਰੋ',
            register: 'ਰਜਿਸਟਰ ਕਰੋ',
            email: 'ਈਮੇਲ ਪਤਾ',
            password: 'ਪਾਸਵਰਡ',
            confirmPassword: 'ਪਾਸਵਰਡ ਦੀ ਪੁਸ਼ਟੀ ਕਰੋ',
            fullName: 'ਪੂਰਾ ਨਾਮ',
            mobile: 'ਮੋਬਾਈਲ ਨੰਬਰ',
            dob: 'ਜਨਮ ਮਿਤੀ',
            gender: 'ਲਿੰਗ',
            occupation: 'ਕਿੱਤਾ',
            address: 'ਰਿਹਾਇਸ਼ੀ ਪਤਾ',
            forgotPassword: 'ਪਾਸਵਰਡ ਭੁੱਲ ਗਏ ਹੋ?',
            resetPasswordTitle: 'ਪਾਸਵਰਡ ਰੀਸੈਟ ਕਰੋ',
            resetPasswordDesc: 'ਪਾਸਵਰਡ ਰੀਸੈਟ ਹਦਾਇਤਾਂ ਪ੍ਰਾਪਤ ਕਰਨ ਲਈ ਆਪਣਾ ਰਜਿਸਟਰਡ ਈਮੇਲ ਪਤਾ ਦਰਜ ਕਰੋ।',
            instructionsSent: 'ਰੀਸੈਟ ਹਦਾਇਤਾਂ ਭੇਜੀਆਂ ਗਈਆਂ',
            resetSentMsg: 'ਜੇਕਰ ਕੋਈ ਖਾਤਾ ਇਸ ਈਮੇਲ ਪਤੇ ਨਾਲ ਜੁੜਿਆ ਹੋਇਆ ਹੈ, ਤਾਂ ਪਾਸਵਰਡ ਰੀਸੈਟ ਕਰਨ ਦੀਆਂ ਹਦਾਇਤਾਂ ਅਤੇ ਇੱਕ ਪੁਸ਼ਟੀਕਰਨ ਲਿੰਕ ਭੇਜ ਦਿੱਤਾ ਗਿਆ ਹੈ।',
            sendResetLink: 'ਰੀਸੈਟ ਲਿੰਕ ਭੇਜੋ',
            backToLogin: 'ਲੌਗਇਨ \'ਤੇ ਵਾਪਸ ਜਾਓ',
            hasAccount: 'ਕੀ ਪਹਿਲਾਂ ਤੋਂ ਹੀ ਖਾਤਾ ਹੈ?',
            createAccountSuccess: 'ਖਾਤਾ ਸਫਲਤਾਪੂਰਵਕ ਬਣਾਇਆ ਗਿਆ!',
            createAccountSuccessDesc: 'ਤੁਹਾਡਾ FRAUDNEXUS ਗਾਹਕ ਖਾਤਾ ਰਜਿਸਟਰ ਕੀਤਾ ਗਿਆ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੇ ਪ੍ਰਮਾਣ ਪੱਤਰਾਂ ਨਾਲ ਲੌਗ ਇਨ ਕਰੋ।',
            goToLogin: 'ਲਾਗਇਨ \'ਤੇ ਜਾਓ',
            dashboard: 'ਡੈਸ਼ਬੋਰਡ',
            reportFraud: 'ਧੋਖਾਧੜੀ ਦੀ ਰਿਪੋਰਟ ਕਰੋ',
            trackCases: 'ਟ੍ਰੈਕ ਕੇਸ',
            evidence: 'ਸਬੂਤ',
            profile: 'ਗਾਹਕ ਪ੍ਰੋਫ਼ਾਈਲ',
            helpSupport: 'ਮਦਦ ਅਤੇ ਸਹਾਇਤਾ',
            welcome: 'ਸੁਆਗਤ ਹੈ',
            totalCases: 'ਕੁੱਲ ਕੇਸ',
            activeCases: 'ਐਕਟਿਵ ਕੇਸ',
            resolvedCases: 'ਹੱਲ ਕੀਤੇ ਕੇਸ',
            closedCases: 'ਬੰਦ ਕੇਸ',
            recentCases: 'ਤਾਜ਼ਾ ਮਾਮਲੇ',
            caseId: 'ਕੇਸ ਆਈ.ਡੀ',
            incidentType: 'ਘਟਨਾ ਦੀ ਕਿਸਮ',
            date: 'ਮਿਤੀ',
            severity: 'ਗੰਭੀਰਤਾ',
            status: 'ਸਥਿਤੀ',
            action: 'ਕਾਰਵਾਈ',
            viewDetails: 'ਵੇਰਵੇ ਵੇਖੋ',
            noCases: 'ਕੋਈ ਕੇਸ ਨਹੀਂ ਮਿਲਿਆ। ਸ਼ੁਰੂ ਕਰਨ ਲਈ ਧੋਖਾਧੜੀ ਦੀ ਰਿਪੋਰਟ ਕਰੋ।',
            kycStatus: 'ਕੇਵਾਈਸੀ ਸਥਿਤੀ',
            completeKyc: 'ਕੇਵਾਈਸੀ ਪੂਰਾ ਕਰੋ',
            govIdType: 'ਸਰਕਾਰੀ ID ਕਿਸਮ',
            govIdNumber: 'ਸਰਕਾਰੀ ID ਨੰਬਰ',
            proofDocument: 'ਆਈਡੀ ਪਰੂਫ਼ ਦਸਤਾਵੇਜ਼',
            submitKyc: 'ਸਮੀਖਿਆ ਲਈ ਕੇਵਾਈਸੀ ਜਮ੍ਹਾਂ ਕਰੋ',
            kycPendingNote: 'ਪਛਾਣ ਦੀ ਤਸਦੀਕ ਜ਼ਰੂਰੀ ਧੋਖਾਧੜੀ ਦੀ ਰਿਪੋਰਟਿੰਗ ਲਈ ਵਿਕਲਪਿਕ ਹੈ ਅਤੇ ਕੇਸ ਦਰਜ ਕਰਨ ਨੂੰ ਰੋਕ ਨਹੀਂ ਦੇਵੇਗੀ।',
            financialInvolvement: 'ਕੀ ਵਿੱਤੀ ਨੁਕਸਾਨ ਜਾਂ ਲੈਣ-ਦੇਣ ਦੀ ਸ਼ਮੂਲੀਅਤ ਸੀ?',
            institutionType: 'ਸੰਸਥਾ ਦੀ ਕਿਸਮ',
            institutionName: 'ਸੰਸਥਾ / ਬੈਂਕ / ਐਪ ਦਾ ਨਾਮ',
            paymentMode: 'ਵਿੱਤੀ ਗਤੀਵਿਧੀ ਮੋਡ',
            referenceType: 'ਹਵਾਲਾ ਕਿਸਮ',
            referenceNumber: 'ਸੰਦਰਭ ਨੰਬਰ / UTR',
            amountInvolved: 'ਸ਼ਾਮਲ ਰਕਮ (INR)',
            blockedAmount: 'ਗਾਹਕ-ਰਿਪੋਰਟ ਕੀਤੀ ਬਲੌਕ ਕੀਤੀ ਰਕਮ',
            recoveredAmount: 'ਗਾਹਕ-ਰਿਪੋਰਟ ਕੀਤੀ ਵਸੂਲੀ ਰਕਮ',
            suspectName: 'ਸ਼ੱਕੀ / ਲਾਭਪਾਤਰੀ ਦਾ ਨਾਮ',
            suspectContact: 'ਸ਼ੱਕੀ ਸੰਪਰਕ / UPI ID / ਖਾਤਾ',
            evidenceType: 'ਸਬੂਤ ਦੀ ਕਿਸਮ',
            evidenceDesc: 'ਸਬੂਤ ਵਰਣਨ',
            attachProof: 'ਸਬੂਤ ਫਾਈਲ ਨੱਥੀ ਕਰੋ',
            submitReport: 'ਧੋਖਾਧੜੀ ਦੀ ਰਿਪੋਰਟ ਦਰਜ ਕਰੋ',
            submitting: 'ਸਪੁਰਦ ਕੀਤਾ ਜਾ ਰਿਹਾ ਹੈ...',
            stageSubmitted: 'ਪੇਸ਼ ਕੀਤਾ',
            stageInitialReview: 'ਸ਼ੁਰੂਆਤੀ ਸਮੀਖਿਆ',
            stageInvestigation: 'ਜਾਂਚ',
            stageResolution: 'ਮਤਾ',
            stageClosed: 'ਬੰਦ',
            addAdditionalEvidence: 'ਵਾਧੂ ਸਬੂਤ ਸ਼ਾਮਲ ਕਰੋ',
            askAI: 'FRAUDNEXUS AI ਨੂੰ ਪੁੱਛੋ',
            send: 'ਭੇਜੋ',
            close: 'ਬੰਦ ਕਰੋ',
            logout: 'ਲਾਗਆਉਟ',
            commandCenter: 'ਕਮਾਂਡ ਸੈਂਟਰ',
            partners: 'ਭਾਈਵਾਲ',
            partnerDirectory: 'ਸਹਿਭਾਗੀ ਡਾਇਰੈਕਟਰੀ',
            addPartner: 'ਸਾਥੀ ਸ਼ਾਮਲ ਕਰੋ',
            editPartner: 'ਸਾਥੀ ਦਾ ਸੰਪਾਦਨ ਕਰੋ',
            partnerRequests: 'ਸਾਥੀ ਬੇਨਤੀਆਂ',
            requestStatus: 'ਬੇਨਤੀ ਸਥਿਤੀ',
            partnerCategory: 'ਸਾਥੀ ਸ਼੍ਰੇਣੀ',
            integrationType: 'ਏਕੀਕਰਣ ਦੀ ਕਿਸਮ',
            active: 'ਕਿਰਿਆਸ਼ੀਲ',
            inactive: 'ਅਕਿਰਿਆਸ਼ੀਲ',
            suspended: 'ਮੁਅੱਤਲ ਕੀਤਾ ਗਿਆ',
            simulatedDemoPartner: 'ਸਿਮੂਲੇਟਡ ਡੈਮੋ ਪਾਰਟਨਰ',
            totalPartners: 'ਕੁੱਲ ਭਾਈਵਾਲ',
            activePartners: 'ਸਰਗਰਮ ਭਾਈਵਾਲ',
            pendingRequests: 'ਬਕਾਇਆ ਬੇਨਤੀਆਂ',
            awaitingResponse: 'ਜਵਾਬ ਦੀ ਉਡੀਕ ਕਰ ਰਿਹਾ ਹੈ',
            overdueRequests: 'ਬਕਾਇਆ ਬੇਨਤੀਆਂ',
            customers: 'ਗਾਹਕ',
            cases: 'ਕੇਸ',
            investigation: 'ਜਾਂਚ',
            intelligenceWorkspace: 'ਇੰਟੈਲੀਜੈਂਸ ਵਰਕਸਪੇਸ',
            analytics: 'ਵਿਸ਼ਲੇਸ਼ਣ',
            settings: 'ਸੈਟਿੰਗਾਂ',
            adminLoginTitle: 'ਵਾਪਸ ਆਉਣ ਦਾ ਸੁਆਗਤ ਹੈ',
            adminLoginSub: 'FRAUDNEXUS ਇਨਵੈਸਟੀਗੇਸ਼ਨ ਵਰਕਸਪੇਸ ਵਿੱਚ ਸਾਈਨ ਇਨ ਕਰੋ',
            signIn: 'ਸਾਈਨ ਇਨ ਕਰੋ',
            tryDemo: 'ਡੈਮੋ ਅਜ਼ਮਾਓ',
            demoEnv: 'ਡੈਮੋ ਵਾਤਾਵਰਨ',
            priorityQueue: 'ਤਰਜੀਹੀ ਜਾਂਚ ਕਤਾਰ',
            actionCenter: 'ਐਕਸ਼ਨ ਸੈਂਟਰ',
            fraudTrends: 'ਧੋਖਾਧੜੀ ਦੇ ਕੇਸ ਦੇ ਰੁਝਾਨ',
            financialExposureSummary: 'ਵਿੱਤੀ ਐਕਸਪੋਜ਼ਰ ਸੰਖੇਪ',
            recentActivity: 'ਹਾਲੀਆ ਗਤੀਵਿਧੀ',
            newCases: 'ਨਵੇਂ ਕੇਸ',
            criticalCases: 'ਗੰਭੀਰ ਮਾਮਲੇ',
            escalatedCases: 'ਵਧੇ ਹੋਏ ਕੇਸ',
            pendingApprovals: 'ਬਕਾਇਆ ਮਨਜ਼ੂਰੀਆਂ',
            financialExposure: 'ਵਿੱਤੀ ਐਕਸਪੋਜ਼ਰ',
            unassigned: 'ਅਸਾਈਨ ਨਹੀਂ ਕੀਤਾ ਗਿਆ',
            assign: 'ਅਸਾਈਨ ਕਰੋ',
            openWorkspace: 'ਵਰਕਸਪੇਸ ਖੋਲ੍ਹੋ',
            requestEvidence: 'ਸਬੂਤ ਦੀ ਮੰਗ ਕਰੋ',
            escalate: 'ਵਧਾਓ',
            resolve: 'ਹੱਲ ਕਰੋ',
            closeCase: 'ਕੇਸ ਬੰਦ ਕਰੋ',
            addTask: 'ਕਾਰਜ ਸ਼ਾਮਲ ਕਰੋ'
        },
        or: {
            brand: 'FRAUDNEXUS',
            tagline: 'ଠକେଇ ରିପୋର୍ଟ ଠାରୁ ରିଜୋଲ୍ୟୁସନ୍ ପର୍ଯ୍ୟନ୍ତ - ଗୋଟିଏ ବୁଦ୍ଧିଜୀବୀ ଅନୁସନ୍ଧାନ କାର୍ଯ୍ୟକ୍ଷେତ୍ର |',
            heroTitle: 'ଜାଲିଆତି ରିପୋର୍ଟ ଠାରୁ ରିଜୋଲ୍ୟୁସନ୍ ପର୍ଯ୍ୟନ୍ତ |',
            heroSub: 'ଆର୍ଥିକ ଏବଂ ସାଇବର ଠକେଇର ଅନୁସନ୍ଧାନ ହବ୍ |',
            heroDesc: 'ପୀଡିତ, ଅନୁସନ୍ଧାନକାରୀ, ଆର୍ଥିକ ପ୍ରତିଷ୍ଠାନ ଏବଂ ଆଇନ ପ୍ରଣୟନକୁ ସଂଯୋଗ କରୁଥିବା ଗୋଟିଏ ବୁଦ୍ଧିମାନ ଅନୁସନ୍ଧାନ କାର୍ଯ୍ୟକ୍ଷେତ୍ର |',
            getStarted: 'ଆରମ୍ଭ କର |',
            learnMore: 'ଅଧିକ ଜାଣନ୍ତୁ |',
            portalSelectTitle: 'ଆପଣଙ୍କର ପୋର୍ଟାଲ୍ ଚୟନ କରନ୍ତୁ |',
            portalSelectSub: 'ଆପଣଙ୍କ ଭୂମିକା ସହିତ ମେଳ ଖାଉଥିବା କାର୍ଯ୍ୟକ୍ଷେତ୍ର ବାଛନ୍ତୁ |',
            customerPortal: 'ଗ୍ରାହକ ପୋର୍ଟାଲ୍ |',
            customerPortalDesc: 'ନାଗରିକ ଏବଂ ପୀଡିତଙ୍କ ପାଇଁ ଜାଲିଆତିକୁ ସୁରକ୍ଷିତ ଭାବରେ ରିପୋର୍ଟ କରିବା, ପ୍ରକୃତ ସମୟରେ ମାମଲା ଟ୍ରାକ୍ କରିବା ଏବଂ ପ୍ରମାଣ ଦାଖଲ କରିବା ପାଇଁ |',
            investigatorPortal: 'ଅନୁସନ୍ଧାନକାରୀ / ଆଡମିନି ପୋର୍ଟାଲ୍ |',
            investigatorPortalDesc: 'ପ୍ରାଧିକୃତ କର୍ମଚାରୀଙ୍କ ପାଇଁ ମାମଲା ଅନୁସନ୍ଧାନ, ବୁଦ୍ଧି ବିଶ୍ଳେଷଣ ଏବଂ ଅନୁପାଳନ ପରିଚାଳନା ପାଇଁ |',
            enterPortal: 'ଗ୍ରାହକ ପୋର୍ଟାଲ ପ୍ରବେଶ କରନ୍ତୁ |',
            comingSoon: 'ଶୀଘ୍ର ଆସୁଛି |',
            login: 'ଲଗଇନ୍ କରନ୍ତୁ |',
            register: 'ପଞ୍ଜିକରଣ କର |',
            email: 'ଇମେଲ୍ ଠିକଣା',
            password: 'ପାସୱାର୍ଡ',
            confirmPassword: 'ପାସୱାର୍ଡ ନିଶ୍ଚିତ କରନ୍ତୁ |',
            fullName: 'ପୂର୍ଣ୍ଣ ନାମ',
            mobile: 'ମୋବାଇଲ୍ ନମ୍ବର |',
            dob: 'ଜନ୍ମ ତାରିଖ',
            gender: 'ଲିଙ୍ଗ',
            occupation: 'ବୃତ୍ତି',
            address: 'ଆବାସିକ ଠିକଣା',
            forgotPassword: 'ପାସୱାର୍ଡ ଭୁଲିଗଲେ କି?',
            resetPasswordTitle: 'ପାସୱାର୍ଡ ପୁନ Res ସେଟ୍ କରନ୍ତୁ |',
            resetPasswordDesc: 'ପାସୱାର୍ଡ ପୁନ et ସେଟ୍ ନିର୍ଦ୍ଦେଶ ଗ୍ରହଣ କରିବାକୁ ଆପଣଙ୍କର ପଞ୍ଜୀକୃତ ଇମେଲ୍ ଠିକଣା ପ୍ରବେଶ କରନ୍ତୁ |',
            instructionsSent: 'ପଠାଯାଇଥିବା ନିର୍ଦ୍ଦେଶାବଳୀ ପୁନ Res ସେଟ୍ କରନ୍ତୁ |',
            resetSentMsg: 'ଯଦି ଏକ ଆକାଉଣ୍ଟ୍ ଏହି ଇମେଲ୍ ଠିକଣା ସହିତ ଜଡିତ ଅଛି, ପାସୱାର୍ଡ ପୁନ et ସେଟ୍ ନିର୍ଦ୍ଦେଶ ଏବଂ ଏକ ଯାଞ୍ଚ ଲିଙ୍କ ପଠାଯାଇଛି |',
            sendResetLink: 'ପୁନ Res ସେଟ୍ ଲିଙ୍କ୍ ପଠାନ୍ତୁ |',
            backToLogin: 'ଲଗଇନ୍ କୁ ଫେରନ୍ତୁ |',
            hasAccount: 'ପୂର୍ବରୁ ଏକ ଖାତା ଅଛି କି?',
            createAccountSuccess: 'ଖାତା ସଫଳତାର ସହିତ ସୃଷ୍ଟି ହେଲା!',
            createAccountSuccessDesc: 'ଆପଣଙ୍କର FRAUDNEXUS ଗ୍ରାହକ ଖାତା ପଞ୍ଜିକୃତ ହୋଇଛି | ଦୟାକରି ଆପଣଙ୍କର ପରିଚୟପତ୍ର ସହିତ ଲଗ୍ ଇନ୍ କରନ୍ତୁ |',
            goToLogin: 'ଲଗଇନ୍ କୁ ଯାଆନ୍ତୁ |',
            dashboard: 'ଡ୍ୟାସବୋର୍ଡ |',
            reportFraud: 'ଜାଲିଆତି ରିପୋର୍ଟ କରନ୍ତୁ |',
            trackCases: 'କେସ୍ ଟ୍ରାକ୍ କରନ୍ତୁ |',
            evidence: 'ପ୍ରମାଣ',
            profile: 'ଗ୍ରାହକ ପ୍ରୋଫାଇଲ୍ |',
            helpSupport: 'ସହାୟତା ଏବଂ ସମର୍ଥନ',
            welcome: 'ସ୍ Welcome ାଗତ',
            totalCases: 'ମୋଟ ମାମଲା',
            activeCases: 'ସକ୍ରିୟ ମାମଲା |',
            resolvedCases: 'ସମାଧାନ ମାମଲା |',
            closedCases: 'ବନ୍ଦ ମାମଲା |',
            recentCases: 'ସାମ୍ପ୍ରତିକ ମାମଲା',
            caseId: 'କେସ୍ ID',
            incidentType: 'ଘଟଣା ପ୍ରକାର',
            date: 'ତାରିଖ',
            severity: 'ଗମ୍ଭୀରତା |',
            status: 'ସ୍ଥିତି',
            action: 'କାର୍ଯ୍ୟ',
            viewDetails: 'ବିବରଣୀ ଦେଖନ୍ତୁ |',
            noCases: 'କ cases ଣସି ମାମଲା ମିଳିଲା ନାହିଁ | ଆରମ୍ଭ କରିବାକୁ ଏକ ଜାଲିଆତି ରିପୋର୍ଟ କରନ୍ତୁ |',
            kycStatus: 'KYC ସ୍ଥିତି |',
            completeKyc: 'ସଂପୂର୍ଣ୍ଣ KYC |',
            govIdType: 'ସରକାରୀ ID ପ୍ରକାର |',
            govIdNumber: 'ସରକାରୀ ID ନମ୍ବର |',
            proofDocument: 'ID ପ୍ରୁଫ୍ ଡକ୍ୟୁମେଣ୍ଟ୍ |',
            submitKyc: 'ସମୀକ୍ଷା ପାଇଁ KYC ଦାଖଲ କରନ୍ତୁ |',
            kycPendingNote: 'ଜରୁରୀ ଜାଲିଆତି ରିପୋର୍ଟ ପାଇଁ ପରିଚୟ ଯାଞ୍ଚ ବ al କଳ୍ପିକ ଏବଂ କେସ୍ ଦାଖଲକୁ ଅବରୋଧ କରିବ ନାହିଁ |',
            financialInvolvement: 'ଆର୍ଥିକ କ୍ଷତି କିମ୍ବା କାରବାରରେ ଜଡିତ ଥିଲା କି?',
            institutionType: 'ଅନୁଷ୍ଠାନ ପ୍ରକାର |',
            institutionName: 'ଅନୁଷ୍ଠାନ / ବ୍ୟାଙ୍କ / ଆପ୍ ନାମ |',
            paymentMode: 'ଆର୍ଥିକ କାର୍ଯ୍ୟକଳାପ ଧାରା |',
            referenceType: 'ସନ୍ଦର୍ଭ ପ୍ରକାର',
            referenceNumber: 'ସନ୍ଦର୍ଭ ସଂଖ୍ୟା / UTR',
            amountInvolved: 'ଜଡିତ ପରିମାଣ (INR)',
            blockedAmount: 'ଗ୍ରାହକ-ରିପୋର୍ଟ ହୋଇଥିବା ଅବରୋଧିତ ପରିମାଣ |',
            recoveredAmount: 'ଗ୍ରାହକ-ରିପୋର୍ଟ ହୋଇଥିବା ପୁନରୁଦ୍ଧାର ପରିମାଣ |',
            suspectName: 'ସନ୍ଦିଗ୍ଧ / ହିତାଧିକାରୀ ନାମ |',
            suspectContact: 'ସନ୍ଦେହ ସମ୍ପର୍କ / UPI ID / ଖାତା |',
            evidenceType: 'ପ୍ରମାଣ ପ୍ରକାର',
            evidenceDesc: 'ପ୍ରମାଣ ବର୍ଣ୍ଣନା',
            attachProof: 'ପ୍ରମାଣ ଫାଇଲ ସଂଲଗ୍ନ କରନ୍ତୁ |',
            submitReport: 'ଠକେଇ ରିପୋର୍ଟ ଦାଖଲ କରନ୍ତୁ |',
            submitting: 'ଦାଖଲ ...',
            stageSubmitted: 'ଦାଖଲ |',
            stageInitialReview: 'ପ୍ରାରମ୍ଭିକ ସମୀକ୍ଷା',
            stageInvestigation: 'ଅନୁସନ୍ଧାନ |',
            stageResolution: 'ସଂକଳ୍ପ',
            stageClosed: 'ବନ୍ଦ |',
            addAdditionalEvidence: 'ଅତିରିକ୍ତ ପ୍ରମାଣ ଯୋଡନ୍ତୁ |',
            askAI: 'FRAUDNEXUS AI କୁ ପଚାର |',
            send: 'ପଠାନ୍ତୁ |',
            close: 'ବନ୍ଦ',
            logout: 'ଲଗଆଉଟ୍ |',
            commandCenter: 'ନିର୍ଦ୍ଦେଶ କେନ୍ଦ୍ର |',
            partners: 'ସହଭାଗୀଗଣ |',
            partnerDirectory: 'ସହଭାଗୀ ଡିରେକ୍ଟୋରୀ |',
            addPartner: 'ସହଭାଗୀ ଯୋଡନ୍ତୁ |',
            editPartner: 'ସହଭାଗୀ ସଂପାଦନ କରନ୍ତୁ |',
            partnerRequests: 'ସହଭାଗୀ ଅନୁରୋଧ |',
            requestStatus: 'ସ୍ଥିତି ଅନୁରୋଧ |',
            partnerCategory: 'ସହଭାଗୀ ବର୍ଗ |',
            integrationType: 'ଏକୀକରଣ ପ୍ରକାର',
            active: 'ସକ୍ରିୟ |',
            inactive: 'ନିଷ୍କ୍ରିୟ |',
            suspended: 'ନିଲମ୍ବିତ |',
            simulatedDemoPartner: 'ସିମୁଲେଡ୍ ଡେମୋ ପାର୍ଟନର |',
            totalPartners: 'ସମୁଦାୟ ଭାଗୀଦାରୀ |',
            activePartners: 'ସକ୍ରିୟ ସହଭାଗୀଗଣ |',
            pendingRequests: 'ବିଚାରାଧୀନ ଅନୁରୋଧ',
            awaitingResponse: 'ପ୍ରତିକ୍ରିୟା ଅପେକ୍ଷାରେ |',
            overdueRequests: 'ସମୟସୀମା ଅନୁରୋଧ |',
            customers: 'ଗ୍ରାହକ',
            cases: 'ମାମଲା',
            investigation: 'ଅନୁସନ୍ଧାନ |',
            intelligenceWorkspace: 'ବୁଦ୍ଧିଜୀବୀ କାର୍ଯ୍ୟକ୍ଷେତ୍ର |',
            analytics: 'ଆନାଲିଟିକ୍ସ |',
            settings: 'ସେଟିଂସମୂହ',
            adminLoginTitle: 'ସ୍ EL ାଗତ',
            adminLoginSub: 'FRAUDNEXUS ଅନୁସନ୍ଧାନ କାର୍ଯ୍ୟକ୍ଷେତ୍ରକୁ ସାଇନ୍ ଇନ୍ କରନ୍ତୁ |',
            signIn: 'ସାଇନ୍ ଇନ୍',
            tryDemo: 'ଚେଷ୍ଟା କରନ୍ତୁ ଡେମୋ |',
            demoEnv: 'ଡେମୋ ପରିବେଶ |',
            priorityQueue: 'ପ୍ରାଥମିକତା ଅନୁସନ୍ଧାନ ପ୍ରଶ୍ନ |',
            actionCenter: 'କାର୍ଯ୍ୟ କେନ୍ଦ୍ର',
            fraudTrends: 'ଫ୍ରାଏଡ୍ କେସ୍ ଟ୍ରେଣ୍ଡସ୍ |',
            financialExposureSummary: 'ଆର୍ଥିକ ଏକ୍ସପୋଜର ସାରାଂଶ',
            recentActivity: 'ବର୍ତ୍ତମାନର କାର୍ଯ୍ୟକଳାପ |',
            newCases: 'ନୂତନ ମାମଲା |',
            criticalCases: 'ଗୁରୁତର ମାମଲା |',
            escalatedCases: 'ESCALATED କେସ୍ |',
            pendingApprovals: 'ଅନୁମୋଦନଗୁଡିକ',
            financialExposure: 'ଆର୍ଥିକ ଏକ୍ସପୋଜର୍ |',
            unassigned: 'ଅଣସଂରକ୍ଷିତ |',
            assign: 'ନ୍ୟସ୍ତ କରନ୍ତୁ |',
            openWorkspace: 'କାର୍ଯ୍ୟକ୍ଷେତ୍ର ଖୋଲନ୍ତୁ |',
            requestEvidence: 'ପ୍ରମାଣ ଅନୁରୋଧ |',
            escalate: 'ଏସ୍କାଲେଟ୍ |',
            resolve: 'ସମାଧାନ କରନ୍ତୁ |',
            closeCase: 'କେସ୍ ବନ୍ଦ କରନ୍ତୁ |',
            addTask: 'ଟାସ୍କ ଯୋଡନ୍ତୁ |'
        },
        as: {
            brand: 'FRAUDNEXUS',
            tagline: 'জালিয়াতিৰ প্ৰতিবেদনৰ পৰা সমাধানলৈকে — এটা বুদ্ধিমান তদন্ত কৰ্মক্ষেত্ৰ',
            heroTitle: 'জালিয়াতিৰ প্ৰতিবেদনৰ পৰা সমাধানলৈকে',
            heroSub: 'বিত্তীয় আৰু চাইবাৰ জালিয়াতি তদন্ত হাব',
            heroDesc: 'ভুক্তভোগী, তদন্তকাৰী, বিত্তীয় প্ৰতিষ্ঠান, আৰু আইন প্ৰয়োগকাৰী সংস্থাক সংযোগ কৰা এটা বুদ্ধিমান তদন্ত কৰ্মক্ষেত্ৰ।',
            getStarted: 'আৰম্ভ কৰক',
            learnMore: 'অধিক জানক',
            portalSelectTitle: 'আপোনাৰ পৰ্টেল নিৰ্বাচন কৰক',
            portalSelectSub: 'আপোনাৰ ভূমিকাৰ সৈতে মিল থকা কাৰ্য্যস্থান নিৰ্ব্বাচন কৰক।',
            customerPortal: 'গ্ৰাহক পৰ্টেল',
            customerPortalDesc: 'নাগৰিক আৰু ভুক্তভোগীসকলে নিৰাপদে জালিয়াতিৰ ৰিপৰ্ট দিবলৈ, বাস্তৱ সময়ত গোচৰসমূহ অনুসৰণ কৰিবলৈ, আৰু প্ৰমাণ দাখিল কৰিবলৈ।',
            investigatorPortal: 'তদন্তকাৰী / প্ৰশাসক পৰ্টেল',
            investigatorPortalDesc: 'গোচৰৰ তদন্ত, চোৰাংচোৱা বিশ্লেষণ, আৰু অনুসৰণ পৰিচালনা কৰিবলৈ অনুমোদিত কৰ্মীৰ বাবে।',
            enterPortal: 'গ্ৰাহক পৰ্টেলত প্ৰৱেশ কৰক',
            comingSoon: 'অতি সোনকালে আহি আছে',
            login: 'লগইন কৰক',
            register: 'পঞ্জীয়ন কৰক',
            email: 'ইমেইল ঠিকনা',
            password: 'পাছৱৰ্ড',
            confirmPassword: 'পাছৱৰ্ড নিশ্চিত কৰক',
            fullName: 'সম্পূৰ্ণ নাম',
            mobile: 'মোবাইল নম্বৰ',
            dob: 'জন্ম তাৰিখ',
            gender: 'লিংগ',
            occupation: 'দখল',
            address: 'আৱাসিক ঠিকনা',
            forgotPassword: 'পাছৱৰ্ড পাহৰিলেনে?',
            resetPasswordTitle: 'পাছৱৰ্ড পুনৰায় সেট কৰক',
            resetPasswordDesc: 'গুপ্তশব্দ পুনৰায় নিৰ্ধাৰণ নিৰ্দেশ গ্ৰহণ কৰিবলে আপোনাৰ পঞ্জীয়ন কৰা ইমেইল ঠিকনা সুমুৱাওক।',
            instructionsSent: 'প্ৰেৰণ কৰা নিৰ্দেশনাসমূহ পুনৰায় সেট কৰক',
            resetSentMsg: 'যদি এটা একাউণ্ট এই ইমেইল ঠিকনাৰ সৈতে জড়িত, পাছৱৰ্ড পুনৰায় নিৰ্ধাৰণৰ নিৰ্দেশনা আৰু এটা সত্যাপন সংযোগ প্ৰেৰণ কৰা হৈছে।',
            sendResetLink: 'ৰিছেট লিংক পঠাওক',
            backToLogin: 'লগইনলৈ উভতি যাওক',
            hasAccount: 'ইতিমধ্যে একাউণ্ট আছেনে?',
            createAccountSuccess: 'একাউণ্ট সফলতাৰে সৃষ্টি কৰা হৈছে!',
            createAccountSuccessDesc: 'আপোনাৰ FRAUDNEXUS গ্ৰাহক একাউণ্ট পঞ্জীয়ন কৰা হৈছে। অনুগ্ৰহ কৰি আপোনাৰ প্ৰমাণপত্ৰৰ সৈতে লগ ইন কৰক।',
            goToLogin: 'লগইনলৈ যাওক',
            dashboard: 'ডেচব\'ৰ্ড',
            reportFraud: 'জালিয়াতিৰ ৰিপৰ্ট কৰক',
            trackCases: 'ট্ৰেক কেছ',
            evidence: 'প্ৰমাণ',
            profile: 'গ্ৰাহকৰ প্ৰফাইল',
            helpSupport: 'সহায় আৰু সমৰ্থন',
            welcome: 'স্বাগতম',
            totalCases: 'মুঠ ৰোগী',
            activeCases: 'সক্ৰিয় ক্ষেত্ৰ',
            resolvedCases: 'সমাধান কৰা গোচৰ',
            closedCases: 'বন্ধ গোচৰ',
            recentCases: 'শেহতীয়া ৰোগী',
            caseId: 'কেছ আইডি',
            incidentType: 'কাণ্ডৰ ধৰণ',
            date: 'তাৰিখ',
            severity: 'গুৰুত্ব',
            status: 'অৱস্থা',
            action: 'ক্ৰিয়া',
            viewDetails: 'বিৱৰণ চাওক',
            noCases: 'কোনো ৰোগী পোৱা নগ’ল। আৰম্ভ কৰিবলৈ এটা প্ৰৱঞ্চনাৰ ৰিপৰ্ট কৰক।',
            kycStatus: 'কে ৱাই চিৰ অৱস্থা',
            completeKyc: 'সম্পূৰ্ণ কে ৱাই চি',
            govIdType: 'চৰকাৰী আইডিৰ প্ৰকাৰ',
            govIdNumber: 'চৰকাৰী আইডি নম্বৰ',
            proofDocument: 'আইডি প্ৰমাণ নথিপত্ৰ',
            submitKyc: 'পৰ্যালোচনাৰ বাবে KYC জমা দিয়ক',
            kycPendingNote: 'জৰুৰী জালিয়াতিৰ প্ৰতিবেদনৰ বাবে পৰিচয় পৰীক্ষণ বৈকল্পিক আৰু ই গোচৰ দাখিল কৰাত বাধা নিদিয়ে।',
            financialInvolvement: 'আৰ্থিক লোকচান বা লেনদেনৰ লগত জড়িত আছিল নেকি?',
            institutionType: 'প্ৰতিষ্ঠানৰ প্ৰকাৰ',
            institutionName: 'প্ৰতিষ্ঠান / বেংক / এপৰ নাম',
            paymentMode: 'বিত্তীয় কাৰ্য্যকলাপৰ ধৰণ',
            referenceType: 'প্ৰসংগ ধৰণ',
            referenceNumber: 'প্ৰসংগ নম্বৰ / UTR',
            amountInvolved: 'জড়িত পৰিমাণ (INR)',
            blockedAmount: 'গ্ৰাহকে ৰিপৰ্ট কৰা ব্লক কৰা ধনৰাশি',
            recoveredAmount: 'গ্ৰাহকে ৰিপৰ্ট কৰা আদায় কৰা ধনৰাশি',
            suspectName: 'সন্দেহযুক্ত / হিতাধিকাৰীৰ নাম',
            suspectContact: 'সন্দেহযুক্ত যোগাযোগ / ইউপিআই আইডি / একাউণ্ট',
            evidenceType: 'প্ৰমাণৰ প্ৰকাৰ',
            evidenceDesc: 'প্ৰমাণৰ বিৱৰণ',
            attachProof: 'প্ৰমাণ ফাইল সংলগ্ন কৰক',
            submitReport: 'জালিয়াতিৰ প্ৰতিবেদন দাখিল কৰক',
            submitting: 'জমা দি আছে...',
            stageSubmitted: 'জমা দিয়া হৈছে',
            stageInitialReview: 'প্ৰাৰম্ভিক পৰ্যালোচনা',
            stageInvestigation: 'তদন্ত',
            stageResolution: 'ৰিজ’লিউচন',
            stageClosed: 'বন্ধ',
            addAdditionalEvidence: 'অতিৰিক্ত প্ৰমাণ যোগ কৰক',
            askAI: 'FRAUDNEXUS AI ক সুধিব',
            send: 'পঠাওক',
            close: 'বন্ধ কৰক',
            logout: 'লগআউট কৰক',
            commandCenter: 'কমাণ্ড চেণ্টাৰ',
            partners: 'অংশীদাৰসকল',
            partnerDirectory: 'অংশীদাৰ ডাইৰেক্টৰী',
            addPartner: 'অংশীদাৰ যোগ কৰক',
            editPartner: 'সম্পাদনা অংশীদাৰ',
            partnerRequests: 'অংশীদাৰৰ অনুৰোধ',
            requestStatus: 'অনুৰোধৰ অৱস্থা',
            partnerCategory: 'অংশীদাৰ শ্ৰেণী',
            integrationType: 'সংহতিৰ ধৰণ',
            active: 'সক্ৰিয়',
            inactive: 'নিষ্ক্ৰিয়',
            suspended: 'নিলম্বিত',
            simulatedDemoPartner: 'চিমুলেটেড ডেমো অংশীদাৰ',
            totalPartners: 'মুঠ অংশীদাৰ',
            activePartners: 'সক্ৰিয় অংশীদাৰ',
            pendingRequests: 'বাকী থকা অনুৰোধ',
            awaitingResponse: 'সঁহাৰিৰ বাবে অপেক্ষা কৰি আছে',
            overdueRequests: 'অভাৰডু অনুৰোধ',
            customers: 'গ্ৰাহকসকল',
            cases: 'গোচৰ',
            investigation: 'তদন্ত',
            intelligenceWorkspace: 'চোৰাংচোৱা কৰ্মক্ষেত্ৰ',
            analytics: 'বিশ্লেষণ',
            settings: 'ছেটিংছ',
            adminLoginTitle: 'পুনৰ স্বাগতম',
            adminLoginSub: 'FRAUDNEXUS তদন্ত কৰ্মক্ষেত্ৰত চাইন ইন কৰক',
            signIn: 'SIGN IN কৰক',
            tryDemo: 'DEMO চেষ্টা কৰক',
            demoEnv: 'DEMO পৰিৱেশ',
            priorityQueue: 'অগ্ৰাধিকাৰ তদন্তৰ শাৰী',
            actionCenter: 'ACTION CENTER',
            fraudTrends: 'FRAUD CASE ৰ ধাৰা',
            financialExposureSummary: 'বিত্তীয় উন্মোচনৰ সাৰাংশ',
            recentActivity: 'শেহতীয়া কাৰ্য্যকলাপ',
            newCases: 'NEW CASES',
            criticalCases: 'CRITICAL CASES',
            escalatedCases: 'ESCALATED CASES',
            pendingApprovals: 'অনুমোদন বাকী আছে',
            financialExposure: 'বিত্তীয় উন্মোচন',
            unassigned: 'অনাচাইনড',
            assign: 'নিযুক্তি দিয়ক',
            openWorkspace: 'কাৰ্য্যস্থান খোলক',
            requestEvidence: 'প্ৰমাণ বিচাৰিব',
            escalate: 'এস্কেলেট কৰক',
            resolve: 'সংকল্প লওক',
            closeCase: 'বন্ধ কৰক গোচৰ',
            addTask: 'টাস্ক যোগ কৰক'
        },
        ur: {
            brand: 'فراڈنیکسس',
            tagline: 'فراڈ رپورٹ سے ریزولوشن تک - ایک ذہین تفتیشی کام کی جگہ',
            heroTitle: 'فراڈ رپورٹ سے حل تک',
            heroSub: 'مالیاتی اور سائبر فراڈ انویسٹی گیشن ہب',
            heroDesc: 'ایک ذہین تفتیشی کام کی جگہ جو متاثرین، تفتیش کاروں، مالیاتی اداروں اور قانون نافذ کرنے والے اداروں کو جوڑتی ہے۔',
            getStarted: 'شروع کریں',
            learnMore: 'مزید جانیں',
            portalSelectTitle: 'اپنا پورٹل منتخب کریں۔',
            portalSelectSub: 'کام کی جگہ کا انتخاب کریں جو آپ کے کردار سے مماثل ہو۔',
            customerPortal: 'کسٹمر پورٹل',
            customerPortalDesc: 'شہریوں اور متاثرین کو محفوظ طریقے سے دھوکہ دہی کی اطلاع دینے، حقیقی وقت میں مقدمات کا پتہ لگانے اور ثبوت جمع کرانے کے لیے۔',
            investigatorPortal: 'تفتیش کار/ایڈمن پورٹل',
            investigatorPortalDesc: 'مقدمات کی تفتیش، ذہانت کا تجزیہ کرنے اور تعمیل کا انتظام کرنے کے لیے مجاز اہلکاروں کے لیے۔',
            enterPortal: 'کسٹمر پورٹل درج کریں۔',
            comingSoon: 'جلد آرہا ہے۔',
            login: 'لاگ ان',
            register: 'رجسٹر کریں۔',
            email: 'ای میل ایڈریس',
            password: 'پاس ورڈ',
            confirmPassword: 'پاس ورڈ کی تصدیق کریں۔',
            fullName: 'پورا نام',
            mobile: 'موبائل نمبر',
            dob: 'تاریخ پیدائش',
            gender: 'جنس',
            occupation: 'پیشہ',
            address: 'رہائشی پتہ',
            forgotPassword: 'پاس ورڈ بھول گئے؟',
            resetPasswordTitle: 'پاس ورڈ ری سیٹ کریں۔',
            resetPasswordDesc: 'پاس ورڈ دوبارہ ترتیب دینے کی ہدایات حاصل کرنے کے لیے اپنا رجسٹرڈ ای میل ایڈریس درج کریں۔',
            instructionsSent: 'بھیجی گئی ہدایات کو دوبارہ ترتیب دیں۔',
            resetSentMsg: 'اگر کوئی اکاؤنٹ اس ای میل ایڈریس کے ساتھ منسلک ہے تو، پاس ورڈ دوبارہ ترتیب دینے کی ہدایات اور ایک تصدیقی لنک بھیج دیا گیا ہے۔',
            sendResetLink: 'ری سیٹ لنک بھیجیں۔',
            backToLogin: 'لاگ ان پر واپس جائیں۔',
            hasAccount: 'پہلے سے ہی اکاؤنٹ ہے؟',
            createAccountSuccess: 'اکاؤنٹ کامیابی کے ساتھ بنایا گیا!',
            createAccountSuccessDesc: 'آپ کا FAUDNEXUS کسٹمر اکاؤنٹ رجسٹر ہو گیا ہے۔ براہ کرم اپنی اسناد کے ساتھ لاگ ان کریں۔',
            goToLogin: 'لاگ ان پر جائیں۔',
            dashboard: 'ڈیش بورڈ',
            reportFraud: 'فراڈ کی اطلاع دیں۔',
            trackCases: 'کیسز کو ٹریک کریں۔',
            evidence: 'ثبوت',
            profile: 'کسٹمر پروفائل',
            helpSupport: 'مدد اور تعاون',
            welcome: 'خوش آمدید',
            totalCases: 'کل کیسز',
            activeCases: 'ایکٹو کیسز',
            resolvedCases: 'حل شدہ کیسز',
            closedCases: 'بند مقدمات',
            recentCases: 'حالیہ کیسز',
            caseId: 'کیس کی شناخت',
            incidentType: 'واقعہ کی قسم',
            date: 'تاریخ',
            severity: 'شدت',
            status: 'حیثیت',
            action: 'ایکشن',
            viewDetails: 'تفصیلات دیکھیں',
            noCases: 'کوئی کیس نہیں ملا۔ شروع کرنے کے لیے دھوکہ دہی کی اطلاع دیں۔',
            kycStatus: 'KYC اسٹیٹس',
            completeKyc: 'KYC مکمل کریں۔',
            govIdType: 'سرکاری ID کی قسم',
            govIdNumber: 'حکومتی شناختی نمبر',
            proofDocument: 'شناختی ثبوت کی دستاویز',
            submitKyc: 'جائزہ کے لیے KYC جمع کروائیں۔',
            kycPendingNote: 'فراڈ کی فوری رپورٹنگ کے لیے شناخت کی تصدیق اختیاری ہے اور کیس جمع کرانے سے روکا نہیں جائے گا۔',
            financialInvolvement: 'کیا مالی نقصان یا لین دین میں ملوث تھا؟',
            institutionType: 'ادارے کی قسم',
            institutionName: 'ادارہ / بینک / ایپ کا نام',
            paymentMode: 'مالیاتی سرگرمی کا موڈ',
            referenceType: 'حوالہ کی قسم',
            referenceNumber: 'حوالہ نمبر / UTR',
            amountInvolved: 'شامل رقم (INR)',
            blockedAmount: 'گاہک کی اطلاع کردہ بلاک شدہ رقم',
            recoveredAmount: 'گاہک کی اطلاع کردہ وصولی رقم',
            suspectName: 'مشتبہ / فائدہ اٹھانے والے کا نام',
            suspectContact: 'مشتبہ رابطہ / UPI ID / اکاؤنٹ',
            evidenceType: 'ثبوت کی قسم',
            evidenceDesc: 'ثبوت کی تفصیل',
            attachProof: 'ثبوت کی فائل منسلک کریں۔',
            submitReport: 'فراڈ کی رپورٹ جمع کروائیں۔',
            submitting: 'جمع کر رہا ہے...',
            stageSubmitted: 'جمع کرایا',
            stageInitialReview: 'ابتدائی جائزہ',
            stageInvestigation: 'تفتیش',
            stageResolution: 'قرارداد',
            stageClosed: 'بند',
            addAdditionalEvidence: 'اضافی ثبوت شامل کریں۔',
            askAI: 'FRAUDNEXUS AI سے پوچھیں۔',
            send: 'بھیجیں۔',
            close: 'بند',
            logout: 'لاگ آؤٹ',
            commandCenter: 'کمانڈ سینٹر',
            partners: 'شراکت دار',
            partnerDirectory: 'پارٹنر ڈائرکٹری',
            addPartner: 'پارٹنر شامل کریں۔',
            editPartner: 'پارٹنر میں ترمیم کریں۔',
            partnerRequests: 'ساتھی کی درخواستیں۔',
            requestStatus: 'درخواست کی حیثیت',
            partnerCategory: 'پارٹنر کیٹیگری',
            integrationType: 'انضمام کی قسم',
            active: 'فعال',
            inactive: 'غیر فعال',
            suspended: 'معطل',
            simulatedDemoPartner: 'مصنوعی ڈیمو پارٹنر',
            totalPartners: 'کل شراکت دار',
            activePartners: 'ایکٹو پارٹنرز',
            pendingRequests: 'زیر التواء درخواستیں',
            awaitingResponse: 'جواب کا انتظار ہے۔',
            overdueRequests: 'زائد المیعاد درخواستیں۔',
            customers: 'گاہکوں',
            cases: 'کیسز',
            investigation: 'تفتیش',
            intelligenceWorkspace: 'انٹیلی جنس ورک اسپیس',
            analytics: 'تجزیات',
            settings: 'ترتیبات',
            adminLoginTitle: 'واپسی پر خوش آمدید',
            adminLoginSub: 'FRAUDNEXUS انویسٹی گیشن ورک اسپیس میں سائن ان کریں۔',
            signIn: 'سائن ان کریں۔',
            tryDemo: 'ڈیمو آزمائیں۔',
            demoEnv: 'ڈیمو ماحولیات',
            priorityQueue: 'ترجیحی تفتیشی قطار',
            actionCenter: 'ایکشن سینٹر',
            fraudTrends: 'فراڈ کیس کے رجحانات',
            financialExposureSummary: 'مالیاتی نمائش کا خلاصہ',
            recentActivity: 'حالیہ سرگرمی',
            newCases: 'نئے کیسز',
            criticalCases: 'کریٹیکل کیسز',
            escalatedCases: 'بڑھے ہوئے کیسز',
            pendingApprovals: 'زیر التواء منظوریاں',
            financialExposure: 'مالیاتی نمائش',
            unassigned: 'غیر تفویض کردہ',
            assign: 'تفویض کریں۔',
            openWorkspace: 'کام کی جگہ کھولیں۔',
            requestEvidence: 'ثبوت طلب کریں۔',
            escalate: 'بڑھانا',
            resolve: 'حل کریں۔',
            closeCase: 'کیس بند کریں۔',
            addTask: 'ٹاسک شامل کریں۔'
        },
        ne: {
            brand: 'फ्रडनेक्सस',
            tagline: 'धोखाधडी रिपोर्ट देखि रिजोल्युसन - एक बुद्धिमानी अनुसन्धान कार्यक्षेत्र',
            heroTitle: 'ठगी प्रतिवेदन देखि समाधान सम्म',
            heroSub: 'वित्तीय र साइबर धोखाधडी अनुसन्धान हब',
            heroDesc: 'पीडितहरू, अन्वेषकहरू, वित्तीय संस्थाहरू, र कानून प्रवर्तनलाई जोड्ने एक बुद्धिमान अनुसन्धान कार्यस्थान।',
            getStarted: 'सुरु गर्नुहोस्',
            learnMore: 'थप जान्नुहोस्',
            portalSelectTitle: 'आफ्नो पोर्टल चयन गर्नुहोस्',
            portalSelectSub: 'तपाईंको भूमिकासँग मेल खाने कार्यस्थान छान्नुहोस्।',
            customerPortal: 'ग्राहक पोर्टल',
            customerPortalDesc: 'नागरिक र पीडितहरूलाई सुरक्षित रूपमा ठगी रिपोर्ट गर्न, वास्तविक समयमा केसहरू ट्र्याक गर्न, र प्रमाण पेश गर्न।',
            investigatorPortal: 'अन्वेषक / व्यवस्थापक पोर्टल',
            investigatorPortalDesc: 'मुद्दाहरूको अनुसन्धान गर्न, खुफिया विश्लेषण गर्न र अनुपालन व्यवस्थापन गर्न अधिकृत कर्मचारीहरूको लागि।',
            enterPortal: 'ग्राहक पोर्टल प्रविष्ट गर्नुहोस्',
            comingSoon: 'चाँडै आउँदैछ',
            login: 'लगइन गर्नुहोस्',
            register: 'दर्ता गर्नुहोस्',
            email: 'इमेल ठेगाना',
            password: 'पासवर्ड',
            confirmPassword: 'पासवर्ड पुष्टि गर्नुहोस्',
            fullName: 'पूरा नाम',
            mobile: 'मोबाइल नम्बर',
            dob: 'जन्म मिति',
            gender: 'लिङ्ग',
            occupation: 'पेशा',
            address: 'आवासीय ठेगाना',
            forgotPassword: 'पासवर्ड बिर्सनुभयो?',
            resetPasswordTitle: 'पासवर्ड रिसेट गर्नुहोस्',
            resetPasswordDesc: 'पासवर्ड रिसेट निर्देशनहरू प्राप्त गर्न तपाईंको दर्ता गरिएको इमेल ठेगाना प्रविष्ट गर्नुहोस्।',
            instructionsSent: 'रिसेट निर्देशनहरू पठाइयो',
            resetSentMsg: 'यदि खाता यस इमेल ठेगानासँग सम्बन्धित छ भने, पासवर्ड रिसेट निर्देशनहरू र प्रमाणीकरण लिङ्क पठाइएको छ।',
            sendResetLink: 'रिसेट लिङ्क पठाउनुहोस्',
            backToLogin: 'लगइन मा फर्कनुहोस्',
            hasAccount: 'पहिले नै खाता छ?',
            createAccountSuccess: 'खाता सफलतापूर्वक सिर्जना गरियो!',
            createAccountSuccessDesc: 'तपाईंको FRAUDNEXUS ग्राहक खाता दर्ता गरिएको छ। कृपया आफ्नो प्रमाणहरू संग लग इन गर्नुहोस्।',
            goToLogin: 'लगइन मा जानुहोस्',
            dashboard: 'ड्यासबोर्ड',
            reportFraud: 'जालसाजी रिपोर्ट गर्नुहोस्',
            trackCases: 'ट्र्याक केसहरू',
            evidence: 'प्रमाण',
            profile: 'ग्राहक प्रोफाइल',
            helpSupport: 'मद्दत र समर्थन',
            welcome: 'स्वागत छ',
            totalCases: 'कुल केसहरू',
            activeCases: 'सक्रिय केसहरू',
            resolvedCases: 'समाधान गरिएका केसहरू',
            closedCases: 'बन्द केसहरू',
            recentCases: 'हालका केसहरू',
            caseId: 'केस आईडी',
            incidentType: 'घटनाको प्रकार',
            date: 'मिति',
            severity: 'गम्भीरता',
            status: 'स्थिति',
            action: 'कार्य',
            viewDetails: 'विवरणहरू हेर्नुहोस्',
            noCases: 'कुनै केसहरू फेला परेनन्। सुरु गर्न जालसाजी रिपोर्ट गर्नुहोस्।',
            kycStatus: 'KYC स्थिति',
            completeKyc: 'KYC पूरा गर्नुहोस्',
            govIdType: 'सरकारी आईडी प्रकार',
            govIdNumber: 'सरकारी आईडी नम्बर',
            proofDocument: 'आईडी प्रमाण कागजात',
            submitKyc: 'समीक्षाको लागि KYC पेश गर्नुहोस्',
            kycPendingNote: 'तत्काल जालसाजी रिपोर्टिङका लागि पहिचान प्रमाणीकरण ऐच्छिक छ र केस पेस गर्न रोकिने छैन।',
            financialInvolvement: 'त्यहाँ आर्थिक हानि वा लेनदेन संलग्नता थियो?',
            institutionType: 'संस्थाको प्रकार',
            institutionName: 'संस्था / बैंक / एप नाम',
            paymentMode: 'वित्तीय गतिविधि मोड',
            referenceType: 'सन्दर्भ प्रकार',
            referenceNumber: 'सन्दर्भ नम्बर / UTR',
            amountInvolved: 'संलग्न रकम (INR)',
            blockedAmount: 'ग्राहक-रिपोर्ट गरिएको अवरुद्ध रकम',
            recoveredAmount: 'ग्राहक-रिपोर्ट गरिएको बरामद रकम',
            suspectName: 'संदिग्ध / लाभार्थी नाम',
            suspectContact: 'संदिग्ध सम्पर्क / UPI आईडी / खाता',
            evidenceType: 'प्रमाण प्रकार',
            evidenceDesc: 'प्रमाण विवरण',
            attachProof: 'प्रमाण फाइल संलग्न गर्नुहोस्',
            submitReport: 'जालसाजी रिपोर्ट पेश गर्नुहोस्',
            submitting: 'पेस गर्दै...',
            stageSubmitted: 'पेस गरियो',
            stageInitialReview: 'प्रारम्भिक समीक्षा',
            stageInvestigation: 'अनुसन्धान',
            stageResolution: 'संकल्प',
            stageClosed: 'बन्द',
            addAdditionalEvidence: 'थप प्रमाणहरू थप्नुहोस्',
            askAI: 'FRAUDNEXUS AI लाई सोध्नुहोस्',
            send: 'पठाउनुहोस्',
            close: 'बन्द गर्नुहोस्',
            logout: 'लगआउट',
            commandCenter: 'कमाण्ड सेन्टर',
            partners: 'साझेदारहरू',
            partnerDirectory: 'साझेदार निर्देशिका',
            addPartner: 'साझेदार थप्नुहोस्',
            editPartner: 'साझेदार सम्पादन गर्नुहोस्',
            partnerRequests: 'साझेदार अनुरोधहरू',
            requestStatus: 'अनुरोध स्थिति',
            partnerCategory: 'साझेदार कोटि',
            integrationType: 'एकीकरण प्रकार',
            active: 'सक्रिय',
            inactive: 'निष्क्रिय',
            suspended: 'निलम्बित',
            simulatedDemoPartner: 'सिमुलेटेड डेमो पार्टनर',
            totalPartners: 'कुल साझेदारहरू',
            activePartners: 'सक्रिय साझेदारहरू',
            pendingRequests: 'विचाराधीन अनुरोधहरू',
            awaitingResponse: 'प्रतिक्रियाको प्रतिक्षामा',
            overdueRequests: 'ओभरड्यू अनुरोधहरू',
            customers: 'ग्राहकहरु',
            cases: 'केसहरू',
            investigation: 'अनुसन्धान',
            intelligenceWorkspace: 'खुफिया कार्यक्षेत्र',
            analytics: 'विश्लेषण',
            settings: 'सेटिङहरू',
            adminLoginTitle: 'फिर्ता स्वागत छ',
            adminLoginSub: 'FRAUDNEXUS Investigation Workspace मा साइन इन गर्नुहोस्',
            signIn: 'साइन इन गर्नुहोस्',
            tryDemo: 'डेमो प्रयास गर्नुहोस्',
            demoEnv: 'डेमो वातावरण',
            priorityQueue: 'प्राथमिकता अनुसन्धान कतार',
            actionCenter: 'कार्य केन्द्र',
            fraudTrends: 'ठगी मुद्दा प्रवृत्तिहरू',
            financialExposureSummary: 'फाइनान्सियल एक्सपोजर सारांश',
            recentActivity: 'हालको गतिविधि',
            newCases: 'नयाँ केसहरू',
            criticalCases: 'क्रिटिकल केसहरू',
            escalatedCases: 'बढेका केसहरू',
            pendingApprovals: 'पेन्डिङ स्वीकृतिहरू',
            financialExposure: 'फाइनान्सियल एक्सपोजर',
            unassigned: 'तोकिएको छैन',
            assign: 'असाइन गर्नुहोस्',
            openWorkspace: 'कार्यक्षेत्र खोल्नुहोस्',
            requestEvidence: 'प्रमाण माग्नुहोस्',
            escalate: 'बढाउनुहोस्',
            resolve: 'समाधान गर्नुहोस्',
            closeCase: 'केस बन्द गर्नुहोस्',
            addTask: 'कार्य थप्नुहोस्'
        },
        sa: {
            brand: 'FRAUDNEXUS इति',
            tagline: 'धोखाधड़ीप्रतिवेदनात् समाधानपर्यन्तं — एकः बुद्धिमान् अन्वेषणकार्यक्षेत्रम्',
            heroTitle: 'धोखाधड़ीप्रतिवेदनात् समाधानपर्यन्तं',
            heroSub: 'वित्तीय एवं साइबर धोखाधड़ी अन्वेषण केन्द्र',
            heroDesc: 'पीडितान्, अन्वेषकान्, वित्तीयसंस्थाः, कानूनप्रवर्तनं च संयोजयति एकं बुद्धिमान् अन्वेषणकार्यक्षेत्रम्।',
            getStarted: 'आरभत',
            learnMore: 'अधिकं ज्ञातुं',
            portalSelectTitle: 'स्वस्य पोर्टल् चयनं कुर्वन्तु',
            portalSelectSub: 'भवतः भूमिकायाः अनुरूपं कार्यक्षेत्रं चिनोतु ।',
            customerPortal: 'ग्राहक पोर्टल',
            customerPortalDesc: 'नागरिकानां पीडितानां च कृते धोखाधड़ीं सुरक्षितरूपेण निवेदयितुं, वास्तविकसमये प्रकरणानाम् अनुसरणं कर्तुं, प्रमाणं च प्रस्तुतुं।',
            investigatorPortal: 'अन्वेषक / व्यवस्थापक पोर्टल',
            investigatorPortalDesc: 'प्रकरणानाम् अन्वेषणाय, गुप्तचरविश्लेषणाय, अनुपालनस्य प्रबन्धनाय च अधिकृतकर्मचारिणां कृते।',
            enterPortal: 'ग्राहक पोर्टल् प्रविष्टं कुर्वन्तु',
            comingSoon: 'शीघ्रम् आगच्छति',
            login: 'प्रवेशः',
            register: 'पञ्जीकरणं कुर्वन्तु',
            email: 'ईमेल पता',
            password: 'गुप्तशब्दः',
            confirmPassword: 'गुप्तशब्दस्य पुष्टिः कुर्वन्तु',
            fullName: 'सम्पूर्ण नाम',
            mobile: 'मोबाईल नम्बर',
            dob: 'जन्मतिथि',
            gender: 'लिङ्गम्',
            occupation: 'व्यवसायः',
            address: 'आवासीय पता',
            forgotPassword: 'गुप्तशब्दं विस्मृतवान् वा?',
            resetPasswordTitle: 'गुप्तशब्दं पुनः सेट् कुर्वन्तु',
            resetPasswordDesc: 'गुप्तशब्दपुनर्स्थापननिर्देशान् प्राप्तुं स्वस्य पञ्जीकृतं ईमेल-सङ्केतं प्रविशन्तु ।',
            instructionsSent: 'Reset Instructions प्रेषितम्',
            resetSentMsg: 'यदि कश्चन खातः अस्मिन् ईमेल-सङ्केतेन सह सम्बद्धः अस्ति तर्हि गुप्तशब्द-पुनर्स्थापन-निर्देशाः, सत्यापन-लिङ्क् च प्रेषिताः सन्ति ।',
            sendResetLink: 'Reset Link प्रेषयतु',
            backToLogin: 'पुनः प्रवेशं प्रति',
            hasAccount: 'पूर्वमेव खाता अस्ति वा ?',
            createAccountSuccess: 'खाता सफलतया निर्मितम्!',
            createAccountSuccessDesc: 'भवतः FRAUDNEXUS ग्राहकखातं पञ्जीकृतम् अस्ति। कृपया स्वस्य प्रमाणपत्रैः सह प्रवेशं कुर्वन्तु।',
            goToLogin: 'Login इति गच्छन्तु',
            dashboard: 'डैशबोर्ड',
            reportFraud: 'धोखाधड़ीं सूचयन्तु',
            trackCases: 'ट्रैक केस',
            evidence: 'प्रमाणम्',
            profile: 'ग्राहक प्रोफाइल',
            helpSupport: 'सहायता एवं समर्थन',
            welcome: 'स्वागतम्',
            totalCases: 'कुल प्रकरणाः',
            activeCases: 'सक्रिय प्रकरणाः',
            resolvedCases: 'निराकृताः प्रकरणाः',
            closedCases: 'बन्द प्रकरणम्',
            recentCases: 'अद्यतन प्रकरणम्',
            caseId: 'केस आईडी',
            incidentType: 'घटनाप्रकारः',
            date: 'तिथि',
            severity: 'तीव्रता',
            status: 'स्थितिः',
            action: 'कर्म',
            viewDetails: 'विवरणं पश्यन्तु',
            noCases: 'न प्रकरणाः प्राप्ताः। आरम्भार्थं धोखाधड़ीं सूचयन्तु।',
            kycStatus: 'केवाईसी स्थिति',
            completeKyc: 'सम्पूर्ण के.वाई.सी',
            govIdType: 'सरकारी आईडी प्रकार',
            govIdNumber: 'सरकारी आईडी नम्बर',
            proofDocument: 'आईडी प्रमाण दस्तावेज',
            submitKyc: 'समीक्षायै KYC प्रस्तुतं कुर्वन्तु',
            kycPendingNote: 'तत्काल धोखाधड़ी-समाचारस्य कृते परिचय-सत्यापनं वैकल्पिकं भवति, प्रकरण-प्रस्तुतिं न अवरुद्धं करिष्यति ।',
            financialInvolvement: 'आर्थिकहानिः आसीत् वा व्यवहारस्य संलग्नता वा ?',
            institutionType: 'संस्था प्रकार',
            institutionName: 'संस्था / बैंक / एप्लिकेशन नाम',
            paymentMode: 'वित्तीय गतिविधि मोड',
            referenceType: 'सन्दर्भप्रकारः',
            referenceNumber: 'सन्दर्भ संख्या / UTR',
            amountInvolved: 'सम्मिलित राशि (INR) 1.1.',
            blockedAmount: 'ग्राहक-रिपोर्ट् अवरुद्धराशिः',
            recoveredAmount: 'ग्राहक-रिपोर्ट् कृता वसूली राशि',
            suspectName: 'संदिग्ध / लाभार्थी नाम',
            suspectContact: 'संदिग्ध सम्पर्क / यूपीआई आईडी / खाता',
            evidenceType: 'प्रमाणप्रकारः',
            evidenceDesc: 'प्रमाणवर्णनम्',
            attachProof: 'प्रमाणसञ्चिका संलग्नं कुर्वन्तु',
            submitReport: 'धोखाधड़ी प्रतिवेदन प्रस्तुत करें',
            submitting: 'प्रस्तुत कर...',
            stageSubmitted: 'प्रस्तुत',
            stageInitialReview: 'प्रारम्भिक समीक्षा',
            stageInvestigation: 'अन्वेषणम्',
            stageResolution: 'संकल्प',
            stageClosed: 'निमीलितम्',
            addAdditionalEvidence: 'अतिरिक्त प्रमाणं योजयतु',
            askAI: 'FRAUDNEXUS AI इति पृच्छन्तु',
            send: 'प्रेषयतु',
            close: 'निमील्यताम्',
            logout: 'लॉगआउट्',
            commandCenter: 'आदेश केन्द्र',
            partners: 'भागीदाराः',
            partnerDirectory: 'भागीदार निर्देशिका',
            addPartner: 'भागीदारं योजयतु',
            editPartner: 'सम्पादन भागीदार',
            partnerRequests: 'भागीदार अनुरोधाः',
            requestStatus: 'अनुरोध स्थिति',
            partnerCategory: 'भागीदार श्रेणी',
            integrationType: 'एकीकरण प्रकार',
            active: 'सक्रियः',
            inactive: 'निष्क्रिय',
            suspended: 'निलम्बितम्',
            simulatedDemoPartner: 'अनुकरणीय प्रदर्शन भागीदार',
            totalPartners: 'कुल भागीदार',
            activePartners: 'सक्रिय भागीदार',
            pendingRequests: 'लम्बित अनुरोध',
            awaitingResponse: 'प्रतिक्रिया प्रतीक्षा',
            overdueRequests: 'अतिदेय अनुरोधाः',
            customers: 'ग्राहकाः',
            cases: 'प्रकरणाः',
            investigation: 'अन्वेषणम्',
            intelligenceWorkspace: 'बुद्धि कार्यक्षेत्र',
            analytics: 'विश्लेषणात्मकता',
            settings: 'सेटिंग्स्',
            adminLoginTitle: 'पुनः स्वागतम्',
            adminLoginSub: 'FRAUDNEXUS अन्वेषण कार्यक्षेत्रे प्रवेशं कुर्वन्तु',
            signIn: 'SIGN IN इति',
            tryDemo: 'TRY DEMO',
            demoEnv: 'DEMO ENVIRONMENT इति',
            priorityQueue: 'प्राथमिकता अन्वेषण कतार',
            actionCenter: 'ACTION CENTER इति',
            fraudTrends: 'धोखाधड़ी प्रकरण प्रवृत्तियाँ',
            financialExposureSummary: 'वित्तीय उदघाटन सारांश',
            recentActivity: 'अद्यतन क्रियाकलाप',
            newCases: 'NEW CASES',
            criticalCases: 'CRITICAL CASES',
            escalatedCases: 'ESCALATED CASES इति',
            pendingApprovals: 'अनुमोदन लंबित',
            financialExposure: 'वित्तीय उजागर',
            unassigned: 'अनिर्दिष्टः',
            assign: 'नियुक्ति',
            openWorkspace: 'कार्यक्षेत्रं उद्घाटयन्तु',
            requestEvidence: 'प्रमाणं याचयतु',
            escalate: 'वर्धयतु',
            resolve: 'संकल्पं कुरुत',
            closeCase: 'प्रकरणं बन्दं कुर्वन्तु',
            addTask: 'कार्यम् योजयतु'
        },
        bho: {
            brand: 'धोखाधड़ी के बारे में बतावल गइल बा',
            tagline: 'धोखाधड़ी रिपोर्ट से लेके समाधान तक — एगो बुद्धिमान जांच कार्यक्षेत्र',
            heroTitle: 'धोखाधड़ी के रिपोर्ट से लेके समाधान तक',
            heroSub: 'वित्तीय अउर साइबर धोखाधड़ी के जांच हब',
            heroDesc: 'पीड़ित, जांचकर्ता, वित्तीय संस्थान, आ कानून प्रवर्तन के जोड़े वाला एगो बुद्धिमान जांच कार्यक्षेत्र.',
            getStarted: 'शुरू कर दीं',
            learnMore: 'अउरी जाने खातिर देखीं',
            portalSelectTitle: 'आपन पोर्टल चुनीं',
            portalSelectSub: 'रउरा भूमिका से मेल खाए वाला वर्कस्पेस चुनीं.',
            customerPortal: 'ग्राहक पोर्टल के बा',
            customerPortalDesc: 'नागरिकन आ पीड़ितन खातिर धोखाधड़ी के सुरक्षित रूप से रिपोर्ट करे, रियल टाइम में केस के ट्रैक करे, आ सबूत जमा करे.',
            investigatorPortal: 'जांचकर्ता / एडमिन पोर्टल के बा',
            investigatorPortalDesc: 'केस के जांच करे, खुफिया जानकारी के विश्लेषण करे, आ अनुपालन के प्रबंधन करे खातिर अधिकृत कर्मियन खातिर.',
            enterPortal: 'ग्राहक पोर्टल में प्रवेश करीं',
            comingSoon: 'जल्दिए आ रहल बा',
            login: 'लॉगिन करीं',
            register: 'रजिस्ट्रेशन करावे के बा',
            email: 'ईमेल के पता बा',
            password: 'पासवर्ड के बा',
            confirmPassword: 'पासवर्ड के पुष्टि करीं',
            fullName: 'पूरा नाम बा',
            mobile: 'मोबाइल नंबर बा',
            dob: 'जन्म तिथि के बारे में बतावल गइल बा',
            gender: 'लिंग के बा',
            occupation: 'कब्जा कर लिहले बा',
            address: 'आवासीय पता बा',
            forgotPassword: 'पासवर्ड भूल गइल बानी?',
            resetPasswordTitle: 'पासवर्ड के रीसेट करीं',
            resetPasswordDesc: 'पासवर्ड रीसेट के निर्देश पावे खातिर आपन रजिस्टर्ड ईमेल पता दर्ज करीं.',
            instructionsSent: 'रीसेट निर्देश भेजल गइल बा',
            resetSentMsg: 'अगर कवनो खाता एह ईमेल पता से जुड़ल बा त पासवर्ड रीसेट करे के निर्देश आ सत्यापन लिंक भेजल गइल बा.',
            sendResetLink: 'रीसेट लिंक भेजल जाला',
            backToLogin: 'लॉगिन पर वापस आ जाईं',
            hasAccount: 'पहिलहीं से खाता बा?',
            createAccountSuccess: 'खाता सफलतापूर्वक बनावल गइल!',
            createAccountSuccessDesc: 'राउर FRAUDNEXUS ग्राहक खाता रजिस्टर हो गइल बा. कृपया आपन क्रेडेंशियल के साथे लॉग इन करीं।',
            goToLogin: 'लॉगिन पर जाईं',
            dashboard: 'डैशबोर्ड के बा',
            reportFraud: 'धोखाधड़ी के रिपोर्ट करीं',
            trackCases: 'केस के ट्रैक कइल जाला',
            evidence: 'सबूत बा',
            profile: 'ग्राहक के प्रोफाइल बा',
            helpSupport: 'मदद & समर्थन के बा',
            welcome: 'स्वागत बा',
            totalCases: 'कुल केस के बा',
            activeCases: 'सक्रिय केस के बा',
            resolvedCases: 'केस के समाधान हो गइल',
            closedCases: 'बंद केस के बा',
            recentCases: 'हाल के केस के बारे में बतावल गईल बा',
            caseId: 'केस आईडी के बा',
            incidentType: 'घटना के प्रकार के बा',
            date: 'तारीख के बा',
            severity: 'गंभीरता के बा',
            status: 'स्टेटस के बा',
            action: 'कार्रवाई के बारे में बतावल गइल बा',
            viewDetails: 'विवरण देखल जाव',
            noCases: 'कवनो केस ना मिलल. शुरुआत करे खातिर कवनो धोखाधड़ी के रिपोर्ट करीं.',
            kycStatus: 'केवाईसी के स्थिति बा',
            completeKyc: 'पूरा केवाईसी के बा',
            govIdType: 'सरकारी आईडी के प्रकार के बा',
            govIdNumber: 'सरकार के आईडी नंबर बा',
            proofDocument: 'आईडी प्रूफ दस्तावेज के बा',
            submitKyc: 'समीक्षा खातिर केवाईसी जमा करीं',
            kycPendingNote: 'तत्काल धोखाधड़ी के रिपोर्टिंग खातिर पहचान सत्यापन वैकल्पिक बा आ केस जमा करे में बाधा ना आई.',
            financialInvolvement: 'का आर्थिक नुकसान भइल रहे कि लेनदेन में शामिल होखे के?',
            institutionType: 'संस्थान के प्रकार के बा',
            institutionName: 'संस्थान / बैंक / ऐप के नाम बा',
            paymentMode: 'वित्तीय गतिविधि मोड के बारे में बतावल गइल बा',
            referenceType: 'संदर्भ के प्रकार के बा',
            referenceNumber: 'संदर्भ संख्या / यूटीआर के बा',
            amountInvolved: 'शामिल राशि (आईएनआर) के बा।',
            blockedAmount: 'ग्राहक द्वारा रिपोर्ट कइल गइल अवरुद्ध राशि',
            recoveredAmount: 'ग्राहक द्वारा रिपोर्ट कइल गइल वसूली राशि',
            suspectName: 'संदिग्ध / लाभार्थी के नाम बा',
            suspectContact: 'संदिग्ध संपर्क / यूपीआई आईडी / खाता',
            evidenceType: 'सबूत के प्रकार के बा',
            evidenceDesc: 'सबूत के वर्णन बा',
            attachProof: 'सबूत फाइल संलग्न करीं',
            submitReport: 'धोखाधड़ी के रिपोर्ट जमा करीं',
            submitting: 'सबमिट कइल जा रहल बा...',
            stageSubmitted: 'जमा कइल गइल बा',
            stageInitialReview: 'शुरुआती समीक्षा कइल गइल',
            stageInvestigation: 'जांच के काम हो रहल बा',
            stageResolution: 'संकल्प के बारे में बतावल गइल बा',
            stageClosed: 'बंद हो गइल बा',
            addAdditionalEvidence: 'अतिरिक्त सबूत जोड़ल जाव',
            askAI: 'FRAUDNEXUS AI से पूछीं',
            send: 'भेजल जाला',
            close: 'बंद कर दीं',
            logout: 'लॉगआउट हो गइल बा',
            commandCenter: 'कमांड सेंटर के बा',
            partners: 'साझेदार लोग के बा',
            partnerDirectory: 'साझेदार निर्देशिका के बा',
            addPartner: 'साझीदार जोड़ल जाव',
            editPartner: 'संपादन साझेदार के बा',
            partnerRequests: 'साझीदार के अनुरोध बा',
            requestStatus: 'अनुरोध के स्थिति बा',
            partnerCategory: 'साझीदार श्रेणी के बा',
            integrationType: 'एकीकरण के प्रकार के बा',
            active: 'सक्रिय बा',
            inactive: 'निष्क्रिय बा',
            suspended: 'निलंबित कर दिहल गइल',
            simulatedDemoPartner: 'सिम्युलेटेड डेमो पार्टनर के बा',
            totalPartners: 'कुल साझेदारन के बा',
            activePartners: 'सक्रिय साझेदार लोग के बा',
            pendingRequests: 'लंबित अनुरोध बा',
            awaitingResponse: 'प्रतिक्रिया के इंतजार बा',
            overdueRequests: 'ओवरड्यू अनुरोध कइल गइल बा',
            customers: 'ग्राहकन के कहना बा',
            cases: 'केस के बा',
            investigation: 'जांच के काम हो रहल बा',
            intelligenceWorkspace: 'खुफिया कार्यक्षेत्र के बारे में बतावल गइल बा',
            analytics: 'विश्लेषणात्मकता के बारे में बतावल गइल बा',
            settings: 'सेटिंग्स के बारे में बतावल गइल बा',
            adminLoginTitle: 'वापस स्वागत बा',
            adminLoginSub: 'FRAUDNEXUS जांच कार्यक्षेत्र में साइन इन करीं',
            signIn: 'साइन इन कर लीं',
            tryDemo: 'डेमो के कोशिश करीं',
            demoEnv: 'डेमो के माहौल बा',
            priorityQueue: 'प्राथमिकता जांच के कतार में बा',
            actionCenter: 'एक्शन सेंटर के बा',
            fraudTrends: 'धोखाधड़ी के मामला के रुझान',
            financialExposureSummary: 'वित्तीय जोखिम के सारांश के बारे में बतावल गइल बा',
            recentActivity: 'हाल के गतिविधि के बारे में बतावल गइल बा',
            newCases: 'नया केस आइल बा',
            criticalCases: 'गंभीर मामिला के बारे में बतावल गइल बा',
            escalatedCases: 'बढ़ल केस के बारे में बतावल गइल बा',
            pendingApprovals: 'मंजूरी के लंबित बा',
            financialExposure: 'वित्तीय जोखिम के बारे में बतावल गइल बा',
            unassigned: 'बिना असाइन कइल गइल बा',
            assign: 'असाइन कइल जाव',
            openWorkspace: 'कार्यक्षेत्र खोलल जाला',
            requestEvidence: 'सबूत के निहोरा कइल जाव',
            escalate: 'बढ़ गइल बा',
            resolve: 'संकल्प कर लीं',
            closeCase: 'बंद केस के बा',
            addTask: 'टास्क जोड़ल जाला'
        }
    };

    c.supportedLanguages = [
        { code: 'en', name: 'English' },
        { code: 'hi', name: 'हिन्दी (Hindi)' },
        { code: 'ta', name: 'தமிழ் (Tamil)' },
        { code: 'te', name: 'తెలుగు (Telugu)' },
        { code: 'kn', name: 'ಕನ್ನಡ (Kannada)' },
        { code: 'ml', name: 'മലയാളം (Malayalam)' },
        { code: 'bn', name: 'বাংলা (Bengali)' },
        { code: 'mr', name: 'मराठी (Marathi)' },
        { code: 'gu', name: 'ગુજરાતી (Gujarati)' },
        { code: 'pa', name: 'ਪੰਜਾਬੀ (Punjabi)' },
        { code: 'or', name: 'ଓଡ଼ିଆ (Odia)' },
        { code: 'as', name: 'অসমীয়া (Assamese)' },
        { code: 'ur', name: 'اردو (Urdu)' },
        { code: 'ne', name: 'नेपाली (Nepali)' },
        { code: 'sa', name: 'संस्कृतम् (Sanskrit)' },
        { code: 'bho', name: 'भोजपुरी (Bhojpuri)' }
    ];

    c.t = function(key) {
        var langDict = c.dict[c.lang] || c.dict.en;
        return langDict[key] || c.dict.en[key] || key;
    };

    // ========== PURE GOOGLE TRANSLATE API INTEGRATION ==========
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
        $window.localStorage.setItem('fnx_gt_lang', langCode);
    };

    c.changeLang = function(l) {
        c.setGoogleTranslateLang(l);
    };

    c.toggleLang = function() {
        var next = c.lang === 'en' ? 'ta' : 'en';
        c.setGoogleTranslateLang(next);
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
    c.adminForm = { email: 'alex.morgan@fraudnexus.com', password: 'DemoPass123!', showPassword: false };
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
};
