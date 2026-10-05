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

print('Fetched live widget successfully. Template len:', len(template))

# -------------------------------------------------------------
# 2. UPDATE GLOBAL LOGO IN CUSTOMER PORTAL HEADER
# -------------------------------------------------------------
old_brand_pat = re.compile(r'<div class="fnx-header-brand"[^>]*>.*?</div>', re.DOTALL)
new_brand_html = '''<div class="fnx-header-brand" ng-click="c.navigate('dashboard')" style="display: flex; align-items: center; gap: 0.75rem; cursor: pointer;">
                <svg width="34" height="34" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M26 4L8 11v14c0 11.05 7.68 21.37 18 24 10.32-2.63 18-12.95 18-24V11L26 4z" fill="#00B8D9" fill-opacity="0.18" stroke="#00B8D9" stroke-width="2.5"/>
                    <circle cx="24" cy="24" r="7" fill="none" stroke="#00B8D9" stroke-width="2.5"/>
                    <line x1="29" y1="29" x2="35" y2="35" stroke="#00B8D9" stroke-width="2.5" stroke-linecap="round"/>
                </svg>
                <div style="display: flex; align-items: baseline; gap: 0.65rem;">
                    <span style="font-size: 1.25rem; font-weight: 800; color: #FFFFFF; letter-spacing: 0.5px; font-family: 'Outfit', sans-serif;">FRAUDNEXUS</span>
                    <span style="font-size: 0.78rem; color: #94A3B8; font-weight: 400; border-left: 1px solid rgba(255,255,255,0.25); padding-left: 0.75rem;">Financial &amp; Cyber Fraud Investigation Hub</span>
                </div>
            </div>'''

m_brand = old_brand_pat.search(template)
if m_brand:
    template = template[:m_brand.start()] + new_brand_html + template[m_brand.end():]
    print('Updated Customer Header Brand with Global Logo.')
else:
    print('Warning: fnx-header-brand pattern not found!')

# -------------------------------------------------------------
# 3. UPDATE CUSTOMER HEADER RIGHT (Notifications & User Avatar)
# -------------------------------------------------------------
old_header_right_sub = '<span class="fnx-avatar-lg">{{c.user.name.charAt(0).toUpperCase()}}</span>'
if old_header_right_sub in template:
    new_avatar = '''<span class="fnx-avatar-lg" style="background:#00B8D9 !important; color:#071527 !important; font-weight:800 !important;">{{(c.customer.name || c.user.name || 'Arun Kumar').charAt(0).toUpperCase()}}</span>
                    <span style="color:#FFFFFF; font-weight:600; font-size:0.88rem; margin:0 0.35rem 0 0.5rem;">{{c.customer.name || c.user.name || 'Arun Kumar'}}</span>'''
    template = template.replace(old_header_right_sub, new_avatar, 1)
    print('Updated Customer Header Profile Avatar & Name.')

# Also add badge '3' to notification bell if not present
if '<span class="fnx-notif-dot" ng-if="c.cases.length > 0"></span>' in template:
    template = template.replace('<span class="fnx-notif-dot" ng-if="c.cases.length > 0"></span>', '<span class="fnx-notif-badge">3</span>', 1)
    print('Updated Notification Bell Badge.')

# -------------------------------------------------------------
# 4. UPDATE SIDEBAR: ADD NEED SUPPORT CARD AT BOTTOM
# -------------------------------------------------------------
old_sidebar_close = '</nav>\n    </aside>'
if old_sidebar_close in template:
    new_sidebar_footer = '''    <div class="fnx-sidebar-support-card">
            <div class="fnx-ssc-icon">&#127911;</div>
            <div class="fnx-ssc-title">Need Support?</div>
            <div class="fnx-ssc-sub">Contact our support team</div>
            <button type="button" class="fnx-btn-ssc" ng-click="c.navigate('help')">Contact Support &rarr;</button>
        </div>
        </nav>
    </aside>'''
    template = template.replace(old_sidebar_close, new_sidebar_footer, 1)
    print('Added Need Support card to sidebar bottom.')

# -------------------------------------------------------------
# 5. REPLACE 4A. DASHBOARD VIEW WITH POLARIS / UI16 MODERN LAYOUT
# -------------------------------------------------------------
idx_dash_start = template.find('<!-- ============ 4A. DASHBOARD VIEW')
if idx_dash_start == -1:
    idx_dash_start = template.find('4A. DASHBOARD VIEW')
    idx_dash_start = template.rfind('<!--', 0, idx_dash_start)

idx_dash_end = template.find('<!-- ============ 4B. CUSTOMER PROFILE & KYC VIEW')
if idx_dash_end == -1:
    idx_dash_end = template.find('4B. CUSTOMER PROFILE')
    idx_dash_end = template.rfind('<!--', 0, idx_dash_end)

print(f'Dashboard template slice: {idx_dash_start} to {idx_dash_end}')

