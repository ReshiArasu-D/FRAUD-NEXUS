import sys, os, re, requests

sys.stdout.reconfigure(encoding='utf-8')

print("=== APPLYING VERIFICATION WORKSPACE UPDATES ===")

# ==========================================
# 1. UPDATE CLIENT LOGIC (build_vw_client.py)
# ==========================================
print("1. Updating Client Logic...")
with open('d:/KPMG/build_vw_client.py', 'r', encoding='utf-8') as f:
    client_code = f.read()

# Add verification filter state and entity verify helper
if 'c.verificationQueueFilter' not in client_code:
    client_code = client_code.replace(
        "c.investigationTab = 'overview';",
        "c.investigationTab = 'overview';\n    c.verificationQueueFilter = 'all';"
    )

# Add setVerificationFilter, resetVerificationQueue, verifyEntity
helpers_code = """
    // Verification Workspace Helpers
    c.setVerificationFilter = function(filter) {
        c.verificationQueueFilter = filter;
    };

    c.verifyEntity = function(ind) {
        ind.verified = !ind.verified;
        c.addTimelineEvent('HUMAN', 'Entity Verified', 'Investigator verified graph entity: ' + ind.type + ' (' + ind.value + ')', ind.value);
    };

    c.resetVerificationQueue = function() {
        if (!c.activeInvestigationCase) return;
        (c.activeInvestigationCase.evidence || []).forEach(function(e) {
            e.status = 'Needs Review';
        });
        (c.activeInvestigationCase.findings || []).forEach(function(f) {
            f.status = 'Needs Review';
            f.reviewer = 'Pending Human Review';
            f.reviewed_on = null;
        });
        if (c.activeInvestigationCase.cyber && c.activeInvestigationCase.cyber.indicators) {
            c.activeInvestigationCase.cyber.indicators.forEach(function(i) {
                i.verified = false;
            });
        }
        c.activeInvestigationCase.decision = { status: 'Pending', outcome: 'Under Review' };
        c.addTimelineEvent('SYSTEM', 'Verification Queue Reset', 'All evidence artifacts and findings reset to Needs Review for testing.', 'SYS-RESET');
        alert('Verification Queue reset! All 4 evidence artifacts and 4 findings are now pending human review.');
    };
"""

if 'c.resetVerificationQueue' not in client_code:
    client_code = client_code.replace(
        "c.confirmAllPending = function() {",
        helpers_code + "\n    c.confirmAllPending = function() {"
    )

with open('d:/KPMG/build_vw_client.py', 'w', encoding='utf-8') as f:
    f.write(client_code)

# Execute build_vw_client.py to generate verification_workspace_client.js
import subprocess
subprocess.run(['python', 'd:/KPMG/build_vw_client.py'], check=True)
print("Client script generated successfully.")

# ==========================================
# 2. UPDATE CSS (build_vw_css.py)
# ==========================================
print("2. Updating CSS Styles...")
with open('d:/KPMG/build_vw_css.py', 'r', encoding='utf-8') as f:
    css_code = f.read()

