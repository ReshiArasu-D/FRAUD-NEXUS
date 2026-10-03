# FRAUDNEXUS Data Model & Schema

## 1. Shared Table Architecture

FRAUDNEXUS uses 7 primary tables in the ServiceNow schema:

| Table Name | Display Label | Description | Prefix |
|---|---|---|---|
| `u_x_fnx_customer` | Customer | Customer profile, contact info, KYC status | `CNX-` |
| `u_x_fnx_case` | Fraud Case | Core fraud case record, incident type, status, risk | `FNX-` |
| `u_x_fnx_transaction` | Transaction | Financial transaction linked to a fraud case | `TXN-` |
| `u_x_fnx_evidence` | Evidence | Uploaded evidence metadata, SHA-256 hash, custody | `EV-` |
| `u_x_fnx_custody_log` | Custody Log | Chain-of-custody tracking for evidence records | `LOG-` |
| `u_x_fnx_audit` | Audit Log | System-wide audit trail for case events | `AUD-` |
| `u_x_fnx_task` | Investigation Task | Operational task assigned to investigators | `TSK-` |

---

## 2. Table Schemas

### `u_x_fnx_case`
- `u_case_id` (String, Unique): e.g. `FNX-2026-001234`
- `u_customer` (Reference to `u_x_fnx_customer`)
- `u_incident_type` (Choice): `unauthorized_transaction`, `phishing`, `account_compromise`, `identity_theft`, `cyber_fraud`, `payment_fraud`, `money_laundering`, `investment_scam`
- `u_severity` (Choice): `critical`, `high`, `medium`, `low`
- `u_status` (Choice): `new`, `assigned`, `investigating`, `under_review`, `escalated`, `resolved`, `closed`
- `u_risk_score` (Integer): `1 - 100`
- `u_financial_exposure` (Decimal): Amount in INR
- `u_assigned_handler` (Reference to `sys_user`): Assigned investigator
- `u_assignment_group` (Reference to `sys_user_group`)
- `u_description` (String / Large text)
- `u_sla_due` (GlideDateTime): Target resolution SLA

### `u_x_fnx_task`
- `u_task_number` (String, Unique): e.g. `TSK-2026-000101`
- `u_case` (Reference to `u_x_fnx_case`)
- `u_short_description` (String)
- `u_description` (String)
- `u_assigned_to` (Reference to `sys_user`)
- `u_priority` (Choice): `1`, `2`, `3`, `4`
- `u_state` (Choice): `pending`, `in_progress`, `completed`, `cancelled`
- `u_due_date` (GlideDateTime)
- `u_completion_notes` (String)\n