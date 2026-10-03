# FRAUDNEXUS Test Plan & Quality Assurance

## 1. Testing Strategy

The test plan ensures zero regression of the existing Customer Portal while certifying all new Admin Portal capabilities across four levels:

1. **Unit & API Testing:** Verify REST API responses, schema adherence, and error handling.
2. **Regression Testing:** Ensure all Phase 2 Customer Portal functionalities remain 100% operational.
3. **End-to-End Integration Testing:** Validate the complete 13-step lifecycle from customer submission to investigator closure.
4. **Visual & Cross-Browser Verification:** Test responsiveness, contrast, and layout across desktop resolutions (1366x768 to 1920x1080).

---

## 2. Test Execution Suite

| Script | Purpose | Test Count | Pass Rate |
|---|---|---|---|
| `run_phase2_tests.py` | Customer portal API & core workflows | 20 | 100% (20/20) |
| `run_phase2_ux_tests.py` | Customer portal UI & widget rendering | 20 | 100% (20/20) |
| `test_admin_api.py` | Admin REST API endpoints | 8 | 100% (8/8) |
| `test_customer_to_admin_e2e.py` | Full Customer -> Admin cross-portal flow | 13 | 100% (13/13) |\n