new_dashboard_html = '''<!-- ============ 4A. DASHBOARD VIEW (MODERN SERVICENOW UI16 / POLARIS EXPERIENCE) ============ -->
        <div ng-if="c.currentView === 'dashboard'" class="fnx-dashboard-view">
            
            <!-- Dashboard Main Container (2-Column Layout) -->
            <div class="fnx-dash-layout">
                
                <!-- LEFT COLUMN: Main Activity & Analytics (approx 72%) -->
                <div class="fnx-dash-main-col">
                    
                    <!-- Top Welcome & Report Button Row -->
                    <div class="fnx-dash-top-bar">
                        <div class="fnx-dash-greeting">
                            <h1 class="fnx-dash-heading">Welcome Back, {{c.customer.name || c.user.name || 'Arun Kumar'}}!</h1>
                            <p class="fnx-dash-subheading">Here's an overview of your fraud reports and case activities.</p>
                        </div>
                        <button type="button" class="fnx-btn-report-header" ng-click="c.navigate('reportFraud')">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/></svg>
                            Report Fraud
                        </button>
                    </div>

                    <!-- 4 Metric KPI Cards Row -->
                    <div class="fnx-kpi-quad-row">
                        <!-- Card 1: Total Cases -->
                        <div class="fnx-kpi-card kpi-card-total">
                            <div class="fnx-kpi-icon-wrap icon-total">
                                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
                            </div>
                            <div class="fnx-kpi-number">{{c.stats.total || c.cases.length || 5}}</div>
                            <div class="fnx-kpi-title">Total Cases</div>
                            <div class="fnx-kpi-subtitle">All fraud reports you have submitted</div>
                        </div>

                        <!-- Card 2: Active Cases -->
                        <div class="fnx-kpi-card kpi-card-active">
                            <div class="fnx-kpi-icon-wrap icon-active">
                                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                            </div>
                            <div class="fnx-kpi-number">{{c.stats.active || 2}}</div>
                            <div class="fnx-kpi-title">Active Cases</div>
                            <div class="fnx-kpi-subtitle">Under investigation or in progress</div>
                        </div>

                        <!-- Card 3: Pending Cases -->
                        <div class="fnx-kpi-card kpi-card-pending">
                            <div class="fnx-kpi-icon-wrap icon-pending">
                                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                            </div>
                            <div class="fnx-kpi-number">{{c.stats.pending || 2}}</div>
                            <div class="fnx-kpi-title">Pending Cases</div>
                            <div class="fnx-kpi-subtitle">Awaiting review or action</div>
                        </div>

                        <!-- Card 4: Closed Cases -->
                        <div class="fnx-kpi-card kpi-card-closed">
                            <div class="fnx-kpi-icon-wrap icon-closed">
                                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                            </div>
                            <div class="fnx-kpi-number">{{c.stats.closed || 1}}</div>
                            <div class="fnx-kpi-title">Closed Cases</div>
                            <div class="fnx-kpi-subtitle">Resolved and closed</div>
                        </div>
                    </div>

                    <!-- Middle Analytics Row: Case Status Overview + Incident Type Distribution -->
                    <div class="fnx-analytics-twin-grid">
                        <!-- Chart 1: Case Status Overview (Donut Chart) -->
                        <div class="fnx-panel-card">
                            <div class="fnx-panel-header">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 17v-4M12 17v-8M17 17v-6"/></svg>
                                <span>Case Status Overview</span>
                            </div>
                            <div class="fnx-donut-container">
                                <!-- Donut SVG -->
                                <div class="fnx-donut-chart-wrap">
                                    <svg class="fnx-donut-svg" width="150" height="150" viewBox="0 0 160 160">
                                        <!-- Background circle -->
                                        <circle cx="80" cy="80" r="50" fill="none" stroke="#F1F5F9" stroke-width="22"/>
                                        <!-- Segment 1: Investigation (Green, 40% = 125.66) -->
                                        <circle cx="80" cy="80" r="50" fill="none" stroke="#10B981" stroke-width="22"
                                                stroke-dasharray="125.66 314.16" stroke-dashoffset="0" transform="rotate(-90 80 80)"/>
                                        <!-- Segment 2: Initial Review (Blue, 20% = 62.83) -->
                                        <circle cx="80" cy="80" r="50" fill="none" stroke="#0284C7" stroke-width="22"
                                                stroke-dasharray="62.83 314.16" stroke-dashoffset="-125.66" transform="rotate(-90 80 80)"/>
                                        <!-- Segment 3: Caseworker Allotted (Orange, 20% = 62.83) -->
                                        <circle cx="80" cy="80" r="50" fill="none" stroke="#F59E0B" stroke-width="22"
                                                stroke-dasharray="62.83 314.16" stroke-dashoffset="-188.49" transform="rotate(-90 80 80)"/>
                                        <!-- Segment 4: Closed (Red, 20% = 62.83) -->
                                        <circle cx="80" cy="80" r="50" fill="none" stroke="#EF4444" stroke-width="22"
                                                stroke-dasharray="62.83 314.16" stroke-dashoffset="-251.32" transform="rotate(-90 80 80)"/>
                                        <!-- Center Donut Text -->
                                        <text x="80" y="76" text-anchor="middle" font-size="24" font-weight="800" fill="#0F172A">5</text>
                                        <text x="80" y="93" text-anchor="middle" font-size="11" font-weight="600" fill="#64748B">Total Cases</text>
                                    </svg>
                                </div>

                                <!-- Legend List -->
                                <div class="fnx-donut-legend">
                                    <div class="fnx-legend-item">
                                        <div class="fnx-legend-left">
                                            <span class="fnx-legend-dot dot-green"></span>
                                            <span class="fnx-legend-name">Investigation</span>
                                        </div>
                                        <div class="fnx-legend-right">
                                            <strong class="fnx-legend-count">2</strong>
                                            <span class="fnx-legend-pct">40%</span>
                                        </div>
                                    </div>
                                    <div class="fnx-legend-item">
                                        <div class="fnx-legend-left">
                                            <span class="fnx-legend-dot dot-blue"></span>
                                            <span class="fnx-legend-name">Initial Review</span>
                                        </div>
                                        <div class="fnx-legend-right">
                                            <strong class="fnx-legend-count">1</strong>
                                            <span class="fnx-legend-pct">20%</span>
                                        </div>
                                    </div>
                                    <div class="fnx-legend-item">
                                        <div class="fnx-legend-left">
                                            <span class="fnx-legend-dot dot-orange"></span>
                                            <span class="fnx-legend-name">Caseworker Allotted</span>
                                        </div>
                                        <div class="fnx-legend-right">
                                            <strong class="fnx-legend-count">1</strong>
                                            <span class="fnx-legend-pct">20%</span>
                                        </div>
                                    </div>
                                    <div class="fnx-legend-item">
                                        <div class="fnx-legend-left">
                                            <span class="fnx-legend-dot dot-red"></span>
                                            <span class="fnx-legend-name">Closed</span>
                                        </div>
                                        <div class="fnx-legend-right">
                                            <strong class="fnx-legend-count">1</strong>
                                            <span class="fnx-legend-pct">20%</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Chart 2: Incident Type Distribution -->
                        <div class="fnx-panel-card">
                            <div class="fnx-panel-header">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><path d="M12 20V10M18 20V4M6 20v-4"/></svg>
                                <span>Incident Type Distribution</span>
                            </div>
                            <div class="fnx-bars-container">
                                <!-- Row 1: Payment Fraud -->
                                <div class="fnx-bar-row">
                                    <span class="fnx-bar-label">Payment Fraud</span>
                                    <div class="fnx-bar-track">
                                        <div class="fnx-bar-fill fill-blue" style="width: 100%;"></div>
                                    </div>
                                    <span class="fnx-bar-val">2</span>
                                </div>
                                <!-- Row 2: Phishing -->
                                <div class="fnx-bar-row">
                                    <span class="fnx-bar-label">Phishing</span>
                                    <div class="fnx-bar-track">
                                        <div class="fnx-bar-fill fill-skyblue" style="width: 50%;"></div>
                                    </div>
                                    <span class="fnx-bar-val">1</span>
                                </div>
                                <!-- Row 3: Account Compromise -->
                                <div class="fnx-bar-row">
                                    <span class="fnx-bar-label">Account Compromise</span>
                                    <div class="fnx-bar-track">
                                        <div class="fnx-bar-fill fill-purple" style="width: 50%;"></div>
                                    </div>
                                    <span class="fnx-bar-val">1</span>
                                </div>
                                <!-- Row 4: Online Shopping Fraud -->
                                <div class="fnx-bar-row">
                                    <span class="fnx-bar-label">Online Shopping Fraud</span>
                                    <div class="fnx-bar-track">
                                        <div class="fnx-bar-fill fill-pink" style="width: 50%;"></div>
                                    </div>
                                    <span class="fnx-bar-val">1</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Lower Section: Recent Cases Table -->
                    <div class="fnx-panel-card fnx-recent-cases-card">
                        <div class="fnx-panel-header-row">
                            <div class="fnx-panel-header" style="margin-bottom:0;">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
                                <span>Recent Cases</span>
                            </div>
                            <a class="fnx-link-view-all" ng-click="c.navigate('trackCases')">View All &rarr;</a>
                        </div>

                        <div class="fnx-table-responsive" style="margin-top: 1rem;">
                            <table class="fnx-cases-table">
                                <thead>
                                    <tr>
                                        <th>Case ID</th>
                                        <th>Incident Type</th>
                                        <th>Date Submitted</th>
                                        <th>Status</th>
                                        <th>Last Updated</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr ng-repeat="cs in c.cases | limitTo:5">
                                        <td class="font-mono"><strong>{{cs.number}}</strong></td>
                                        <td>
                                            <span class="fnx-type-cell">
                                                <svg ng-if="cs.type.includes('Payment')" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#EF4444" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
                                                <svg ng-if="cs.type.includes('Phishing')" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
                                                <svg ng-if="cs.type.includes('Account')" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#A855F7" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                                                <svg ng-if="cs.type.includes('Shopping')" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#EC4899" stroke-width="2"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
                                                <span>{{cs.type}}</span>
                                            </span>
                                        </td>
                                        <td>{{cs.incident_date}}</td>
                                        <td>
                                            <span class="fnx-status-pill" ng-class="{
                                                'st-investigation': cs.status === 'Investigation',
                                                'st-initial': cs.status === 'Initial Review',
                                                'st-allotted': cs.status === 'Caseworker Allotted',
                                                'st-closed': cs.status === 'Closed',
                                                'st-pending': cs.status === 'Pending' || cs.status === 'Case Submitted'
                                            }">{{cs.status}}</span>
                                        </td>
                                        <td>{{cs.last_updated || cs.incident_date}}</td>
                                        <td>
                                            <button type="button" class="fnx-btn-view-pill" ng-click="c.viewCase(cs)">View &rarr;</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Need Guidance Banner -->
                    <div class="fnx-guidance-banner">
                        <div class="fnx-guidance-content">
                            <div class="fnx-guidance-title">
                                <span class="fnx-guidance-lamp">&#128161;</span>
                                <strong>Need Guidance?</strong>
                            </div>
                            <p class="fnx-guidance-desc">Not sure what information to provide or which category fits your incident?</p>
                            <button type="button" class="fnx-btn-ask-ai" ng-click="c.showAI = true">
                                <span class="fnx-sparkle-star">&#10024;</span>
                                <span>Ask FRAUDNEXUS AI</span>
                            </button>
                        </div>
                        <div class="fnx-guidance-robot-art">
                            <svg width="84" height="84" viewBox="0 0 100 100" fill="none">
                                <circle cx="50" cy="50" r="44" fill="#E0F2FE" fill-opacity="0.6"/>
                                <rect x="30" y="32" width="40" height="34" rx="8" fill="#0284C7"/>
                                <circle cx="42" cy="46" r="4" fill="#FFFFFF"/>
                                <circle cx="58" cy="46" r="4" fill="#FFFFFF"/>
                                <path d="M42 56h16" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
                                <line x1="50" y1="24" x2="50" y2="32" stroke="#0284C7" stroke-width="3" stroke-linecap="round"/>
                                <circle cx="50" cy="22" r="3" fill="#00B8D9"/>
                                <path d="M22 45v8M78 45v8" stroke="#0284C7" stroke-width="3" stroke-linecap="round"/>
                            </svg>
                        </div>
                    </div>

                </div>

                <!-- RIGHT COLUMN: User Info, Quick Actions & Tips (approx 28%) -->
                <div class="fnx-dash-side-col">
                    
                    <!-- Card 1: Your Information -->
                    <div class="fnx-panel-card">
                        <div class="fnx-panel-header-row">
                            <div class="fnx-panel-header" style="margin-bottom:0;">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                                <span>Your Information</span>
                            </div>
                            <button type="button" class="fnx-btn-edit-pill" ng-click="c.navigate('editProfile')">Edit</button>
                        </div>
                        
                        <div class="fnx-user-info-kv-list">
                            <div class="fnx-kv-row">
                                <span class="fnx-kv-k">Name</span>
                                <span class="fnx-kv-v">{{c.customer.name || c.user.name || 'Arun Kumar'}}</span>
                            </div>
                            <div class="fnx-kv-row">
                                <span class="fnx-kv-k">Customer ID</span>
                                <span class="fnx-kv-v font-mono">{{c.customer.customer_id || 'CNX-2026-001034'}}</span>
                            </div>
                            <div class="fnx-kv-row">
                                <span class="fnx-kv-k">Email</span>
                                <span class="fnx-kv-v">{{c.customer.email || c.user.email || 'arun.kumar@example.com'}}</span>
                            </div>
                            <div class="fnx-kv-row">
                                <span class="fnx-kv-k">Mobile</span>
                                <span class="fnx-kv-v">{{c.customer.mobile || '+91 9876543210'}}</span>
                            </div>
                        </div>
                    </div>

                    <!-- Card 2: Quick Actions -->
                    <div class="fnx-panel-card">
                        <div class="fnx-panel-header">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                            <span>Quick Actions</span>
                        </div>
                        <div class="fnx-quick-actions-quad">
                            <!-- Action 1: Report Fraud -->
                            <div class="fnx-qa-tile tile-blue" ng-click="c.navigate('reportFraud')">
                                <div class="fnx-qa-icon icon-blue">
                                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/></svg>
                                </div>
                                <span class="fnx-qa-label">Report Fraud</span>
                            </div>
                            <!-- Action 2: Track Cases -->
                            <div class="fnx-qa-tile tile-green" ng-click="c.navigate('trackCases')">
                                <div class="fnx-qa-icon icon-green">
                                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                                </div>
                                <span class="fnx-qa-label">Track Cases</span>
                            </div>
                            <!-- Action 3: Upload Evidence -->
                            <div class="fnx-qa-tile tile-purple" ng-click="c.navigate('evidenceVault')">
                                <div class="fnx-qa-icon icon-purple">
                                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#9333EA" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                                </div>
                                <span class="fnx-qa-label">Upload Evidence</span>
                            </div>
                            <!-- Action 4: Help & Support -->
                            <div class="fnx-qa-tile tile-orange" ng-click="c.navigate('help')">
                                <div class="fnx-qa-icon icon-orange">
                                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                                </div>
                                <span class="fnx-qa-label">Help &amp; Support</span>
                            </div>
                        </div>
                    </div>

                    <!-- Card 3: Fraud Prevention Tips -->
                    <div class="fnx-panel-card">
                        <div class="fnx-panel-header">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                            <span>Fraud Prevention Tips</span>
                        </div>
                        <div class="fnx-tips-list">
                            <div class="fnx-tip-item">
                                <span class="fnx-tip-icon tip-red">&#128683;</span>
                                <span class="fnx-tip-text">Never share OTP, PIN, UPI PIN or passwords.</span>
                            </div>
                            <div class="fnx-tip-item">
                                <span class="fnx-tip-icon tip-blue">&#127760;</span>
                                <span class="fnx-tip-text">Verify the authenticity of websites and apps.</span>
                            </div>
                            <div class="fnx-tip-item">
                                <span class="fnx-tip-icon tip-amber">&#9888;&#65039;</span>
                                <span class="fnx-tip-text">Be cautious of unsolicited calls and messages.</span>
                            </div>
                            <div class="fnx-tip-item">
                                <span class="fnx-tip-icon tip-green">&#9989;</span>
                                <span class="fnx-tip-text">Use trusted and secure payment methods.</span>
                            </div>
                            <div class="fnx-tip-item">
                                <span class="fnx-tip-icon tip-info">&#8505;&#65039;</span>
                                <span class="fnx-tip-text">Report suspicious activities immediately.</span>
                            </div>
                        </div>
                    </div>

                </div>

            </div>

        </div>

        '''

