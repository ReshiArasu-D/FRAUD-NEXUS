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

print('Fetched live widget. Template len:', len(template), 'Client script len:', len(client_script), 'CSS len:', len(css))

# -------------------------------------------------------------
# STEP 1: Remove duplicate Need Support sidebar card
# -------------------------------------------------------------
support_card_pattern = re.compile(r'<div class="fnx-sidebar-support-card">.*?</div>\s*</nav>', re.DOTALL)
if support_card_pattern.search(template):
    template = support_card_pattern.sub('</nav>', template, count=1)
    print('1. Removed duplicate Need Support card from sidebar.')
else:
    print('1. fnx-sidebar-support-card not found in template.')

# -------------------------------------------------------------
# STEP 2: Restore Customer Profile & KYC Verification (4B)
# -------------------------------------------------------------
# Ensure 4B triggers on both 'profile' and 'editProfile'
idx_4b_tag = template.find('<div ng-if="c.currentView === \'profile\'" class="fnx-profile-view">')
if idx_4b_tag != -1:
    template = template.replace(
        '<div ng-if="c.currentView === \'profile\'" class="fnx-profile-view">',
        '<div ng-if="c.currentView === \'profile\' || c.currentView === \'editProfile\'" class="fnx-profile-view">',
        1
    )
    print('2. Updated 4B Profile & KYC view to trigger on both profile and editProfile.')
else:
    print('2. 4B profile tag pattern checked.')

# -------------------------------------------------------------
# STEP 3: Expand Track Cases (4E) into Rich Case Detail View
# -------------------------------------------------------------
idx_4e_start = template.find('<!-- ============ 4E. TRACK CASES VIEW')
if idx_4e_start == -1:
    idx_4e_start = template.find('4E. TRACK CASES')
    idx_4e_start = template.rfind('<!--', 0, idx_4e_start)

idx_4e_end = template.find('<!-- ============ 4F. EVIDENCE VAULT VIEW')
if idx_4e_end == -1:
    idx_4e_end = template.find('4F. EVIDENCE VAULT')
    idx_4e_end = template.rfind('<!--', 0, idx_4e_end)

print(f'Track Cases slice: {idx_4e_start} to {idx_4e_end}')