new_styles = """
/* Overview Case Dossier & Metrics Grid */
.fnx-overview-metrics-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1px;
    background: #E2E8F0;
}
.fnx-metric-tile {
    background: #FFFFFF;
    padding: 1rem 0.85rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.15s ease;
}
.fnx-metric-tile:hover {
    background: #F8FAFC;
    transform: translateY(-1px);
}
.fnx-metric-tile .m-icon {
    font-size: 1.35rem;
    margin-bottom: 0.25rem;
}
.fnx-metric-tile .m-val {
    font-size: 1.25rem;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.2;
}
.fnx-metric-tile .m-label {
    font-size: 0.68rem;
    font-weight: 700;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 0.15rem;
}
.fnx-metric-tile .m-sub {
    font-size: 0.68rem;
    color: #94A3B8;
    margin-top: 0.15rem;
}

/* Zero Silent AI Decisions Policy Alert Banner */
.fnx-zero-ai-banner {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    background: #FEF3C7;
    border: 1px solid #F59E0B;
    border-radius: 8px;
    padding: 0.85rem 1.15rem;
    color: #92400E;
    font-size: 0.82rem;
}
.fnx-zero-ai-banner .banner-icon {
    font-size: 1.6rem;
    line-height: 1;
}
.fnx-zero-ai-banner .banner-body {
    flex: 1;
    line-height: 1.45;
}
.fnx-zero-ai-banner .banner-body strong {
    color: #78350F;
}

/* Verification Domain Filter Tabs */
.fnx-verif-tabs-bar {
    display: flex;
    gap: 0.5rem;
    border-bottom: 2px solid #E2E8F0;
    padding-bottom: 0.5rem;
    overflow-x: auto;
}
.fnx-verif-tab-btn {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.5rem 0.85rem;
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 600;
    color: #475569;
    cursor: pointer;
    transition: all 0.15s ease;
    white-space: nowrap;
}
.fnx-verif-tab-btn:hover {
    background: #F1F5F9;
    border-color: #94A3B8;
}
.fnx-verif-tab-btn.active {
    background: #0F172A;
    border-color: #0F172A;
    color: #FFFFFF;
}
.fnx-verif-tab-btn.active .tab-badge {
    background: #00B8D9;
    color: #0F172A;
}
.tab-badge {
    background: #E2E8F0;
    color: #475569;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.1rem 0.45rem;
    border-radius: 10px;
}

/* Verification Stream Cards */
.fnx-verif-stream-list {
    display: flex;
    flex-direction: column;
}
.fnx-verif-stream-card {
    border-bottom: 1px solid #E2E8F0;
    padding: 1.15rem 1.35rem;
    background: #FFFFFF;
    transition: background 0.15s ease;
}
.fnx-verif-stream-card:last-child {
    border-bottom: none;
}
.fnx-verif-stream-card:hover {
    background: #F8FAFC;
}
.fnx-verif-stream-card.card-verified {
    border-left: 4px solid #10B981;
}
.fnx-verif-stream-card.card-rejected {
    border-left: 4px solid #EF4444;
    opacity: 0.75;
}
.stream-card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.65rem;
}
.stream-card-id-block {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.stream-icon {
    font-size: 1.5rem;
    line-height: 1;
}
.stream-id {
    font-size: 0.92rem;
    font-weight: 700;
    color: #0F172A;
}
.stream-sub {
    font-size: 0.75rem;
}
.stream-meta-row {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.65rem;
    font-size: 0.72rem;
}
.badge-classification {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    color: #1D4ED8;
    padding: 0.2rem 0.55rem;
    border-radius: 4px;
}
.badge-pipeline {
    background: #F3E8FF;
    border: 1px solid #E9D5FF;
    color: #7E22CE;
    padding: 0.2rem 0.55rem;
    border-radius: 4px;
}
.badge-hash {
    background: #F1F5F9;
    border: 1px solid #CBD5E1;
    color: #475569;
    padding: 0.2rem 0.55rem;
    border-radius: 4px;
}
.stream-extraction-box {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 0.75rem 0.95rem;
    margin-top: 0.5rem;
}
.extraction-lbl {
    font-size: 0.65rem;
    font-weight: 800;
    color: #64748B;
    letter-spacing: 0.5px;
    margin-bottom: 0.25rem;
}
.extraction-content {
    font-size: 0.82rem;
    color: #1E293B;
    line-height: 1.45;
}
.stream-card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.85rem;
    padding-top: 0.65rem;
    border-top: 1px dashed #E2E8F0;
}
.stream-actions {
    display: flex;
    gap: 0.45rem;
}
.stream-confidence-badge {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    background: #F1F5F9;
    padding: 0.25rem 0.65rem;
    border-radius: 12px;
}
.conf-lbl {
    font-size: 0.68rem;
    color: #64748B;
}
.conf-val {
    font-size: 0.82rem;
    font-weight: 800;
}
.finding-desc {
    font-size: 0.84rem;
    color: #334155;
    line-height: 1.45;
}
.finding-meta-row {
    font-size: 0.75rem;
    color: #64748B;
}

/* Cross-Channel Contradiction & Consistency Signals */
.fnx-contradiction-grid {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}
.fnx-signal-card {
    border-radius: 8px;
    padding: 0.85rem 1.15rem;
    border: 1px solid #E2E8F0;
}
.fnx-signal-card.signal-consistent {
    background: #F0FDF4;
    border-color: #86EFAC;
}
.fnx-signal-card.signal-anomaly {
    background: #FEF3C7;
    border-color: #FCD34D;
}
.signal-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.35rem;
}
.signal-title {
    font-size: 0.82rem;
    font-weight: 700;
    color: #0F172A;
    flex: 1;
}
.signal-badge {
    font-size: 0.75rem;
    font-weight: 800;
}
.signal-desc {
    font-size: 0.78rem;
    color: #334155;
    line-height: 1.45;
}
"""

