"""
Script to inject the full 7-Step Report Fraud Workspace HTML and Enterprise CSS
into deploy_customer_experience_master.py.
"""
import re

with open('deploy_customer_experience_master.py', 'r', encoding='utf-8') as f:
    content = f.read()

# =========================================================================
# NEW REPORT FRAUD HTML WORKSPACE (Replacing lines 1445-1638)
# =========================================================================
new_template_section = r'''        <!-- 4C. REPORT FRAUD WIZARD / CASE REGISTRATION WORKSPACE -->
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

                        <!-- Financial Impact Section -->
                        <div class="fnx-subcard-section">
                            <div class="fnx-subcard-title">FINANCIAL IMPACT <span class="fnx-chip-customer-reported">Customer Reported</span></div>
                            <div class="fnx-field">
                                <label>Was your money lost?</label>
                                <select ng-model="c.reportForm.money_lost" ng-change="c.reportForm.financial_involvement = c.reportForm.money_lost">
                                    <option value="Yes">Yes</option>
                                    <option value="No">No</option>
                                    <option value="Not sure">Not sure</option>
                                </select>
                            </div>

                            <div ng-if="c.reportForm.money_lost === 'Yes'" class="fnx-form-grid-3">
                                <div class="fnx-field">
                                    <label>Estimated Amount Involved (₹)</label>
                                    <input type="number" ng-model="c.reportForm.exposure" ng-change="c.updateSeverity()" placeholder="e.g. 5000">
                                </div>
                                <div class="fnx-field">
                                    <label>Currency</label>
                                    <select ng-model="c.reportForm.currency">
                                        <option value="INR (₹)">INR (₹)</option>
                                        <option value="USD ($)">USD ($)</option>
                                        <option value="EUR (€)">EUR (€)</option>
                                        <option value="GBP (£)">GBP (£)</option>
                                    </select>
                                </div>
                                <div class="fnx-field">
                                    <label>Number of Transactions</label>
                                    <input type="number" ng-model="c.reportForm.num_transactions" min="1" placeholder="1">
                                </div>
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

                        <!-- Structured Financial Fields (when Yes) -->
                        <div ng-if="c.reportForm.financial_involvement === 'Yes'" class="fnx-financial-fields">
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

                            <div class="fnx-form-grid-3">
                                <div class="fnx-field">
                                    <label>{{c.t('amountInvolved')}} (₹)</label>
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
                        </div>

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

                        <!-- Quick Sample Evidence Helpers -->
                        <div class="fnx-quick-evidence-row">
                            <small>Quick Demo Attachments:</small>
                            <button type="button" class="fnx-btn-pill" ng-click="c.addSampleEvidence('Payment_Screenshot.png', 'Image', '1.4 MB')">+ Payment Screenshot</button>
                            <button type="button" class="fnx-btn-pill" ng-click="c.addSampleEvidence('Chat_Conversation.pdf', 'PDF', '520 KB')">+ Chat Transcript</button>
                            <button type="button" class="fnx-btn-pill" ng-click="c.addSampleEvidence('Bank_Statement.pdf', 'PDF', '2.1 MB')">+ Bank Statement</button>
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
                                    <span><strong>Legal Declaration:</strong> I confirm that the information provided is accurate and truthful to the best of my knowledge. I understand that submitting false fraud reports is punishable under applicable cybersecurity and financial crime legislation.</span>
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
        </div>'''

# Locate template section to replace
start_marker = r'<!-- 4C. REPORT FRAUD WIZARD VIEW -->'
end_marker = r'<!-- 4E. TRACK CASES VIEW -->'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

assert start_idx != -1, "start_marker not found"
assert end_idx != -1, "end_marker not found"

content = content[:start_idx] + new_template_section + "\n\n        " + content[end_idx:]

# =========================================================================
# NEW CSS ADDITIONS FOR 7-STEP REPORT FRAUD WORKSPACE
# =========================================================================
new_css = r"""
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
"""

# Append new_css into the css block
css_end_marker = '"""\n\nprint("--- Uploading Master Widget Components to ServiceNow ---")'
assert css_end_marker in content, "css_end_marker not found"

content = content.replace(css_end_marker, new_css + '\n' + css_end_marker, 1)

with open('deploy_customer_experience_master.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected template and CSS successfully into deploy_customer_experience_master.py!")