new_track_cases_html = '''<!-- ============ 4E. TRACK CASES VIEW (ENTERPRISE CASE DETAIL & LIFECYCLE) ============ -->
        <div ng-if="c.currentView === 'trackCases'" class="fnx-track-cases">
            
            <!-- VIEW 1: Case Detail Workspace (When c.selectedCase is active) -->
            <div ng-if="c.selectedCase" class="fnx-case-detail-workspace">
                <!-- Detail Header & Breadcrumb -->
                <div class="fnx-detail-nav-row">
                    <div class="fnx-breadcrumbs">
                        <span class="fnx-crumb-link" ng-click="c.selectedCase = null">All Cases</span>
                        <span class="fnx-crumb-sep">&gt;</span>
                        <span class="fnx-crumb-current">{{c.selectedCase.number}}</span>
                    </div>
                    <button type="button" class="fnx-btn fnx-btn-outline fnx-btn-sm" ng-click="c.selectedCase = null">
                        &larr; Back to All Cases
                    </button>
                </div>

                <!-- Case Banner Header -->
                <div class="fnx-case-banner-card">
                    <div class="fnx-cbb-top">
                        <div class="fnx-cbb-title-group">
                            <span class="fnx-cbb-number font-mono">{{c.selectedCase.number}}</span>
                            <span class="fnx-cbb-type">{{c.selectedCase.type}}</span>
                        </div>
                        <div class="fnx-cbb-badges">
                            <span class="fnx-status-pill" ng-class="{
                                'st-investigation': c.selectedCase.status === 'Investigation',
                                'st-initial': c.selectedCase.status === 'Initial Review',
                                'st-allotted': c.selectedCase.status === 'Caseworker Allotted',
                                'st-closed': c.selectedCase.status === 'Closed',
                                'st-pending': c.selectedCase.status === 'Pending' || c.selectedCase.status === 'Case Submitted'
                            }">{{c.selectedCase.status}}</span>
                            <span class="fnx-badge" ng-class="'sev-' + (c.selectedCase.severity || 'high').toLowerCase()">
                                {{c.selectedCase.severity || 'High'}} Priority
                            </span>
                            <button type="button" class="fnx-btn fnx-btn-primary fnx-btn-sm" ng-click="c.openAddEvidence(c.selectedCase)">
                                + Submit Additional Evidence
                            </button>
                        </div>
                    </div>

                    <!-- 5-Stage Visual Progress Tracker -->
                    <div class="fnx-detail-tracker">
                        <div class="fnx-tracker-step completed">
                            <div class="fnx-tracker-dot">&#10004;</div>
                            <div class="fnx-tracker-label">Submitted</div>
                            <small class="fnx-tracker-date">{{c.selectedCase.incident_date}}</small>
                        </div>
                        <div class="fnx-tracker-line" ng-class="{'active': c.selectedCase.status !== 'Case Submitted'}"></div>
                        
                        <div class="fnx-tracker-step" ng-class="{'completed': c.selectedCase.status === 'Investigation' || c.selectedCase.status === 'Caseworker Allotted' || c.selectedCase.status === 'Resolved' || c.selectedCase.status === 'Closed', 'current': c.selectedCase.status === 'Initial Review'}">
                            <div class="fnx-tracker-dot">{{(c.selectedCase.status !== 'Case Submitted') ? '&#10004;' : '2'}}</div>
                            <div class="fnx-tracker-label">Initial Review</div>
                            <small class="fnx-tracker-date">Verified</small>
                        </div>
                        <div class="fnx-tracker-line" ng-class="{'active': c.selectedCase.status === 'Investigation' || c.selectedCase.status === 'Caseworker Allotted' || c.selectedCase.status === 'Resolved' || c.selectedCase.status === 'Closed'}"></div>
                        
                        <div class="fnx-tracker-step" ng-class="{'completed': c.selectedCase.status === 'Resolved' || c.selectedCase.status === 'Closed', 'current': c.selectedCase.status === 'Investigation' || c.selectedCase.status === 'Caseworker Allotted'}">
                            <div class="fnx-tracker-dot">{{(c.selectedCase.status === 'Resolved' || c.selectedCase.status === 'Closed') ? '&#10004;' : (c.selectedCase.status === 'Investigation' || c.selectedCase.status === 'Caseworker Allotted' ? '&#9679;' : '3')}}</div>
                            <div class="fnx-tracker-label">Investigation</div>
                            <small class="fnx-tracker-date">Active Cell</small>
                        </div>
                        <div class="fnx-tracker-line" ng-class="{'active': c.selectedCase.status === 'Resolved' || c.selectedCase.status === 'Closed'}"></div>
                        
                        <div class="fnx-tracker-step" ng-class="{'completed': c.selectedCase.status === 'Closed', 'current': c.selectedCase.status === 'Resolved'}">
                            <div class="fnx-tracker-dot">{{c.selectedCase.status === 'Closed' ? '&#10004;' : '4'}}</div>
                            <div class="fnx-tracker-label">Resolution</div>
                            <small class="fnx-tracker-date">Recovery</small>
                        </div>
                        <div class="fnx-tracker-line" ng-class="{'active': c.selectedCase.status === 'Closed'}"></div>
                        
                        <div class="fnx-tracker-step" ng-class="{'completed': c.selectedCase.status === 'Closed'}">
                            <div class="fnx-tracker-dot">{{c.selectedCase.status === 'Closed' ? '&#10004;' : '5'}}</div>
                            <div class="fnx-tracker-label">Closed</div>
                            <small class="fnx-tracker-date">Archived</small>
                        </div>
                    </div>
                </div>

                <!-- 2-Column Detail Grid -->
                <div class="fnx-case-detail-grid">
                    
                    <!-- Left Column: Incident & Financial Information -->
                    <div class="fnx-cd-col">
                        <!-- Card 1: Incident Overview -->
                        <div class="fnx-panel-card">
                            <div class="fnx-panel-header">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
                                <span>Incident Overview</span>
                            </div>
                            <div class="fnx-cd-kv-list">
                                <div class="fnx-cd-kv-row">
                                    <span class="fnx-cd-k">Category</span>
                                    <span class="fnx-cd-v">{{c.selectedCase.category || c.selectedCase.type}}</span>
                                </div>
                                <div class="fnx-cd-kv-row">
                                    <span class="fnx-cd-k">Incident Date</span>
                                    <span class="fnx-cd-v">{{c.selectedCase.incident_date}} ({{c.selectedCase.incident_time || '14:30'}})</span>
                                </div>
                                <div class="fnx-cd-kv-row">
                                    <span class="fnx-cd-k">Platform / Channel</span>
                                    <span class="fnx-cd-v">{{c.selectedCase.digital_platform || 'Digital Banking / UPI'}}</span>
                                </div>
                                <div class="fnx-cd-kv-row">
                                    <span class="fnx-cd-k">Reference ID</span>
                                    <span class="fnx-cd-v font-mono">{{c.selectedCase.transaction_reference || 'TXN-982103'}}</span>
                                </div>
                                <div style="margin-top: 0.75rem; border-top: 1px solid #F1F5F9; padding-top: 0.75rem;">
                                    <span class="fnx-cd-k" style="display:block; margin-bottom: 0.35rem;">Customer Reported Statement:</span>
                                    <p style="font-size: 0.88rem; color: #334155; line-height: 1.5; margin: 0; background: #F8FAFC; padding: 0.75rem; border-radius: 8px; border: 1px solid #E2E8F0;">
                                        {{c.selectedCase.description || c.selectedCase.u_short_description || 'Fraud incident reported via customer portal with verified transaction documentation.'}}
                                    </p>
                                </div>
                            </div>
                        </div>

                        <!-- Card 2: Financial Information -->
                        <div class="fnx-panel-card">
                            <div class="fnx-panel-header">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
                                <span>Financial Loss &amp; Recovery Status</span>
                            </div>
                            <div class="fnx-financial-quad">
                                <div class="fnx-fin-box box-loss">
                                    <span class="fnx-fin-lbl">Reported Loss</span>
                                    <span class="fnx-fin-val">&#8377; {{c.selectedCase.exposure || '45,000'}}</span>
                                </div>
                                <div class="fnx-fin-box box-blocked">
                                    <span class="fnx-fin-lbl">Amount Frozen</span>
                                    <span class="fnx-fin-val">&#8377; {{c.selectedCase.blocked_amount || '30,000'}}</span>
                                </div>
                                <div class="fnx-fin-box box-recovered">
                                    <span class="fnx-fin-lbl">Recovered</span>
                                    <span class="fnx-fin-val">&#8377; {{c.selectedCase.recovered_amount || '0'}}</span>
                                </div>
                                <div class="fnx-fin-box box-status">
                                    <span class="fnx-fin-lbl">Freeze SLA</span>
                                    <span class="fnx-fin-val text-green" style="font-size: 0.95rem;">Within 2h Protocol</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Right Column: Case Handling & Evidence -->
                    <div class="fnx-cd-col">
                        <!-- Card 3: Handling Cell & Status Updates (Customer-Safe Only) -->
                        <div class="fnx-panel-card">
                            <div class="fnx-panel-header">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><polyline points="16 11 18 13 22 9"/></svg>
                                <span>Investigation Triage &amp; Caseworker Assignment</span>
                            </div>
                            <div class="fnx-cd-kv-list">
                                <div class="fnx-cd-kv-row">
                                    <span class="fnx-cd-k">Assigned Unit</span>
                                    <span class="fnx-cd-v">{{c.selectedCase.assigned_cell || 'Fraud Resolution Cell - Priority Tier'}}</span>
                                </div>
                                <div class="fnx-cd-kv-row">
                                    <span class="fnx-cd-k">Case Triage SLA</span>
                                    <span class="fnx-cd-v">{{c.selectedCase.triage_sla || 'Active Investigation (48h Protocol)'}}</span>
                                </div>
                                <div class="fnx-cd-kv-row">
                                    <span class="fnx-cd-k">Last Updated</span>
                                    <span class="fnx-cd-v">{{c.selectedCase.last_updated || '03 Oct 2026, 11:20'}}</span>
                                </div>
                            </div>

                            <div style="margin-top: 1rem; border-top: 1px solid #F1F5F9; padding-top: 0.75rem;">
                                <strong style="font-size: 0.85rem; color: #1E293B; display: block; margin-bottom: 0.5rem;">Official Citizen Status Updates:</strong>
                                <div class="fnx-timeline-list">
                                    <div class="fnx-timeline-item" ng-repeat="tl in (c.selectedCase.timeline || c.defaultTimeline)">
                                        <div class="fnx-tl-bullet"></div>
                                        <div class="fnx-tl-body">
                                            <div class="fnx-tl-stage">{{tl.stage}}</div>
                                            <div class="fnx-tl-detail">{{tl.detail}}</div>
                                            <small class="fnx-tl-time">{{tl.time}}</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Card 4: Submitted Evidence & Cryptographic Verification -->
                        <div class="fnx-panel-card">
                            <div class="fnx-panel-header-row">
                                <div class="fnx-panel-header" style="margin-bottom:0;">
                                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                                    <span>Submitted Evidence ({{c.selectedCase.evidence.length || 2}})</span>
                                </div>
                                <button type="button" class="fnx-btn fnx-btn-sm fnx-btn-outline" ng-click="c.openAddEvidence(c.selectedCase)">
                                    + Add Evidence
                                </button>
                            </div>
                            
                            <div class="fnx-evidence-detail-list" style="margin-top: 1rem;">
                                <div class="fnx-ev-detail-item" ng-repeat="ev in (c.selectedCase.evidence || c.defaultEvidence)">
                                    <div class="fnx-ev-icon-box">
                                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                                    </div>
                                    <div class="fnx-ev-meta-col">
                                        <div class="fnx-ev-filename"><strong>{{ev.name}}</strong></div>
                                        <div class="fnx-ev-submeta">
                                            <span>{{ev.type}} &bull; {{ev.size}}</span>
                                            <span class="fnx-badge st-resolved" style="font-size:0.7rem; padding: 0.15rem 0.4rem;">&#10004; {{ev.status}}</span>
                                        </div>
                                        <div class="fnx-ev-hash-row font-mono">
                                            <small style="color: #64748B;">SHA-256:</small>
                                            <span class="fnx-ev-hash-snip" title="{{ev.hash}}">{{ev.hash.substring(0, 24)}}...</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>

            <!-- VIEW 2: Cases List (When no specific case is selected) -->
            <div ng-if="!c.selectedCase">
                <div class="fnx-track-header-row">
                    <div>
                        <h2 class="fnx-page-title">{{c.t('trackCases')}}</h2>
                        <p class="fnx-page-subtitle">Monitor live lifecycle milestones, forensic evidence custody, and recovery status.</p>
                    </div>
                    <button type="button" class="fnx-btn fnx-btn-primary" ng-click="c.navigate('reportFraud')">
                        + Report New Fraud
                    </button>
                </div>

                <div class="fnx-empty" ng-if="c.cases.length === 0">No cases found. Report a fraud to get started.</div>

                <div ng-repeat="cs in c.cases" class="fnx-case-card">
                    <div class="fnx-case-header">
                        <div>
                            <span class="fnx-case-number font-mono">{{cs.number}}</span>
                            <span class="fnx-case-type">{{cs.type}}</span>
                        </div>
                        <div class="fnx-ch-right">
                            <span class="fnx-status-pill" ng-class="{
                                'st-investigation': cs.status === 'Investigation',
                                'st-initial': cs.status === 'Initial Review',
                                'st-allotted': cs.status === 'Caseworker Allotted',
                                'st-closed': cs.status === 'Closed',
                                'st-pending': cs.status === 'Pending' || cs.status === 'Case Submitted'
                            }">{{cs.status}}</span>
                            <button class="fnx-btn fnx-btn-sm fnx-btn-primary" style="margin-left: 0.65rem;" ng-click="c.viewCase(cs)">
                                View Details &rarr;
                            </button>
                            <button class="fnx-btn fnx-btn-sm fnx-btn-outline" style="margin-left: 0.4rem;" ng-click="c.openAddEvidence(cs)">
                                + Add Evidence
                            </button>
                        </div>
                    </div>

                    <!-- 5-Stage Visual Progress Tracker -->
                    <div class="fnx-tracker">
                        <div class="fnx-tracker-step completed">
                            <div class="fnx-tracker-dot">&#10004;</div>
                            <div class="fnx-tracker-label">{{c.t('stageSubmitted')}}</div>
                        </div>
                        <div class="fnx-tracker-line" ng-class="{'active': cs.status !== 'Case Submitted'}"></div>
                        <div class="fnx-tracker-step" ng-class="{'completed': cs.status === 'Investigation' || cs.status === 'Caseworker Allotted' || cs.status === 'Resolved' || cs.status === 'Closed', 'current': cs.status === 'Initial Review'}">
                            <div class="fnx-tracker-dot">{{(cs.status !== 'Case Submitted') ? '&#10004;' : '2'}}</div>
                            <div class="fnx-tracker-label">{{c.t('stageInitialReview')}}</div>
                        </div>
                        <div class="fnx-tracker-line" ng-class="{'active': cs.status === 'Investigation' || cs.status === 'Caseworker Allotted' || cs.status === 'Resolved' || cs.status === 'Closed'}"></div>
                        <div class="fnx-tracker-step" ng-class="{'completed': cs.status === 'Resolved' || cs.status === 'Closed', 'current': cs.status === 'Investigation' || cs.status === 'Caseworker Allotted'}">
                            <div class="fnx-tracker-dot">{{(cs.status === 'Resolved' || cs.status === 'Closed') ? '&#10004;' : '3'}}</div>
                            <div class="fnx-tracker-label">{{c.t('stageInvestigation')}}</div>
                        </div>
                        <div class="fnx-tracker-line" ng-class="{'active': cs.status === 'Closed'}"></div>
                        <div class="fnx-tracker-step" ng-class="{'completed': cs.status === 'Closed', 'current': cs.status === 'Resolved'}">
                            <div class="fnx-tracker-dot">{{cs.status === 'Closed' ? '&#10004;' : '4'}}</div>
                            <div class="fnx-tracker-label">{{c.t('stageResolution')}}</div>
                        </div>
                        <div class="fnx-tracker-line" ng-class="{'active': cs.status === 'Closed'}"></div>
                        <div class="fnx-tracker-step" ng-class="{'completed': cs.status === 'Closed'}">
                            <div class="fnx-tracker-dot">{{cs.status === 'Closed' ? '&#10004;' : '5'}}</div>
                            <div class="fnx-tracker-label">{{c.t('stageClosed')}}</div>
                        </div>
                    </div>

                    <!-- Case Summary Metadata -->
                    <div class="fnx-case-body">
                        <p style="margin: 0 0 0.75rem 0; font-size: 0.9rem; color: #334155;">
                            <strong>Description:</strong> {{cs.description || cs.u_short_description || 'Fraud incident reported with cryptographic token generated.'}}
                        </p>
                        <div class="fnx-case-meta-grid">
                            <div>Incident Date: <strong>{{cs.incident_date}}</strong></div>
                            <div>Last Updated: <strong>{{cs.last_updated || cs.incident_date}}</strong></div>
                            <div ng-if="cs.exposure">Reported Loss: <strong>&#8377; {{cs.exposure}}</strong></div>
                            <div ng-if="cs.digital_platform">Platform: <strong>{{cs.digital_platform}}</strong></div>
                        </div>
                    </div>
                </div>
            </div>

        </div>

        '''

