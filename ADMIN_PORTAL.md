# FRAUDNEXUS Admin & Investigator Portal

## 1. Overview
The Admin Portal provides fraud investigators, senior analysts, and compliance managers with an operational environment to manage cases, verify evidence, orchestrate tasks, and resolve financial and cyber fraud incidents.

---

## 2. Module Breakdown

### 2.1 Admin Login Experience
- Two-column responsive layout: Deep Navy branding card on the left with dynamic SVG network graph, white enterprise card on the right.
- Password toggle icon (eye/eye-off).
- Dual login pathways: standard credential login and **Try Demo** button for instant evaluation without password entry.

### 2.2 Command Center
- **6 Dynamic KPI Cards:**
  1. *New Cases* (Cases in status 'New')
  2. *Active Cases* (Cases in status 'Investigating' or 'Under Review')
  3. *Critical Cases* (Severity 'Critical')
  4. *Escalated Cases* (Status 'Escalated')
  5. *Pending Approvals* (Action items awaiting review)
  6. *Financial Exposure* (Sum of exposed transaction amounts in INR)
- **Priority Investigation Queue:** Full table listing Case ID, Incident Type, Severity, Risk Score, Financial Exposure, Assigned Handler, SLA Target, Status, and Action buttons (`View`, `Assign`, `Open Workspace`).
- **Action Center:** Actionable alerts for unassigned critical incidents and pending approvals.
- **Fraud Case Trends:** SVG line chart visualizing incidents across fraud categories over 7, 30, and 90 days.
- **Financial Exposure Summary:** 4 metric cards: Total Exposure, Blocked Amount, Recovered Amount, Outstanding Amount.
- **Recent Activity Feed:** Timestamped stream of case creation, assignment, evidence upload, and status transition events.

### 2.3 Customers Module
- Searchable customer directory pulling from `u_x_fnx_customer`.
- Displays Customer ID (`CNX-`), Full Name, Email, Phone, Verification/KYC Status, and Associated Case Count.

### 2.4 Case Management Module
- Comprehensive case inventory with multi-criteria filtering: All, New, Unassigned, Active, Critical, Escalated, Near SLA.
- Direct operational actions: View, Assign, Reassign, Escalate, Request Evidence, Add Task, Resolve, Close.

### 2.5 Investigation Workspace (3-Column Layout)
- **Left Column:** Case navigation list with search and filter.
- **Center Column:** Tabbed operational workspace:
  - *Overview Tab:* Case details, incident narrative, financial transactions, customer details.
  - *Evidence Tab:* File records, MIME types, file sizes, SHA-256 integrity hashes, custody logs, and 'Request Evidence' action.
  - *Tasks Tab:* Linked operational tasks (`u_x_fnx_task`), assignment, due date, status, and 'Create Task' modal.
  - *Timeline Tab:* Chronological audit history from `u_x_fnx_audit`.
- **Right Column:** Case summary card showing severity, risk score, financial exposure, SLA countdown, and operational action buttons.

### 2.6 Intelligence Workspace (Phase 1 Shell)
- Clean, professional placeholder adhering to Phase 1 boundaries.
- Displays safe operational summaries and explains future Phase 2 graph visualization, fraud ring detection, and entity correlation.

### 2.7 Analytics Module
- Operational reporting charts: Cases by Type, Status, Severity, and Resolution metrics using live case records.

### 2.8 Settings Module
- Investigator profile view, role privileges display, notification preferences, and language selection.

### 2.9 Operational AI Assistant (`✨ Ask FRAUDNEXUS AI`)
- Floating button in bottom-right corner opening an interactive drawer.
- Provides contextual operational answers based on active cases, unassigned queues, and specific case IDs.\n