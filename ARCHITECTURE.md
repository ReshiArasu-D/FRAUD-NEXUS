# FRAUDNEXUS Architecture Specification

## 1. High-Level Architecture

FRAUDNEXUS utilizes a dual-portal presentation tier over a unified, shared ServiceNow data and logic tier:

```
                       FRAUDNEXUS PLATFORM
                               │
            ┌──────────────────┴──────────────────┐
            │                                     │
      CUSTOMER PORTAL                       ADMIN PORTAL
      (Service Portal)             (Configurable Workspace / SP)
      Route: /fnx                          Route: /fnx?view=admin
            │                                     │
            └──────────────────┬──────────────────┘
                               │
               SERVICENOW REST APIS (/api/4e92fc73c36743d0e54832f1b401317d/fnx_api)
                               │
            ┌──────────────────┼──────────────────┐
            ▼                  ▼                  ▼
     SCRIPT INCLUDES    BUSINESS RULES     FLOW DESIGNER
     - FNX_AdminCase    - BR-FNX-001..005  - Intake Flow
     - FNX_CaseService  - BR-FNX-006 (Asgn)- Assignment Flow
     - FNX_AuditService - BR-FNX-007 (Stat)- Escalate Flow
     - FNX_Evidence     - BR-FNX-009 (Task)- Resolve/Close
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │
                      SHARED DATA TIER
            ┌──────────────────┼──────────────────┐
            ▼                  ▼                  ▼
      u_x_fnx_customer    u_x_fnx_case       u_x_fnx_task
      u_x_fnx_evidence    u_x_fnx_custody    u_x_fnx_audit
      u_x_fnx_transaction
```

---

## 2. Key Architectural Decisions

1. **Zero Data Duplication:**
   Admin and Customer portals interact with the exact same physical records. When a customer submits a report, record `u_x_fnx_case` is created immediately. When an investigator updates status to `Investigating` or `Resolved`, the customer's tracking view updates in real-time.
2. **Rhino Engine Compatibility:**
   All ServiceNow server scripts avoid JavaScript reserved keywords as unquoted object keys (e.g. using `{"case": sys_id}` instead of `{case: sys_id}`).
3. **Dedicated REST API Operation Routing:**
   Methods are divided cleanly into distinct `sys_ws_operation` records (`/admin_login`, `/admin_dashboard`, `/admin_cases` [GET], `/admin_cases` [POST], `/admin_customers`, `/admin_ai`).
4. **Legitimate Authentication in Demo Mode:**
   Try Demo uses `POST /admin_login` with seeded investigator credentials (`alex.morgan@fraudnexus.com`), creating a valid authenticated user session rather than an insecure client-side bypass.\n