template = template[:idx_dash_start] + new_dashboard_html + template[idx_dash_end:]
print('Replaced 4A. DASHBOARD VIEW successfully.')

# -------------------------------------------------------------
# 6. UPDATE CLIENT SCRIPT DEMO DATA FOR ARUN KUMAR & 5 CASES
# -------------------------------------------------------------
# 5 standard reference cases
sample_cases_js = '''[
            { sys_id: 'dc01', number: 'FNX-2026-001034', type: 'Payment Fraud', incident_date: '02 Oct 2026', severity: 'High', status: 'Investigation', last_updated: '03 Oct 2026', u_short_description: 'Unauthorized UPI debit transaction' },
            { sys_id: 'dc02', number: 'FNX-2026-001021', type: 'Phishing', incident_date: '28 Sep 2026', severity: 'Critical', status: 'Initial Review', last_updated: '29 Sep 2026', u_short_description: 'Fake netbanking credentials harvest' },
            { sys_id: 'dc03', number: 'FNX-2026-001015', type: 'Account Compromise', incident_date: '20 Sep 2026', severity: 'High', status: 'Caseworker Allotted', last_updated: '22 Sep 2026', u_short_description: 'SIM swap & account takeover attempt' },
            { sys_id: 'dc04', number: 'FNX-2026-001008', type: 'Online Shopping Fraud', incident_date: '14 Sep 2026', severity: 'Medium', status: 'Closed', last_updated: '18 Sep 2026', u_short_description: 'Counterfeit merchant delivery fraud' },
            { sys_id: 'dc05', number: 'FNX-2026-001002', type: 'Payment Fraud', incident_date: '05 Sep 2026', severity: 'Medium', status: 'Pending', last_updated: '06 Sep 2026', u_short_description: 'Duplicate charge on payment gateway' }
        ]'''

