# FRAUDNEXUS Security & Access Control Model

## 1. Role Hierarchy

| Role Name | Description | Key Privileges |
|---|---|---|
| `x_fnx_customer_user` | Customer / Citizen | Report fraud, upload evidence, track own cases |
| `fnx_investigator` | Fraud Investigator | View & work assigned cases, create tasks, inspect evidence |
| `fnx_manager` | Fraud Team Lead / Manager | Assign, reassign, approve escalations, view team analytics |
| `fnx_admin` | Platform Administrator | Full configuration, user role management, system settings |
| `fnx_compliance` | Compliance Officer | Regulatory audit access, compliance reporting |
| `fnx_kyc` | KYC Verification Agent | Access and verify customer sensitive KYC documents |

---

## 2. Access Control Lists (ACLs)

### Customer Isolation
- Customers can only read and write their own case records (`u_customer = gs.getUserID()`).
- Customers have zero read/write access to `u_x_fnx_task` or internal investigator work notes.

### Investigator Protection
- Investigators require role `fnx_investigator` or `fnx_admin` to access the Admin Portal REST endpoints.
- Read, write, and create ACLs are enforced on `u_x_fnx_task`, `u_x_fnx_case`, and `u_x_fnx_evidence`.\n