if '.fnx-overview-metrics-grid' not in css_code:
    css_code = css_code.replace(
        "/* ============================================================\n   FRAUDNEXUS — ENTERPRISE VERIFICATION WORKSPACE STYLES",
        new_styles + "\n/* ============================================================\n   FRAUDNEXUS — ENTERPRISE VERIFICATION WORKSPACE STYLES"
    )
    with open('d:/KPMG/build_vw_css.py', 'w', encoding='utf-8') as f:
        f.write(css_code)
    subprocess.run(['python', 'd:/KPMG/build_vw_css.py'], check=True)
    print("CSS script generated successfully.")

# ==========================================
# 3. UPDATE TEMPLATE (build_vw_template.py)
# ==========================================
print("3. Updating Workspace Template...")
with open('d:/KPMG/build_vw_template.py', 'r', encoding='utf-8') as f:
    template_code = f.read()

# Replace technical status card in Overview
old_overview_card = """                    <div class="fnx-card">
                        <div class="fnx-card-header">
                            <span class="card-header-title">🛡️ INTELLIGENCE STATUS</span>
                        </div>
                        <div class="fnx-card-body">
                            <div class="fnx-intel-status-pill">
                                <div class="intel-title">JOREN Processing Engine</div>
                                <div class="intel-val text-success">Active &bull; Multimodal Classification Completed</div>
                            </div>
                            <div class="fnx-intel-status-pill">
                                <div class="intel-title">Dynamic Byte-Level BPE Tokenizer</div>
                                <div class="intel-val text-success">Completed &bull; Sub-token Embeddings Indexed</div>
                            </div>
                            <div class="fnx-intel-status-pill">
                                <div class="intel-title">Multi-RAG & Neo4j Knowledge Graph</div>
                                <div class="intel-val text-success">Linked &bull; 8 Entities &bull; 2 Related Syndicate Cases</div>
                            </div>
                            <div class="fnx-intel-status-pill">
                                <div class="intel-title">Context Fusion & Agentic Reasoning</div>
                                <div class="intel-val text-success">11-Stage Fusion Validated &bull; Human Sign-off Required</div>
                            </div>
                        </div>
                    </div>"""

new_overview_card = """                    <div class="fnx-card">
                        <div class="fnx-card-header d-flex justify-content-between align-items-center">
                            <span class="card-header-title">📊 CASE DOSSIER & METRICS BREAKDOWN</span>
                            <span class="badge-tag">SLA: On Track</span>
                        </div>
                        <div class="fnx-card-body p-0">
                            <div class="fnx-overview-metrics-grid">
                                <div class="fnx-metric-tile" ng-click="c.setInvestigationTab('evidence')">
                                    <div class="m-icon">📁</div>
                                    <div class="m-val">{{c.activeInvestigationCase.evidence.length || 4}}</div>
                                    <div class="m-label">Evidence Items</div>
                                    <div class="m-sub">{{c.isEvidenceVerified() ? '✓ All Verified' : 'Needs Review'}}</div>
                                </div>
                                <div class="fnx-metric-tile" ng-click="c.setInvestigationTab('findings')">
                                    <div class="m-icon">🎯</div>
                                    <div class="m-val">{{c.activeInvestigationCase.findings.length || 4}}</div>
                                    <div class="m-label">AI Findings</div>
                                    <div class="m-sub">{{c.isFindingsConfirmed() ? '✓ Confirmed' : 'Pending Sign-off'}}</div>
                                </div>
                                <div class="fnx-metric-tile" ng-click="c.setInvestigationTab('partnerRequests')">
                                    <div class="m-icon">🤝</div>
                                    <div class="m-val">{{c.activeInvestigationCase.partner_requests.length || 1}}</div>
                                    <div class="m-label">Partner Traces</div>
                                    <div class="m-sub">Partner Bank A</div>
                                </div>
                                <div class="fnx-metric-tile" ng-click="c.setInvestigationTab('tasks')">
                                    <div class="m-icon">📋</div>
                                    <div class="m-val">{{c.activeInvestigationCase.tasks.length || 3}}</div>
                                    <div class="m-label">Action Tasks</div>
                                    <div class="m-sub">1 Done &bull; 2 Active</div>
                                </div>
                                <div class="fnx-metric-tile" ng-click="c.setInvestigationTab('relatedCases')">
                                    <div class="m-icon">🔗</div>
                                    <div class="m-val">{{c.activeInvestigationCase.related_cases.length || 2}}</div>
                                    <div class="m-label">Related Cases</div>
                                    <div class="m-sub">Syndicate Match</div>
                                </div>
                                <div class="fnx-metric-tile" ng-click="c.setInvestigationTab('verification')">
                                    <div class="m-icon">🔍</div>
                                    <div class="m-val" ng-class="c.getPendingVerificationCount() > 0 ? 'text-warning' : 'text-success'">{{c.getPendingVerificationCount()}}</div>
                                    <div class="m-label">Verification Queue</div>
                                    <div class="m-sub">{{c.getPendingVerificationCount() > 0 ? 'Pending Review' : '✓ Verified'}}</div>
                                </div>
                            </div>
                            <div class="p-3 bg-light border-top d-flex justify-content-between align-items-center">
                                <span class="text-xs text-muted">Assigned Officer: <strong>{{c.activeInvestigationCase.handler || 'Alex Morgan'}}</strong> &bull; Incident: <strong>Cyber-Financial Fraud</strong></span>
                                <button class="fnx-btn fnx-btn-xs fnx-btn-primary" ng-click="c.setInvestigationTab('verification')">Enter Verification Workspace &rarr;</button>
                            </div>
                        </div>
                    </div>"""