# Update loadDemoSession
idx_ld = client_script.find('c.loadDemoSession =')
idx_ld_end = client_script.find('c.editProfileForm =')
if idx_ld != -1 and idx_ld_end != -1:
    new_load_demo = f'''c.loadDemoSession = function() {{
        c.user = {{ sys_id: 'demo_u01', name: 'Arun Kumar', email: 'arun.kumar@example.com', user_name: 'arun.kumar' }};
        c.customer = {{ sys_id: 'demo_c01', customer_id: 'CNX-2026-001034', name: 'Arun Kumar', email: 'arun.kumar@example.com', mobile: '+91 9876543210', dob: '1990-01-15', gender: 'Male', occupation: 'Software Professional', address: 'Indiranagar, Bengaluru, Karnataka 560038', kyc_status: 'Verified', gov_id_type: 'Aadhaar', masked_id: 'XXXX-XXXX-4567' }};
        c.cases = {sample_cases_js};
        c.stats = {{ total: 5, active: 2, pending: 2, closed: 1 }};
        c.currentView = 'dashboard';
    }};

    '''
    client_script = client_script[:idx_ld] + new_load_demo + client_script[idx_ld_end:]
    print('Updated c.loadDemoSession with Arun Kumar & 5 cases.')

# Also update c.loadCases fallback
target_fallback_search = 'c.stats = { total: 2, active: 2, resolved: 0, closed: 0 };'
if target_fallback_search in client_script:
    client_script = client_script.replace(
        'c.cases = [\n                    { sys_id: \'dc01\', number: \'FNX-2026-001001\', type: \'Payment Fraud\', incident_date: \'2026-09-15\', severity: \'High\', status: \'Investigation\', u_short_description: \'UPI fraud - product not delivered\' },\n                    { sys_id: \'dc02\', number: \'FNX-2026-001002\', type: \'Phishing\', incident_date: \'2026-09-20\', severity: \'Critical\', status: \'Initial Review\', u_short_description: \'Fake bank portal phishing\' }\n                ];\n                c.stats = { total: 2, active: 2, resolved: 0, closed: 0 };',
        f'c.cases = {sample_cases_js};\n                c.stats = {{ total: 5, active: 2, pending: 2, closed: 1 }};',
        1
    )
    print('Updated c.loadCases fallback with 5 cases.')

