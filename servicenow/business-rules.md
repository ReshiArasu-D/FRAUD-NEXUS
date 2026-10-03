# ServiceNow Business Rules

## Existing Frozen Rules (Customer Portal)
- `BR-FNX-001 Customer Record Creation`: Generates customer profile and sends welcome notification.
- `BR-FNX-002 Case Initialization`: Auto-generates Case ID (`FNX-`) and computes initial risk score.
- `BR-FNX-003 Customer Status`: Updates customer verification state upon KYC submission.
- `BR-FNX-004 Evidence Custody`: Automatically creates `u_x_fnx_custody_log` entry when evidence is uploaded.
- `BR-FNX-005 Case Audit`: Logs all case field changes into `u_x_fnx_audit`.

## Admin Operational Rules
- `BR-FNX-006 Case Assignment`: Triggers when `u_assigned_handler` changes; sets status to `Assigned` and logs audit entry.
- `BR-FNX-007 Case Status Transition`: Validates allowable status transitions and records status history.
- `BR-FNX-009 Task Lifecycle`: Logs audit trail when investigation tasks are created, updated, or completed.\n