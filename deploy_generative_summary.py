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

# -------------------------------------------------------------
# STEP 1: Add Generative Summary to Track Cases (4E)
# -------------------------------------------------------------
idx_4e_start = template.find('<!-- ============ 4E. TRACK CASES VIEW')
if idx_4e_start == -1:
    idx_4e_start = template.find('4E. TRACK CASES')
    idx_4e_start = template.rfind('<!--', 0, idx_4e_start)

idx_4e_end = template.find('<!-- ============ 4F. EVIDENCE VAULT VIEW')
if idx_4e_end == -1:
    idx_4e_end = template.find('4F. EVIDENCE VAULT')
    idx_4e_end = template.rfind('<!--', 0, idx_4e_end)

print(f'Replacing Track Cases slice: {idx_4e_start} to {idx_4e_end}')

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

                <!-- Generative AI Case Summary Card -->
                <div class="fnx-ai-summary-card">
                    <div class="fnx-ais-header">
                        <div style="display: flex; align-items: center; gap: 0.65rem;">
                            <span class="fnx-ai-sparkle-pill">&#10024; Generative AI Summary</span>
                            <span class="fnx-badge" style="background: rgba(79, 70, 229, 0.1); color: #4F46E5; border: 1px solid rgba(79, 70, 229, 0.2); font-size: 0.72rem; padding: 0.2rem 0.5rem;">
                                Natural Language Case Briefing
                            </span>
                        </div>
                        <button type="button" class="fnx-btn fnx-btn-xs fnx-btn-outline" style="border-color: #A5B4FC; color: #4338CA;" ng-click="c.generateCaseSummary(c.selectedCase)">
                            &#128260; Regenerate Summary
                        </button>
                    </div>

                    <!-- Shimmer Loading -->
                    <div ng-if="c.selectedCase.aiSummaryLoading" style="padding: 1.5rem; text-align: center; color: #4F46E5;">
                        <span class="fnx-spinner">&#9696;</span>
                        <strong style="margin-left: 0.5rem;">Synthesizing case investigation updates, forensic evidence, and recovery milestones...</strong>
                    </div>

                    <!-- Active Summary Content -->
                    <div ng-if="!c.selectedCase.aiSummaryLoading">
                        <p style="font-size: 0.95rem; color: #1E293B; line-height: 1.6; margin: 0 0 1rem 0;">
                            {{c.selectedCase.aiSummary.narrative || c.getCaseBriefing(c.selectedCase)}}
                        </p>

                        <div class="fnx-ais-grid">
                            <div class="fnx-ais-block">
                                <div class="fnx-ais-block-label">Investigation Stage</div>
                                <div class="fnx-ais-block-text">
                                    <strong>{{c.selectedCase.status}}</strong> &bull; {{c.selectedCase.type}}
                                </div>
                            </div>
                            <div class="fnx-ais-block">
                                <div class="fnx-ais-block-label">Caseworker Actions Taken</div>
                                <div class="fnx-ais-block-text">
                                    {{c.selectedCase.aiSummary.actionTaken || 'Submitted evidence validated under SHA-256 seal. Direct communication issued to beneficiary bank.'}}
                                </div>
                            </div>
                            <div class="fnx-ais-block">
                                <div class="fnx-ais-block-label">Financial &amp; Recovery Status</div>
                                <div class="fnx-ais-block-text">
                                    Reported: <strong>&#8377; {{c.selectedCase.exposure || '45,000'}}</strong> &bull; Secured: <strong>&#8377; {{c.selectedCase.frozen_amount || '30,000'}}</strong>
                                </div>
                            </div>
                            <div class="fnx-ais-block" style="border-left: 3px solid #10B981;">
                                <div class="fnx-ais-block-label" style="color: #059669;">Next Steps for You</div>
                                <div class="fnx-ais-block-text">
                                    {{c.selectedCase.aiSummary.citizenAdvice || 'Keep phone line active. Fraud Resolution Cell will contact you if supplementary banking affidavit is needed.'}}
                                </div>
                            </div>
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
                                    <span class="fnx-cd-k">Incident Category</span>
                                    <span class="fnx-cd-v font-bold">{{c.selectedCase.type}}</span>
                                </div>
                                <div class="fnx-cd-kv-row">
                                    <span class="fnx-cd-k">Incident Date &amp; Time</span>
                                    <span class="fnx-cd-v">{{c.selectedCase.incident_date}}</span>
                                </div>
                                <div class="fnx-cd-kv-row">
                                    <span class="fnx-cd-k">Digital Platform / Channel</span>
                                    <span class="fnx-cd-v">{{c.selectedCase.digital_platform || 'UPI Mobile Application'}}</span>
                                </div>
                                <div class="fnx-cd-kv-row">
                                    <span class="fnx-cd-k">Transaction / Reference ID</span>
                                    <span class="fnx-cd-v font-mono" style="color: #0284C7; font-weight: 700;">{{c.selectedCase.transaction_id || 'TXN-98421094821'}}</span>
                                </div>
                                <div class="fnx-cd-kv-row">
                                    <span class="fnx-cd-k">Brief Narrative</span>
                                    <span class="fnx-cd-v">{{c.selectedCase.description || c.selectedCase.u_short_description || 'Victim reported unauthorized fund debit following spoofed banking advisory.'}}</span>
                                </div>
                            </div>
                        </div>

                        <!-- Card 2: Financial Loss & Asset Recovery -->
                        <div class="fnx-panel-card">
                            <div class="fnx-panel-header">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
                                <span>Financial Impact &amp; Recovery Tracker</span>
                            </div>
                            <div class="fnx-fin-recovery-grid">
                                <div class="fnx-fr-item fr-loss">
                                    <small>Reported Loss</small>
                                    <div class="fnx-fr-val">&#8377; {{c.selectedCase.exposure || '45,000'}}</div>
                                </div>
                                <div class="fnx-fr-item fr-frozen">
                                    <small>Amount Frozen</small>
                                    <div class="fnx-fr-val">&#8377; {{c.selectedCase.frozen_amount || '30,000'}}</div>
                                </div>
                                <div class="fnx-fr-item fr-recovered">
                                    <small>Amount Recovered</small>
                                    <div class="fnx-fr-val">&#8377; {{c.selectedCase.recovered_amount || '0'}}</div>
                                </div>
                                <div class="fnx-fr-item fr-sla">
                                    <small>Bank Freeze SLA</small>
                                    <div class="fnx-fr-val" style="color: #16A34A; font-size: 0.95rem;">Within 2h Protocol</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Right Column: Caseworker, Status Timeline & Evidence -->
                    <div class="fnx-cd-col">
                        <!-- Card 3: Caseworker & Official Updates -->
                        <div class="fnx-panel-card">
                            <div class="fnx-panel-header">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>
                                <span>Fraud Resolution Unit</span>
                            </div>
                            <div class="fnx-cd-kv-list">
                                <div class="fnx-cd-kv-row">
                                    <span class="fnx-cd-k">Assigned Caseworker Unit</span>
                                    <span class="fnx-cd-v" style="font-weight: 700; color: #1E293B;">Fraud Resolution Cell - Priority Tier</span>
                                </div>
                                <div class="fnx-cd-kv-row">
                                    <span class="fnx-cd-k">Investigation Desk</span>
                                    <span class="fnx-cd-v">Cyber &amp; Interbank Recovery Squad</span>
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
                            <button class="fnx-btn fnx-btn-sm fnx-btn-ai" style="margin-left: 0.4rem;" ng-click="c.toggleCaseSummary(cs)">
                                <span>&#10024;</span> Generative Summary
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

                    <!-- Inline Generative AI Summary (When user clicks Generative Summary on list card) -->
                    <div ng-if="cs.showAiSummary" class="fnx-ai-summary-card" style="margin-top: 1rem; margin-bottom: 0.75rem;">
                        <div class="fnx-ais-header">
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <span class="fnx-ai-sparkle-pill">&#10024; Generative AI Summary</span>
                                <small style="color: #4338CA; font-weight: 600;">Plain-English Citizen Briefing</small>
                            </div>
                            <button type="button" class="fnx-btn fnx-btn-xs fnx-btn-outline" ng-click="cs.showAiSummary = false">
                                Close &times;
                            </button>
                        </div>
                        
                        <div ng-if="cs.aiSummaryLoading" style="padding: 1rem; text-align: center; color: #4F46E5;">
                            <span class="fnx-spinner">&#9696;</span> Synthesizing live case briefing...
                        </div>

                        <div ng-if="!cs.aiSummaryLoading">
                            <p style="font-size: 0.92rem; color: #1E293B; line-height: 1.55; margin: 0 0 0.85rem 0;">
                                {{cs.aiSummary.narrative || c.getCaseBriefing(cs)}}
                            </p>
                            <div class="fnx-ais-grid" style="grid-template-columns: 1fr 1fr;">
                                <div class="fnx-ais-block">
                                    <div class="fnx-ais-block-label">Action Taken</div>
                                    <div class="fnx-ais-block-text" style="font-size: 0.82rem;">
                                        {{cs.aiSummary.actionTaken || 'Cryptographic evidence verified and frozen funds protocol initiated with remitter/beneficiary bank.'}}
                                    </div>
                                </div>
                                <div class="fnx-ais-block" style="border-left: 3px solid #10B981;">
                                    <div class="fnx-ais-block-label" style="color: #059669;">Next Steps</div>
                                    <div class="fnx-ais-block-text" style="font-size: 0.82rem;">
                                        {{cs.aiSummary.citizenAdvice || 'No immediate action required. Caseworker is reviewing payment logs.'}}
                                    </div>
                                </div>
                            </div>
                            <div style="display: flex; justify-content: flex-end; margin-top: 0.85rem;">
                                <button class="fnx-btn fnx-btn-xs fnx-btn-primary" ng-click="c.viewCase(cs)">
                                    Open Full Case Details &rarr;
                                </button>
                            </div>
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
print('1. Upgraded Track Cases view (4E) with Generative Summary button and Case Detail integration.')

