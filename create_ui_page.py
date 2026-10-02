import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

portal_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FRAUDNEXUS — Customer Fraud Investigation Portal</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-navy: #0B1F3A;
            --secondary-navy: #123B63;
            --intel-cyan: #00B8D9;
            --success: #16A34A;
            --warning: #F59E0B;
            --critical: #DC2626;
            --bg-color: #F5F7FA;
            --card-bg: #FFFFFF;
            --border-color: #E2E8F0;
            --text-primary: #0F172A;
            --text-secondary: #64748B;
            --font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: var(--font-family);
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* HEADER */
        .fnx-header {
            background-color: var(--primary-navy);
            color: #FFFFFF;
            padding: 1rem 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 2px solid var(--intel-cyan);
            box-shadow: 0 4px 12px rgba(11, 31, 58, 0.15);
        }

        .fnx-brand {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-decoration: none;
            color: #FFFFFF;
            font-weight: 700;
            font-size: 1.35rem;
            letter-spacing: -0.5px;
            cursor: pointer;
        }

        .fnx-logo-icon {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, var(--intel-cyan), var(--secondary-navy));
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #FFFFFF;
            font-weight: 800;
            font-size: 1.1rem;
        }

        .fnx-nav {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }

        .fnx-nav a {
            color: #E2E8F0;
            text-decoration: none;
            font-size: 0.95rem;
            font-weight: 500;
            transition: color 0.2s;
            cursor: pointer;
        }

        .fnx-nav a:hover, .fnx-nav a.active {
            color: var(--intel-cyan);
        }

        .fnx-user-badge {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            background: rgba(255, 255, 255, 0.1);
            padding: 0.4rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
        }

        /* BUTTONS */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            padding: 0.65rem 1.25rem;
            font-size: 0.95rem;
            font-weight: 600;
            border-radius: 6px;
            border: none;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
            text-decoration: none;
        }

        .btn-primary {
            background-color: var(--intel-cyan);
            color: #0B1F3A;
        }

        .btn-primary:hover {
            background-color: #00a0be;
            transform: translateY(-1px);
        }

        .btn-navy {
            background-color: var(--secondary-navy);
            color: #FFFFFF;
        }

        .btn-navy:hover {
            background-color: #0b2540;
        }

        .btn-outline {
            background-color: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-primary);
        }

        .btn-outline:hover {
            background-color: #E2E8F0;
        }

        .btn-outline-white {
            background-color: transparent;
            border: 1px solid #FFFFFF;
            color: #FFFFFF;
        }

        .btn-outline-white:hover {
            background-color: rgba(255,255,255,0.1);
        }

        /* APP CONTAINER */
        .main-container {
            flex: 1;
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
            width: 100%;
        }

        .view-section {
            display: none;
        }

        .view-section.active {
            display: block;
            animation: fadeIn 0.3s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* HERO & LANDING */
        .hero-banner {
            background: linear-gradient(135deg, var(--primary-navy) 0%, var(--secondary-navy) 100%);
            color: #FFFFFF;
            border-radius: 12px;
            padding: 3.5rem 3rem;
            margin-bottom: 2.5rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(11, 31, 58, 0.2);
        }

        .hero-banner::after {
            content: '';
            position: absolute;
            right: -50px;
            bottom: -50px;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(0, 184, 217, 0.15) 0%, rgba(0,0,0,0) 70%);
            border-radius: 50%;
        }

        .hero-title {
            font-size: 2.5rem;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 1rem;
            letter-spacing: -0.5px;
        }

        .hero-title span {
            color: var(--intel-cyan);
        }

        .hero-subtitle {
            font-size: 1.15rem;
            color: #CBD5E1;
            max-width: 700px;
            margin-bottom: 2rem;
            line-height: 1.6;
        }

        .hero-actions {
            display: flex;
            gap: 1rem;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }

        .feature-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1.75rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.02);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .feature-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.06);
            border-color: var(--intel-cyan);
        }

        .feature-icon {
            font-size: 1.8rem;
            margin-bottom: 1rem;
            display: inline-block;
        }

        .feature-title {
            font-size: 1.15rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--primary-navy);
        }

        .feature-desc {
            font-size: 0.9rem;
            color: var(--text-secondary);
            line-height: 1.5;
        }

        /* FORMS & CARDS */
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
            margin-bottom: 2rem;
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.25rem;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }

        .form-group.full-width {
            grid-column: 1 / -1;
        }

        .form-label {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        .form-label span.req {
            color: var(--critical);
        }

        .form-control {
            padding: 0.65rem 0.85rem;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            font-size: 0.95rem;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        .form-control:focus {
            border-color: var(--intel-cyan);
            box-shadow: 0 0 0 3px rgba(0, 184, 217, 0.15);
        }

        textarea.form-control {
            min-height: 90px;
            resize: vertical;
        }

        /* STATS */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.25rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1.5rem;
            border-left: 5px solid var(--intel-cyan);
        }

        .stat-card.active-cases {
            border-left-color: var(--warning);
        }

        .stat-card.resolved-cases {
            border-left-color: var(--success);
        }

        .stat-value {
            font-size: 2.2rem;
            font-weight: 700;
            color: var(--primary-navy);
            margin: 0.25rem 0;
        }

        .stat-label {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* TABLES */
        .table-container {
            overflow-x: auto;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            background: #FFFFFF;
        }

        table.fnx-table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.9rem;
        }

        table.fnx-table th {
            background-color: #F8FAFC;
            color: var(--text-secondary);
            font-weight: 600;
            padding: 0.85rem 1rem;
            border-bottom: 1px solid var(--border-color);
        }

        table.fnx-table td {
            padding: 0.85rem 1rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-primary);
        }

        table.fnx-table tr:hover td {
            background-color: #F1F5F9;
        }

        .badge {
            display: inline-block;
            padding: 0.25rem 0.65rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .badge-new { background-color: #E0F2FE; color: #0284C7; }
        .badge-active { background-color: #FEF3C7; color: #D97706; }
        .badge-resolved { background-color: #DCFCE7; color: #16A34A; }
        .badge-critical { background-color: #FEE2E2; color: #DC2626; }

        /* WIZARD STEPS */
        .step-progress {
            display: flex;
            justify-content: space-between;
            margin-bottom: 2rem;
            position: relative;
        }

        .step-item {
            text-align: center;
            flex: 1;
            position: relative;
        }

        .step-circle {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: #E2E8F0;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 0.5rem auto;
            font-weight: 600;
            font-size: 0.85rem;
        }

        .step-item.active .step-circle {
            background: var(--intel-cyan);
            color: #0B1F3A;
            font-weight: 700;
        }

        .step-item.completed .step-circle {
            background: var(--success);
            color: #FFFFFF;
        }

        .step-title {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-secondary);
        }

        /* TIMELINE */
        .timeline {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 2rem 0;
            padding: 1.5rem;
            background: #F8FAFC;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }

        .tl-node {
            text-align: center;
            position: relative;
            flex: 1;
        }

        .tl-dot {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #CBD5E1;
            margin: 0 auto 0.5rem auto;
        }

        .tl-node.active .tl-dot {
            background: var(--intel-cyan);
            box-shadow: 0 0 0 4px rgba(0, 184, 217, 0.2);
        }

        .tl-node.completed .tl-dot {
            background: var(--success);
        }

        .tl-label {
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-secondary);
        }

        /* AI ASSISTANT */
        .fnx-ai-pill {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: linear-gradient(135deg, var(--primary-navy), var(--secondary-navy));
            border: 2px solid var(--intel-cyan);
            color: #FFFFFF;
            padding: 0.75rem 1.25rem;
            border-radius: 30px;
            box-shadow: 0 6px 20px rgba(0, 184, 217, 0.35);
            display: flex;
            align-items: center;
            gap: 0.6rem;
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            z-index: 1000;
            transition: all 0.2s ease;
        }

        .fnx-ai-pill:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 25px rgba(0, 184, 217, 0.5);
        }

        .fnx-ai-drawer {
            position: fixed;
            top: 0;
            right: -420px;
            width: 400px;
            height: 100vh;
            background: #FFFFFF;
            box-shadow: -5px 0 25px rgba(0,0,0,0.15);
            z-index: 1100;
            transition: right 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            flex-direction: column;
        }

        .fnx-ai-drawer.open {
            right: 0;
        }

        .ai-drawer-header {
            background: var(--primary-navy);
            color: #FFFFFF;
            padding: 1.25rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .ai-drawer-body {
            flex: 1;
            padding: 1.25rem;
            overflow-y: auto;
            background: #F8FAFC;
        }

        .ai-msg {
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            padding: 0.85rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        .ai-intent-btn {
            display: block;
            width: 100%;
            text-align: left;
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            padding: 0.65rem 0.85rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
            font-size: 0.85rem;
            color: var(--primary-navy);
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s;
        }

        .ai-intent-btn:hover {
            border-color: var(--intel-cyan);
            background: #F0FDFA;
        }

        /* MODAL */
        .fnx-modal-backdrop {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(11, 31, 58, 0.6);
            z-index: 2000;
            align-items: center;
            justify-content: center;
            padding: 1rem;
        }

        .fnx-modal-backdrop.open {
            display: flex;
        }

        .fnx-modal {
            background: #FFFFFF;
            border-radius: 12px;
            max-width: 700px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
            padding: 2rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            position: relative;
        }

        .alert-box {
            padding: 0.85rem 1.2rem;
            border-radius: 6px;
            margin-bottom: 1.25rem;
            font-size: 0.9rem;
            display: none;
        }

        .alert-error {
            background: #FEE2E2;
            color: #991B1B;
            border: 1px solid #FCA5A5;
        }

        .alert-success {
            background: #DCFCE7;
            color: #166534;
            border: 1px solid #86EFAC;
        }
    </style>
</head>
<body>

    <!-- HEADER -->
    <header class="fnx-header">
        <div class="fnx-brand" onclick="navigateTo('landing-view')">
            <div class="fnx-logo-icon">F</div>
            <span>FRAUDNEXUS</span>
        </div>
        <nav class="fnx-nav">
            <a onclick="navigateTo('landing-view')" id="nav-home">Home</a>
            <a onclick="handleReportFraudNav()" id="nav-report">Report Fraud</a>
            <a onclick="handleMyCasesNav()" id="nav-cases">Track Case</a>
            <a onclick="showInfoModal('About FRAUDNEXUS', 'FRAUDNEXUS is the next-generation financial & cyber fraud investigation platform built directly on ServiceNow. Platform vision: From Fraud Report to Resolution — One Intelligent Investigation Workspace.')">About</a>
        </nav>
        <div class="fnx-nav-auth" id="header-auth">
            <!-- Injected via JavaScript based on session -->
            <button class="btn btn-outline-white" onclick="navigateTo('login-view')">Customer Login</button>
            <button class="btn btn-primary" onclick="navigateTo('register-view')">Register</button>
        </div>
    </header>

    <!-- MAIN APP CONTENT CONTAINER -->
    <main class="main-container">

        <!-- 1. LANDING PAGE VIEW -->
        <section id="landing-view" class="view-section active">
            <div class="hero-banner">
                <div class="hero-title">
                    Financial &amp; Cyber Fraud<br><span>Investigation Hub</span>
                </div>
                <div class="hero-subtitle">
                    From Fraud Report to Resolution — One Intelligent Investigation Workspace. Report suspicious transactions, submit forensic evidence securely, and track your case lifecycle in real time.
                </div>
                <div class="hero-actions">
                    <button class="btn btn-primary" onclick="handleReportFraudNav()">🚨 Report Fraud</button>
                    <button class="btn btn-outline-white" onclick="handleMyCasesNav()">🔍 Track My Case</button>
                </div>
            </div>

            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🛡️</div>
                    <div class="feature-title">Secure Fraud Reporting</div>
                    <div class="feature-desc">Report unauthorized transactions, payment fraud, phishing, and identity compromises with bank-grade confidentiality.</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📁</div>
                    <div class="feature-title">Evidence Management</div>
                    <div class="feature-desc">Submit transaction screenshots, chat logs, audio, and documents with cryptographic chain-of-custody verification.</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <div class="feature-title">Investigation Tracking</div>
                    <div class="feature-desc">Full visibility into investigation stages from Initial Review to Resolution and Asset Recovery.</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🧠</div>
                    <div class="feature-title">Intelligent Investigation</div>
                    <div class="feature-desc">FRAUDNEXUS connects fraud-related accounts and entities across multiple networks to accelerate case closure.</div>
                </div>
            </div>
        </section>

        <!-- 2. REGISTRATION VIEW -->
        <section id="register-view" class="view-section">
            <div class="card" style="max-width: 550px; margin: 0 auto;">
                <h2 style="color: var(--primary-navy); margin-bottom: 0.5rem;">Create FRAUDNEXUS Account</h2>
                <p style="color: var(--text-secondary); margin-bottom: 1.5rem; font-size: 0.9rem;">Register to report fraud incidents and track investigation updates.</p>

                <div id="reg-alert" class="alert-box"></div>

                <form id="reg-form" onsubmit="handleRegistration(event)">
                    <div class="form-group" style="margin-bottom: 1rem;">
                        <label class="form-label">Full Name <span class="req">*</span></label>
                        <input type="text" id="reg-name" class="form-control" placeholder="e.g. Arun Kumar" required>
                    </div>

                    <div class="form-group" style="margin-bottom: 1rem;">
                        <label class="form-label">Email Address <span class="req">*</span></label>
                        <input type="email" id="reg-email" class="form-control" placeholder="name@example.com" required>
                    </div>

                    <div class="form-group" style="margin-bottom: 1rem;">
                        <label class="form-label">Mobile Number <span class="req">*</span></label>
                        <input type="tel" id="reg-mobile" class="form-control" placeholder="10-digit mobile number" required>
                    </div>

                    <div class="form-group" style="margin-bottom: 1rem;">
                        <label class="form-label">Password <span class="req">*</span></label>
                        <input type="password" id="reg-password" class="form-control" placeholder="Minimum 6 characters" required>
                    </div>

                    <div class="form-group" style="margin-bottom: 1.5rem;">
                        <label class="form-label">Confirm Password <span class="req">*</span></label>
                        <input type="password" id="reg-confirm" class="form-control" placeholder="Confirm your password" required>
                    </div>

                    <button type="submit" class="btn btn-navy" style="width: 100%;" id="btn-reg-submit">Create Account</button>
                </form>

                <div style="margin-top: 1.5rem; text-align: center; font-size: 0.9rem; color: var(--text-secondary);">
                    Already have an account? <a onclick="navigateTo('login-view')" style="color: var(--intel-cyan); cursor: pointer; font-weight: 600;">Login here</a>
                </div>
            </div>
        </section>

        <!-- 3. LOGIN VIEW -->
        <section id="login-view" class="view-section">
            <div class="card" style="max-width: 450px; margin: 0 auto;">
                <h2 style="color: var(--primary-navy); margin-bottom: 0.5rem;">Customer Login</h2>
                <p style="color: var(--text-secondary); margin-bottom: 1.5rem; font-size: 0.9rem;">Sign in to your FRAUDNEXUS customer workspace.</p>

                <div id="login-alert" class="alert-box"></div>

                <form id="login-form" onsubmit="handleLogin(event)">
                    <div class="form-group" style="margin-bottom: 1rem;">
                        <label class="form-label">Email Address</label>
                        <input type="email" id="login-email" class="form-control" placeholder="name@example.com" required>
                    </div>

                    <div class="form-group" style="margin-bottom: 1.5rem;">
                        <label class="form-label">Password</label>
                        <input type="password" id="login-password" class="form-control" placeholder="Enter password" required>
                    </div>

                    <button type="submit" class="btn btn-navy" style="width: 100%;" id="btn-login-submit">Login</button>
                </form>

                <div style="margin-top: 1.5rem; text-align: center; font-size: 0.9rem; color: var(--text-secondary);">
                    Don't have an account? <a onclick="navigateTo('register-view')" style="color: var(--intel-cyan); cursor: pointer; font-weight: 600;">Create one</a>
                </div>
            </div>
        </section>

        <!-- 4. CUSTOMER DASHBOARD VIEW -->
        <section id="dashboard-view" class="view-section">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                <div>
                    <h2 style="color: var(--primary-navy);">Customer Workspace</h2>
                    <p style="color: var(--text-secondary); font-size: 0.9rem;">
                        Welcome, <span id="dash-customer-name" style="font-weight: 600; color: var(--primary-navy);">Customer</span> | 
                        ID: <span id="dash-customer-id" style="font-weight: 600; color: var(--intel-cyan);">CNX-2026-XXXXXX</span>
                    </p>
                </div>
                <div style="display: flex; gap: 0.75rem;">
                    <button class="btn btn-primary" onclick="startReportWizard()">🚨 Report New Fraud</button>
                    <button class="btn btn-outline" onclick="logoutCustomer()">Logout</button>
                </div>
            </div>

            <!-- Stats -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Total Cases</div>
                    <div class="stat-value" id="stat-total">0</div>
                    <div style="font-size: 0.8rem; color: var(--text-secondary);">Reported by you</div>
                </div>
                <div class="stat-card active-cases">
                    <div class="stat-label">Active Investigations</div>
                    <div class="stat-value" id="stat-active" style="color: var(--warning);">0</div>
                    <div style="font-size: 0.8rem; color: var(--text-secondary);">Under active review</div>
                </div>
                <div class="stat-card resolved-cases">
                    <div class="stat-label">Resolved Cases</div>
                    <div class="stat-value" id="stat-resolved" style="color: var(--success);">0</div>
                    <div style="font-size: 0.8rem; color: var(--text-secondary);">Investigation closed</div>
                </div>
            </div>

            <!-- Recent Cases -->
            <div class="card" style="padding: 1.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="color: var(--primary-navy); font-size: 1.15rem;">My Fraud Cases</h3>
                    <button class="btn btn-outline" style="padding: 0.35rem 0.75rem; font-size: 0.85rem;" onclick="loadCustomerCases()">🔄 Refresh</button>
                </div>

                <div class="table-container">
                    <table class="fnx-table">
                        <thead>
                            <tr>
                                <th>Case ID</th>
                                <th>Fraud Type</th>
                                <th>Incident Date</th>
                                <th>Amount (INR)</th>
                                <th>Stage</th>
                                <th>Status</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody id="cases-table-body">
                            <tr>
                                <td colspan="7" style="text-align: center; color: var(--text-secondary); padding: 2rem;">No fraud cases reported yet.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- 5. REPORT FRAUD WIZARD VIEW -->
        <section id="report-view" class="view-section">
            <div class="card" style="max-width: 850px; margin: 0 auto;">
                <h2 style="color: var(--primary-navy); margin-bottom: 0.25rem;">Report Fraud Incident</h2>
                <p style="color: var(--text-secondary); margin-bottom: 1.5rem; font-size: 0.9rem;">Provide comprehensive incident details to initiate investigation.</p>

                <!-- Steps Progress Bar -->
                <div class="step-progress">
                    <div class="step-item active" id="wiz-step-ind-1"><div class="step-circle">1</div><div class="step-title">Incident Details</div></div>
                    <div class="step-item" id="wiz-step-ind-2"><div class="step-circle">2</div><div class="step-title">Location &amp; Platform</div></div>
                    <div class="step-item" id="wiz-step-ind-3"><div class="step-circle">3</div><div class="step-title">Financial Details</div></div>
                    <div class="step-item" id="wiz-step-ind-4"><div class="step-circle">4</div><div class="step-title">Evidence &amp; Submit</div></div>
                </div>

                <div id="fraud-alert" class="alert-box"></div>

                <!-- Step 1: Incident -->
                <div id="wiz-step-1">
                    <h3 style="margin-bottom: 1rem; color: var(--secondary-navy); font-size: 1rem;">Section 1: Incident Details</h3>
                    <div class="form-grid">
                        <div class="form-group">
                            <label class="form-label">Fraud Type <span class="req">*</span></label>
                            <select id="fr-type" class="form-control" required>
                                <option value="Payment Fraud">Payment Fraud</option>
                                <option value="Unauthorized Transaction">Unauthorized Transaction</option>
                                <option value="Phishing">Phishing</option>
                                <option value="Account Compromise">Account Compromise</option>
                                <option value="Identity Theft">Identity Theft</option>
                                <option value="Cyber Fraud">Cyber Fraud</option>
                                <option value="Money Laundering">Money Laundering</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Incident Date <span class="req">*</span></label>
                            <input type="date" id="fr-date" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Incident Time</label>
                            <input type="time" id="fr-time" class="form-control">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Severity Level</label>
                            <select id="fr-severity" class="form-control">
                                <option value="Critical">Critical (Immediate Asset Threat)</option>
                                <option value="High">High</option>
                                <option value="Medium" selected>Medium</option>
                                <option value="Low">Low</option>
                            </select>
                        </div>
                        <div class="form-group full-width">
                            <label class="form-label">Case Description <span class="req">*</span></label>
                            <textarea id="fr-desc" class="form-control" placeholder="Provide detailed explanation of what transpired, messages received, links clicked, etc." required></textarea>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: flex-end; margin-top: 1.5rem;">
                        <button type="button" class="btn btn-navy" onclick="goToStep(2)">Next: Location &amp; Platform &rarr;</button>
                    </div>
                </div>

                <!-- Step 2: Location -->
                <div id="wiz-step-2" style="display: none;">
                    <h3 style="margin-bottom: 1rem; color: var(--secondary-navy); font-size: 1rem;">Section 2: Location &amp; Platform</h3>
                    <div class="form-grid">
                        <div class="form-group">
                            <label class="form-label">Digital Platform / App / Website</label>
                            <input type="text" id="fr-platform" class="form-control" placeholder="e.g. DemoBank Mobile App, WhatsApp, FakePortal.com">
                        </div>
                        <div class="form-group">
                            <label class="form-label">City / Location</label>
                            <input type="text" id="fr-location" class="form-control" placeholder="e.g. Mumbai, Bangalore, Chennai">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Area / Landmark</label>
                            <input type="text" id="fr-area" class="form-control" placeholder="e.g. Andheri East, Koramangala">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Pincode</label>
                            <input type="text" id="fr-pincode" class="form-control" placeholder="e.g. 400069">
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 1.5rem;">
                        <button type="button" class="btn btn-outline" onclick="goToStep(1)">&larr; Back</button>
                        <button type="button" class="btn btn-navy" onclick="goToStep(3)">Next: Financial Details &rarr;</button>
                    </div>
                </div>

                <!-- Step 3: Financial Details -->
                <div id="wiz-step-3" style="display: none;">
                    <h3 style="margin-bottom: 1rem; color: var(--secondary-navy); font-size: 1rem;">Section 3: Financial &amp; Suspect Information</h3>
                    <div class="form-grid">
                        <div class="form-group">
                            <label class="form-label">Defrauded / Exposed Amount (INR)</label>
                            <input type="number" id="fr-amount" class="form-control" placeholder="e.g. 450000" min="0" value="0">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Transaction Reference / UTR Number</label>
                            <input type="text" id="fr-utr" class="form-control" placeholder="e.g. UTR-98218731">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Suspect Name / Phone / Account</label>
                            <input type="text" id="fr-suspect" class="form-control" placeholder="Name or account identifier provided by fraudster">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Communication Channel</label>
                            <select id="fr-channel" class="form-control">
                                <option value="Mobile Call">Mobile Call</option>
                                <option value="WhatsApp / Telegram">WhatsApp / Telegram</option>
                                <option value="SMS / Phishing Link">SMS / Phishing Link</option>
                                <option value="Email">Email</option>
                                <option value="Social Media">Social Media</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 1.5rem;">
                        <button type="button" class="btn btn-outline" onclick="goToStep(2)">&larr; Back</button>
                        <button type="button" class="btn btn-navy" onclick="goToStep(4)">Next: Evidence &amp; Review &rarr;</button>
                    </div>
                </div>

                <!-- Step 4: Evidence & Review -->
                <div id="wiz-step-4" style="display: none;">
                    <h3 style="margin-bottom: 1rem; color: var(--secondary-navy); font-size: 1rem;">Section 4: Evidence Upload &amp; Review</h3>
                    <div class="form-grid">
                        <div class="form-group">
                            <label class="form-label">Evidence Type</label>
                            <select id="fr-ev-type" class="form-control">
                                <option value="Image">Screenshot / Image</option>
                                <option value="PDF">PDF Bank Statement</option>
                                <option value="Chat Export">Chat / WhatsApp Export</option>
                                <option value="Email">Email Header / Msg</option>
                                <option value="Transaction Reference">Transaction Slip</option>
                                <option value="Document">Other Document</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Select Evidence File</label>
                            <input type="file" id="fr-file" class="form-control">
                        </div>
                        <div class="form-group full-width">
                            <label class="form-label">Evidence Description</label>
                            <input type="text" id="fr-ev-desc" class="form-control" placeholder="e.g. Screenshot of fake bank SMS and UPI payment confirmation">
                        </div>
                    </div>

                    <!-- Summary Preview -->
                    <div style="background: #F8FAFC; border: 1px solid var(--border-color); border-radius: 8px; padding: 1.25rem; margin-top: 1.5rem;">
                        <h4 style="color: var(--primary-navy); margin-bottom: 0.75rem;">Submission Summary</h4>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.85rem;">
                            <div><strong>Type:</strong> <span id="sum-type">-</span></div>
                            <div><strong>Amount:</strong> INR <span id="sum-amount">0</span></div>
                            <div><strong>Date:</strong> <span id="sum-date">-</span></div>
                            <div><strong>Platform:</strong> <span id="sum-platform">-</span></div>
                        </div>
                    </div>

                    <div style="display: flex; justify-content: space-between; margin-top: 1.5rem;">
                        <button type="button" class="btn btn-outline" onclick="goToStep(3)">&larr; Back</button>
                        <button type="button" class="btn btn-primary" id="btn-submit-case" onclick="submitFraudReport()">Submit Fraud Report</button>
                    </div>
                </div>

            </div>
        </section>

        <!-- 6. CONFIRMATION VIEW -->
        <section id="confirmation-view" class="view-section">
            <div class="card" style="max-width: 600px; margin: 0 auto; text-align: center; padding: 3rem 2rem;">
                <div style="width: 60px; height: 60px; background: #DCFCE7; color: var(--success); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2rem; margin: 0 auto 1.5rem auto;">✓</div>
                <h2 style="color: var(--primary-navy); margin-bottom: 0.5rem;">Fraud Report Submitted Successfully</h2>
                <p style="color: var(--text-secondary); margin-bottom: 2rem;">Your investigation case has been registered in the ServiceNow FRAUDNEXUS engine.</p>

                <div style="background: #F8FAFC; border: 1px dashed var(--border-color); border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; text-align: left;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span style="color: var(--text-secondary); font-size: 0.9rem;">Case ID:</span>
                        <strong id="conf-case-id" style="color: var(--primary-navy); font-size: 1.1rem; font-family: monospace;">FNX-2026-000001</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span style="color: var(--text-secondary); font-size: 0.9rem;">Initial Status:</span>
                        <span class="badge badge-new" id="conf-status">New</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: var(--text-secondary); font-size: 0.9rem;">Submitted On:</span>
                        <span id="conf-date" style="font-size: 0.9rem; color: var(--text-primary);">-</span>
                    </div>
                </div>

                <div style="display: flex; gap: 1rem; justify-content: center;">
                    <button class="btn btn-primary" onclick="navigateTo('dashboard-view')">Track in Dashboard</button>
                    <button class="btn btn-outline" onclick="startReportWizard()">Report Another Fraud</button>
                </div>
            </div>
        </section>

    </main>

    <!-- CASE DETAILS MODAL -->
    <div id="case-modal" class="fnx-modal-backdrop">
        <div class="fnx-modal">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem;">
                <div>
                    <h3 id="modal-case-number" style="color: var(--primary-navy); font-family: monospace;">FNX-2026-XXXXXX</h3>
                    <div id="modal-case-type" style="color: var(--text-secondary); font-size: 0.85rem;">Payment Fraud</div>
                </div>
                <button onclick="closeCaseModal()" class="btn btn-outline" style="padding: 0.3rem 0.6rem;">&times;</button>
            </div>

            <!-- Timeline -->
            <div class="timeline">
                <div class="tl-node completed" id="tl-node-submitted">
                    <div class="tl-dot"></div>
                    <div class="tl-label">Submitted</div>
                </div>
                <div class="tl-node active" id="tl-node-review">
                    <div class="tl-dot"></div>
                    <div class="tl-label">Initial Review</div>
                </div>
                <div class="tl-node" id="tl-node-investigation">
                    <div class="tl-dot"></div>
                    <div class="tl-label">Investigation</div>
                </div>
                <div class="tl-node" id="tl-node-resolution">
                    <div class="tl-dot"></div>
                    <div class="tl-label">Resolution</div>
                </div>
                <div class="tl-node" id="tl-node-closed">
                    <div class="tl-dot"></div>
                    <div class="tl-label">Closed</div>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem; font-size: 0.9rem;">
                <div><strong>Status:</strong> <span id="modal-status">-</span></div>
                <div><strong>Severity:</strong> <span id="modal-severity">-</span></div>
                <div><strong>Exposure Amount:</strong> INR <span id="modal-amount">-</span></div>
                <div><strong>Platform:</strong> <span id="modal-platform">-</span></div>
                <div><strong>Incident Date:</strong> <span id="modal-date">-</span></div>
                <div><strong>Location:</strong> <span id="modal-location">-</span></div>
            </div>

            <div style="margin-bottom: 1.5rem;">
                <h4 style="color: var(--primary-navy); margin-bottom: 0.5rem; font-size: 0.95rem;">Description</h4>
                <div id="modal-desc" style="background: #F8FAFC; padding: 0.85rem; border-radius: 6px; font-size: 0.9rem; line-height: 1.5; color: var(--text-primary);">-</div>
            </div>

            <div style="margin-bottom: 1rem;">
                <h4 style="color: var(--primary-navy); margin-bottom: 0.5rem; font-size: 0.95rem;">Evidence Submitted</h4>
                <div id="modal-evidence-list" style="font-size: 0.85rem; color: var(--text-secondary);">No evidence uploaded.</div>
            </div>
        </div>
    </div>

    <!-- GENERAL INFO MODAL -->
    <div id="info-modal" class="fnx-modal-backdrop">
        <div class="fnx-modal" style="max-width: 500px;">
            <h3 id="info-modal-title" style="color: var(--primary-navy); margin-bottom: 1rem;">Information</h3>
            <p id="info-modal-body" style="color: var(--text-secondary); line-height: 1.6; margin-bottom: 1.5rem;"></p>
            <div style="display: flex; justify-content: flex-end;">
                <button class="btn btn-navy" onclick="closeInfoModal()">Close</button>
            </div>
        </div>
    </div>

    <!-- FLOATING AI ASSISTANT PILL -->
    <div class="fnx-ai-pill" onclick="toggleAiDrawer()">
        <span>✨</span> Ask FRAUDNEXUS AI
    </div>

    <!-- SLIDING AI DRAWER -->
    <div id="ai-drawer" class="fnx-ai-drawer">
        <div class="ai-drawer-header">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span>✨</span>
                <strong>FRAUDNEXUS Assistant</strong>
            </div>
            <button onclick="toggleAiDrawer()" style="background: none; border: none; color: #FFFFFF; font-size: 1.25rem; cursor: pointer;">&times;</button>
        </div>
        <div class="ai-drawer-body">
            <div class="ai-msg">
                Hello! I am your <strong>FRAUDNEXUS</strong> fraud guidance assistant. How can I assist you with your report or investigation today?
            </div>

            <div style="margin-top: 1rem;">
                <div style="font-size: 0.8rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 0.5rem; text-transform: uppercase;">Suggested Topics</div>
                <button class="ai-intent-btn" onclick="askAi('How to report fraud')">📌 How to report fraud</button>
                <button class="ai-intent-btn" onclick="askAi('Where is my case?')">🔍 Where is my case?</button>
                <button class="ai-intent-btn" onclick="askAi('What does case status mean?')">ℹ️ What does case status mean?</button>
                <button class="ai-intent-btn" onclick="askAi('How do I upload evidence?')">📎 How do I upload evidence?</button>
                <button class="ai-intent-btn" onclick="askAi('How do I contact support?')">📞 How do I contact support?</button>
            </div>

            <div id="ai-chat-history" style="margin-top: 1.25rem;"></div>
        </div>
    </div>

    <!-- CLIENT LOGIC & REST CLIENT -->
    <script>
        const API_BASE = '/api/2229367/fnx_api';
        let currentUser = null;
        let currentCustomer = null;
        let customerCases = [];

        // INITIALIZE ON LOAD
        window.addEventListener('DOMContentLoaded', () => {
            // Set default date in fraud report
            const today = new Date().toISOString().split('T')[0];
            const dateInput = document.getElementById('fr-date');
            if (dateInput) dateInput.value = today;

            // Check persisted session
            const savedUser = localStorage.getItem('fnx_user');
            const savedCust = localStorage.getItem('fnx_customer');
            if (savedUser && savedCust) {
                try {
                    currentUser = JSON.parse(savedUser);
                    currentCustomer = JSON.parse(savedCust);
                    updateHeaderAuth();
                } catch(e) {
                    console.error('Session load error', e);
                }
            }
        });

        function navigateTo(viewId) {
            document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
            const target = document.getElementById(viewId);
            if (target) target.classList.add('active');

            // Update nav active states
            document.querySelectorAll('.fnx-nav a').forEach(a => a.classList.remove('active'));
            if (viewId === 'landing-view') document.getElementById('nav-home')?.classList.add('active');

            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function handleReportFraudNav() {
            if (!currentUser) {
                showAlert('login-alert', 'Please login or create an account to submit a fraud report.', 'error');
                navigateTo('login-view');
            } else {
                startReportWizard();
            }
        }

        function handleMyCasesNav() {
            if (!currentUser) {
                showAlert('login-alert', 'Please login to track your fraud investigation cases.', 'error');
                navigateTo('login-view');
            } else {
                loadCustomerCases();
                navigateTo('dashboard-view');
            }
        }

        function updateHeaderAuth() {
            const container = document.getElementById('header-auth');
            if (!container) return;

            if (currentUser) {
                container.innerHTML = `
                    <div class="fnx-user-badge">
                        <span>👤 ${escapeHtml(currentUser.name)}</span>
                    </div>
                    <button class="btn btn-outline-white" style="padding: 0.4rem 0.8rem; font-size: 0.85rem;" onclick="navigateTo('dashboard-view')">Dashboard</button>
                    <button class="btn btn-outline-white" style="padding: 0.4rem 0.8rem; font-size: 0.85rem;" onclick="logoutCustomer()">Logout</button>
                `;
            } else {
                container.innerHTML = `
                    <button class="btn btn-outline-white" onclick="navigateTo('login-view')">Customer Login</button>
                    <button class="btn btn-primary" onclick="navigateTo('register-view')">Register</button>
                `;
            }
        }

        // REGISTRATION
        async function handleRegistration(e) {
            e.preventDefault();
            const alertBox = document.getElementById('reg-alert');
            alertBox.style.display = 'none';

            const name = document.getElementById('reg-name').value.trim();
            const email = document.getElementById('reg-email').value.trim();
            const mobile = document.getElementById('reg-mobile').value.trim();
            const password = document.getElementById('reg-password').value;
            const confirm = document.getElementById('reg-confirm').value;

            if (!name || !email || !mobile || !password) {
                showAlert('reg-alert', 'Please fill in all mandatory fields.', 'error');
                return;
            }

            if (password !== confirm) {
                showAlert('reg-alert', 'Passwords do not match.', 'error');
                return;
            }

            if (password.length < 6) {
                showAlert('reg-alert', 'Password must be at least 6 characters long.', 'error');
                return;
            }

            const btn = document.getElementById('btn-reg-submit');
            btn.disabled = true;
            btn.innerText = 'Creating ServiceNow Account...';

            try {
                const res = await fetch(`${API_BASE}/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email, mobile, password })
                });

                const data = await res.json();
                const result = data.result || data;

                if (res.ok && result.success) {
                    currentUser = {
                        sys_id: result.user_id,
                        name: result.name,
                        email: result.email
                    };
                    currentCustomer = {
                        customer_id: result.customer_id,
                        name: result.name,
                        email: result.email,
                        status: 'Active'
                    };

                    localStorage.setItem('fnx_user', JSON.stringify(currentUser));
                    localStorage.setItem('fnx_customer', JSON.stringify(currentCustomer));

                    updateHeaderAuth();
                    showInfoModal('Account Created Successfully', 
                        `Your FRAUDNEXUS customer profile has been registered in ServiceNow!\\n\\nCustomer ID: ${result.customer_id}\\nName: ${result.name}\\nEmail: ${result.email}\\n\\nYou can now report fraud and track cases.`
                    );
                    loadCustomerCases();
                    navigateTo('dashboard-view');
                } else {
                    showAlert('reg-alert', result.error || 'Failed to create account.', 'error');
                }
            } catch (err) {
                showAlert('reg-alert', 'Connection error. Please try again.', 'error');
            } finally {
                btn.disabled = false;
                btn.innerText = 'Create Account';
            }
        }

        // LOGIN
        async function handleLogin(e) {
            e.preventDefault();
            const alertBox = document.getElementById('login-alert');
            alertBox.style.display = 'none';

            const email = document.getElementById('login-email').value.trim();
            const password = document.getElementById('login-password').value;

            const btn = document.getElementById('btn-login-submit');
            btn.disabled = true;
            btn.innerText = 'Authenticating...';

            try {
                const res = await fetch(`${API_BASE}/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                const data = await res.json();
                const result = data.result || data;

                if (res.ok && result.success) {
                    currentUser = result.user;
                    currentCustomer = result.customer;

                    localStorage.setItem('fnx_user', JSON.stringify(currentUser));
                    localStorage.setItem('fnx_customer', JSON.stringify(currentCustomer));

                    updateHeaderAuth();
                    loadCustomerCases();
                    navigateTo('dashboard-view');
                } else {
                    showAlert('login-alert', result.error || 'Invalid credentials.', 'error');
                }
            } catch (err) {
                showAlert('login-alert', 'Login failed. Please verify credentials.', 'error');
            } finally {
                btn.disabled = false;
                btn.innerText = 'Login';
            }
        }

        function logoutCustomer() {
            currentUser = null;
            currentCustomer = null;
            customerCases = [];
            localStorage.removeItem('fnx_user');
            localStorage.removeItem('fnx_customer');
            updateHeaderAuth();
            navigateTo('landing-view');
        }

        // DASHBOARD & CASES
        async function loadCustomerCases() {
            if (!currentUser) return;

            document.getElementById('dash-customer-name').innerText = currentUser.name || 'Customer';
            document.getElementById('dash-customer-id').innerText = (currentCustomer && currentCustomer.customer_id) ? currentCustomer.customer_id : 'CNX-2026-ACTIVE';

            try {
                const res = await fetch(`${API_BASE}/cases?user_id=${currentUser.sys_id}`);
                const data = await res.json();
                const result = data.result || data;

                if (res.ok && result.success) {
                    customerCases = result.cases || [];
                    const stats = result.stats || { total: 0, active: 0, resolved: 0 };

                    document.getElementById('stat-total').innerText = stats.total;
                    document.getElementById('stat-active').innerText = stats.active;
                    document.getElementById('stat-resolved').innerText = stats.resolved;

                    renderCasesTable(customerCases);
                }
            } catch(e) {
                console.error('Failed loading cases', e);
            }
        }

        function renderCasesTable(cases) {
            const tbody = document.getElementById('cases-table-body');
            if (!cases || cases.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: var(--text-secondary); padding: 2rem;">No fraud cases reported yet.</td></tr>';
                return;
            }

            tbody.innerHTML = cases.map(c => `
                <tr>
                    <td style="font-family: monospace; font-weight: 600; color: var(--secondary-navy);">${escapeHtml(c.number || '')}</td>
                    <td><strong>${escapeHtml(c.type || '')}</strong></td>
                    <td>${escapeHtml(c.incident_date || c.created_on?.split(' ')[0] || '')}</td>
                    <td>₹${Number(c.exposure || 0).toLocaleString('en-IN')}</td>
                    <td><span class="badge ${c.stage === 'Resolved' || c.stage === 'Closed' ? 'badge-resolved' : 'badge-active'}">${escapeHtml(c.stage || 'New')}</span></td>
                    <td><span class="badge badge-new">${escapeHtml(c.status || 'New')}</span></td>
                    <td>
                        <button class="btn btn-outline" style="padding: 0.3rem 0.6rem; font-size: 0.8rem;" onclick="viewCaseDetails('${c.sys_id}')">Track</button>
                    </td>
                </tr>
            `).join('');
        }

        function viewCaseDetails(caseSysId) {
            const c = customerCases.find(item => item.sys_id === caseSysId);
            if (!c) return;

            document.getElementById('modal-case-number').innerText = c.number || 'Case Details';
            document.getElementById('modal-case-type').innerText = c.type || '';
            document.getElementById('modal-status').innerText = c.status || 'New';
            document.getElementById('modal-severity').innerText = c.severity || 'Medium';
            document.getElementById('modal-amount').innerText = Number(c.exposure || 0).toLocaleString('en-IN');
            document.getElementById('modal-platform').innerText = c.digital_platform || 'N/A';
            document.getElementById('modal-date').innerText = c.incident_date || 'N/A';
            document.getElementById('modal-location').innerText = c.location || 'N/A';
            document.getElementById('modal-desc').innerText = c.description || 'No description provided.';

            // Evidence
            const evBox = document.getElementById('modal-evidence-list');
            if (c.evidence && c.evidence.length > 0) {
                evBox.innerHTML = c.evidence.map(ev => `
                    <div style="background: #FFFFFF; border: 1px solid var(--border-color); padding: 0.5rem 0.75rem; border-radius: 6px; margin-bottom: 0.35rem;">
                        <strong>${escapeHtml(ev.number)}</strong> (${escapeHtml(ev.type)}): ${escapeHtml(ev.description || 'Uploaded')} - <em>${escapeHtml(ev.status || 'Verified')}</em>
                    </div>
                `).join('');
            } else {
                evBox.innerHTML = '<em>No evidence files attached.</em>';
            }

            document.getElementById('case-modal').classList.add('open');
        }

        function closeCaseModal() {
            document.getElementById('case-modal').classList.remove('open');
        }

        // REPORT FRAUD WIZARD
        function startReportWizard() {
            if (!currentUser) {
                showAlert('login-alert', 'Please login to submit a fraud report.', 'error');
                navigateTo('login-view');
                return;
            }
            goToStep(1);
            navigateTo('report-view');
        }

        function goToStep(stepNum) {
            for (let i = 1; i <= 4; i++) {
                document.getElementById(`wiz-step-${i}`).style.display = (i === stepNum) ? 'block' : 'none';
                const ind = document.getElementById(`wiz-step-ind-${i}`);
                if (ind) {
                    ind.classList.remove('active', 'completed');
                    if (i < stepNum) ind.classList.add('completed');
                    if (i === stepNum) ind.classList.add('active');
                }
            }

            // Update summary if step 4
            if (stepNum === 4) {
                document.getElementById('sum-type').innerText = document.getElementById('fr-type').value;
                document.getElementById('sum-amount').innerText = Number(document.getElementById('fr-amount').value || 0).toLocaleString('en-IN');
                document.getElementById('sum-date').innerText = document.getElementById('fr-date').value || 'Today';
                document.getElementById('sum-platform').innerText = document.getElementById('fr-platform').value || 'Not specified';
            }
        }

        async function submitFraudReport() {
            const type = document.getElementById('fr-type').value;
            const desc = document.getElementById('fr-desc').value.trim();
            const date = document.getElementById('fr-date').value;
            const time = document.getElementById('fr-time').value;
            const severity = document.getElementById('fr-severity').value;
            const platform = document.getElementById('fr-platform').value.trim();
            const location = document.getElementById('fr-location').value.trim();
            const area = document.getElementById('fr-area').value.trim();
            const pincode = document.getElementById('fr-pincode').value.trim();
            const amount = document.getElementById('fr-amount').value || '0';
            const evType = document.getElementById('fr-ev-type').value;
            const evDesc = document.getElementById('fr-ev-desc').value.trim();
            const fileInput = document.getElementById('fr-file');
            const attachmentName = fileInput?.files?.[0]?.name || '';

            if (!desc) {
                alert('Please enter a case description in Step 1.');
                goToStep(1);
                return;
            }

            const btn = document.getElementById('btn-submit-case');
            btn.disabled = true;
            btn.innerText = 'Creating ServiceNow Fraud Case...';

            const payload = {
                user_id: currentUser.sys_id,
                customer_id: currentCustomer ? currentCustomer.sys_id : '',
                type: type,
                description: desc,
                incident_date: date,
                incident_time: time,
                severity: severity,
                digital_platform: platform,
                location: location,
                area: area,
                pincode: pincode,
                exposure: amount,
                evidence_type: evType,
                evidence_description: evDesc,
                attachment_name: attachmentName
            };

            try {
                const res = await fetch(`${API_BASE}/cases`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const data = await res.json();
                const result = data.result || data;

                if (res.ok && result.success) {
                    document.getElementById('conf-case-id').innerText = result.number || 'FNX-2026-CONFIRMED';
                    document.getElementById('conf-status').innerText = result.status || 'New';
                    document.getElementById('conf-date').innerText = result.submitted_on || new Date().toLocaleString();

                    // Reload cases in background
                    loadCustomerCases();
                    navigateTo('confirmation-view');
                } else {
                    alert('Submission failed: ' + (result.error || 'Server error'));
                }
            } catch(e) {
                alert('Connection error while submitting fraud report.');
            } finally {
                btn.disabled = false;
                btn.innerText = 'Submit Fraud Report';
            }
        }

        // AI ASSISTANT
        function toggleAiDrawer() {
            document.getElementById('ai-drawer').classList.toggle('open');
        }

        function askAi(intent) {
            const history = document.getElementById('ai-chat-history');
            const answers = {
                'How to report fraud': 'To report fraud, click "Report Fraud" in the navigation. Follow the 4-step wizard: specify the fraud type, describe what occurred, add financial and platform details, and upload any evidence (screenshots, receipts, or chat logs).',
                'Where is my case?': 'You can track all your submitted cases under the "Dashboard" or "Track Case" tab. Each case has an assigned FNX identifier (e.g. FNX-2026-000001) with live status updates.',
                'What does case status mean?': 'Case Statuses:\\n• New: Case registered in ServiceNow.\\n• Initial Review: Evidence and accounts are being verified.\\n• Investigation: Forensic analysis and entity correlation active.\\n• Resolved: Investigation completed with recovery steps taken.',
                'How do I upload evidence?': 'During fraud report submission (Step 4), use the file upload selector to attach screenshots, PDFs, or chat exports. The ServiceNow chain-of-custody engine logs and protects all uploaded materials.',
                'How do I contact support?': 'For urgent account freeze requests or severe financial threats, please call the 24/7 National Cyber Fraud Helpline at 1930 or your bank\\'s immediate fraud hotline.'
            };

            const userHtml = `<div style="text-align: right; margin-bottom: 0.5rem;"><span style="background: var(--intel-cyan); color: #0B1F3A; padding: 0.4rem 0.75rem; border-radius: 12px; font-size: 0.85rem; font-weight: 500;">${escapeHtml(intent)}</span></div>`;
            const botHtml = `<div class="ai-msg">${escapeHtml(answers[intent] || 'I can assist you with fraud reporting and status tracking.')}</div>`;

            history.innerHTML += userHtml + botHtml;
            history.scrollTop = history.scrollHeight;
        }

        // UTILITIES
        function showAlert(id, msg, type) {
            const el = document.getElementById(id);
            if (!el) return;
            el.className = `alert-box alert-${type}`;
            el.innerText = msg;
            el.style.display = 'block';
        }

        function showInfoModal(title, body) {
            document.getElementById('info-modal-title').innerText = title;
            document.getElementById('info-modal-body').innerText = body;
            document.getElementById('info-modal').classList.add('open');
        }

        function closeInfoModal() {
            document.getElementById('info-modal').classList.remove('open');
        }

        function escapeHtml(text) {
            if (!text) return '';
            const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
            return String(text).replace(/[&<>"']/g, m => map[m]);
        }
    </script>
</body>
</html>
"""

# Check or Create sys_ui_page
r_chk = requests.get(f"{url}/api/now/table/sys_ui_page?sysparm_query=name=fnx_portal", auth=auth, headers=headers)
existing = r_chk.json().get('result', [])

page_payload = {
    "name": "fnx_portal",
    "html": portal_html,
    "description": "FRAUDNEXUS Customer Portal Foundation (Phase 1)",
    "direct": "true" # Full HTML document rendering
}

if existing:
    page_id = existing[0]['sys_id']
    r_update = requests.patch(f"{url}/api/now/table/sys_ui_page/{page_id}", auth=auth, headers=headers, json=page_payload)
    print("Updated sys_ui_page 'fnx_portal':", r_update.status_code)
else:
    r_create = requests.post(f"{url}/api/now/table/sys_ui_page", auth=auth, headers=headers, json=page_payload)
    print("Created sys_ui_page 'fnx_portal':", r_create.status_code)

# Check access to the page
test_url = f"{url}/fnx_portal.do"
r_page = requests.get(test_url, auth=auth)
print(f"Page URL: {test_url} -> Status {r_page.status_code}, Length: {len(r_page.text)}")
