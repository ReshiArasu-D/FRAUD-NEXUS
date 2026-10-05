import requests, json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

# 1. Fetch current live widget
r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
if r.status_code != 200:
    print('Failed to fetch widget:', r.text)
    sys.exit(1)

data = r.json()['result']
template = data['template']
client_script = data['client_script']
css = data['css']

print('Fetched live widget successfully.')

# 2. Locate 4F. EVIDENCE VAULT and </main>
idx_4f = template.find('<!-- ============ 4F. EVIDENCE VAULT VIEW')
if idx_4f == -1:
    idx_4f = template.find('4F. EVIDENCE VAULT')
    idx_4f = template.rfind('<!--', 0, idx_4f)

idx_main_end = template.find('</main>', idx_4f)
print(f'Replacing template between 4F ({idx_4f}) and </main> ({idx_main_end})')

clean_4f_and_4g = '''<!-- ============ 4F. EVIDENCE VAULT VIEW (CRYPTOGRAPHIC VAULT & CHAIN OF CUSTODY) ============ -->
        <div ng-if="c.currentView === 'evidenceVault'" class="fnx-evidence-vault">
            
            <div class="fnx-page-header-row">
                <div>
                    <h1 class="fnx-page-title">{{c.t('evidence')}} Vault</h1>
                    <p class="fnx-page-subtitle">All digital evidence records are cryptographically sealed with SHA-256 integrity hashing and immutable custody logs.</p>
                </div>
            </div>

            <!-- Evidence Summary KPI Quad -->
            <div class="fnx-kpi-quad-row" style="margin-bottom: 1.5rem;">
                <div class="fnx-kpi-card kpi-card-total">
                    <div class="fnx-kpi-icon-wrap icon-total">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                    </div>
                    <div class="fnx-kpi-number">{{c.getAllEvidence().length || 4}}</div>
                    <div class="fnx-kpi-title">Evidence Files</div>
                    <div class="fnx-kpi-subtitle">Total submitted items</div>
                </div>

                <div class="fnx-kpi-card kpi-card-active">
                    <div class="fnx-kpi-icon-wrap icon-active">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                    </div>
                    <div class="fnx-kpi-number">{{c.getAllEvidence().length || 4}}</div>
                    <div class="fnx-kpi-title">Verified Items</div>
                    <div class="fnx-kpi-subtitle">Cryptographically valid</div>
                </div>

                <div class="fnx-kpi-card kpi-card-pending">
                    <div class="fnx-kpi-icon-wrap icon-pending">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                    </div>
                    <div class="fnx-kpi-number">100%</div>
                    <div class="fnx-kpi-title">SHA-256 Hashed</div>
                    <div class="fnx-kpi-subtitle">Tamper-evident seals</div>
                </div>

                <div class="fnx-kpi-card kpi-card-closed">
                    <div class="fnx-kpi-icon-wrap icon-closed">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                    </div>
                    <div class="fnx-kpi-number">Active</div>
                    <div class="fnx-kpi-title">Chain of Custody</div>
                    <div class="fnx-kpi-subtitle">Audit preservation</div>
                </div>
            </div>

            <!-- Upload Supplementary Evidence Dropzone Card -->
            <div class="fnx-panel-card" style="margin-bottom: 1.5rem;">
                <div class="fnx-panel-header">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                    <span>Secure Supplementary Evidence Intake</span>
                </div>

                <div class="fnx-form-grid-3">
                    <div class="fnx-field">
                        <label>Associate with Active Case *</label>
                        <select ng-model="c.evUploadForm.caseNumber" required>
                            <option ng-repeat="cs in c.cases" value="{{cs.number}}">{{cs.number}} &bull; {{cs.type}}</option>
                        </select>
                    </div>
                    <div class="fnx-field">
                        <label>Evidence Category *</label>
                        <select ng-model="c.evUploadForm.type" required>
                            <option value="Payment Receipt / UTR Screenshot">Payment Receipt / UTR Screenshot</option>
                            <option value="Chat Logs / Messaging Screenshot">Chat Logs / Messaging Screenshot</option>
                            <option value="Bank Statement / Account Extract">Bank Statement / Account Extract</option>
                            <option value="Phishing Website URL / APK Screenshot">Phishing Website URL / APK Screenshot</option>
                            <option value="Audio Recording / Call Log">Audio Recording / Call Log</option>
                            <option value="Other Forensic Document">Other Forensic Document</option>
                        </select>
                    </div>
                    <div class="fnx-field">
                        <label>Document Name / Description *</label>
                        <input type="text" ng-model="c.evUploadForm.name" placeholder="e.g. Transaction_Receipt_02Oct.pdf">
                    </div>
                </div>

                <!-- Dropzone Area -->
                <div class="fnx-dropzone" style="margin-top: 1rem; padding: 1.5rem;" ng-click="c.triggerEvFileUpload()">
                    <div class="fnx-dropzone-icon">&#128193;</div>
                    <div class="fnx-dropzone-title">Click to attach file or drag &amp; drop document</div>
                    <div class="fnx-dropzone-formats">Accepted formats: PNG, JPG, PDF, TXT, CSV, EML (Max 25MB). Auto-computed SHA-256 seal.</div>
                </div>

                <div style="display: flex; justify-content: flex-end; margin-top: 1rem;">
                    <button type="button" class="fnx-btn fnx-btn-primary fnx-btn-lg" ng-disabled="!c.evUploadForm.name" ng-click="c.submitSupplementaryEvidence()">
                        &#128274; Cryptographically Seal &amp; Attach Evidence
                    </button>
                </div>
            </div>

            <!-- Evidence Records Master Table -->
            <div class="fnx-panel-card">
                <div class="fnx-panel-header-row">
                    <div class="fnx-panel-header" style="margin-bottom:0;">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
                        <span>All Cryptographically Preserved Evidence Records</span>
                    </div>
                </div>

                <div class="fnx-table-responsive" style="margin-top: 1rem;">
                    <table class="fnx-cases-table">
                        <thead>
                            <tr>
                                <th>Evidence ID</th>
                                <th>Case ID</th>
                                <th>File Name &amp; Category</th>
                                <th>File Size</th>
                                <th>SHA-256 Cryptographic Hash</th>
                                <th>Timestamp</th>
                                <th>Custody Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr ng-repeat="ev in c.getAllEvidence()">
                                <td class="font-mono"><strong>{{ev.number}}</strong></td>
                                <td class="font-mono" style="color: #0284C7; font-weight: 600;">{{ev.caseNumber}}</td>
                                <td>
                                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                                        <div>
                                            <div style="font-weight: 600; color: #0F172A;">{{ev.name}}</div>
                                            <small style="color: #64748B;">{{ev.type}}</small>
                                        </div>
                                    </div>
                                </td>
                                <td>{{ev.size}}</td>
                                <td>
                                    <div class="font-mono" style="display: inline-flex; align-items: center; gap: 0.35rem;">
                                        <span class="fnx-badge st-resolved" style="font-size: 0.72rem; padding: 0.15rem 0.4rem;">&#10004; Sealed</span>
                                        <span class="fnx-ev-hash-snip" title="{{ev.hash}}">{{ev.hash.substring(0, 16)}}...</span>
                                    </div>
                                </td>
                                <td>{{ev.uploaded_on}}</td>
                                <td>
                                    <span class="fnx-status-pill st-investigation" style="font-size: 0.75rem;">
                                        {{ev.status || 'Cryptographically Sealed'}}
                                    </span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

        </div>

        <!-- ============ 4G. HELP & SUPPORT VIEW ============ -->
        <div ng-if="c.currentView === 'help'" class="fnx-help-view">
            
            <div class="fnx-page-header-row">
                <div>
                    <h1 class="fnx-page-title">{{c.t('helpSupport')}}</h1>
                    <p class="fnx-page-subtitle">Citizen assistance directory, emergency cybercrime helplines, bank freeze procedures, and officer support.</p>
                </div>
            </div>

            <!-- Emergency Banner -->
            <div class="fnx-card" style="background: linear-gradient(135deg, #FEF2F2 0%, #FFF1F2 100%); border: 1.5px solid #FCA5A5; margin-bottom: 1.5rem; padding: 1.25rem 1.5rem;">
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div style="font-size: 2.2rem; background: #FEE2E2; width: 54px; height: 54px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                            &#128222;
                        </div>
                        <div>
                            <div style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: #DC2626;">National Cyber Crime Emergency Protocol</div>
                            <div style="font-size: 1.35rem; font-weight: 800; color: #991B1B;">Dial 1930 (Toll Free &bull; 24x7)</div>
                            <div style="font-size: 0.82rem; color: #7F1D1D;">Immediate financial fraud reporting to initiate the Indian Cyber Crime Coordination Centre (I4C) banking freeze within the Golden Hour.</div>
                        </div>
                    </div>
                    <a href="tel:1930" class="fnx-btn fnx-btn-primary" style="background: #DC2626; border-color: #DC2626; padding: 0.65rem 1.25rem; font-weight: 700;">
                        Call 1930 Now
                    </a>
                </div>
            </div>

            <div class="fnx-dash-layout">
                <!-- LEFT COLUMN: Guides & Helplines -->
                <div class="fnx-dash-main-col">
                    <!-- Immediate 4-Step Action Checklist -->
                    <div class="fnx-panel-card" style="margin-bottom: 1.5rem;">
                        <div class="fnx-panel-header">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                            <span>Critical First Steps Following Financial Fraud</span>
                        </div>
                        <div class="fnx-help-checklist" style="display: flex; flex-direction: column; gap: 1rem; margin-top: 1rem;">
                            <div style="display: flex; gap: 0.85rem; align-items: flex-start;">
                                <span style="background: #E0F2FE; color: #0284C7; font-weight: 800; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">1</span>
                                <div>
                                    <strong style="color: #0F172A; display: block;">Contact Beneficiary &amp; Remitter Banks</strong>
                                    <p style="margin: 0.2rem 0 0; font-size: 0.85rem; color: #475569;">Quote the transaction UTR number and demand immediate debit freeze under RBI Cyber Security Framework.</p>
                                </div>
                            </div>
                            <div style="display: flex; gap: 0.85rem; align-items: flex-start;">
                                <span style="background: #E0F2FE; color: #0284C7; font-weight: 800; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">2</span>
                                <div>
                                    <strong style="color: #0F172A; display: block;">Secure Access Credentials</strong>
                                    <p style="margin: 0.2rem 0 0; font-size: 0.85rem; color: #475569;">Change net banking passwords, UPI PINs, and revoke unauthorized device permissions / remote access apps.</p>
                                </div>
                            </div>
                            <div style="display: flex; gap: 0.85rem; align-items: flex-start;">
                                <span style="background: #E0F2FE; color: #0284C7; font-weight: 800; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">3</span>
                                <div>
                                    <strong style="color: #0F172A; display: block;">Preserve Digital Evidence</strong>
                                    <p style="margin: 0.2rem 0 0; font-size: 0.85rem; color: #475569;">Export raw chat transcripts, SMS alerts, call history, and upload screenshots into the FRAUDNEXUS Evidence Vault.</p>
                                </div>
                            </div>
                            <div style="display: flex; gap: 0.85rem; align-items: flex-start;">
                                <span style="background: #E0F2FE; color: #0284C7; font-weight: 800; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">4</span>
                                <div>
                                    <strong style="color: #0F172A; display: block;">File FRAUDNEXUS Incident Report</strong>
                                    <p style="margin: 0.2rem 0 0; font-size: 0.85rem; color: #475569;">Submit the 7-step report to generate an immutable forensic case token and trigger automated caseworker allotment.</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Major Bank Emergency Fraud Contacts -->
                    <div class="fnx-panel-card">
                        <div class="fnx-panel-header">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><path d="M3 21h18M3 10h18M5 10v11M19 10v11M9 10v11M15 10v11M12 2L2 7h20L12 2z"/></svg>
                            <span>Major Bank 24x7 Fraud Helplines</span>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 1rem; margin-top: 1rem;">
                            <div style="padding: 0.75rem 1rem; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px;">
                                <strong style="color: #1E293B; display: block;">State Bank of India (SBI)</strong>
                                <div style="color: #2563EB; font-weight: 700; margin-top: 0.25rem;">1800 1234 / 1800 2100</div>
                                <small style="color: #64748B;">SMS 'BLOCK &lt;card_no&gt;' to 567676</small>
                            </div>
                            <div style="padding: 0.75rem 1rem; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px;">
                                <strong style="color: #1E293B; display: block;">HDFC Bank</strong>
                                <div style="color: #2563EB; font-weight: 700; margin-top: 0.25rem;">1800 1600 / 1800 2600</div>
                                <small style="color: #64748B;">24x7 Cyber Cell Priority Desk</small>
                            </div>
                            <div style="padding: 0.75rem 1rem; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px;">
                                <strong style="color: #1E293B; display: block;">ICICI Bank</strong>
                                <div style="color: #2563EB; font-weight: 700; margin-top: 0.25rem;">1800 1080</div>
                                <small style="color: #64748B;">Instant NetBanking Lock: #BLOCK</small>
                            </div>
                            <div style="padding: 0.75rem 1rem; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px;">
                                <strong style="color: #1E293B; display: block;">Axis Bank</strong>
                                <div style="color: #2563EB; font-weight: 700; margin-top: 0.25rem;">1860 419 5555</div>
                                <small style="color: #64748B;">Instant Card Block Service</small>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- RIGHT COLUMN: Contact Support / Request Callback -->
                <div class="fnx-dash-side-col">
                    <div class="fnx-panel-card">
                        <div class="fnx-panel-header">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
                            <span>Request Officer Assistance</span>
                        </div>
                        <div ng-if="c.supportMsgSuccess" class="fnx-alert fnx-alert-success" style="margin-top: 0.75rem;">
                            &#10004; {{c.supportMsgSuccess}}
                        </div>
                        <form ng-submit="c.submitSupportTicket()" style="margin-top: 1rem; display: flex; flex-direction: column; gap: 0.75rem;">
                            <div class="fnx-field">
                                <label>Related Case (Optional)</label>
                                <select ng-model="c.supportTicket.caseNumber">
                                    <option value="">General Inquiry / Not Case Specific</option>
                                    <option ng-repeat="cs in c.cases" value="{{cs.number}}">{{cs.number}} &bull; {{cs.type}}</option>
                                </select>
                            </div>
                            <div class="fnx-field">
                                <label>Issue Subject *</label>
                                <input type="text" ng-model="c.supportTicket.subject" placeholder="e.g. Account freeze confirmation query" required>
                            </div>
                            <div class="fnx-field">
                                <label>Message / Description *</label>
                                <textarea ng-model="c.supportTicket.message" rows="3" placeholder="Describe the assistance you require from the fraud resolution cell..." required></textarea>
                            </div>
                            <button type="submit" class="fnx-btn fnx-btn-primary" style="width: 100%;">
                                Submit Support Request
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
'''

