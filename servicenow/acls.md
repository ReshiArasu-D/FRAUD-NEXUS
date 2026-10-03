# ServiceNow Access Control Lists (ACLs)

## ACL Configurations
- `u_x_fnx_case`: Read/Write granted to `fnx_investigator` and `fnx_admin`. Customers restricted to own records.
- `u_x_fnx_task`: Read/Write/Create granted to `fnx_investigator`. Customers denied all access.
- `u_x_fnx_evidence`: Read granted to `fnx_investigator`. Customers can only create and read own uploads.
- `u_x_fnx_customer`: Sensitive KYC fields restricted to `fnx_kyc` and `fnx_admin`.\n