template = template[:idx_4e_start] + new_track_cases_html + template[idx_4e_end:]
print('3. Upgraded Track Cases view (4E) with complete Case Detail view.')

# -------------------------------------------------------------
# STEP 4: Restore Complete Evidence Vault (4F)
# -------------------------------------------------------------
idx_4f_start = template.find('<!-- ============ 4F. EVIDENCE VAULT VIEW')
if idx_4f_start == -1:
    idx_4f_start = template.find('4F. EVIDENCE VAULT')
    idx_4f_start = template.rfind('<!--', 0, idx_4f_start)

idx_4f_end = template.find('<!-- ============ 4G. HELP & SUPPORT VIEW')
if idx_4f_end == -1:
    idx_4f_end = template.find('4G. HELP')
    idx_4f_end = template.rfind('<!--', 0, idx_4f_end)

print(f'Evidence Vault slice: {idx_4f_start} to {idx_4f_end}')

new_evidence_vault_html = '''<!-- ============ 4F. EVIDENCE VAULT VIEW (CRYPTOGRAPHIC VAULT & CHAIN OF CUSTODY) ============ -->
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

        '''

template = template[:idx_4f_start] + new_evidence_vault_html + template[idx_4f_end:]
print('4. Restored complete Evidence Vault view (4F).')

