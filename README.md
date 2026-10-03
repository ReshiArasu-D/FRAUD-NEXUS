# FRAUDNEXUS — Financial & Cyber Fraud Investigation Hub

> **Tagline:** *From Fraud Report to Resolution — One Intelligent Investigation Workspace*  
> **Platform:** ServiceNow Utah / Vancouver / Washington Compatible  
> **Architecture:** Dual-Portal Experience with Unified Shared Data Model

---

## 📌 Executive Summary

**FRAUDNEXUS** is an enterprise-grade financial and cyber fraud investigation management platform built directly on the ServiceNow platform. It unites the customer reporting journey and the investigator operational lifecycle into a single high-integrity system.

- **Customer Portal (`/fnx`):** Self-service intake for reporting financial and cyber fraud, secure evidence upload with SHA-256 custody tracking, real-time case tracking, KYC profile management, and multi-language support.
- **Admin / Investigator Portal (`/fnx?view=admin` or via Portal Selection):** High-throughput operational command center for fraud investigators, team leads, and compliance officers featuring real-time KPI metrics, priority investigation queue, 3-column operational investigation workspace, task orchestration, live evidence inspection, and conversational AI assistant.

Both portals share the exact same underlying scoped tables (`u_x_fnx_case`, `u_x_fnx_customer`, `u_x_fnx_evidence`, `u_x_fnx_custody_log`, `u_x_fnx_audit`, `u_x_fnx_transaction`, `u_x_fnx_task`), ensuring zero data duplication, real-time status synchronization, and strict ServiceNow-native role-based security.

---

## 🌟 Key Capabilities

1. **Enterprise Two-Column Admin Login & Demo Mode**
   - High-contrast Deep Navy (`#0B1F3A`) brand panel with network graph visualization.
   - White enterprise authentication card with password visibility toggle.
   - **Try Demo / Quick Login:** Instant judge access using seeded investigator credentials (`alex.morgan@fraudnexus.com`) without bypassing authentication. Displays persistent `DEMO ENVIRONMENT` banner.

2. **Unified Command Center**
   - 6 Dynamic KPI cards: New Cases, Active Cases, Critical Cases, Escalated Cases, Pending Approvals, Financial Exposure.
   - **Priority Investigation Queue:** Interactive grid with quick filters (Critical, High Risk, Near SLA, Unassigned, Escalated) and direct operational actions (View, Assign, Open Workspace).
   - **Action Center:** Contextual operational alerts requiring investigator attention.
   - **SVG Fraud Case Trends:** Interactive trend chart by fraud category (Unauthorized Transaction, Phishing, Identity Theft, etc.).
   - **Financial Exposure Summary:** Total exposure, blocked funds, recovered funds, and outstanding exposure tiles.
   - **Live Recent Activity:** Real-time audit events streamed directly from ServiceNow audit logs.

3. **Strict 7-Module Sidebar Navigation**
   - `Command Center`: Executive operational overview.
   - `Customers`: Customer directory, KYC verification status, linked cases.
   - `Cases`: Filterable case inventory with operational action triggers.
   - `Investigation`: 3-Column operational workspace (Case Navigator, 4-Tab Workspace: Overview, Evidence, Tasks, Timeline, and Case Summary Card).
   - `Intelligence Workspace`: Clean Phase 1 shell ready for Phase 2 graph intelligence and fraud ring detection.
   - `Analytics`: Operational breakdown of cases by type, status, severity, exposure, and resolution.
   - `Settings`: Investigator profile, notification preferences, language selector.

4. **Operational AI Assistant Drawer (`✨ Ask FRAUDNEXUS AI`)**
   - Reuses existing FRAUDNEXUS AI assistant infrastructure.
   - Operational context: answers investigator queries on open cases, unassigned queues, critical risk cases, and status transitions using live ServiceNow records.
   - Case-context awareness when viewing specific fraud cases.

5. **Global Multilingual Support**
   - Fully wired to the existing 13-language translation dictionary (English, Tamil, Hindi, Spanish, French, German, Japanese, etc.).
   - Instant header dropdown switching for all navigation, dashboard titles, action labels, and table headers.

---

## 🔐 Credentials & Quick Access

- **Instance URL:** `https://dev187180.service-now.com/fnx`
- **Admin / Investigator Direct:** `https://dev187180.service-now.com/fnx?view=admin`
- **Seeded Demo Investigator Account:**
  - **Email:** `alex.morgan@fraudnexus.com`
  - **Password:** `DemoPass123!`
  - **Role:** `fnx_investigator`
- **ServiceNow Instance Admin:**
  - **Username:** `admin`

---

## 🧪 Verification & Regression Testing

To run the complete automated test suite locally:

```bash
# 1. Phase 2 Core Tests (20 tests)
python run_phase2_tests.py

# 2. Phase 2 UX & Widget Tests (20 tests)
python run_phase2_ux_tests.py

# 3. End-to-End Customer -> Admin Lifecycle Test (13 steps)
python test_customer_to_admin_e2e.py

# 4. Admin REST API Verification
python test_admin_api.py
```

All 40 regression tests and 13 E2E integration steps pass with **100% success rate**.\n