if old_overview_card in template_code:
    template_code = template_code.replace(old_overview_card, new_overview_card)
    print("Overview technical card successfully replaced with Case Dossier & Metrics Breakdown.")
else:
    print("WARNING: old_overview_card not found directly; attempting regex replacement...")
    template_code = re.sub(
        r'<div class="fnx-card">\s*<div class="fnx-card-header">\s*<span class="card-header-title">🛡️ INTELLIGENCE STATUS</span>.*?</div>\s*</div>\s*</div>',
        new_overview_card + "\n                </div>",
        template_code,
        flags=re.DOTALL
    )

# Now replace Section 3: Verification Queue with the complete 3-column Verification Workspace
new_verif_section = """            <!-- ----------------------------------------
                 SECTION 3: VERIFICATION QUEUE (FULL 3-COLUMN VERIFICATION WORKSPACE)
                 ---------------------------------------- -->
            <div ng-if="c.investigationTab === 'verification'" class="fnx-vw-view">
                
                <!-- Title Row with Action Toolbar -->
                <div class="fnx-view-title-row">
                    <div>
                        <h2>Human Verification Workspace & Intelligence Queue</h2>
                        <p class="text-muted">Strict human-in-the-loop control tower. Review, interrogate, and verify JOREN multimodal extractions, agentic hypotheses, extracted graph entities, and cross-channel contradictions.</p>
                    </div>
                    <div class="view-actions d-flex gap-2">
                        <button class="fnx-btn fnx-btn-sm fnx-btn-outline" ng-click="c.resetVerificationQueue()" title="Reset all evidence and findings to unverified state to demonstrate interactive verification">🔄 Reset for Demo</button>
                        <button class="fnx-btn fnx-btn-sm fnx-btn-outline" ng-click="c.confirmAllEvidence()">✓ Confirm Evidence</button>
                        <button class="fnx-btn fnx-btn-sm fnx-btn-outline" ng-click="c.confirmAllFindings()">✓ Confirm Findings</button>
                        <button class="fnx-btn fnx-btn-sm fnx-btn-success" ng-click="c.confirmAllPending()">✓ Batch Verify All Pending</button>
                    </div>
                </div>

                <!-- Zero Silent AI Decisions Policy Alert Banner -->
                <div class="fnx-zero-ai-banner mb-3">
                    <div class="banner-icon">🛡️</div>
                    <div class="banner-body">
                        <strong>ZERO SILENT AI DECISIONS ENFORCED:</strong>
                        <span>Machine extractions from JOREN multimodal processing, Byte-Level BPE tokenizer, and 9-stage agentic reasoning remain provisional recommendations. Human investigator confirmation is legally required before any finding or evidence enters the official fraud record.</span>
                    </div>
                    <div class="banner-badge">
                        <span class="badge" ng-class="c.getPendingVerificationCount() > 0 ? 'badge-warning' : 'badge-success'">
                            {{c.getPendingVerificationCount()}} Pending Verification
                        </span>
                    </div>
                </div>

                <!-- Verification Domain Filter Tabs -->
                <div class="fnx-verif-tabs-bar mb-3">
                    <button type="button" class="fnx-verif-tab-btn" ng-class="{'active': c.verificationQueueFilter === 'all'}" ng-click="c.setVerificationFilter('all')">
                        <span>All Intelligence Outputs</span>
                        <span class="tab-badge">{{c.activeInvestigationCase.evidence.length + c.activeInvestigationCase.findings.length}}</span>
                    </button>
                    <button type="button" class="fnx-verif-tab-btn" ng-class="{'active': c.verificationQueueFilter === 'evidence'}" ng-click="c.setVerificationFilter('evidence')">
                        <span>📁 Multimodal Evidence</span>
                        <span class="tab-badge">{{c.activeInvestigationCase.evidence.length}}</span>
                    </button>
                    <button type="button" class="fnx-verif-tab-btn" ng-class="{'active': c.verificationQueueFilter === 'findings'}" ng-click="c.setVerificationFilter('findings')">
                        <span>🎯 AI Findings & Hypotheses</span>
                        <span class="tab-badge">{{c.activeInvestigationCase.findings.length}}</span>
                    </button>
                    <button type="button" class="fnx-verif-tab-btn" ng-class="{'active': c.verificationQueueFilter === 'entities'}" ng-click="c.setVerificationFilter('entities')">
                        <span>🕸️ Extracted Graph Entities</span>
                        <span class="tab-badge">5</span>
                    </button>
                    <button type="button" class="fnx-verif-tab-btn" ng-class="{'active': c.verificationQueueFilter === 'contradictions'}" ng-click="c.setVerificationFilter('contradictions')">
                        <span>⚖️ Consistency & Signals</span>
                        <span class="tab-badge">3</span>
                    </button>
                </div>

                <!-- STREAM 1: MULTIMODAL EVIDENCE VERIFICATION STREAM -->
                <div class="fnx-card mb-4" ng-if="c.verificationQueueFilter === 'all' || c.verificationQueueFilter === 'evidence'">
                    <div class="fnx-card-header d-flex justify-content-between align-items-center">
                        <div class="card-header-title">
                            <span>📁 MULTIMODAL EVIDENCE VERIFICATION STREAM — JOREN EXTRACTIONS ({{c.activeInvestigationCase.evidence.length}})</span>
                        </div>
                        <span class="text-xs text-muted">SHA-256 Immutability Active &bull; Zero Modification</span>
                    </div>
                    <div class="fnx-card-body p-0">
                        <div class="fnx-verif-stream-list">
                            <div class="fnx-verif-stream-card" ng-repeat="ev in c.activeInvestigationCase.evidence" ng-class="{'card-verified': ev.status === 'Confirmed', 'card-rejected': ev.status === 'Rejected'}">
                                <div class="stream-card-header">
                                    <div class="stream-card-id-block">
                                        <span class="stream-icon">{{ev.icon || '📄'}}</span>
                                        <div>
                                            <div class="stream-id">{{ev.id}} &bull; <strong>{{ev.title}}</strong></div>
                                            <div class="stream-sub text-muted">{{ev.type}} &bull; Source: {{ev.source}} &bull; Submitted by: {{ev.submitter}} ({{ev.date}})</div>
                                        </div>
                                    </div>
                                    <div class="stream-status-block">
                                        <span class="fnx-status-chip" ng-class="'chip-' + ev.status.toLowerCase().replace(' ', '-')">
                                            {{ev.status}}
                                        </span>
                                    </div>
                                </div>
                                <div class="stream-card-body">
                                    <div class="stream-meta-row mb-2">
                                        <span class="badge-classification">Classification: <strong>{{ev.classification}}</strong></span>
                                        <span class="badge-pipeline">Pipeline: {{ev.pipeline || 'JOREN Multimodal Vision OCR'}}</span>
                                        <span class="badge-hash">SHA256: <code>{{ev.sha256 | limitTo:16}}...</code></span>
                                    </div>
                                    <div class="stream-extraction-box">
                                        <div class="extraction-lbl">INTELLIGENCE EXTRACTION (OCR / NLP):</div>
                                        <div class="extraction-content">{{ev.extracted_info}}</div>
                                        <div class="stream-tags-row mt-2" ng-if="ev.entities && ev.entities.length">
                                            <span class="ev-tag" ng-repeat="ent in ev.entities">🏷️ {{ent}}</span>
                                            <span class="ev-tag ev-tag-txn" ng-if="ev.transaction_ref">💳 {{ev.transaction_ref}}</span>
                                            <span class="ev-tag ev-tag-url" ng-if="ev.url_ref">🌐 {{ev.url_ref}}</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="stream-card-footer">
                                    <div class="stream-notes text-xs">
                                        <em>Forensic Note: {{ev.notes || 'Awaiting investigator verification sign-off.'}}</em>
                                    </div>
                                    <div class="stream-actions">
                                        <button type="button" class="fnx-btn fnx-btn-xs fnx-btn-success" ng-click="c.confirmEvidence(ev)" ng-disabled="ev.status === 'Confirmed'">
                                            {{ev.status === 'Confirmed' ? '✓ Evidence Verified' : '✓ Verify Evidence'}}
                                        </button>
                                        <button type="button" class="fnx-btn fnx-btn-xs fnx-btn-danger" ng-click="c.rejectEvidence(ev)" ng-disabled="ev.status === 'Rejected'">
                                            ✕ Reject
                                        </button>
                                        <button type="button" class="fnx-btn fnx-btn-xs fnx-btn-outline" ng-click="c.addEvidenceNote(ev)">
                                            💬 Add Note
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- STREAM 2: AI FINDINGS & HYPOTHESES VERIFICATION STREAM -->
                <div class="fnx-card mb-4" ng-if="c.verificationQueueFilter === 'all' || c.verificationQueueFilter === 'findings'">
                    <div class="fnx-card-header d-flex justify-content-between align-items-center">
                        <div class="card-header-title">
                            <span>🎯 AI-GENERATED INTELLIGENCE FINDINGS — 9-STAGE AGENTIC HYPOTHESES ({{c.activeInvestigationCase.findings.length}})</span>
                        </div>
                        <span class="text-xs text-muted">Provisional Output &bull; Requires Investigator Sign-off</span>
                    </div>
                    <div class="fnx-card-body p-0">
                        <div class="fnx-verif-stream-list">
                            <div class="fnx-verif-stream-card" ng-repeat="fnd in c.activeInvestigationCase.findings" ng-class="{'card-verified': fnd.status === 'Confirmed', 'card-rejected': fnd.status === 'Rejected'}">
                                <div class="stream-card-header">
                                    <div class="stream-card-id-block">
                                        <span class="stream-icon">💡</span>
                                        <div>
                                            <div class="stream-id">{{fnd.id}} &bull; <strong>{{fnd.title}}</strong></div>
                                            <div class="stream-sub text-muted">Source: {{fnd.source || '9-Stage Local-LLM Agentic Reasoning'}} &bull; Reviewer: {{fnd.reviewer || 'Pending Human Review'}} ({{fnd.reviewed_on || 'Awaiting Sign-off'}})</div>
                                        </div>
                                    </div>
                                    <div class="stream-confidence-badge">
                                        <span class="conf-lbl">Confidence:</span>
                                        <span class="conf-val" ng-class="fnd.confidence >= 95 ? 'text-success' : 'text-primary'">{{fnd.confidence}}%</span>
                                    </div>
                                    <div class="stream-status-block">
                                        <span class="fnx-status-chip" ng-class="'chip-' + fnd.status.toLowerCase().replace(' ', '-')">
                                            {{fnd.status}}
                                        </span>
                                    </div>
                                </div>
                                <div class="stream-card-body">
                                    <p class="finding-desc mb-2">{{fnd.description}}</p>
                                    <div class="finding-meta-row">
                                        <div class="meta-item">
                                            <strong>Supporting Evidence:</strong>
                                            <span class="badge-tag me-1" ng-repeat="s in fnd.supporting_evidence">{{s}}</span>
                                        </div>
                                        <div class="meta-item" ng-if="fnd.notes">
                                            <strong>Investigator Comment:</strong> {{fnd.notes}}
                                        </div>
                                    </div>
                                </div>
                                <div class="stream-card-footer">
                                    <div class="text-xs text-muted">
                                        Status: <strong ng-class="fnd.status === 'Confirmed' ? 'text-success' : 'text-warning'">{{fnd.status === 'Confirmed' ? 'Legally Admissible in Investigation Record' : 'Provisional Recommendation Only'}}</strong>
                                    </div>
                                    <div class="stream-actions">
                                        <button type="button" class="fnx-btn fnx-btn-xs fnx-btn-success" ng-click="c.confirmFinding(fnd)" ng-disabled="fnd.status === 'Confirmed'">
                                            {{fnd.status === 'Confirmed' ? '✓ Finding Confirmed' : '✓ Confirm Finding'}}
                                        </button>
                                        <button type="button" class="fnx-btn fnx-btn-xs fnx-btn-danger" ng-click="c.rejectFinding(fnd)" ng-disabled="fnd.status === 'Rejected'">
                                            ✕ Reject
                                        </button>
                                        <button type="button" class="fnx-btn fnx-btn-xs fnx-btn-outline" ng-click="c.addFindingNote(fnd)">
                                            📝 Edit Rationale
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- STREAM 3: EXTRACTED GRAPH ENTITIES & RELATIONSHIPS -->
                <div class="fnx-card mb-4" ng-if="c.verificationQueueFilter === 'all' || c.verificationQueueFilter === 'entities'">
                    <div class="fnx-card-header d-flex justify-content-between align-items-center">
                        <div class="card-header-title">
                            <span>🕸️ EXTRACTED ENTITIES & GRAPH RELATIONSHIPS — DYNAMIC BPE & KNOWLEDGE GRAPH (5)</span>
                        </div>
                        <span class="text-xs text-muted">Neo4j Entity Resolution &bull; 53 Node Types</span>
                    </div>
                    <div class="fnx-card-body p-0">
                        <table class="fnx-table">
                            <thead>
                                <tr>
                                    <th>ENTITY TYPE</th>
                                    <th>EXTRACTED VALUE</th>
                                    <th>THREAT / REPUTATION</th>
                                    <th>ASSOCIATED SYNDICATE / CLUSTER</th>
                                    <th>GRAPH CORRELATION</th>
                                    <th>VERIFICATION</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr ng-repeat="ind in c.activeInvestigationCase.cyber.indicators">
                                    <td><span class="badge badge-purple">{{ind.type}}</span></td>
                                    <td><code>{{ind.value}}</code></td>
                                    <td><span class="fnx-status-chip chip-high-risk">{{ind.reputation}}</span></td>
                                    <td><strong>{{ind.syndicate}}</strong></td>
                                    <td><span class="text-xs text-muted">{{ind.classification}}</span></td>
                                    <td>
                                        <button class="fnx-btn fnx-btn-xs" ng-class="ind.verified ? 'fnx-btn-success' : 'fnx-btn-outline'" ng-click="c.verifyEntity(ind)">
                                            {{ind.verified ? '✓ Verified' : 'Verify Entity'}}
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- STREAM 4: CROSS-CHANNEL CONTRADICTION & CONSISTENCY SIGNALS -->
                <div class="fnx-card mb-4" ng-if="c.verificationQueueFilter === 'all' || c.verificationQueueFilter === 'contradictions'">
                    <div class="fnx-card-header d-flex justify-content-between align-items-center">
                        <div class="card-header-title">
                            <span>⚖️ CROSS-CHANNEL CONTRADICTION & CONSISTENCY SIGNALS (11-STAGE FUSION)</span>
                        </div>
                        <span class="badge-tag bg-green text-white">0 Contradictions Detected</span>
                    </div>
                    <div class="fnx-card-body">
                        <div class="fnx-contradiction-grid">
                            <div class="fnx-signal-card signal-consistent">
                                <div class="signal-header">
                                    <span class="signal-icon">⏱️</span>
                                    <span class="signal-title">Temporal Chronology Check</span>
                                    <span class="signal-badge text-success">✓ 100% Consistent</span>
                                </div>
                                <div class="signal-desc">
                                    Phishing SMS received 14:10 IST &rarr; Malicious URL visited 14:15 IST &rarr; Tor session initiated 14:19 IST &rarr; Unauthorized UPI debit executed 14:22:18 IST. Perfect sequence alignment with zero time-travel paradoxes.
                                </div>
                            </div>
                            <div class="fnx-signal-card signal-anomaly">
                                <div class="signal-header">
                                    <span class="signal-icon">🌍</span>
                                    <span class="signal-title">Impossible Travel Anomaly Check</span>
                                    <span class="signal-badge text-warning">⚠️ Anomaly Flagged</span>
                                </div>
                                <div class="signal-desc">
                                    Victim mobile cellular IP located in Mumbai, India. NetBanking login session originated from Tor exit node IP 185.220.101.5 in Frankfurt, Germany within 4 minutes. Physical impossibility confirms remote session hijacking.
                                </div>
                            </div>
                            <div class="fnx-signal-card signal-consistent">
                                <div class="signal-header">
                                    <span class="signal-icon">💰</span>
                                    <span class="signal-title">Financial Ledger Reconciliation</span>
                                    <span class="signal-badge text-success">✓ Amount Reconciled</span>
                                </div>
                                <div class="signal-desc">
                                    Victim-claimed exposure of ₹ 85,000 matches transaction receipt PDF, debit alert email, and Partner Bank A settlement feed to the exact rupee (INR 85,000.00). No discrepancy detected.
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- STREAM 5: FORENSIC VERIFICATION CHECKLIST -->
                <div class="fnx-card mb-4">
                    <div class="fnx-card-header d-flex justify-content-between align-items-center">
                        <span class="card-header-title">📋 FORENSIC VERIFICATION CHECKLIST & AUDIT CRITERIA</span>
                        <span class="text-xs text-muted">Legal Chain of Custody Required</span>
                    </div>
                    <div class="fnx-card-body">
                        <div class="fnx-checklist-grid">
                            <label class="fnx-chk-item">
                                <input type="checkbox" checked disabled>
                                <span><strong>Customer KYC Identity:</strong> National PAN / Aadhaar verified. Remitter identity authenticated against core banking record.</span>
                            </label>
                            <label class="fnx-chk-item">
                                <input type="checkbox" checked disabled>
                                <span><strong>Bank Statement Corroboration:</strong> Transaction reference UPI/2026/84920194819 matches debit ledger.</span>
                            </label>
                            <label class="fnx-chk-item">
                                <input type="checkbox" ng-checked="c.isEvidenceVerified()" disabled>
                                <span><strong>Artifact Provenance Hashes:</strong> SHA-256 hashes generated for all 4 items and stored in tamper-evident audit log.</span>
                            </label>
                            <label class="fnx-chk-item">
                                <input type="checkbox" ng-checked="c.isFindingsConfirmed()" disabled>
                                <span><strong>Attack Vector Identified:</strong> Phishing SMS + Credential Harvester + Foreign Tor IP verified.</span>
                            </label>
                        </div>
                    </div>
                </div>

                <!-- Next Steps Progression Footer -->
                <div class="fnx-verif-next-bar p-3 bg-white border rounded d-flex justify-content-between align-items-center">
                    <div>
                        <strong>Verification Progress:</strong>
                        <span class="ms-2" ng-if="c.getPendingVerificationCount() > 0">
                            <span class="text-warning font-monospace fw-bold">{{c.getPendingVerificationCount()}} items</span> pending human review before resolution can be signed.
                        </span>
                        <span class="ms-2 text-success fw-bold" ng-if="c.getPendingVerificationCount() === 0">
                            🎉 All evidence items and intelligence findings are fully human-verified!
                        </span>
                    </div>
                    <div class="d-flex gap-2">
                        <button class="fnx-btn fnx-btn-sm fnx-btn-primary" ng-click="c.setInvestigationTab('partnerRequests')">🤝 Proceed to Partner Verification &rarr;</button>
                        <button class="fnx-btn fnx-btn-sm fnx-btn-outline" ng-click="c.openGenAIModal()">✨ Generate Synthesis</button>
                        <button class="fnx-btn fnx-btn-sm fnx-btn-success" ng-click="c.setInvestigationTab('decision')">🏛️ Final Decision &rarr;</button>
                    </div>
                </div>

            </div>"""