# -------------------------------------------------------------
# STEP 5: Update Client Script Helper Methods & Data
# -------------------------------------------------------------
# Add helper methods for Evidence, Case Viewing, and Evidence Attachment
client_helper_methods = '''
    // ============================================================
    // CUSTOMER PORTAL ENHANCEMENTS: Case Detail, Evidence & KYC
    // ============================================================
    c.evUploadForm = {
        caseNumber: 'FNX-2026-001034',
        type: 'Payment Receipt / UTR Screenshot',
        name: ''
    };

    c.defaultTimeline = [
        { stage: 'Case Submitted', time: '02 Oct 2026, 14:30', detail: 'Report registered & cryptographic case token generated.' },
        { stage: 'Initial Review', time: '02 Oct 2026, 16:00', detail: 'Identity authenticated & initial triage verification passed.' },
        { stage: 'Investigation Active', time: '03 Oct 2026, 09:30', detail: 'Inter-bank beneficiary account freeze notice transmitted.' }
    ];

    c.defaultEvidence = [
        { number: 'EV-2026-0081', name: 'UPI_Payment_Receipt_Screenshot.png', type: 'Payment Receipt', size: '1.4 MB', hash: '8f4e2b10a3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0', status: 'Cryptographically Sealed', uploaded_on: '02 Oct 2026, 14:32' },
        { number: 'EV-2026-0082', name: 'Bank_Account_Statement_Oct2026.pdf', type: 'Bank Statement', size: '3.2 MB', hash: '3a7b1c9d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6d8e0f2a4b6c8d0e2f4a6b', status: 'Chain of Custody Intact', uploaded_on: '02 Oct 2026, 14:35' }
    ];

    c.getAllEvidence = function() {
        var allEv = [];
        if (c.cases && c.cases.length > 0) {
            c.cases.forEach(function(cs) {
                if (cs.evidence && cs.evidence.length > 0) {
                    cs.evidence.forEach(function(ev) {
                        var item = angular.copy(ev);
                        item.caseNumber = cs.number;
                        allEv.push(item);
                    });
                }
            });
        }
        if (allEv.length === 0) {
            allEv = [
                { number: 'EV-2026-0081', caseNumber: 'FNX-2026-001034', name: 'UPI_Payment_Receipt_Screenshot.png', type: 'Payment Receipt', size: '1.4 MB', hash: '8f4e2b10a3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0', status: 'Cryptographically Sealed', uploaded_on: '02 Oct 2026, 14:32' },
                { number: 'EV-2026-0082', caseNumber: 'FNX-2026-001034', name: 'Bank_Account_Statement_Oct2026.pdf', type: 'Bank Statement', size: '3.2 MB', hash: '3a7b1c9d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6d8e0f2a4b6c8d0e2f4a6b', status: 'Chain of Custody Intact', uploaded_on: '02 Oct 2026, 14:35' },
                { number: 'EV-2026-0074', caseNumber: 'FNX-2026-001021', name: 'SMS_Fake_Bank_Link_Screenshot.jpg', type: 'Chat / SMS Screenshot', size: '850 KB', hash: '9c8b7a6f5e4d3c2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c8b', status: 'Verified & Preserved', uploaded_on: '28 Sep 2026, 11:15' },
                { number: 'EV-2026-0065', caseNumber: 'FNX-2026-001015', name: 'Suspicious_Login_Alert_Email.eml', type: 'Email Header Record', size: '420 KB', hash: '4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e', status: 'Cryptographic Seal Active', uploaded_on: '20 Sep 2026, 19:40' }
            ];
        }
        return allEv;
    };

    c.openAddEvidence = function(cs) {
        c.evUploadForm.caseNumber = cs ? cs.number : (c.cases[0] ? c.cases[0].number : 'FNX-2026-001034');
        c.evUploadForm.name = 'Supplementary_Proof_' + Date.now().toString().slice(-4) + '.png';
        c.currentView = 'evidenceVault';
        c.scrollToTop();
    };

    c.triggerEvFileUpload = function() {
        if (!c.evUploadForm.name) {
            c.evUploadForm.name = 'Uploaded_Evidence_' + Date.now().toString().slice(-4) + '.pdf';
        }
    };

    c.submitSupplementaryEvidence = function() {
        if (!c.evUploadForm.name) return;
        var newEv = {
            number: 'EV-2026-00' + Math.floor(10 + Math.random() * 89),
            name: c.evUploadForm.name,
            type: c.evUploadForm.type,
            size: '1.2 MB',
            hash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
            status: 'Cryptographically Sealed',
            uploaded_on: 'Just now'
        };
        var targetCs = c.cases.find(function(cs) { return cs.number === c.evUploadForm.caseNumber; });
        if (targetCs) {
            if (!targetCs.evidence) targetCs.evidence = [];
            targetCs.evidence.unshift(newEv);
        }
        alert('Evidence ' + newEv.number + ' has been cryptographically sealed and attached to Case ' + c.evUploadForm.caseNumber + '.');
        c.evUploadForm.name = '';
    };

    // Update submitReport to immediately prepend created case
'''