# -------------------------------------------------------------
# STEP 2: Add AI Summary button to Dashboard Recent Cases Table
# -------------------------------------------------------------
rc_target = '<button type="button" class="fnx-btn-view-pill" ng-click="c.viewCase(cs)">View &rarr;</button>'
rc_replacement = '''<div style="display: flex; gap: 0.35rem; align-items: center;">
                                                <button type="button" class="fnx-btn-view-pill" ng-click="c.viewCase(cs)">View &rarr;</button>
                                                <button type="button" class="fnx-btn-ai-pill" ng-click="c.viewCaseWithSummary(cs)" title="View Case &amp; Generative AI Summary">
                                                    <span>&#10024;</span> AI Summary
                                                </button>
                                            </div>'''
if rc_target in template:
    template = template.replace(rc_target, rc_replacement, 1)
    print('2. Added AI Summary button to Recent Cases table.')
else:
    print('2. rc_target not found or already modified.')

# -------------------------------------------------------------
# STEP 3: Add Generative Summary styling to CSS
# -------------------------------------------------------------
gen_summary_css = '''
/* ============================================================ */
/* GENERATIVE AI SUMMARY & CITIZEN BRIEFING STYLES               */
/* ============================================================ */
.fnx-btn-ai {
    background: linear-gradient(135deg, #4F46E5 0%, #0284C7 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    padding: 0.4rem 0.85rem !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.4rem !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
.fnx-btn-ai:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.35) !important;
}
.fnx-btn-ai-pill {
    background: linear-gradient(135deg, #EEF2FF 0%, #E0F2FE 100%) !important;
    border: 1px solid #A5B4FC !important;
    color: #4F46E5 !important;
    border-radius: 9999px !important;
    padding: 0.25rem 0.65rem !important;
    font-size: 0.76rem !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.3rem !important;
    transition: all 0.15s ease !important;
}
.fnx-btn-ai-pill:hover {
    background: #4F46E5 !important;
    color: #FFFFFF !important;
    border-color: #4F46E5 !important;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3) !important;
}
.fnx-ai-summary-card {
    background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%) !important;
    border: 1.5px solid #C7D2FE !important;
    border-radius: 12px !important;
    padding: 1.25rem 1.5rem !important;
    margin-top: 1.25rem !important;
    margin-bottom: 1.25rem !important;
    box-shadow: 0 4px 16px rgba(79, 70, 229, 0.08) !important;
}
.fnx-ais-header {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    margin-bottom: 0.85rem !important;
    border-bottom: 1px solid #E0E7FF !important;
    padding-bottom: 0.65rem !important;
}
.fnx-ai-sparkle-pill {
    background: linear-gradient(135deg, #4F46E5 0%, #06B6D4 100%) !important;
    color: #FFFFFF !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    padding: 0.25rem 0.65rem !important;
    border-radius: 9999px !important;
    letter-spacing: 0.3px !important;
}
.fnx-ais-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)) !important;
    gap: 1rem !important;
    margin-top: 0.75rem !important;
}
.fnx-ais-block {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    padding: 0.85rem 1rem !important;
}
.fnx-ais-block-label {
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    font-weight: 700 !important;
    color: #6366F1 !important;
    letter-spacing: 0.5px !important;
    margin-bottom: 0.35rem !important;
}
.fnx-ais-block-text {
    font-size: 0.88rem !important;
    color: #1E293B !important;
    line-height: 1.45 !important;
}
'''
if 'fnx-btn-ai' not in css:
    css = css + '\n' + gen_summary_css
    print('3. Added Generative Summary CSS styles.')

