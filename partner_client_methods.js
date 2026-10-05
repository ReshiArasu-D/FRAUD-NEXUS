    // ============================================================
    // FRAUDNEXUS ADMIN / INVESTIGATOR PORTAL: PARTNERS MODULE
    // ============================================================
    c.partnerTab = 'directory';
    c.partnersList = [];
    c.partnerRequestsList = [];
    c.partnerCasesList = [];
    c.partnerRecentAudit = [];
    c.partnerKpis = {
        total_partners: 0,
        active_partners: 0,
        inactive_partners: 0,
        pending_requests: 0,
        awaiting_response: 0,
        overdue_requests: 0
    };
    c.partnerSearch = '';
    c.partnerCategoryFilter = 'all';
    c.partnerStatusFilter = 'all';
    c.partnerIntegrationFilter = 'all';
    c.partnerDemoFilter = 'all';

    c.partnerReqSearch = '';
    c.partnerReqStatusFilter = 'all';
    c.partnerReqPriorityFilter = 'all';
    c.partnerReqTypeFilter = 'all';
    c.partnerReqPartnerFilter = 'all';

    c.activePartner = null;
    c.activePartnerRequest = null;
    c.showAddPartnerModal = false;
    c.isEditingPartner = false;
    c.partnerActionLoading = false;
    c.partnerFeedback = '';
    c.partnerFeedbackIsError = false;

    c.showPartnerBlockedModal = false;
    c.blockedPartnerMessage = '';
    c.targetBlockedPartner = null;

    c.partnerForm = {
        sys_id: '',
        partner_number: '',
        name: '',
        category: 'Banks / Financial Institutions',
        organization: '',
        description: '',
        contact_person: '',
        contact_email: '',
        contact_phone: '',
        status: 'Active',
        integration_type: 'Simulated API',
        endpoint_reference: '',
        sla: '4 Hours',
        demo_flag: true,
        notes: 'SIMULATED DEMO PARTNER'
    };

    c.showPartnerReqModal = false;
    c.partnerReqForm = {
        partner_id: '',
        case_id: '',
        request_type: 'Request Transaction Information',
        priority: 'High',
        reference: '',
        description: '',
        simulate: true
    };

    c.setPartnerTab = function(tab) {
        c.partnerTab = tab;
    };

    c.loadPartners = function() {
        $http.get(API + '/admin_partners')
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.partnerKpis = d.kpis || c.partnerKpis;
                c.partnersList = d.partners || [];
                c.partnerRequestsList = d.requests || [];
                c.partnerCasesList = d.cases || [];
                c.partnerRecentAudit = d.recent_audit || [];
                
                // If an active partner is open in drawer, update its reference
                if (c.activePartner) {
                    for (var i = 0; i < c.partnersList.length; i++) {
                        if (c.partnersList[i].sys_id === c.activePartner.sys_id) {
                            c.activePartner = c.partnersList[i];
                            break;
                        }
                    }
                }
            }
        }, function(err) {
            console.error('Failed to load partners:', err);
        });
    };

    c.getFilteredPartners = function() {
        if (!c.partnersList) return [];
        return c.partnersList.filter(function(p) {
            // Text Search
            if (c.partnerSearch) {
                var q = c.partnerSearch.toLowerCase().trim();
                var pNum = (p.partner_number || '').toLowerCase();
                var pName = (p.name || '').toLowerCase();
                var pOrg = (p.organization || '').toLowerCase();
                var pDesc = (p.description || '').toLowerCase();
                if (pNum.indexOf(q) === -1 && pName.indexOf(q) === -1 && pOrg.indexOf(q) === -1 && pDesc.indexOf(q) === -1) {
                    return false;
                }
            }
            // Category Filter
            if (c.partnerCategoryFilter !== 'all' && p.category !== c.partnerCategoryFilter) {
                return false;
            }
            // Status Filter
            if (c.partnerStatusFilter !== 'all' && p.status !== c.partnerStatusFilter) {
                return false;
            }
            // Integration Type Filter
            if (c.partnerIntegrationFilter !== 'all' && p.integration_type !== c.partnerIntegrationFilter) {
                return false;
            }
            // Demo Filter
            if (c.partnerDemoFilter === 'demo' && !p.demo_flag) {
                return false;
            }
            if (c.partnerDemoFilter === 'production' && p.demo_flag) {
                return false;
            }
            return true;
        });
    };

    c.getFilteredPartnerRequests = function() {
        if (!c.partnerRequestsList) return [];
        return c.partnerRequestsList.filter(function(r) {
            // Text Search
            if (c.partnerReqSearch) {
                var q = c.partnerReqSearch.toLowerCase().trim();
                var rNum = (r.request_number || '').toLowerCase();
                var cNum = (r.case_number || '').toLowerCase();
                var pName = (r.partner_name || '').toLowerCase();
                var rType = (r.request_type || '').toLowerCase();
                var rRef = (r.reference || '').toLowerCase();
                if (rNum.indexOf(q) === -1 && cNum.indexOf(q) === -1 && pName.indexOf(q) === -1 && rType.indexOf(q) === -1 && rRef.indexOf(q) === -1) {
                    return false;
                }
            }
            // Status Filter
            if (c.partnerReqStatusFilter !== 'all') {
                if (c.partnerReqStatusFilter === 'pending') {
                    if (r.status !== 'Draft' && r.status !== 'Submitted' && r.status !== 'In Progress' && r.status !== 'Awaiting Response') {
                        return false;
                    }
                } else if (r.status !== c.partnerReqStatusFilter) {
                    return false;
                }
            }
            // Priority Filter
            if (c.partnerReqPriorityFilter !== 'all' && r.priority !== c.partnerReqPriorityFilter) {
                return false;
            }
            // Request Type Filter
            if (c.partnerReqTypeFilter !== 'all' && r.request_type !== c.partnerReqTypeFilter) {
                return false;
            }
            // Partner Filter
            if (c.partnerReqPartnerFilter !== 'all' && r.partner_id !== c.partnerReqPartnerFilter) {
                return false;
            }
            return true;
        });
    };

    c.getCasePartnerRequests = function(cs) {
        if (!cs || !c.partnerRequestsList) return [];
        var csId = cs.sys_id;
        var csNum = cs.number || cs.task_effective_number || cs.u_number;
        return c.partnerRequestsList.filter(function(r) {
            return (csId && r.case_id === csId) || (csNum && r.case_number === csNum);
        });
    };

    c.getCategoryBadgeClass = function(cat) {
        if (!cat) return 'cat-bank';
        if (cat.indexOf('Bank') !== -1) return 'cat-bank';
        if (cat.indexOf('Payment') !== -1) return 'cat-payment';
        if (cat.indexOf('Cyber') !== -1) return 'cat-cyber';
        if (cat.indexOf('Threat') !== -1) return 'cat-intel';
        if (cat.indexOf('AML') !== -1) return 'cat-aml';
        if (cat.indexOf('KYC') !== -1) return 'cat-kyc';
        if (cat.indexOf('Regulat') !== -1) return 'cat-reg';
        if (cat.indexOf('Law') !== -1) return 'cat-law';
        return 'cat-bank';
    };

    c.getCategoryBreakdown = function() {
        var bd = {};
        for (var i = 0; i < c.partnersList.length; i++) {
            var cat = c.partnersList[i].category || 'Other';
            bd[cat] = (bd[cat] || 0) + 1;
        }
        return bd;
    };

    c.getIntegrationBreakdown = function() {
        var bd = {};
        for (var i = 0; i < c.partnersList.length; i++) {
            var it = c.partnersList[i].integration_type || 'Simulated API';
            bd[it] = (bd[it] || 0) + 1;
        }
        return bd;
    };

    c.getCompletedRequestsCount = function() {
        var cnt = 0;
        for (var i = 0; i < c.partnerRequestsList.length; i++) {
            if (c.partnerRequestsList[i].status === 'Completed' || c.partnerRequestsList[i].status === 'Response Received') {
                cnt++;
            }
        }
        return cnt;
    };

    c.getPartnerActiveRequests = function(p) {
        if (!p) return [];
        return c.partnerRequestsList.filter(function(r) {
            return r.partner_id === p.sys_id && r.status !== 'Completed' && r.status !== 'Cancelled' && r.status !== 'Rejected';
        });
    };

    c.getPartnerCompletedRequests = function(p) {
        if (!p) return [];
        return c.partnerRequestsList.filter(function(r) {
            return r.partner_id === p.sys_id && (r.status === 'Completed' || r.status === 'Response Received');
        });
    };

    c.getPartnerRelatedCases = function(p) {
        if (!p) return [];
        var caseSet = {};
        for (var i = 0; i < c.partnerRequestsList.length; i++) {
            var r = c.partnerRequestsList[i];
            if (r.partner_id === p.sys_id && r.case_number) {
                caseSet[r.case_number] = true;
            }
        }
        return Object.keys(caseSet);
    };

    c.getPartnerAuditEvents = function(p) {
        if (!p || !c.partnerRecentAudit) return [];
        return c.partnerRecentAudit.filter(function(a) {
            return (a.record_id && (a.record_id === p.partner_number || a.record_id === p.name)) ||
                   (a.details && (a.details.indexOf(p.name) !== -1 || a.details.indexOf(p.partner_number) !== -1));
        });
    };

    c.openAddPartner = function() {
        c.isEditingPartner = false;
        c.partnerForm = {
            sys_id: '',
            partner_number: '',
            name: '',
            category: 'Banks / Financial Institutions',
            organization: '',
            description: '',
            contact_person: '',
            contact_email: '',
            contact_phone: '',
            status: 'Active',
            integration_type: 'Simulated API',
            endpoint_reference: '',
            sla: '4 Hours',
            demo_flag: true,
            notes: 'SIMULATED DEMO PARTNER'
        };
        c.showAddPartnerModal = true;
    };

    c.openEditPartner = function(p) {
        c.isEditingPartner = true;
        c.partnerForm = {
            sys_id: p.sys_id,
            partner_number: p.partner_number,
            name: p.name,
            category: p.category,
            organization: p.organization,
            description: p.description,
            contact_person: p.contact_person,
            contact_email: p.contact_email,
            contact_phone: p.contact_phone,
            status: p.status,
            integration_type: p.integration_type,
            endpoint_reference: p.endpoint_reference,
            sla: p.sla,
            demo_flag: p.demo_flag,
            notes: p.notes
        };
        c.showAddPartnerModal = true;
    };

    c.savePartner = function() {
        if (!c.partnerForm.name || !c.partnerForm.category || !c.partnerForm.organization) return;
        c.partnerActionLoading = true;
        var act = c.isEditingPartner ? 'update_partner' : 'create_partner';
        var payload = {
            action: act,
            actor: (c.adminUser && c.adminUser.name) || 'Alex Morgan',
            sys_id: c.partnerForm.sys_id,
            partner: c.partnerForm
        };

        $http.post(API + '/admin_partners', payload)
        .then(function(resp) {
            c.partnerActionLoading = false;
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.showAddPartnerModal = false;
                c.partnerFeedback = c.isEditingPartner ? 'Partner updated successfully.' : 'Partner created successfully with ID: ' + (d.partner_number || 'Generated');
                c.partnerFeedbackIsError = false;
                c.loadPartners();
            } else {
                c.partnerFeedback = d.error || 'Failed to save partner.';
                c.partnerFeedbackIsError = true;
            }
        }, function(err) {
            c.partnerActionLoading = false;
            c.partnerFeedback = 'Server error occurred while saving partner.';
            c.partnerFeedbackIsError = true;
        });
    };

    c.togglePartnerStatus = function(p) {
        if (!p) return;
        var newStatus = p.status === 'Active' ? 'Inactive' : 'Active';
        var payload = {
            action: 'set_status',
            actor: (c.adminUser && c.adminUser.name) || 'Alex Morgan',
            sys_id: p.sys_id,
            status: newStatus
        };

        $http.post(API + '/admin_partners', payload)
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                p.status = newStatus;
                c.partnerFeedback = 'Partner status changed to ' + newStatus + '.';
                c.partnerFeedbackIsError = false;
                c.loadPartners();
            }
        });
    };

    c.removePartner = function(p) {
        if (!p) return;
        var payload = {
            action: 'delete_partner',
            actor: (c.adminUser && c.adminUser.name) || 'Alex Morgan',
            sys_id: p.sys_id
        };

        $http.post(API + '/admin_partners', payload)
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.blocked) {
                // Partner is referenced: block deletion!
                c.targetBlockedPartner = p;
                c.blockedPartnerMessage = d.message || 'Partner is referenced by existing records. Deactivate the partner instead of deleting it.';
                c.showPartnerBlockedModal = true;
            } else if (d.success) {
                c.partnerFeedback = 'Partner removed successfully.';
                c.partnerFeedbackIsError = false;
                if (c.activePartner && c.activePartner.sys_id === p.sys_id) {
                    c.closePartnerDetail();
                }
                c.loadPartners();
            } else {
                c.partnerFeedback = d.error || 'Unable to delete partner.';
                c.partnerFeedbackIsError = true;
            }
        });
    };

    c.deactivateBlockedPartner = function() {
        if (!c.targetBlockedPartner) return;
        c.togglePartnerStatus(c.targetBlockedPartner);
        c.showPartnerBlockedModal = false;
        c.targetBlockedPartner = null;
    };

    c.viewPartner = function(p) {
        c.activePartner = p;
    };

    c.closePartnerDetail = function() {
        c.activePartner = null;
    };

    c.openCreatePartnerRequest = function(partner, caseId) {
        c.partnerReqForm = {
            partner_id: partner ? partner.sys_id : (c.partnersList.length > 0 ? c.partnersList[0].sys_id : ''),
            case_id: caseId || (c.activeInvestigationCase ? c.activeInvestigationCase.sys_id : (c.partnerCasesList.length > 0 ? c.partnerCasesList[0].sys_id : '')),
            request_type: 'Request Transaction Information',
            priority: 'High',
            reference: '',
            description: '',
            simulate: true
        };
        c.showPartnerReqModal = true;
    };

    c.submitPartnerRequest = function() {
        if (!c.partnerReqForm.partner_id || !c.partnerReqForm.case_id || !c.partnerReqForm.request_type) return;
        c.partnerActionLoading = true;
        var payload = {
            action: 'create_request',
            actor: (c.adminUser && c.adminUser.name) || 'Alex Morgan',
            request: c.partnerReqForm
        };

        $http.post(API + '/admin_partners', payload)
        .then(function(resp) {
            c.partnerActionLoading = false;
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.showPartnerReqModal = false;
                c.partnerFeedback = 'Partner Request ' + (d.request_number || '') + ' dispatched successfully (Status: ' + d.status + ').';
                c.partnerFeedbackIsError = false;
                c.loadPartners();
            } else {
                c.partnerFeedback = d.error || 'Failed to dispatch request.';
                c.partnerFeedbackIsError = true;
            }
        }, function(err) {
            c.partnerActionLoading = false;
            c.partnerFeedback = 'Server error occurred while dispatching request.';
            c.partnerFeedbackIsError = true;
        });
    };

    c.viewPartnerRequest = function(r) {
        c.activePartnerRequest = r;
    };

    c.closePartnerRequestDetail = function() {
        c.activePartnerRequest = null;
    };

    c.simulatePartnerResponse = function(r) {
        if (!r) return;
        var payload = {
            action: 'simulate_response',
            actor: (c.adminUser && c.adminUser.name) || 'Alex Morgan',
            sys_id: r.sys_id
        };

        $http.post(API + '/admin_partners', payload)
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                r.status = d.status;
                r.response = d.response;
                c.partnerFeedback = 'Simulated response generated and recorded in Case Timeline & Audit Log.';
                c.partnerFeedbackIsError = false;
                c.loadPartners();
            }
        });
    };

    c.updatePartnerRequestStatus = function(r, newStatus) {
        if (!r) return;
        var payload = {
            action: 'update_request_status',
            actor: (c.adminUser && c.adminUser.name) || 'Alex Morgan',
            sys_id: r.sys_id,
            status: newStatus,
            resolution_notes: 'Status updated by investigator to ' + newStatus + '.'
        };

        $http.post(API + '/admin_partners', payload)
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                r.status = newStatus;
                c.partnerFeedback = 'Request ' + r.request_number + ' marked as ' + newStatus + '.';
                c.partnerFeedbackIsError = false;
                c.loadPartners();
            }
        });
    };
