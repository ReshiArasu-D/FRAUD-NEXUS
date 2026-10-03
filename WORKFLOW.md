# FRAUDNEXUS End-to-End Workflow

## 1. Lifecycle Overview

```
[CUSTOMER]
   │
   ├─► 1. Logs into Customer Portal (/fnx)
   ├─► 2. Submits Fraud Report + Uploads Evidence
   ├─► 3. Case Record Created in u_x_fnx_case with 'New' status
   │
[ADMIN / INVESTIGATOR]
   │
   ├─► 4. Logs in via /fnx?view=admin (or Try Demo)
   ├─► 5. Case appears in Command Center Priority Queue
   ├─► 6. Investigator opens case in Investigation Workspace
   ├─► 7. Investigator Assigns Case to self or peer
   │       └── BR-FNX-006 fires -> Status changes to 'Assigned' -> Audit logged
   ├─► 8. Investigator creates an operational task in Tasks tab
   │       └── BR-FNX-009 fires -> u_x_fnx_task created -> Audit logged
   ├─► 9. Investigator sends Evidence Request
   │       └── Timeline updated -> Customer notification triggered
   ├─► 10. Investigator Escalates Case
   │       └── Status changes to 'Escalated' -> Manager alerted
   ├─► 11. Investigator Resolves Case
   │       └── BR-FNX-007 fires -> Status changes to 'Resolved'
   ├─► 12. Case is Closed with Closure Code
   │       └── Status changes to 'Closed' -> Final audit entry
   │
[CUSTOMER]
   │
   └─► 13. Customer refreshes Tracking page -> Sees updated status 'Closed'
```\n