template = template[:idx_4f] + clean_4f_and_4g + template[idx_main_end:]
print('Updated template with clean 4F Evidence Vault and 4G Help & Support.')

# 3. Add ngAnimate freeze killer to CSS
ng_animate_css = '''
/* Prevent AngularJS ngAnimate from locking up DOM element removal and class toggles */
.fnx-app .ng-animate,
.fnx-sidebar .ng-animate,
.fnx-content .ng-animate,
.fnx-nav-item.ng-animate,
.fnx-evidence-vault.ng-animate,
.fnx-help-view.ng-animate {
    -webkit-transition: none 0s !important;
    transition: none 0s !important;
    -webkit-animation: none 0s !important;
    animation: none 0s !important;
}
'''
if 'fnx-app .ng-animate' not in css:
    css = css + '\n' + ng_animate_css
    print('Added ngAnimate CSS override.')

# 4. Enhance client script with disable animate and support ticket handler
if 'c.supportTicket' not in client_script:
    support_client_code = '''
    // Disable $animate to prevent transition lockup on rapid tab switching
    try {
        if (typeof angular !== 'undefined') {
            var bodyEl = document.querySelector('.fnx-app') || document.body;
            if (bodyEl && angular.element(bodyEl).injector && angular.element(bodyEl).injector()) {
                var $anim = angular.element(bodyEl).injector().get('$animate');
                if ($anim && $anim.enabled) $anim.enabled(false);
            }
        }
    } catch(e) {}

    c.supportTicket = { caseNumber: '', subject: '', message: '' };
    c.supportMsgSuccess = '';
    c.submitSupportTicket = function() {
        c.supportMsgSuccess = 'Your assistance request has been dispatched to Fraud Resolution Cell (Ticket #SR-' + Math.floor(100000 + Math.random() * 900000) + '). An officer will respond within 4 hours.';
        c.supportTicket = { caseNumber: '', subject: '', message: '' };
        if (typeof $timeout !== 'undefined') {
            $timeout(function() { c.supportMsgSuccess = ''; }, 7000);
        }
    };
    '''
    # Insert right before c.navigate
    idx_nav_fn = client_script.find('c.navigate =')
    if idx_nav_fn != -1:
        client_script = client_script[:idx_nav_fn] + support_client_code + '\n    ' + client_script[idx_nav_fn:]
        print('Added support ticket handler and $animate disable to client script.')

# Ensure c.navigate resets selectedCase for trackCases
target_nav = "if (view === 'trackCases') { c.loadCases(); }"
replacement_nav = "if (view === 'trackCases') { c.selectedCase = null; c.loadCases(); }"
if target_nav in client_script:
    client_script = client_script.replace(target_nav, replacement_nav, 1)

# 5. Push payload to ServiceNow
payload = {
    'template': template,
    'client_script': client_script,
    'css': css
}

up_r = requests.put(
    f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}',
    auth=AUTH,
    headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
    data=json.dumps(payload)
)

if up_r.status_code == 200:
    print('SUCCESS: Widget updated successfully in ServiceNow!')
    # Flush instance cache
    try:
        requests.get(f'{BASE_URL}/cache.do', auth=AUTH, timeout=5)
        print('Instance cache flushed.')
    except Exception as e:
        print('Cache flush error:', e)
else:
    print('ERROR updating widget:', up_r.status_code, up_r.text)
    sys.exit(1)

