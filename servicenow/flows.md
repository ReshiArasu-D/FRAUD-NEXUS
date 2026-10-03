# ServiceNow Flow Designer Specifications

## Operational Flows
1. **Flow 1: Fraud Case Intake**
   - Trigger: Record created in `u_x_fnx_case`.
   - Actions: Validate fields, calculate SLA window, publish to Command Center queue.
2. **Flow 2: Case Assignment Notification**
   - Trigger: `u_assigned_handler` changes.
   - Actions: Notify assigned investigator, log audit event.
3. **Flow 3: Evidence Request Notification**
   - Trigger: Investigator requests additional evidence.
   - Actions: Create pending request record, send notification to customer.
4. **Flow 4: Case Escalation**
   - Trigger: Status changes to `Escalated`.
   - Actions: Notify fraud management group, elevate priority to Critical.
5. **Flow 5: Resolution & Closure**
   - Trigger: Status changes to `Resolved` / `Closed`.
   - Actions: Record resolution notes, notify customer via portal and email.\n