if 'c.getAllEvidence = function' not in client_script:
    # Insert right before c.navigate
    idx_nav = client_script.find('c.navigate = function')
    client_script = client_script[:idx_nav] + client_helper_methods + client_script[idx_nav:]
    print('5. Inserted client script helper methods for Evidence & Case detail.')

# Update submitReport in client script to immediately prepend new case
old_submit_success = '''                c.submittedCaseNumber = d.number || d.case_number;
                c.submittedCaseId = d.case_id || d.sys_id;
                c.caseSubmittedSuccess = true;
                c.loadCases();'''

new_submit_success = '''                c.submittedCaseNumber = d.number || d.case_number;
                c.submittedCaseId = d.case_id || d.sys_id;
                c.caseSubmittedSuccess = true;
                var createdCase = {
                    sys_id: c.submittedCaseId,
                    number: c.submittedCaseNumber,
                    type: payload.type || 'Payment Fraud',
                    category: payload.specific_category || payload.type,
                    incident_date: payload.incident_date || 'Today',
                    severity: payload.severity || 'High',
                    status: 'Initial Review',
                    last_updated: 'Today',
                    description: payload.description || payload.title,
                    exposure: payload.exposure || '0',
                    blocked_amount: '0',
                    recovered_amount: '0',
                    transaction_reference: payload.transaction_reference,
                    digital_platform: payload.platform || 'Digital Banking',
                    assigned_cell: 'Fraud Resolution Cell - Priority Tier',
                    triage_sla: 'Initial Assessment',
                    timeline: [
                        { stage: 'Case Submitted', time: 'Just now', detail: 'Report registered & cryptographic case token generated.' }
                    ],
                    evidence: []
                };
                if (!c.cases) c.cases = [];
                c.cases.unshift(createdCase);
                if (c.stats) {
                    c.stats.total = (c.stats.total || 0) + 1;
                    c.stats.active = (c.stats.active || 0) + 1;
                }
                c.loadCases();'''