# Replace Section 3 in template_code
verif_start_marker = "<!-- ----------------------------------------\n                 SECTION 3: VERIFICATION QUEUE"
verif_end_marker = "<!-- ----------------------------------------\n                 SECTION 4: INVESTIGATION (JOURNAL)"

v_start = template_code.find(verif_start_marker)
v_end = template_code.find(verif_end_marker)

if v_start != -1 and v_end != -1:
    print(f"Replacing Verification section from index {v_start} to {v_end}")
    template_code = template_code[:v_start] + new_verif_section + "\n\n" + template_code[v_end:]
    with open('d:/KPMG/build_vw_template.py', 'w', encoding='utf-8') as f:
        f.write(template_code)
    subprocess.run(['python', 'd:/KPMG/build_vw_template.py'], check=True)
    print("Template script generated successfully.")
else:
    print("ERROR: Could not locate Section 3 and Section 4 markers in build_vw_template.py")
    sys.exit(1)

# ==========================================
# 4. DEPLOY WIDGET TO SERVICENOW
# ==========================================
print("4. Deploying updated Verification Workspace to ServiceNow instance...")
subprocess.run(['python', 'd:/KPMG/deploy_verification_workspace.py'], check=True)

print("=== ALL UPDATES DEPLOYED SUCCESSFULLY! ===")
