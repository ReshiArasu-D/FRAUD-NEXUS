# ServiceNow Script Includes

## Active Script Includes
- `global.FNX_AdminCaseService` (Sys ID: `d239ea00c3f347d0e54832f1b401311c`):
  - `getDashboardKPIs()`: Returns live counts and exposure metrics.
  - `getCases(filter, limit, offset)`: Retrieves filtered case list.
  - `getCaseDetail(caseId)`: Retrieves comprehensive case details with evidence, tasks, and audit logs.
  - `performAction(caseId, action, payload)`: Handles assignment, escalation, tasks, and status changes.
- `global.FNX_CaseService`: Core case lifecycle operations.
- `global.FNX_EvidenceService`: Evidence integrity and custody logging.
- `global.FNX_AuditService`: System audit trail recorder.\n