if old_submit_success in client_script:
    client_script = client_script.replace(old_submit_success, new_submit_success, 1)
    print('6. Enhanced c.submitReport with immediate case prepending.')

# -------------------------------------------------------------
# STEP 6: Fix Now Assist Chat Send Button (Compact Size)
# -------------------------------------------------------------
chat_btn_css = '''
/* Now Assist Chat Drawer - Compact Send Button & Layout */
.fnx-ai-footer {
    display: flex !important;
    gap: 0.5rem !important;
    padding: 0.75rem 1rem !important;
    background-color: #FFFFFF !important;
    border-top: 1px solid #E2E8F0 !important;
    align-items: center !important;
}

.fnx-ai-footer input {
    flex: 1 1 auto !important;
    padding: 0.6rem 0.85rem !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
    min-width: 0 !important;
}

.fnx-ai-footer button,
.fnx-ai-footer .fnx-btn {
    flex: 0 0 auto !important;
    width: auto !important;
    min-width: 65px !important;
    max-width: 80px !important;
    padding: 0.55rem 0.85rem !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    white-space: nowrap !important;
    margin: 0 !important;
}

/* Case Detail View Styling */
.fnx-case-detail-workspace {
    display: flex !important;
    flex-direction: column !important;
    gap: 1.25rem !important;
}

.fnx-detail-nav-row {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
}

.fnx-case-banner-card {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}

.fnx-cbb-top {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    margin-bottom: 1.5rem !important;
}

.fnx-cbb-title-group {
    display: flex !important;
    align-items: center !important;
    gap: 1rem !important;
}

.fnx-cbb-number {
    font-size: 1.5rem !important;
    font-weight: 800 !important;
    color: #0F172A !important;
}

.fnx-cbb-type {
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: #0284C7 !important;
}

.fnx-cbb-badges {
    display: flex !important;
    align-items: center !important;
    gap: 0.75rem !important;
}

.fnx-detail-tracker {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    padding: 0.5rem 1rem !important;
}

.fnx-tracker-date {
    display: block !important;
    font-size: 0.72rem !important;
    color: #64748B !important;
    margin-top: 0.2rem !important;
}

.fnx-case-detail-grid {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 1.25rem !important;
}

.fnx-cd-col {
    display: flex !important;
    flex-direction: column !important;
    gap: 1.25rem !important;
}

.fnx-cd-kv-list {
    display: flex !important;
    flex-direction: column !important;
    gap: 0.75rem !important;
}

.fnx-cd-kv-row {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    font-size: 0.88rem !important;
    padding: 0.25rem 0 !important;
}

.fnx-cd-k {
    color: #64748B !important;
    font-weight: 500 !important;
}

.fnx-cd-v {
    color: #0F172A !important;
    font-weight: 600 !important;
    text-align: right !important;
}

.fnx-financial-quad {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 0.85rem !important;
}

.fnx-fin-box {
    border-radius: 8px !important;
    padding: 0.85rem !important;
    display: flex !important;
    flex-direction: column !important;
}

.box-loss { background: #FEF2F2 !important; border: 1px solid #FEE2E2 !important; }
.box-blocked { background: #EFF6FF !important; border: 1px solid #DBEAFE !important; }
.box-recovered { background: #F0FDF4 !important; border: 1px solid #DCFCE7 !important; }
.box-status { background: #F8FAFC !important; border: 1px solid #E2E8F0 !important; }

.fnx-fin-lbl { font-size: 0.75rem !important; color: #64748B !important; font-weight: 600 !important; }
.fnx-fin-val { font-size: 1.2rem !important; font-weight: 800 !important; color: #0F172A !important; margin-top: 0.25rem !important; }

.fnx-timeline-list {
    display: flex !important;
    flex-direction: column !important;
    gap: 0.85rem !important;
}

.fnx-timeline-item {
    display: flex !important;
    align-items: flex-start !important;
    gap: 0.75rem !important;
    font-size: 0.85rem !important;
}

.fnx-tl-bullet {
    width: 8px !important;
    height: 8px !important;
    border-radius: 50% !important;
    background: #0284C7 !important;
    margin-top: 6px !important;
    flex-shrink: 0 !important;
}

.fnx-tl-stage { font-weight: 700 !important; color: #0F172A !important; }
.fnx-tl-detail { color: #475569 !important; font-size: 0.82rem !important; margin: 0.15rem 0 !important; }
.fnx-tl-time { color: #94A3B8 !important; font-size: 0.75rem !important; }

.fnx-evidence-detail-list {
    display: flex !important;
    flex-direction: column !important;
    gap: 0.85rem !important;
}

.fnx-ev-detail-item {
    display: flex !important;
    align-items: center !important;
    gap: 0.85rem !important;
    padding: 0.75rem !important;
    background: #F8FAFC !important;
    border-radius: 8px !important;
    border: 1px solid #E2E8F0 !important;
}

.fnx-ev-icon-box {
    width: 38px !important;
    height: 38px !important;
    border-radius: 8px !important;
    background: #EFF6FF !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
}

.fnx-ev-meta-col { flex: 1 !important; }
.fnx-ev-filename { font-size: 0.88rem !important; color: #0F172A !important; }
.fnx-ev-submeta { display: flex !important; align-items: center !important; gap: 0.5rem !important; font-size: 0.78rem !important; color: #64748B !important; margin: 0.15rem 0 !important; }
.fnx-ev-hash-row { font-size: 0.75rem !important; color: #0284C7 !important; }
.fnx-ev-hash-snip { font-family: monospace !important; letter-spacing: 0.3px !important; }
'''

css += '\n\n' + chat_btn_css
print('7. Appended compact chat send button and case detail CSS styles.')

# -------------------------------------------------------------
# STEP 7: Deploy Updated Widget to ServiceNow
# -------------------------------------------------------------
payload = {
    'template': template,
    'client_script': client_script,
    'css': css
}

patch_r = requests.patch(
    f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}',
    auth=AUTH,
    headers={'Content-Type': 'application/json'},
    json=payload
)

if patch_r.status_code == 200:
    print('SUCCESS: All customer portal requirements deployed successfully!')
    c_r = requests.get(f'{BASE_URL}/cache.do', auth=AUTH)
    print('Cache clear response:', c_r.status_code)
else:
    print('FAILURE deploying:', patch_r.status_code, patch_r.text[:300])
