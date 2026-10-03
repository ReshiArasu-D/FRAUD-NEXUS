# Admin Portal — Investigation Workspace

## Specifications
- 3-Column operational investigation workspace:
  - **Left Navigation:** Compact case list with search and filter.
  - **Center Operational Workspace:** 4 tabs:
    - *Overview:* Incident description, financial transaction details, customer profile.
    - *Evidence:* Evidence files, MIME types, file sizes, SHA-256 hashes, custody history, and request additional evidence trigger.
    - *Tasks:* List of linked tasks from `u_x_fnx_task` with status and assignee; includes 'New Task' modal.
    - *Timeline:* Chronological audit log events.
  - **Right Column:** Case summary card showing severity, risk score, exposure, SLA countdown, and operational action buttons.\n