# -------------------------------------------------------------
# 7. APPEND MODERN POLARIS / UI16 CSS STYLES
# -------------------------------------------------------------
polaris_css = '''
/* ============================================================
   FRAUDNEXUS CUSTOMER PORTAL - SERVICENOW UI16 / POLARIS THEME
   ============================================================ */

/* Topbar Notification Badge */
.fnx-notif-badge {
    position: absolute !important;
    top: -4px !important;
    right: -4px !important;
    background: #EF4444 !important;
    color: #FFFFFF !important;
    font-size: 0.65rem !important;
    font-weight: 800 !important;
    border-radius: 50% !important;
    width: 17px !important;
    height: 17px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 2px 5px rgba(239,68,68,0.4) !important;
}

/* Sidebar Styling & Active Pill */
.fnx-sidebar {
    background-color: #071527 !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}

.fnx-nav-item {
    color: #94A3B8 !important;
    border-radius: 8px !important;
    margin: 0.25rem 0.75rem !important;
    padding: 0.65rem 1rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    transition: all 0.15s ease !important;
}

.fnx-nav-item:hover {
    background-color: rgba(255,255,255,0.06) !important;
    color: #FFFFFF !important;
}

.fnx-nav-item.active {
    background-color: #0284C7 !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 12px rgba(2,132,199,0.3) !important;
}

.fnx-sidebar-support-card {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    margin: 3rem 0.75rem 1.5rem 0.75rem !important;
    text-align: left !important;
}

.fnx-ssc-icon {
    font-size: 1.5rem !important;
    margin-bottom: 0.35rem !important;
}

.fnx-ssc-title {
    color: #FFFFFF !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
}

.fnx-ssc-sub {
    color: #94A3B8 !important;
    font-size: 0.76rem !important;
    margin: 0.15rem 0 0.75rem 0 !important;
}

.fnx-btn-ssc {
    background: transparent !important;
    border: 1px solid rgba(255, 255, 255, 0.25) !important;
    color: #FFFFFF !important;
    border-radius: 20px !important;
    padding: 0.35rem 0.75rem !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    width: 100% !important;
    text-align: center !important;
    transition: all 0.15s !important;
}

.fnx-btn-ssc:hover {
    background: rgba(255, 255, 255, 0.12) !important;
    border-color: #FFFFFF !important;
}

/* Main Dashboard Canvas */
.fnx-content {
    background-color: #F4F7FB !important;
}

.fnx-dashboard-view {
    max-width: 1550px !important;
    margin: 0 auto !important;
}

.fnx-dash-layout {
    display: flex !important;
    gap: 1.5rem !important;
    align-items: flex-start !important;
}

.fnx-dash-main-col {
    flex: 1 !important;
    min-width: 0 !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 1.25rem !important;
}

.fnx-dash-side-col {
    width: 320px !important;
    flex-shrink: 0 !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 1.25rem !important;
}

/* Top Greeting Bar */
.fnx-dash-top-bar {
    display: flex !important;
    justify-content: space-between !important;
    align-items: flex-start !important;
}

.fnx-dash-heading {
    font-size: 1.65rem !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    letter-spacing: -0.3px !important;
    margin: 0 !important;
}

.fnx-dash-subheading {
    font-size: 0.95rem !important;
    color: #64748B !important;
    margin: 0.3rem 0 0 0 !important;
}

.fnx-btn-report-header {
    background: #0B1B33 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.25rem !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
    box-shadow: 0 4px 12px rgba(11,27,51,0.2) !important;
    transition: transform 0.15s, background 0.15s !important;
}

.fnx-btn-report-header:hover {
    background: #122B52 !important;
    transform: translateY(-1px) !important;
}

/* KPI Quad Row */
.fnx-kpi-quad-row {
    display: grid !important;
    grid-template-columns: repeat(4, 1fr) !important;
    gap: 1rem !important;
}

.fnx-kpi-card {
    border-radius: 12px !important;
    padding: 1.15rem 1.25rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
    display: flex !important;
    flex-direction: column !important;
}

.fnx-kpi-card:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(0,0,0,0.06) !important;
}

.kpi-card-total {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
}

.kpi-card-active {
    background: #F0FDF4 !important;
    border: 1px solid #DCFCE7 !important;
}

.kpi-card-pending {
    background: #FFFBEB !important;
    border: 1px solid #FEF3C7 !important;
}

.kpi-card-closed {
    background: #FEF2F2 !important;
    border: 1px solid #FEE2E2 !important;
}

.fnx-kpi-icon-wrap {
    width: 42px !important;
    height: 42px !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin-bottom: 0.6rem !important;
}

.icon-total { background: #DBEAFE !important; }
.icon-active { background: #DCFCE7 !important; }
.icon-pending { background: #FEF3C7 !important; }
.icon-closed { background: #FEE2E2 !important; }

.fnx-kpi-number {
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    line-height: 1 !important;
}

.fnx-kpi-title {
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    color: #1E293B !important;
    margin-top: 0.35rem !important;
}

.fnx-kpi-subtitle {
    font-size: 0.74rem !important;
    color: #64748B !important;
    margin-top: 0.2rem !important;
}

/* Panel Card Base */
.fnx-panel-card {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 1.25rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
}

.fnx-panel-header {
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: #0F172A !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
    margin-bottom: 1.15rem !important;
}

.fnx-panel-header-row {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    margin-bottom: 0.75rem !important;
}

/* Analytics Twin Grid */
.fnx-analytics-twin-grid {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 1.25rem !important;
}

/* Donut Chart Layout */
.fnx-donut-container {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 1.5rem !important;
}

.fnx-donut-chart-wrap {
    flex-shrink: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

.fnx-donut-legend {
    flex: 1 !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 0.65rem !important;
}

.fnx-legend-item {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    font-size: 0.85rem !important;
}

.fnx-legend-left {
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
}

.fnx-legend-dot {
    width: 10px !important;
    height: 10px !important;
    border-radius: 50% !important;
}

.dot-green { background: #10B981 !important; }
.dot-blue { background: #0284C7 !important; }
.dot-orange { background: #F59E0B !important; }
.dot-red { background: #EF4444 !important; }

.fnx-legend-name {
    color: #334155 !important;
    font-weight: 500 !important;
}

.fnx-legend-right {
    display: flex !important;
    align-items: center !important;
    gap: 0.75rem !important;
}

.fnx-legend-count {
    color: #0F172A !important;
    font-weight: 700 !important;
}

.fnx-legend-pct {
    color: #64748B !important;
    font-size: 0.78rem !important;
    min-width: 32px !important;
    text-align: right !important;
}

/* Incident Type Bars */
.fnx-bars-container {
    display: flex !important;
    flex-direction: column !important;
    gap: 1rem !important;
    margin-top: 0.35rem !important;
}

.fnx-bar-row {
    display: flex !important;
    align-items: center !important;
    gap: 0.85rem !important;
}

.fnx-bar-label {
    width: 155px !important;
    font-size: 0.84rem !important;
    color: #334155 !important;
    font-weight: 500 !important;
    flex-shrink: 0 !important;
}

.fnx-bar-track {
    flex: 1 !important;
    height: 18px !important;
    background: #F1F5F9 !important;
    border-radius: 6px !important;
    overflow: hidden !important;
}

.fnx-bar-fill {
    height: 100% !important;
    border-radius: 6px !important;
    transition: width 0.3s ease !important;
}

.fill-blue { background: #0284C7 !important; }
.fill-skyblue { background: #60A5FA !important; }
.fill-purple { background: #A855F7 !important; }
.fill-pink { background: #F472B6 !important; }

.fnx-bar-val {
    width: 20px !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    color: #0F172A !important;
    text-align: right !important;
}

/* Recent Cases Table */
.fnx-link-view-all {
    color: #0284C7 !important;
    font-size: 0.86rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    text-decoration: none !important;
}

.fnx-link-view-all:hover {
    text-decoration: underline !important;
}

.fnx-cases-table {
    width: 100% !important;
    border-collapse: collapse !important;
    font-size: 0.88rem !important;
}

.fnx-cases-table th {
    color: #64748B !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.4px !important;
    padding: 0.75rem 0.5rem !important;
    border-bottom: 1px solid #E2E8F0 !important;
    text-align: left !important;
}

.fnx-cases-table td {
    padding: 0.85rem 0.5rem !important;
    border-bottom: 1px solid #F1F5F9 !important;
    color: #1E293B !important;
    vertical-align: middle !important;
}

.fnx-type-cell {
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
}

.fnx-status-pill {
    display: inline-block !important;
    padding: 0.25rem 0.65rem !important;
    border-radius: 20px !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
}

.st-investigation {
    background: #E0F2FE !important;
    color: #0284C7 !important;
}

.st-initial {
    background: #DCFCE7 !important;
    color: #16A34A !important;
}

.st-allotted {
    background: #FEF3C7 !important;
    color: #D97706 !important;
}

.st-closed {
    background: #FEE2E2 !important;
    color: #EF4444 !important;
}

.st-pending {
    background: #F1F5F9 !important;
    color: #475569 !important;
}

.fnx-btn-view-pill {
    background: transparent !important;
    border: 1.5px solid #BAE6FD !important;
    color: #0284C7 !important;
    border-radius: 16px !important;
    padding: 0.25rem 0.75rem !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.15s !important;
}

.fnx-btn-view-pill:hover {
    background: #E0F2FE !important;
    border-color: #0284C7 !important;
}

/* Need Guidance Banner */
.fnx-guidance-banner {
    background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%) !important;
    border: 1px solid #BAE6FD !important;
    border-radius: 14px !important;
    padding: 1.25rem 1.5rem !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    box-shadow: 0 2px 8px rgba(2,132,199,0.06) !important;
}

.fnx-guidance-title {
    display: flex !important;
    align-items: center !important;
    gap: 0.4rem !important;
    font-size: 1.05rem !important;
    color: #0369A1 !important;
    font-weight: 800 !important;
}

.fnx-guidance-desc {
    color: #475569 !important;
    font-size: 0.88rem !important;
    margin: 0.35rem 0 0.85rem 0 !important;
}

.fnx-btn-ask-ai {
    background: #FFFFFF !important;
    border: 1.5px solid #00B8D9 !important;
    color: #0284C7 !important;
    font-weight: 700 !important;
    border-radius: 20px !important;
    padding: 0.5rem 1.15rem !important;
    font-size: 0.85rem !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.4rem !important;
    box-shadow: 0 2px 8px rgba(0,184,217,0.15) !important;
    transition: all 0.15s !important;
}

.fnx-btn-ask-ai:hover {
    background: #00B8D9 !important;
    color: #FFFFFF !important;
    transform: translateY(-1px) !important;
}

/* Right Column: User Info Card */
.fnx-btn-edit-pill {
    background: transparent !important;
    border: 1px solid #CBD5E1 !important;
    color: #475569 !important;
    border-radius: 14px !important;
    padding: 0.2rem 0.65rem !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
}

.fnx-btn-edit-pill:hover {
    border-color: #0284C7 !important;
    color: #0284C7 !important;
}

.fnx-user-info-kv-list {
    display: flex !important;
    flex-direction: column !important;
    gap: 0.75rem !important;
}

.fnx-kv-row {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    font-size: 0.86rem !important;
}

.fnx-kv-k {
    color: #64748B !important;
}

.fnx-kv-v {
    color: #0F172A !important;
    font-weight: 600 !important;
    text-align: right !important;
}

/* Quick Actions Quad */
.fnx-quick-actions-quad {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 0.75rem !important;
}

.fnx-qa-tile {
    border-radius: 10px !important;
    padding: 1.1rem 0.5rem !important;
    text-align: center !important;
    cursor: pointer !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}

.fnx-qa-tile:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06) !important;
}

.tile-blue { background: #EFF6FF !important; border: 1px solid #DBEAFE !important; }
.tile-green { background: #F0FDF4 !important; border: 1px solid #DCFCE7 !important; }
.tile-purple { background: #FAF5FF !important; border: 1px solid #F3E8FF !important; }
.tile-orange { background: #FFFBEB !important; border: 1px solid #FEF3C7 !important; }

.fnx-qa-icon {
    width: 38px !important;
    height: 38px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin-bottom: 0.4rem !important;
}

.fnx-qa-label {
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    color: #1E293B !important;
}

/* Fraud Prevention Tips */
.fnx-tips-list {
    display: flex !important;
    flex-direction: column !important;
    gap: 0.85rem !important;
}

.fnx-tip-item {
    display: flex !important;
    align-items: flex-start !important;
    gap: 0.65rem !important;
    font-size: 0.84rem !important;
    color: #334155 !important;
    line-height: 1.35 !important;
}

.fnx-tip-icon {
    font-size: 1rem !important;
    flex-shrink: 0 !important;
    margin-top: -1px !important;
}

'''

css += '\n\n' + polaris_css
print('Appended modern Polaris / UI16 styles.')

# -------------------------------------------------------------
# 8. DEPLOY ALL UPDATES TO SERVICENOW
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
    print('SUCCESS: Widget successfully updated with modern customer dashboard!')
    # Flush instance cache
    c_r = requests.get(f'{BASE_URL}/cache.do', auth=AUTH)
    print('Cache clear response:', c_r.status_code)
else:
    print('FAILURE updating widget:', patch_r.status_code, patch_r.text[:300])