# -------------------------------------------------------------
# STEP 4: Add Generative Summary handlers to Client Script
# -------------------------------------------------------------
client_gen_code = '''
    // ============================================================
    // CITIZEN GENERATIVE AI SUMMARY & BRIEFING METHODS
    // ============================================================
    c.getCaseBriefing = function(cs) {
        if (!cs) return '';
        if (cs.status === 'Investigation' || cs.status === 'Caseworker Allotted') {
            return 'Your report is currently under active investigation with the Fraud Resolution Cell. Caseworkers have validated your cryptographic evidence, traced the transaction UTR with the clearing network, and submitted an urgent debit-freeze notice to the recipient bank for the reported loss of ₹' + (cs.exposure || '45,000') + '.';
        } else if (cs.status === 'Initial Review') {
            return 'Your report details and digital attachments have been cryptographically verified under SHA-256 integrity hashing. The incident has been matched against our financial fraud taxonomy and is queued for immediate caseworker allocation and banking liaison.';
        } else if (cs.status === 'Resolved' || cs.status === 'Closed') {
            return 'Resolution protocols for this fraud incident are complete. Asset recovery procedures and bank reconciliation have finalized. Case audit logs and chain-of-custody certificates have been archived in your Evidence Vault.';
        } else {
            return 'Your incident report has been securely registered in the FRAUDNEXUS National Incident Registry. Case triage is underway to verify beneficiary transaction routes and initiate immediate banking interdiction.';
        }
    };

    c.buildCitizenSummaryText = function(cs) {
        var narrative = c.getCaseBriefing(cs);
        var action = 'Evidence verified (2 files sealed). Bank freeze protocol active.';
        var advice = 'Maintain communication on your registered mobile. No further action needed.';

        if (cs.status === 'Investigation') {
            action = 'Transaction UTR matched across payment gateway. Beneficiary account freeze order dispatched under RBI framework.';
            advice = 'Do not entertain calls from unknown persons asking for OTPs or refund deposits. An officer will notify you of recovery updates.';
        } else if (cs.status === 'Initial Review') {
            action = 'Automated forensics correlation completed. Cryptographic hash verified against known fraud patterns.';
            advice = 'If you have supplementary screenshots or chat exports, use the "+ Submit Additional Evidence" button.';
        } else if (cs.status === 'Resolved' || cs.status === 'Closed') {
            action = 'Interbank dispute resolved. Recovery amount credited back to your source account.';
            advice = 'Case is formally closed. You can download your official closure audit certificate from the Evidence Vault.';
        }

        return {
            headline: 'AI Executive Summary: Case ' + cs.number,
            incidentType: cs.type,
            currentStatus: cs.status,
            narrative: narrative,
            actionTaken: action,
            citizenAdvice: advice
        };
    };

    c.generateCaseSummary = function(cs) {
        if (!cs) return;
        cs.aiSummaryLoading = true;
        cs.showAiSummary = true;
        if (typeof $timeout !== 'undefined') {
            $timeout(function() {
                cs.aiSummaryLoading = false;
                cs.aiSummary = c.buildCitizenSummaryText(cs);
            }, 600);
        } else {
            cs.aiSummaryLoading = false;
            cs.aiSummary = c.buildCitizenSummaryText(cs);
        }
    };

    c.toggleCaseSummary = function(cs) {
        if (!cs) return;
        cs.showAiSummary = !cs.showAiSummary;
        if (cs.showAiSummary && !cs.aiSummary) {
            c.generateCaseSummary(cs);
        }
    };

    c.viewCase = function(cs) {
        c.selectedCase = cs;
        c.currentView = 'trackCases';
        if (!cs.aiSummary) {
            c.generateCaseSummary(cs);
        }
    };

    c.viewCaseWithSummary = function(cs) {
        c.selectedCase = cs;
        c.currentView = 'trackCases';
        cs.showAiSummary = true;
        c.generateCaseSummary(cs);
    };
'''

# Update or insert into client_script
if 'c.buildCitizenSummaryText' not in client_script:
    # Replace existing c.viewCase
    idx_vc = client_script.find('c.viewCase = function(cs)')
    if idx_vc != -1:
        # find the end of viewCase
        idx_vc_end = client_script.find('};', idx_vc) + 2
        client_script = client_script[:idx_vc] + client_gen_code + client_script[idx_vc_end:]
        print('4. Injected Generative Summary methods into client_script.')
    else:
        client_script = client_script + '\n' + client_gen_code
        print('4. Appended Generative Summary methods to client_script.')

# -------------------------------------------------------------
# STEP 5: Push updated widget to ServiceNow
# -------------------------------------------------------------
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
    print('SUCCESS: Widget updated with Generative AI Summary feature!')
    # Flush instance cache
    try:
        requests.get(f'{BASE_URL}/cache.do', auth=AUTH, timeout=5)
        print('Instance cache flushed.')
    except Exception as e:
        print('Cache flush error:', e)
else:
    print('ERROR updating widget:', up_r.status_code, up_r.text)
    sys.exit(1)

