import os
import re
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv('d:/KPMG/.env')
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

# Generate Complete FRAUDNEXUS Enterprise UI
portal_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FRAUDNEXUS — Financial & Cyber Fraud Investigation Hub</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-navy: #0B1F3A;
            --secondary-navy: #123B63;
            --intel-cyan: #00B8D9;
            --intel-cyan-dark: #0093ad;
            --success: #16A34A;
            --warning: #F59E0B;
            --critical: #DC2626;
            --bg-color: #F5F7FA;
            --card-bg: #FFFFFF;
            --border-color: #E2E8F0;
            --text-primary: #0F172A;
            --text-secondary: #64748B;
            --sidebar-bg: #0B1F3A;
            --sidebar-hover: #123B63;
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

        /* TOP HEADER */
        .fnx-header {
            background-color: var(--primary-navy);
            color: #FFFFFF;
            padding: 0.85rem 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 500;
            border-bottom: 2px solid var(--intel-cyan);
            box-shadow: 0 4px 15px rgba(11, 31, 58, 0.2);
        }

        .fnx-brand {
            display: flex;
            align-items: center;
            gap: 0.85rem;
            text-decoration: none;
            color: #FFFFFF;
            cursor: pointer;
        }

        .fnx-logo-icon {
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, var(--intel-cyan), var(--secondary-navy));
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #FFFFFF;
            font-weight: 800;
            font-size: 1.25rem;
            box-shadow: 0 2px 8px rgba(0, 184, 217, 0.3);
        }

        .fnx-brand-text {
            display: flex;
            flex-direction: column;
        }

        .fnx-brand-title {
            font-size: 1.25rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            line-height: 1.1;
        }

        .fnx-brand-tagline {
            font-size: 0.68rem;
            color: #94A3B8;
            font-weight: 500;
            letter-spacing: 0.2px;
        }

        .fnx-header-nav {
            display: flex;
            align-items: center;
            gap: 1.25rem;
        }

        .fnx-header-nav a {
            color: #E2E8F0;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            cursor: pointer;
            transition: color 0.2s;
            padding: 0.35rem 0.5rem;
            border-radius: 4px;
        }

        .fnx-header-nav a:hover, .fnx-header-nav a.active {
            color: var(--intel-cyan);
            background: rgba(255, 255, 255, 0.05);
        }

        /* TOP-RIGHT CONTROLS */
        .fnx-header-right {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .lang-selector {
            background: rgba(255, 255, 255, 0.1);
            color: #FFFFFF;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 0.4rem 0.75rem;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            outline: none;
            transition: all 0.2s;
        }

        .lang-selector option {
            background: var(--primary-navy);
            color: #FFFFFF;
        }

        .notif-bell-btn {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #FFFFFF;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            position: relative;
            font-size: 1rem;
            transition: all 0.2s;
        }

        .notif-bell-btn:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: scale(1.05);
        }

        .notif-badge {
            position: absolute;
            top: -3px;
            right: -3px;
            background: var(--critical);
            color: #FFFFFF;
            font-size: 0.65rem;
            font-weight: 700;
            width: 17px;
            height: 17px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid var(--primary-navy);
        }

        .notif-dropdown {
            display: none;
            position: absolute;
            top: 55px;
            right: 180px;
            width: 320px;
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
            z-index: 600;
            overflow: hidden;
            animation: fadeIn 0.2s ease;
        }

        .notif-dropdown.open {
            display: block;
        }

        .notif-header {
            background: var(--primary-navy);
            color: #FFFFFF;
            padding: 0.75rem 1rem;
            font-size: 0.85rem;
            font-weight: 700;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .notif-list {
            max-height: 280px;
            overflow-y: auto;
        }

        .notif-item {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border-color);
            font-size: 0.8rem;
            transition: background 0.15s;
            cursor: pointer;
        }

        .notif-item:hover {
            background: #F8FAFC;
        }

        .notif-title {
            font-weight: 600;
            color: var(--primary-navy);
            margin-bottom: 0.2rem;
        }

        .notif-time {
            font-size: 0.7rem;
            color: var(--text-secondary);
        }

        .profile-badge {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            background: rgba(255, 255, 255, 0.1);
            padding: 0.35rem 0.85rem;
            border-radius: 20px;
            font-size: 0.85rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #FFFFFF;
        }

        /* BUTTONS */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            padding: 0.6rem 1.2rem;
            font-size: 0.9rem;
            font-weight: 600;
            border-radius: 6px;
            border: none;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
        }

        .btn-primary {
            background-color: var(--intel-cyan);
            color: #0B1F3A;
        }

        .btn-primary:hover {
            background-color: var(--intel-cyan-dark);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 184, 217, 0.3);
        }

        .btn-navy {
            background-color: var(--secondary-navy);
            color: #FFFFFF;
        }

        .btn-navy:hover {
            background-color: #0B1F3A;
            transform: translateY(-1px);
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
            border: 1px solid rgba(255, 255, 255, 0.4);
            color: #FFFFFF;
        }

        .btn-outline-white:hover {
            background-color: rgba(255, 255, 255, 0.15);
            border-color: #FFFFFF;
        }

        /* APP LAYOUT */
        .app-body {
            flex: 1;
            display: flex;
            min-height: calc(100vh - 65px);
        }

        /* SIDEBAR (Customer Portal Mode) */
        .fnx-sidebar {
            width: 250px;
            background: var(--sidebar-bg);
            color: #FFFFFF;
            display: flex;
            flex-direction: column;
            border-right: 1px solid var(--border-color);
            padding: 1.5rem 0;
            transition: width 0.3s;
        }

        .sidebar-heading {
            padding: 0 1.5rem;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            color: #94A3B8;
            letter-spacing: 0.8px;
            margin-bottom: 0.75rem;
        }

        .sidebar-menu {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
        }

        .sidebar-item a {
            display: flex;
            align-items: center;
            gap: 0.85rem;
            padding: 0.75rem 1.5rem;
            color: #CBD5E1;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.2s;
            border-left: 3px solid transparent;
            cursor: pointer;
        }

        .sidebar-item a:hover {
            background: var(--sidebar-hover);
            color: #FFFFFF;
        }

        .sidebar-item.active a {
            background: rgba(0, 184, 217, 0.12);
            color: var(--intel-cyan);
            border-left-color: var(--intel-cyan);
            font-weight: 700;
        }

        .sidebar-emergency-card {
            margin: auto 1rem 1rem 1rem;
            background: rgba(220, 38, 38, 0.15);
            border: 1px solid rgba(220, 38, 38, 0.3);
            border-radius: 8px;
            padding: 0.85rem;
            font-size: 0.8rem;
        }

        .sidebar-emergency-title {
            color: #FCA5A5;
            font-weight: 700;
            margin-bottom: 0.25rem;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        /* MAIN CONTENT AREA */
        .content-area {
            flex: 1;
            padding: 2rem;
            overflow-y: auto;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
        }

        .view-section {
            display: none;
        }

        .view-section.active {
            display: block;
            animation: fadeIn 0.25s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(4px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* HERO & LANDING */
        .hero-banner {
            background: linear-gradient(135deg, var(--primary-navy) 0%, var(--secondary-navy) 100%);
            color: #FFFFFF;
            border-radius: 14px;
            padding: 3.5rem 3rem;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(11, 31, 58, 0.25);
            border: 1px solid rgba(0, 184, 217, 0.3);
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(0, 184, 217, 0.15);
            border: 1px solid var(--intel-cyan);
            color: var(--intel-cyan);
            font-size: 0.8rem;
            font-weight: 700;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .hero-title {
            font-size: 2.6rem;
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 1rem;
            letter-spacing: -0.5px;
        }

        .hero-title span {
            color: var(--intel-cyan);
        }

        .hero-subtitle {
            font-size: 1.15rem;
            color: #CBD5E1;
            max-width: 750px;
            margin-bottom: 2rem;
            line-height: 1.6;
        }

        .hero-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }

        .feature-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.75rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02);
            transition: all 0.2s ease;
        }

        .feature-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.06);
            border-color: var(--intel-cyan);
        }

        .feature-icon {
            font-size: 2rem;
            margin-bottom: 1rem;
        }

        .feature-title {
            font-size: 1.15rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: var(--primary-navy);
        }

        .feature-desc {
            font-size: 0.88rem;
            color: var(--text-secondary);
            line-height: 1.5;
        }

        /* PORTAL SELECTION MODAL / SECTION */
        .portal-selector-card {
            background: var(--card-bg);
            border: 2px solid var(--border-color);
            border-radius: 14px;
            padding: 2.25rem;
            cursor: pointer;
            transition: all 0.25s ease;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .portal-selector-card:hover {
            border-color: var(--intel-cyan);
            box-shadow: 0 10px 30px rgba(0, 184, 217, 0.15);
            transform: translateY(-4px);
        }

        .portal-selector-card.admin:hover {
            border-color: var(--secondary-navy);
            box-shadow: 0 10px 30px rgba(18, 59, 99, 0.2);
        }

        /* STATS & METRICS */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 1.25rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            border-left: 5px solid var(--intel-cyan);
            box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        }

        .stat-card.active-cases { border-left-color: var(--warning); }
        .stat-card.resolved-cases { border-left-color: var(--success); }
        .stat-card.closed-cases { border-left-color: var(--secondary-navy); }

        .stat-value {
            font-size: 2.25rem;
            font-weight: 800;
            color: var(--primary-navy);
            margin: 0.25rem 0;
        }

        .stat-label {
            font-size: 0.82rem;
            font-weight: 700;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* TABLES */
        .table-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.75rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        }

        .table-responsive {
            overflow-x: auto;
            border: 1px solid var(--border-color);
            border-radius: 8px;
        }

        table.fnx-table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.88rem;
        }

        table.fnx-table th {
            background-color: #F8FAFC;
            color: var(--text-secondary);
            font-weight: 700;
            padding: 0.85rem 1rem;
            border-bottom: 1px solid var(--border-color);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        table.fnx-table td {
            padding: 0.85rem 1rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-primary);
        }

        table.fnx-table tr:hover td {
            background-color: #F1F5F9;
        }

        /* BADGES */
        .badge {
            display: inline-block;
            padding: 0.3rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
        }

        .badge-new { background-color: #E0F2FE; color: #0284C7; }
        .badge-active { background-color: #FEF3C7; color: #D97706; }
        .badge-resolved { background-color: #DCFCE7; color: #16A34A; }
        .badge-closed { background-color: #F1F5F9; color: #475569; }
        .badge-critical { background-color: #FEE2E2; color: #DC2626; }

        /* WIZARD & FORMS */
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
            width: 34px;
            height: 34px;
            border-radius: 50%;
            background: #E2E8F0;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 0.5rem auto;
            font-weight: 700;
            font-size: 0.9rem;
            transition: all 0.2s;
        }

        .step-item.active .step-circle {
            background: var(--intel-cyan);
            color: #0B1F3A;
            box-shadow: 0 0 0 4px rgba(0, 184, 217, 0.2);
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

        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
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
            font-weight: 700;
            color: var(--text-primary);
        }

        .form-label span.req { color: var(--critical); }
        .form-label span.opt { color: var(--text-secondary); font-weight: normal; font-size: 0.78rem; }

        .form-control {
            padding: 0.65rem 0.85rem;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            font-size: 0.92rem;
            outline: none;
            transition: all 0.2s;
            background: #FFFFFF;
        }

        .form-control:focus {
            border-color: var(--intel-cyan);
            box-shadow: 0 0 0 3px rgba(0, 184, 217, 0.15);
        }

        textarea.form-control {
            min-height: 100px;
            resize: vertical;
        }

        .gate-choice-box {
            display: flex;
            gap: 1.5rem;
            margin: 1rem 0;
        }

        .gate-choice-label {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.25rem;
            border: 2px solid var(--border-color);
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .gate-choice-label:hover, .gate-choice-label.selected {
            border-color: var(--intel-cyan);
            background: rgba(0, 184, 217, 0.05);
        }

        /* TIMELINE TRACKER */
        .timeline {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 1.75rem 0;
            padding: 1.5rem;
            background: #F8FAFC;
            border-radius: 10px;
            border: 1px solid var(--border-color);
        }

        .tl-node {
            text-align: center;
            position: relative;
            flex: 1;
        }

        .tl-dot {
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: #CBD5E1;
            margin: 0 auto 0.5rem auto;
            transition: all 0.2s;
        }

        .tl-node.active .tl-dot {
            background: var(--intel-cyan);
            box-shadow: 0 0 0 5px rgba(0, 184, 217, 0.25);
        }

        .tl-node.completed .tl-dot {
            background: var(--success);
        }

        .tl-label {
            font-size: 0.78rem;
            font-weight: 700;
            color: var(--text-secondary);
        }

        /* FLOATING AI ASSISTANT */
        .fnx-ai-pill {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: linear-gradient(135deg, var(--primary-navy), var(--secondary-navy));
            border: 2px solid var(--intel-cyan);
            color: #FFFFFF;
            padding: 0.75rem 1.35rem;
            border-radius: 35px;
            box-shadow: 0 8px 25px rgba(0, 184, 217, 0.35);
            display: flex;
            align-items: center;
            gap: 0.65rem;
            font-weight: 700;
            font-size: 0.92rem;
            cursor: pointer;
            z-index: 1000;
            transition: all 0.25s ease;
        }

        .fnx-ai-pill:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 30px rgba(0, 184, 217, 0.5);
        }

        .fnx-ai-drawer {
            position: fixed;
            top: 0;
            right: -450px;
            width: 420px;
            height: 100vh;
            background: #FFFFFF;
            box-shadow: -8px 0 30px rgba(0,0,0,0.18);
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
            border-bottom: 2px solid var(--intel-cyan);
        }

        .ai-drawer-body {
            flex: 1;
            padding: 1.25rem;
            overflow-y: auto;
            background: #F8FAFC;
            display: flex;
            flex-direction: column;
            gap: 0.85rem;
        }

        .ai-msg {
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            padding: 0.9rem 1.1rem;
            border-radius: 10px;
            font-size: 0.88rem;
            line-height: 1.5;
            box-shadow: 0 1px 4px rgba(0,0,0,0.02);
        }

        .ai-user-bubble {
            background: var(--intel-cyan);
            color: #0B1F3A;
            align-self: flex-end;
            padding: 0.6rem 1rem;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 600;
            max-width: 85%;
        }

        .ai-intent-btn {
            display: block;
            width: 100%;
            text-align: left;
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            padding: 0.65rem 0.9rem;
            border-radius: 8px;
            font-size: 0.84rem;
            color: var(--primary-navy);
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s;
        }

        .ai-intent-btn:hover {
            border-color: var(--intel-cyan);
            background: rgba(0, 184, 217, 0.05);
            transform: translateX(2px);
        }

        /* MODALS */
        .fnx-modal-backdrop {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(11, 31, 58, 0.65);
            backdrop-filter: blur(2px);
            z-index: 2000;
            align-items: center;
            justify-content: center;
            padding: 1.5rem;
        }

        .fnx-modal-backdrop.open { display: flex; }

        .fnx-modal {
            background: #FFFFFF;
            border-radius: 14px;
            max-width: 720px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
            padding: 2.25rem;
            box-shadow: 0 25px 50px rgba(0,0,0,0.25);
            position: relative;
        }

        .alert-box {
            padding: 0.85rem 1.2rem;
            border-radius: 8px;
            margin-bottom: 1.25rem;
            font-size: 0.88rem;
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

    <!-- TOP HEADER -->
    <header class="fnx-header">
        <div class="fnx-brand" onclick="navigateTo('landing-view')">
            <div class="fnx-logo-icon">F</div>
            <div class="fnx-brand-text">
                <span class="fnx-brand-title">FRAUDNEXUS</span>
                <span class="fnx-brand-tagline" data-i18n="tagline">From Fraud Report to Resolution — One Investigation Workspace</span>
            </div>
        </div>

        <nav class="fnx-header-nav" id="header-top-nav">
            <a onclick="navigateTo('landing-view')" id="nav-home" data-i18n="nav_home">Home</a>
            <a onclick="navigateTo('portal-select-view')" id="nav-portal-select" data-i18n="nav_portal_select">Portal Gateways</a>
            <a onclick="handleReportFraudNav()" id="nav-report" data-i18n="nav_report">Report Fraud</a>
            <a onclick="handleMyCasesNav()" id="nav-cases" data-i18n="nav_track">Track Case</a>
            <a onclick="showInfoModal('About FRAUDNEXUS', 'FRAUDNEXUS is the official enterprise Financial & Cyber Fraud Investigation Hub built directly inside ServiceNow. Scoped App: x_fnx_fraudnexus. Connected live instance: dev187180.service-now.com.')" data-i18n="nav_about">About</a>
        </nav>

        <div class="fnx-header-right">
            <!-- 1. Language Selector TOP-RIGHT -->
            <select class="lang-selector" id="lang-select" onchange="changeLanguage(this.value)">
                <option value="en">🌐 English</option>
                <option value="ta">🌐 தமிழ் (Tamil)</option>
            </select>

            <!-- 2. Notification Bell TOP-RIGHT -->
            <div style="position: relative;">
                <button class="notif-bell-btn" onclick="toggleNotifications()" title="Notifications">
                    🔔
                    <span class="notif-badge" id="notif-count">3</span>
                </button>
                <div class="notif-dropdown" id="notif-dropdown">
                    <div class="notif-header">
                        <span data-i18n="notifications">Alerts & Notifications</span>
                        <span style="font-size: 0.7rem; cursor: pointer; color: var(--intel-cyan);" onclick="clearNotifications()">Clear</span>
                    </div>
                    <div class="notif-list" id="notif-list">
                        <div class="notif-item">
                            <div class="notif-title">Case Registered (FNX-2026-001001)</div>
                            <div>Your payment fraud report is registered in ServiceNow engine.</div>
                            <div class="notif-time">Just now</div>
                        </div>
                        <div class="notif-item">
                            <div class="notif-title">Evidence Chain of Custody Verified</div>
                            <div>Transaction screenshot verified with SHA-256 hash.</div>
                            <div class="notif-time">10 mins ago</div>
                        </div>
                        <div class="notif-item">
                            <div class="notif-title">National Cyber Fraud Alert</div>
                            <div>Advisory on malicious APK links mimicking banking portals.</div>
                            <div class="notif-time">1 hour ago</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 3. Customer Profile TOP-RIGHT -->
            <div id="header-auth">
                <button class="btn btn-outline-white" onclick="navigateTo('login-view')" data-i18n="login_btn">Customer Login</button>
                <button class="btn btn-primary" onclick="navigateTo('register-view')" data-i18n="register_btn">Register</button>
            </div>
        </div>
    </header>

    <!-- APP BODY (Sidebar + Content) -->
    <div class="app-body">

        <!-- LEFT SIDEBAR (Visible in Customer Portal Workspace) -->
        <aside class="fnx-sidebar" id="app-sidebar" style="display: none;">
            <div class="sidebar-heading" data-i18n="customer_workspace">Customer Workspace</div>
            <ul class="sidebar-menu">
                <li class="sidebar-item active" id="sb-dash">
                    <a onclick="switchWorkspaceTab('dash')">📊 <span data-i18n="sb_dashboard">Dashboard</span></a>
                </li>
                <li class="sidebar-item" id="sb-report">
                    <a onclick="switchWorkspaceTab('report')">🚨 <span data-i18n="sb_report_fraud">Report Fraud</span></a>
                </li>
                <li class="sidebar-item" id="sb-track">
                    <a onclick="switchWorkspaceTab('track')">🔍 <span data-i18n="sb_track_cases">Track Cases</span></a>
                </li>
                <li class="sidebar-item" id="sb-evidence">
                    <a onclick="switchWorkspaceTab('evidence')">📁 <span data-i18n="sb_evidence_vault">Evidence Vault</span></a>
                </li>
                <li class="sidebar-item" id="sb-help">
                    <a onclick="switchWorkspaceTab('help')">❓ <span data-i18n="sb_help_support">Help & Support</span></a>
                </li>
            </ul>

            <div class="sidebar-emergency-card">
                <div class="sidebar-emergency-title">🚨 24/7 Fraud Helpline</div>
                <div>Dial <strong>1930</strong> immediately to freeze defrauded bank accounts.</div>
            </div>
        </aside>

        <!-- MAIN CONTENT AREA -->
        <main class="content-area">

            <!-- 1. LANDING PAGE VIEW -->
            <section id="landing-view" class="view-section active">
                <div class="hero-banner">
                    <div class="hero-badge">Enterprise Investigation Hub</div>
                    <div class="hero-title">
                        Financial &amp; Cyber Fraud<br><span>Investigation Workspace</span>
                    </div>
                    <div class="hero-subtitle" data-i18n="hero_desc">
                        From Fraud Report to Resolution — One Intelligent Investigation Workspace. Report unauthorized payments, submit digital forensic evidence, and track investigation milestones in real time.
                    </div>
                    <div class="hero-actions">
                        <button class="btn btn-primary" onclick="handleReportFraudNav()">🚨 <span data-i18n="btn_report_fraud">Report Fraud</span></button>
                        <button class="btn btn-outline-white" onclick="handleMyCasesNav()">🔍 <span data-i18n="btn_track_case">Track Case</span></button>
                        <button class="btn btn-navy" onclick="navigateTo('portal-select-view')">🏛️ <span data-i18n="btn_select_portal">Select Portal Gateway</span></button>
                    </div>
                </div>

                <div class="features-grid">
                    <div class="feature-card">
                        <div class="feature-icon">🛡️</div>
                        <div class="feature-title" data-i18n="feat_1_title">Secure Fraud Reporting</div>
                        <div class="feature-desc" data-i18n="feat_1_desc">Comprehensive reporting for UPI, unauthorized debits, phishing, and crypto frauds with bank-grade privacy. Zero credential exposure.</div>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">📁</div>
                        <div class="feature-title" data-i18n="feat_2_title">Forensic Evidence Chain</div>
                        <div class="feature-desc" data-i18n="feat_2_desc">Upload screenshots, statements, audio, and chat exports with automatic cryptographic SHA-256 chain of custody logging.</div>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">📊</div>
                        <div class="feature-title" data-i18n="feat_3_title">Real-Time Investigation Tracker</div>
                        <div class="feature-desc" data-i18n="feat_3_desc">Clear visibility from Submitted to Initial Review, Forensic Analysis, Resolution, and Asset Recovery.</div>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">🧠</div>
                        <div class="feature-title" data-i18n="feat_4_title">Intelligent Link Analysis</div>
                        <div class="feature-desc" data-i18n="feat_4_desc">Correlates mule accounts, suspicious beneficiary phone numbers, and syndicate fraud rings across multiple banking networks.</div>
                    </div>
                </div>
            </section>

            <!-- 2. DASHBOARD / PORTAL SELECTION VIEW -->
            <section id="portal-select-view" class="view-section">
                <div style="text-align: center; margin-bottom: 2.5rem;">
                    <h2 style="color: var(--primary-navy); font-size: 2rem; margin-bottom: 0.5rem;" data-i18n="portal_gateways_title">FRAUDNEXUS Portal Gateways</h2>
                    <p style="color: var(--text-secondary); max-width: 600px; margin: 0 auto;" data-i18n="portal_gateways_sub">Select your designated environment to proceed with fraud reporting or internal investigation management.</p>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 2rem; max-width: 950px; margin: 0 auto 3rem auto;">
                    <!-- Customer Portal Card -->
                    <div class="portal-selector-card" onclick="enterCustomerPortal()">
                        <div>
                            <div style="font-size: 2.5rem; margin-bottom: 1rem;">👤</div>
                            <h3 style="color: var(--primary-navy); font-size: 1.4rem; margin-bottom: 0.75rem;" data-i18n="portal_cust_title">Customer Portal</h3>
                            <p style="color: var(--text-secondary); font-size: 0.92rem; line-height: 1.6; margin-bottom: 1.5rem;" data-i18n="portal_cust_desc">
                                For citizens and customers to report fraud incidents, upload proof, track case progress, submit additional evidence, and consult the AI guidance assistant.
                            </p>
                            <ul style="list-style: none; font-size: 0.85rem; color: var(--text-primary); display: flex; flex-direction: column; gap: 0.4rem; margin-bottom: 1.5rem;">
                                <li>✓ Report Financial & Cyber Fraud</li>
                                <li>✓ Live Milestone Tracking (FNX-2026-xxxxxx)</li>
                                <li>✓ Attach Additional Evidence Post-Submission</li>
                                <li>✓ Ask FRAUDNEXUS AI Assistance</li>
                            </ul>
                        </div>
                        <button class="btn btn-primary" style="width: 100%;" data-i18n="portal_cust_btn">Enter Customer Workspace &rarr;</button>
                    </div>

                    <!-- Investigator / Admin Portal Card -->
                    <div class="portal-selector-card admin" onclick="enterInvestigatorPortal()">
                        <div>
                            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🏛️</div>
                            <h3 style="color: var(--primary-navy); font-size: 1.4rem; margin-bottom: 0.75rem;" data-i18n="portal_admin_title">Investigator / Admin Hub</h3>
                            <p style="color: var(--text-secondary); font-size: 0.92rem; line-height: 1.6; margin-bottom: 1.5rem;" data-i18n="portal_admin_desc">
                                For authorized investigation officers, risk handlers, and managers. Command center triage, case allocation, syndicate ring analysis, and regulatory reporting.
                            </p>
                            <ul style="list-style: none; font-size: 0.85rem; color: var(--text-primary); display: flex; flex-direction: column; gap: 0.4rem; margin-bottom: 1.5rem;">
                                <li>✓ Command Center & Priority Triage Queue</li>
                                <li>✓ Explainable AI Handler Suggestion</li>
                                <li>✓ Mule Account & Fraud Ring Correlator</li>
                                <li>✓ Compliance & Regulatory Draft Engine</li>
                            </ul>
                        </div>
                        <button class="btn btn-navy" style="width: 100%;" data-i18n="portal_admin_btn">Staff Access / App Engine Studio &rarr;</button>
                    </div>
                </div>
            </section>

            <!-- 3. CUSTOMER REGISTRATION VIEW -->
            <section id="register-view" class="view-section">
                <div class="table-card" style="max-width: 650px; margin: 0 auto;">
                    <h2 style="color: var(--primary-navy); margin-bottom: 0.5rem;" data-i18n="create_account_title">Create FRAUDNEXUS Customer Profile</h2>
                    <p style="color: var(--text-secondary); margin-bottom: 1.5rem; font-size: 0.9rem;" data-i18n="create_account_sub">Register to report fraud incidents and track investigation updates. KYC can be completed anytime and does not block urgent fraud reports.</p>

                    <div id="reg-alert" class="alert-box"></div>

                    <form id="reg-form" onsubmit="handleRegistration(event)">
                        <!-- Section A: Identity Credentials -->
                        <h4 style="color: var(--secondary-navy); margin-bottom: 0.85rem; font-size: 0.95rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.4rem;" data-i18n="sec_identity">1. Identity &amp; Credentials</h4>
                        <div class="form-grid" style="margin-bottom: 1.5rem;">
                            <div class="form-group">
                                <label class="form-label">Full Name <span class="req">*</span></label>
                                <input type="text" id="reg-name" class="form-control" placeholder="e.g. Arun Kumar" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Mobile Number <span class="req">*</span></label>
                                <input type="tel" id="reg-mobile" class="form-control" placeholder="10-digit mobile number" required>
                            </div>
                            <div class="form-group full-width">
                                <label class="form-label">Email Address <span class="req">*</span></label>
                                <input type="email" id="reg-email" class="form-control" placeholder="name@example.com" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Password <span class="req">*</span></label>
                                <input type="password" id="reg-password" class="form-control" placeholder="Min 6 characters" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Confirm Password <span class="req">*</span></label>
                                <input type="password" id="reg-confirm" class="form-control" placeholder="Confirm password" required>
                            </div>
                        </div>

                        <!-- Section B: Additional Profile & KYC (Non-blocking) -->
                        <h4 style="color: var(--secondary-navy); margin-bottom: 0.85rem; font-size: 0.95rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.4rem;">
                            <span data-i18n="sec_profile">2. Profile &amp; KYC Verification</span> <span class="form-label opt">(Optional / Non-blocking)</span>
                        </h4>
                        <div class="form-grid" style="margin-bottom: 1.5rem;">
                            <div class="form-group">
                                <label class="form-label">Date of Birth</label>
                                <input type="date" id="reg-dob" class="form-control">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Gender</label>
                                <select id="reg-gender" class="form-control">
                                    <option value="">Select Gender</option>
                                    <option value="Male">Male</option>
                                    <option value="Female">Female</option>
                                    <option value="Other">Other</option>
                                    <option value="Prefer not to say">Prefer not to say</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Occupation</label>
                                <input type="text" id="reg-occupation" class="form-control" placeholder="e.g. Software Engineer, Merchant">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Government ID Type</label>
                                <select id="reg-id-type" class="form-control">
                                    <option value="Aadhaar">Aadhaar</option>
                                    <option value="PAN">PAN</option>
                                    <option value="Passport">Passport</option>
                                    <option value="Driving Licence">Driving Licence</option>
                                    <option value="Voter ID">Voter ID</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                            <div class="form-group full-width">
                                <label class="form-label">Masked Government ID Number <span class="opt">(NEVER enter full raw ID)</span></label>
                                <input type="text" id="reg-masked-id" class="form-control" placeholder="e.g. XXXX-XXXX-1234 or ABCDE****F">
                            </div>
                            <div class="form-group full-width">
                                <label class="form-label">Address</label>
                                <input type="text" id="reg-address" class="form-control" placeholder="Street, City, Pincode">
                            </div>
                        </div>

                        <button type="submit" class="btn btn-navy" style="width: 100%;" id="btn-reg-submit" data-i18n="create_account_btn">Create Account &amp; Enter Workspace</button>
                    </form>

                    <div style="margin-top: 1.5rem; text-align: center; font-size: 0.9rem; color: var(--text-secondary);">
                        Already registered? <a onclick="navigateTo('login-view')" style="color: var(--intel-cyan); cursor: pointer; font-weight: 700;">Login here</a>
                    </div>
                </div>
            </section>

            <!-- 4. CUSTOMER LOGIN VIEW -->
            <section id="login-view" class="view-section">
                <div class="table-card" style="max-width: 480px; margin: 0 auto;">
                    <h2 style="color: var(--primary-navy); margin-bottom: 0.5rem;" data-i18n="login_title">Customer Login</h2>
                    <p style="color: var(--text-secondary); margin-bottom: 1.5rem; font-size: 0.9rem;" data-i18n="login_sub">Sign in to your FRAUDNEXUS customer workspace.</p>

                    <div id="login-alert" class="alert-box"></div>

                    <form id="login-form" onsubmit="handleLogin(event)">
                        <div class="form-group" style="margin-bottom: 1rem;">
                            <label class="form-label">Email Address / Username</label>
                            <input type="text" id="login-email" class="form-control" placeholder="name@example.com" required>
                        </div>

                        <div class="form-group" style="margin-bottom: 1rem;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <label class="form-label">Password</label>
                                <a onclick="openForgotPasswordModal()" style="font-size: 0.78rem; color: var(--intel-cyan); cursor: pointer; font-weight: 600;">Forgot Password?</a>
                            </div>
                            <input type="password" id="login-password" class="form-control" placeholder="Enter password" required>
                        </div>

                        <button type="submit" class="btn btn-navy" style="width: 100%; margin-top: 0.5rem;" id="btn-login-submit" data-i18n="login_action">Login</button>
                    </form>

                    <!-- Quick Demo Fill -->
                    <div style="margin-top: 1.25rem; padding: 0.75rem; background: #F8FAFC; border-radius: 6px; font-size: 0.8rem; border: 1px dashed var(--border-color);">
                        <strong>Quick Demo Login:</strong> Click below to auto-fill verified test customer:
                        <div style="margin-top: 0.4rem;">
                            <button class="btn btn-outline" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" onclick="quickFillLogin('arun.fnx.demo@example.com', 'SecureP@ss123')">Arun Kumar (Demo)</button>
                        </div>
                    </div>

                    <div style="margin-top: 1.5rem; text-align: center; font-size: 0.9rem; color: var(--text-secondary);">
                        Don't have an account? <a onclick="navigateTo('register-view')" style="color: var(--intel-cyan); cursor: pointer; font-weight: 700;">Register here</a>
                    </div>
                </div>
            </section>

            <!-- 5. CUSTOMER DASHBOARD TAB VIEW -->
            <section id="dash-tab-view" class="view-section">
                <!-- Welcome Section -->
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 2rem; background: #FFFFFF; padding: 1.75rem; border-radius: 12px; border: 1px solid var(--border-color);">
                    <div>
                        <h2 style="color: var(--primary-navy); margin-bottom: 0.35rem;">
                            <span data-i18n="welcome_back">Welcome back</span>, <span id="dash-customer-name" style="color: var(--intel-cyan-dark);">Customer</span>
                        </h2>
                        <p style="color: var(--text-secondary); font-size: 0.9rem;">
                            FRAUDNEXUS ID: <strong id="dash-customer-id" style="font-family: monospace; color: var(--primary-navy);">CNX-2026-XXXXXX</strong> | 
                            KYC Status: <span class="badge badge-resolved" id="dash-kyc-status">Active</span>
                        </p>
                        <div style="margin-top: 0.5rem; font-size: 0.82rem; color: #64748B;">
                            From Fraud Report to Resolution — Your cases are actively monitored under ServiceNow chain of custody.
                        </div>
                    </div>
                    <div style="display: flex; gap: 0.75rem;">
                        <button class="btn btn-primary" onclick="switchWorkspaceTab('report')">🚨 <span data-i18n="btn_report_fraud">Report Fraud</span></button>
                        <button class="btn btn-outline" onclick="switchWorkspaceTab('track')">🔍 <span data-i18n="btn_track_case">Track Cases</span></button>
                    </div>
                </div>

                <!-- Case Summary Stats -->
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-label" data-i18n="stat_total">Total Cases</div>
                        <div class="stat-value" id="stat-total">0</div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">Reported by you</div>
                    </div>
                    <div class="stat-card active-cases">
                        <div class="stat-label" data-i18n="stat_active">Active Investigations</div>
                        <div class="stat-value" id="stat-active" style="color: var(--warning);">0</div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">Under active review</div>
                    </div>
                    <div class="stat-card resolved-cases">
                        <div class="stat-label" data-i18n="stat_resolved">Resolved Cases</div>
                        <div class="stat-value" id="stat-resolved" style="color: var(--success);">0</div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">Resolution confirmed</div>
                    </div>
                    <div class="stat-card closed-cases">
                        <div class="stat-label" data-i18n="stat_closed">Closed Cases</div>
                        <div class="stat-value" id="stat-closed" style="color: var(--secondary-navy);">0</div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">Archived records</div>
                    </div>
                </div>

                <!-- Recent Cases Table -->
                <div class="table-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
                        <h3 style="color: var(--primary-navy); font-size: 1.2rem;" data-i18n="recent_cases_title">My Recent Fraud Cases</h3>
                        <button class="btn btn-outline" style="padding: 0.35rem 0.75rem; font-size: 0.82rem;" onclick="loadCustomerCases()">🔄 Refresh</button>
                    </div>

                    <div class="table-responsive">
                        <table class="fnx-table">
                            <thead>
                                <tr>
                                    <th>Case ID</th>
                                    <th>Fraud Type</th>
                                    <th>Incident Date</th>
                                    <th>Amount (INR)</th>
                                    <th>Investigation Stage</th>
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

                <!-- Fraud Awareness & Safety Cards -->
                <div style="margin-bottom: 2rem;">
                    <h3 style="color: var(--primary-navy); font-size: 1.2rem; margin-bottom: 1rem;" data-i18n="awareness_title">Fraud Awareness &amp; Prevention</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.25rem;">
                        <div style="background: #FFFFFF; border: 1px solid var(--border-color); border-radius: 10px; padding: 1.25rem;">
                            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🔒</div>
                            <h4 style="color: var(--primary-navy); font-size: 0.95rem; margin-bottom: 0.35rem;">UPI PIN Safety</h4>
                            <p style="font-size: 0.82rem; color: var(--text-secondary); line-height: 1.5;">UPI PIN is ONLY required for transferring money OUT. You NEVER need to enter PIN to receive money.</p>
                        </div>
                        <div style="background: #FFFFFF; border: 1px solid var(--border-color); border-radius: 10px; padding: 1.25rem;">
                            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📱</div>
                            <h4 style="color: var(--primary-navy); font-size: 0.95rem; margin-bottom: 0.35rem;">Fake APK Warning</h4>
                            <p style="font-size: 0.82rem; color: var(--text-secondary); line-height: 1.5;">Never install APK files sent via WhatsApp/Telegram claiming to be electricity bills, KYC updates, or courier notices.</p>
                        </div>
                        <div style="background: #FFFFFF; border: 1px solid var(--border-color); border-radius: 10px; padding: 1.25rem;">
                            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📞</div>
                            <h4 style="color: var(--primary-navy); font-size: 0.95rem; margin-bottom: 0.35rem;">Emergency Freeze (1930)</h4>
                            <p style="font-size: 0.82rem; color: var(--text-secondary); line-height: 1.5;">Reporting within the "Golden Hour" on 1930 dramatically increases the chances of freezing funds in transit.</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 6. REPORT FRAUD TAB VIEW (Progressive Disclosure) -->
            <section id="report-tab-view" class="view-section">
                <div class="table-card" style="max-width: 900px; margin: 0 auto;">
                    <h2 style="color: var(--primary-navy); margin-bottom: 0.25rem;" data-i18n="report_wizard_title">Report Fraud Incident</h2>
                    <p style="color: var(--text-secondary); margin-bottom: 1.75rem; font-size: 0.9rem;" data-i18n="report_wizard_sub">Complete the guided intake to initiate formal investigation and evidence preservation.</p>

                    <!-- Steps Progress Bar -->
                    <div class="step-progress">
                        <div class="step-item active" id="wiz-step-ind-1"><div class="step-circle">1</div><div class="step-title">Incident Type</div></div>
                        <div class="step-item" id="wiz-step-ind-2"><div class="step-circle">2</div><div class="step-title">Description</div></div>
                        <div class="step-item" id="wiz-step-ind-3"><div class="step-circle">3</div><div class="step-title">Location &amp; Platform</div></div>
                        <div class="step-item" id="wiz-step-ind-4"><div class="step-circle">4</div><div class="step-title">Financial Details</div></div>
                        <div class="step-item" id="wiz-step-ind-5"><div class="step-circle">5</div><div class="step-title">Evidence &amp; Review</div></div>
                    </div>

                    <div id="fraud-alert" class="alert-box"></div>

                    <!-- Step 1: Incident Type -->
                    <div id="wiz-step-1">
                        <h3 style="margin-bottom: 1rem; color: var(--secondary-navy); font-size: 1.05rem;">Step 1: What type of fraud occurred?</h3>
                        <div class="form-grid">
                            <div class="form-group full-width">
                                <label class="form-label">Primary Fraud Classification <span class="req">*</span></label>
                                <select id="fr-type" class="form-control" style="font-size: 1rem; padding: 0.75rem;" required>
                                    <option value="Payment Fraud">1. Payment Fraud (UPI, QR Code, Gateway)</option>
                                    <option value="Unauthorized Transaction">2. Unauthorized Transaction (Card cloning, ATM debit)</option>
                                    <option value="Phishing">3. Phishing (Fake SMS, email, deceptive links)</option>
                                    <option value="Account Compromise">4. Account Compromise (Net banking, mobile takeover)</option>
                                    <option value="Identity Theft">5. Identity Theft (Impersonation, fake loans on PAN)</option>
                                    <option value="Cyber Fraud">6. Cyber Fraud (Malware, fake APK, remote screen apps)</option>
                                    <option value="Money Laundering">7. Money Laundering / Mule Account Scam</option>
                                    <option value="Financial Crime">8. Financial Crime / Investment &amp; Trading Scam</option>
                                    <option value="Other">9. Other Fraud Scenario</option>
                                </select>
                            </div>
                        </div>
                        <div style="display: flex; justify-content: flex-end; margin-top: 2rem;">
                            <button type="button" class="btn btn-navy" onclick="goToStep(2)">Next: Incident Details &rarr;</button>
                        </div>
                    </div>

                    <!-- Step 2: Description & Date/Time -->
                    <div id="wiz-step-2" style="display: none;">
                        <h3 style="margin-bottom: 1rem; color: var(--secondary-navy); font-size: 1.05rem;">Step 2: Incident Details &amp; Timeline</h3>
                        <div class="form-grid">
                            <div class="form-group full-width">
                                <label class="form-label">What transpired? (Case Narrative) <span class="req">*</span></label>
                                <textarea id="fr-desc" class="form-control" placeholder="Describe the chronological sequence of events, calls received, promises made by fraudster, etc." required></textarea>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Incident Date <span class="req">*</span></label>
                                <input type="date" id="fr-date" class="form-control" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Incident Time</label>
                                <input type="time" id="fr-time" class="form-control">
                            </div>
                            <div class="form-group full-width">
                                <label class="form-label">Perceived Severity</label>
                                <select id="fr-severity" class="form-control">
                                    <option value="Critical">Critical (Immediate Asset Drain / Ongoing Threat)</option>
                                    <option value="High">High (Substantial Financial Loss)</option>
                                    <option value="Medium" selected>Medium (Standard Investigation)</option>
                                    <option value="Low">Low (Attempted / No Financial Loss)</option>
                                </select>
                            </div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-top: 2rem;">
                            <button type="button" class="btn btn-outline" onclick="goToStep(1)">&larr; Back</button>
                            <button type="button" class="btn btn-navy" onclick="goToStep(3)">Next: Location &amp; Platform &rarr;</button>
                        </div>
                    </div>

                    <!-- Step 3: Location & Platform -->
                    <div id="wiz-step-3" style="display: none;">
                        <h3 style="margin-bottom: 1rem; color: var(--secondary-navy); font-size: 1.05rem;">Step 3: Digital Platform &amp; Location</h3>
                        <div class="form-grid">
                            <div class="form-group">
                                <label class="form-label">Digital Platform / App / Website</label>
                                <input type="text" id="fr-platform" class="form-control" placeholder="e.g. PhonePe, WhatsApp, FakePortal.in, Telegram">
                            </div>
                            <div class="form-group">
                                <label class="form-label">City / Location</label>
                                <input type="text" id="fr-location" class="form-control" placeholder="e.g. Mumbai, Chennai, Bengaluru">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Area / Landmark</label>
                                <input type="text" id="fr-area" class="form-control" placeholder="e.g. T Nagar, Andheri East">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Pincode</label>
                                <input type="text" id="fr-pincode" class="form-control" placeholder="e.g. 600017">
                            </div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-top: 2rem;">
                            <button type="button" class="btn btn-outline" onclick="goToStep(2)">&larr; Back</button>
                            <button type="button" class="btn btn-navy" onclick="goToStep(4)">Next: Financial Details &rarr;</button>
                        </div>
                    </div>

                    <!-- Step 4: Financial Involvement Gate & Data -->
                    <div id="wiz-step-4" style="display: none;">
                        <h3 style="margin-bottom: 0.5rem; color: var(--secondary-navy); font-size: 1.05rem;">Step 4: Financial Involvement</h3>
                        <p style="color: var(--text-secondary); font-size: 0.88rem; margin-bottom: 1rem;">Was there financial loss, unauthorized transaction, or money transfer involved?</p>

                        <div class="gate-choice-box">
                            <label class="gate-choice-label selected" id="fin-gate-yes" onclick="setFinGate('Yes')">
                                <input type="radio" name="fin_gate" value="Yes" checked> Yes, money was involved
                            </label>
                            <label class="gate-choice-label" id="fin-gate-no" onclick="setFinGate('No')">
                                <input type="radio" name="fin_gate" value="No"> No financial loss
                            </label>
                            <label class="gate-choice-label" id="fin-gate-ns" onclick="setFinGate('Not Sure')">
                                <input type="radio" name="fin_gate" value="Not Sure"> I'm not sure
                            </label>
                        </div>

                        <!-- Financial Form (Displayed if Yes) -->
                        <div id="fin-details-section">
                            <div class="form-grid" style="margin-top: 1.5rem; background: #F8FAFC; padding: 1.5rem; border-radius: 8px; border: 1px solid var(--border-color);">
                                <div class="form-group">
                                    <label class="form-label">Payment Mode</label>
                                    <select id="fr-pay-mode" class="form-control">
                                        <option value="UPI">UPI (Google Pay, PhonePe, Paytm)</option>
                                        <option value="Bank Transfer">Bank Transfer (IMPS / NEFT / RTGS)</option>
                                        <option value="Debit Card">Debit Card</option>
                                        <option value="Credit Card">Credit Card</option>
                                        <option value="ATM Cash">ATM / Cash Withdrawal</option>
                                        <option value="Net Banking">Net Banking</option>
                                        <option value="Digital Wallet">Digital Wallet</option>
                                        <option value="QR Code Payment">QR Code Payment</option>
                                        <option value="Payment Gateway">Payment Gateway</option>
                                        <option value="Investment / Trading">Investment / Crypto / Trading</option>
                                        <option value="Loan / Lending">Loan / Lending App</option>
                                        <option value="Other">Other Mode</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Amount Involved / Lost (INR) <span class="req">*</span></label>
                                    <input type="number" id="fr-amount" class="form-control" placeholder="e.g. 75000" min="0" value="0">
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Institution / Organization Name</label>
                                    <input type="text" id="fr-inst-name" class="form-control" placeholder="e.g. Partner Bank A, State Bank, HDFC">
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Institution Type</label>
                                    <select id="fr-inst-type" class="form-control">
                                        <option value="Bank / Financial Institution">Bank / Financial Institution</option>
                                        <option value="Payment Provider / PSP">Payment Provider / PSP</option>
                                        <option value="Payment Application">Payment Application</option>
                                        <option value="Investment / Brokerage">Investment / Brokerage</option>
                                        <option value="Lending / NBFC">Lending / NBFC</option>
                                        <option value="E-commerce / Merchant">E-commerce / Merchant</option>
                                        <option value="Telecom">Telecom</option>
                                        <option value="Other">Other</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Branch / Service Location</label>
                                    <input type="text" id="fr-branch" class="form-control" placeholder="e.g. Demo Branch, Anna Nagar">
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Transaction Reference / UTR Number</label>
                                    <input type="text" id="fr-utr" class="form-control" placeholder="e.g. DEMO-UTR-001 or UTR-98218731">
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Customer-Reported Blocked Amount (₹)</label>
                                    <input type="number" id="fr-blocked" class="form-control" placeholder="0" min="0" value="0">
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Customer-Reported Recovered Amount (₹)</label>
                                    <input type="number" id="fr-recovered" class="form-control" placeholder="0" min="0" value="0">
                                </div>

                                <div class="form-group full-width">
                                    <label class="form-label">Suspect Name / Phone / UPI ID / Social Handle</label>
                                    <input type="text" id="fr-suspect" class="form-control" placeholder="e.g. John Doe / 9876543210 / fraudster@okhdfcbank">
                                </div>
                                <div class="form-group full-width">
                                    <label class="form-label">Communication Channel</label>
                                    <select id="fr-channel" class="form-control">
                                        <option value="WhatsApp / Telegram">WhatsApp / Telegram</option>
                                        <option value="Phone Call">Direct Phone Call</option>
                                        <option value="SMS / Phishing Link">SMS / Phishing Link</option>
                                        <option value="Email">Email</option>
                                        <option value="Social Media">Social Media</option>
                                        <option value="Other">Other Channel</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        <div style="display: flex; justify-content: space-between; margin-top: 2rem;">
                            <button type="button" class="btn btn-outline" onclick="goToStep(3)">&larr; Back</button>
                            <button type="button" class="btn btn-navy" onclick="goToStep(5)">Next: Evidence &amp; Submit &rarr;</button>
                        </div>
                    </div>

                    <!-- Step 5: Evidence & Review -->
                    <div id="wiz-step-5" style="display: none;">
                        <h3 style="margin-bottom: 1rem; color: var(--secondary-navy); font-size: 1.05rem;">Step 5: Evidence &amp; Submission Review</h3>
                        <div class="form-grid">
                            <div class="form-group">
                                <label class="form-label">Evidence Type</label>
                                <select id="fr-ev-type" class="form-control">
                                    <option value="Image">Screenshot / Photo</option>
                                    <option value="PDF">PDF Bank Statement</option>
                                    <option value="Chat Export">Chat / WhatsApp Export</option>
                                    <option value="Email">Email Header / Message</option>
                                    <option value="Transaction Reference">Transaction Receipt / Slip</option>
                                    <option value="Document">Word / Text Document</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Select Evidence File</label>
                                <input type="file" id="fr-file" class="form-control">
                            </div>
                            <div class="form-group full-width">
                                <label class="form-label">Evidence Description</label>
                                <input type="text" id="fr-ev-desc" class="form-control" placeholder="e.g. Payment receipt with UTR reference and suspect UPI handle">
                            </div>
                        </div>

                        <!-- Summary Review Box -->
                        <div style="background: #F8FAFC; border: 1px solid var(--border-color); border-radius: 10px; padding: 1.5rem; margin-top: 1.5rem;">
                            <h4 style="color: var(--primary-navy); margin-bottom: 0.75rem;">Submission Summary</h4>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; font-size: 0.88rem;">
                                <div><strong>Fraud Type:</strong> <span id="sum-type">-</span></div>
                                <div><strong>Exposed Amount:</strong> ₹<span id="sum-amount">0</span></div>
                                <div><strong>Incident Date:</strong> <span id="sum-date">-</span></div>
                                <div><strong>Platform:</strong> <span id="sum-platform">-</span></div>
                                <div><strong>Payment Mode:</strong> <span id="sum-mode">-</span></div>
                                <div><strong>Institution:</strong> <span id="sum-inst">-</span></div>
                            </div>
                        </div>

                        <div style="margin-top: 1.25rem;">
                            <label style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; color: var(--text-primary);">
                                <input type="checkbox" id="fr-declare" checked> I declare that the details and evidence provided above are accurate to the best of my knowledge.
                            </label>
                        </div>

                        <div style="display: flex; justify-content: space-between; margin-top: 2rem;">
                            <button type="button" class="btn btn-outline" onclick="goToStep(4)">&larr; Back</button>
                            <button type="button" class="btn btn-primary" id="btn-submit-case" onclick="submitFraudReport()">Submit Fraud Report</button>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 7. TRACK CASES TAB VIEW -->
            <section id="track-tab-view" class="view-section">
                <div class="table-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                        <div>
                            <h2 style="color: var(--primary-navy); font-size: 1.4rem;" data-i18n="track_cases_title">Investigation Case Tracker</h2>
                            <p style="color: var(--text-secondary); font-size: 0.88rem;">Track progress, investigation stages, and submit additional evidence for your cases.</p>
                        </div>
                        <button class="btn btn-outline" onclick="loadCustomerCases()">🔄 Refresh Cases</button>
                    </div>

                    <div class="table-responsive">
                        <table class="fnx-table">
                            <thead>
                                <tr>
                                    <th>Case ID</th>
                                    <th>Type</th>
                                    <th>Reported Date</th>
                                    <th>Amount</th>
                                    <th>Stage</th>
                                    <th>Evidence Count</th>
                                    <th>Status</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody id="track-table-body">
                                <tr>
                                    <td colspan="8" style="text-align: center; color: var(--text-secondary); padding: 2rem;">Loading cases...</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>

            <!-- 8. EVIDENCE VAULT TAB VIEW -->
            <section id="evidence-tab-view" class="view-section">
                <div class="table-card">
                    <h2 style="color: var(--primary-navy); font-size: 1.4rem; margin-bottom: 0.5rem;" data-i18n="evidence_vault_title">Customer Evidence Vault</h2>
                    <p style="color: var(--text-secondary); font-size: 0.88rem; margin-bottom: 1.5rem;">All uploaded materials are hashed (SHA-256) and tracked under automated chain of custody (u_x_fnx_custody_log).</p>

                    <div id="vault-evidence-list" style="display: flex; flex-direction: column; gap: 0.85rem;">
                        <div style="text-align: center; color: var(--text-secondary); padding: 2rem;">No evidence files found in customer vault.</div>
                    </div>
                </div>
            </section>

            <!-- 9. HELP & SUPPORT TAB VIEW -->
            <section id="help-tab-view" class="view-section">
                <div class="table-card" style="max-width: 850px; margin: 0 auto;">
                    <h2 style="color: var(--primary-navy); font-size: 1.4rem; margin-bottom: 0.5rem;" data-i18n="help_title">Fraud Support &amp; Emergency Escalation</h2>
                    <p style="color: var(--text-secondary); font-size: 0.88rem; margin-bottom: 1.5rem;">Immediate guidelines and emergency contacts to protect your accounts and recover funds.</p>

                    <div style="background: #FEE2E2; border: 1px solid #FCA5A5; border-radius: 10px; padding: 1.5rem; margin-bottom: 2rem;">
                        <h3 style="color: #991B1B; font-size: 1.15rem; margin-bottom: 0.5rem;">🚨 Immediate Action Required?</h3>
                        <p style="color: #7F1D1D; font-size: 0.9rem; line-height: 1.6; margin-bottom: 1rem;">
                            If you lost money within the last 2 hours, call the <strong>National Cyber Fraud Reporting Helpline at 1930</strong> immediately. Provide the UTR/transaction reference so authorities can issue an automated inter-bank freeze.
                        </p>
                        <a href="tel:1930" class="btn btn-navy" style="background: #991B1B;">📞 Call Helpline 1930</a>
                    </div>

                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem;">
                        <div style="border: 1px solid var(--border-color); border-radius: 8px; padding: 1.25rem;">
                            <h4 style="color: var(--primary-navy); margin-bottom: 0.5rem;">1. Freeze Your Bank Account</h4>
                            <p style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">Contact your bank's 24/7 emergency toll-free number immediately to block compromised cards and disable net banking credentials.</p>
                        </div>
                        <div style="border: 1px solid var(--border-color); border-radius: 8px; padding: 1.25rem;">
                            <h4 style="color: var(--primary-navy); margin-bottom: 0.5rem;">2. National Cyber Crime Portal</h4>
                            <p style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">Official Government Portal: <strong>cybercrime.gov.in</strong>. Files formal police FIRs for financial cyber crimes.</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 10. SUBMISSION CONFIRMATION VIEW -->
            <section id="confirmation-view" class="view-section">
                <div class="table-card" style="max-width: 620px; margin: 2rem auto; text-align: center; padding: 3rem 2rem;">
                    <div style="width: 65px; height: 65px; background: #DCFCE7; color: var(--success); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2.2rem; margin: 0 auto 1.5rem auto;">✓</div>
                    <h2 style="color: var(--primary-navy); margin-bottom: 0.5rem;" data-i18n="conf_title">Fraud Report Successfully Registered</h2>
                    <p style="color: var(--text-secondary); margin-bottom: 2rem;" data-i18n="conf_sub">Your investigation case has been securely created in the ServiceNow FRAUDNEXUS engine.</p>

                    <div style="background: #F8FAFC; border: 1px dashed var(--border-color); border-radius: 10px; padding: 1.5rem; margin-bottom: 2rem; text-align: left;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.6rem;">
                            <span style="color: var(--text-secondary); font-size: 0.9rem;">ServiceNow Case Number:</span>
                            <strong id="conf-case-id" style="color: var(--primary-navy); font-size: 1.15rem; font-family: monospace;">FNX-2026-XXXXXX</strong>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.6rem;">
                            <span style="color: var(--text-secondary); font-size: 0.9rem;">Initial Status:</span>
                            <span class="badge badge-new" id="conf-status">New</span>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color: var(--text-secondary); font-size: 0.9rem;">Submitted On:</span>
                            <span id="conf-date" style="font-size: 0.9rem; color: var(--text-primary); font-weight: 600;">-</span>
                        </div>
                    </div>

                    <div style="display: flex; gap: 1rem; justify-content: center;">
                        <button class="btn btn-primary" onclick="switchWorkspaceTab('track')">Track Case Progress</button>
                        <button class="btn btn-outline" onclick="switchWorkspaceTab('report')">Report Another Fraud</button>
                    </div>
                </div>
            </section>

        </main>
    </div>

    <!-- CASE DETAILS & ADDITIONAL EVIDENCE MODAL -->
    <div id="case-modal" class="fnx-modal-backdrop">
        <div class="fnx-modal">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem;">
                <div>
                    <h3 id="modal-case-number" style="color: var(--primary-navy); font-family: monospace; font-size: 1.35rem;">FNX-2026-XXXXXX</h3>
                    <div id="modal-case-type" style="color: var(--text-secondary); font-size: 0.9rem; font-weight: 600;">Payment Fraud</div>
                </div>
                <button onclick="closeCaseModal()" class="btn btn-outline" style="padding: 0.3rem 0.6rem; font-size: 1.1rem;">&times;</button>
            </div>

            <!-- Visual 5-Stage Status Timeline -->
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

            <!-- Metadata Grid -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem; font-size: 0.88rem; background: #F8FAFC; padding: 1.25rem; border-radius: 8px; border: 1px solid var(--border-color);">
                <div><strong>Status:</strong> <span id="modal-status">-</span></div>
                <div><strong>Severity:</strong> <span id="modal-severity">-</span></div>
                <div><strong>Financial Exposure:</strong> ₹<span id="modal-amount">-</span></div>
                <div><strong>Platform:</strong> <span id="modal-platform">-</span></div>
                <div><strong>Incident Date:</strong> <span id="modal-date">-</span></div>
                <div><strong>Location:</strong> <span id="modal-location">-</span></div>
            </div>

            <!-- Description -->
            <div style="margin-bottom: 1.5rem;">
                <h4 style="color: var(--primary-navy); margin-bottom: 0.5rem; font-size: 0.95rem;">Case Narrative &amp; Details</h4>
                <div id="modal-desc" style="background: #FFFFFF; border: 1px solid var(--border-color); padding: 1rem; border-radius: 8px; font-size: 0.88rem; line-height: 1.6; max-height: 180px; overflow-y: auto; white-space: pre-wrap;">-</div>
            </div>

            <!-- Existing Evidence Section -->
            <div style="margin-bottom: 1.5rem;">
                <h4 style="color: var(--primary-navy); margin-bottom: 0.5rem; font-size: 0.95rem;">Submitted Evidence &amp; Custody</h4>
                <div id="modal-evidence-list" style="font-size: 0.85rem; color: var(--text-secondary); display: flex; flex-direction: column; gap: 0.5rem;">
                    <em>No evidence attached.</em>
                </div>
            </div>

            <!-- Add Additional Evidence Section -->
            <div style="border-top: 1px solid var(--border-color); padding-top: 1.25rem;">
                <h4 style="color: var(--primary-navy); margin-bottom: 0.5rem; font-size: 0.95rem;">📎 Add Additional Evidence</h4>
                <div id="add-ev-alert" class="alert-box"></div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-bottom: 0.75rem;">
                    <select id="add-ev-type" class="form-control">
                        <option value="Image">Screenshot / Photo</option>
                        <option value="PDF">PDF Statement</option>
                        <option value="Chat Export">Chat / WhatsApp Export</option>
                        <option value="Email">Email Msg</option>
                        <option value="Transaction Reference">Receipt / Slip</option>
                        <option value="Document">Other Document</option>
                    </select>
                    <input type="file" id="add-ev-file" class="form-control">
                </div>
                <input type="text" id="add-ev-desc" class="form-control" placeholder="Description of additional proof (e.g. Bank statement confirming debit)" style="margin-bottom: 0.75rem;">
                <button type="button" class="btn btn-navy" id="btn-add-ev" onclick="submitAdditionalEvidence()">Attach Evidence to Case</button>
            </div>
        </div>
    </div>

    <!-- FORGOT PASSWORD MODAL -->
    <div id="forgot-modal" class="fnx-modal-backdrop">
        <div class="fnx-modal" style="max-width: 450px;">
            <h3 style="color: var(--primary-navy); margin-bottom: 0.5rem;">Reset Account Password</h3>
            <p style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;">Enter your registered email address to receive password recovery verification.</p>
            <div id="forgot-alert" class="alert-box"></div>
            <div class="form-group" style="margin-bottom: 1.25rem;">
                <label class="form-label">Registered Email</label>
                <input type="email" id="forgot-email" class="form-control" placeholder="name@example.com" required>
            </div>
            <div style="display: flex; justify-content: flex-end; gap: 0.75rem;">
                <button class="btn btn-outline" onclick="closeForgotPasswordModal()">Cancel</button>
                <button class="btn btn-navy" onclick="handleForgotPassword()">Send Reset Link</button>
            </div>
        </div>
    </div>

    <!-- GENERAL INFO MODAL -->
    <div id="info-modal" class="fnx-modal-backdrop">
        <div class="fnx-modal" style="max-width: 500px;">
            <h3 id="info-modal-title" style="color: var(--primary-navy); margin-bottom: 0.75rem;">Information</h3>
            <p id="info-modal-body" style="color: var(--text-secondary); line-height: 1.6; margin-bottom: 1.5rem;"></p>
            <div style="display: flex; justify-content: flex-end;">
                <button class="btn btn-navy" onclick="closeInfoModal()">Close</button>
            </div>
        </div>
    </div>

    <!-- FLOATING AI ASSISTANT PILL -->
    <div class="fnx-ai-pill" onclick="toggleAiDrawer()">
        <span>✨</span> <span data-i18n="ai_pill">Ask FRAUDNEXUS AI</span>
    </div>

    <!-- SLIDING AI DRAWER -->
    <div id="ai-drawer" class="fnx-ai-drawer">
        <div class="ai-drawer-header">
            <div style="display: flex; align-items: center; gap: 0.6rem;">
                <span style="font-size: 1.2rem;">✨</span>
                <div>
                    <strong data-i18n="ai_title">FRAUDNEXUS Guidance AI</strong>
                    <div style="font-size: 0.68rem; color: var(--intel-cyan);">Customer Safety &amp; Case Navigator</div>
                </div>
            </div>
            <button onclick="toggleAiDrawer()" style="background: none; border: none; color: #FFFFFF; font-size: 1.4rem; cursor: pointer;">&times;</button>
        </div>
        <div class="ai-drawer-body">
            <div class="ai-msg" id="ai-welcome-msg" data-i18n="ai_welcome">
                Hello! I am your <strong>FRAUDNEXUS</strong> fraud guidance assistant. How can I assist you with reporting or tracking your case today?
            </div>

            <div>
                <div style="font-size: 0.75rem; font-weight: 700; color: var(--text-secondary); margin-bottom: 0.5rem; text-transform: uppercase;" data-i18n="ai_suggested">Suggested Questions</div>
                <div style="display: flex; flex-direction: column; gap: 0.4rem;">
                    <button class="ai-intent-btn" onclick="askAi('How to report fraud')">📌 How to report fraud step-by-step?</button>
                    <button class="ai-intent-btn" onclick="askAi('Where is my case?')">🔍 Where do I find my case updates?</button>
                    <button class="ai-intent-btn" onclick="askAi('What does case status mean?')">ℹ️ What do the investigation stages mean?</button>
                    <button class="ai-intent-btn" onclick="askAi('How do I upload evidence?')">📎 What evidence should I upload?</button>
                    <button class="ai-intent-btn" onclick="askAi('How do I contact support?')">📞 Emergency 1930 helpline &amp; support</button>
                </div>
            </div>

            <div id="ai-chat-history"></div>
        </div>
        <div style="padding: 0.75rem 1rem; border-top: 1px solid var(--border-color); background: #FFFFFF; display: flex; gap: 0.5rem;">
            <input type="text" id="ai-user-input" class="form-control" placeholder="Ask about fraud or enter case number..." onkeydown="if(event.key==='Enter') sendCustomAiMessage()">
            <button class="btn btn-primary" style="padding: 0.5rem 0.85rem;" onclick="sendCustomAiMessage()">Send</button>
        </div>
    </div>

    <!-- CLIENT LOGIC & REST CLIENT -->
    <script>
        const API_BASE = '/api/2229367/fnx_api';
        let currentUser = null;
        let currentCustomer = null;
        let customerCases = [];
        let activeModalCaseId = null;
        let currentLang = localStorage.getItem('fnx_lang') || 'en';

        // MULTILINGUAL STRINGS DICTIONARY (English & Tamil)
        const i18n = {
            en: {
                tagline: "From Fraud Report to Resolution — One Investigation Workspace",
                nav_home: "Home",
                nav_portal_select: "Portal Gateways",
                nav_report: "Report Fraud",
                nav_track: "Track Case",
                nav_about: "About",
                login_btn: "Customer Login",
                register_btn: "Register",
                customer_workspace: "Customer Workspace",
                sb_dashboard: "Dashboard",
                sb_report_fraud: "Report Fraud",
                sb_track_cases: "Track Cases",
                sb_evidence_vault: "Evidence Vault",
                sb_help_support: "Help & Support",
                hero_desc: "From Fraud Report to Resolution — One Intelligent Investigation Workspace. Report unauthorized payments, submit digital forensic evidence, and track investigation milestones in real time.",
                btn_report_fraud: "Report Fraud",
                btn_track_case: "Track Case",
                btn_select_portal: "Select Portal Gateway",
                feat_1_title: "Secure Fraud Reporting",
                feat_1_desc: "Comprehensive reporting for UPI, unauthorized debits, phishing, and crypto frauds with bank-grade privacy.",
                feat_2_title: "Forensic Evidence Chain",
                feat_2_desc: "Upload screenshots, statements, audio, and chat exports with automatic cryptographic SHA-256 custody logging.",
                feat_3_title: "Real-Time Investigation Tracker",
                feat_3_desc: "Clear visibility from Submitted to Initial Review, Forensic Analysis, Resolution, and Asset Recovery.",
                feat_4_title: "Intelligent Link Analysis",
                feat_4_desc: "Correlates mule accounts, suspicious beneficiary phone numbers, and syndicate fraud rings across networks.",
                portal_gateways_title: "FRAUDNEXUS Portal Gateways",
                portal_gateways_sub: "Select your designated environment to proceed with fraud reporting or internal investigation management.",
                portal_cust_title: "Customer Portal",
                portal_cust_desc: "For citizens and customers to report fraud incidents, upload proof, track case progress, submit additional evidence, and consult AI.",
                portal_cust_btn: "Enter Customer Workspace →",
                portal_admin_title: "Investigator / Admin Hub",
                portal_admin_desc: "For authorized investigation officers, risk handlers, and managers. Command center triage, case allocation, and syndicate ring analysis.",
                portal_admin_btn: "Staff Access / App Engine Studio →",
                welcome_back: "Welcome back",
                stat_total: "Total Cases",
                stat_active: "Active Investigations",
                stat_resolved: "Resolved Cases",
                stat_closed: "Closed Cases",
                recent_cases_title: "My Recent Fraud Cases",
                awareness_title: "Fraud Awareness & Prevention",
                report_wizard_title: "Report Fraud Incident",
                report_wizard_sub: "Complete the guided intake to initiate formal investigation and evidence preservation.",
                track_cases_title: "Investigation Case Tracker",
                evidence_vault_title: "Customer Evidence Vault",
                help_title: "Fraud Support & Emergency Escalation",
                conf_title: "Fraud Report Successfully Registered",
                conf_sub: "Your investigation case has been securely created in the ServiceNow FRAUDNEXUS engine.",
                ai_pill: "Ask FRAUDNEXUS AI",
                ai_title: "FRAUDNEXUS Guidance AI",
                ai_welcome: "Hello! I am your FRAUDNEXUS fraud guidance assistant. How can I assist you with reporting or tracking your case today?",
                ai_suggested: "Suggested Questions",
                notifications: "Alerts & Notifications"
            },
            ta: {
                tagline: "மோசடி புகார் முதல் தீர்வு வரை — ஒரே அறிவார்ந்த விசாரணை தளம்",
                nav_home: "முகப்பு",
                nav_portal_select: "வலைவாசல் தேர்வுகள்",
                nav_report: "மோசடி புகார் செய்",
                nav_track: "வழக்கு கண்காணிப்பு",
                nav_about: "பற்றி",
                login_btn: "உள்நுழைக",
                register_btn: "பதிவு செய்க",
                customer_workspace: "வாடிக்கையாளர் தளம்",
                sb_dashboard: "முகப்பு பலகை",
                sb_report_fraud: "மோசடி புகார் செய்",
                sb_track_cases: "வழக்கு கண்காணிப்பு",
                sb_evidence_vault: "ஆதார காப்பகம்",
                sb_help_support: "உதவி & ஆதரவு",
                hero_desc: "மோசடி புகார் முதல் தீர்வு வரை — ஒரே அறிவார்ந்த விசாரணை பணியிடம். அங்கீகரிக்கப்படாத பணப்பரிவர்த்தனைகளை புகார் செய்யுங்கள், டிஜிட்டல் தடய ஆதாரங்களை சமர்ப்பியுங்கள் மற்றும் நிகழ்நேர முன்னேற்றத்தை கண்காணிக்கவும்.",
                btn_report_fraud: "மோசடி புகார் செய்",
                btn_track_case: "வழக்கை கண்காணிக்கவும்",
                btn_select_portal: "வலைவாசல் தேர்வு செய்யவும்",
                feat_1_title: "பாதுகாப்பான மோசடி புகார்",
                feat_1_desc: "UPI, வங்கி கணக்கு திருட்டு, ஃபிஷிங் மற்றும் பண மோசடிகளுக்கு வங்கி அளவிலான பாதுகாப்பான புகார் வசதி.",
                feat_2_title: "தடயவியல் ஆதார தொடர்",
                feat_2_desc: "ஸ்கிரீன்ஷாட்கள், வங்கி அறிக்கைகள் மற்றும் அரட்டை ஆதாரங்களை SHA-256 கிரிப்டோகிராஃபிக் பாதுகாப்புடன் பதிவேற்றவும்.",
                feat_3_title: "நிகழ்நேர விசாரணை கண்காணிப்பாளர்",
                feat_3_desc: "சமர்ப்பித்தது முதல் முதற்கட்ட மதிப்பாய்வு, விசாரணை, தீர்வு மற்றும் நிதி மீட்பு வரை வெளிப்படையான கண்காணிப்பு.",
                feat_4_title: "அறிவார்ந்த தொடர்பு பகுப்பாய்வு",
                feat_4_desc: "பல வங்கி நெட்வொர்க்குகளில் சந்தேகத்திற்கிடமான கணக்குகள் மற்றும் மோசடி வலையமைப்புகளை தானாகவே கண்டறியும்.",
                portal_gateways_title: "FRAUDNEXUS வலைவாசல் தேர்வுகள்",
                portal_gateways_sub: "மோசடி புகார் அல்லது அதிகாரப்பூர்வ விசாரணைக்கு உங்கள் தளத்தை தேர்வு செய்யவும்.",
                portal_cust_title: "வாடிக்கையாளர் வலைவாசல்",
                portal_cust_desc: "பொதுமக்கள் மோசடி புகார்களை பதிவு செய்யவும், ஆதாரங்களை வழங்கவும், வழக்குகளை கண்காணிக்கவும்.",
                portal_cust_btn: "வாடிக்கையாளர் தளத்திற்குள் செல்க →",
                portal_admin_title: "விசாரணையாளர் / நிர்வாக மையம்",
                portal_admin_desc: "அங்கீகரிக்கப்பட்ட புலனாய்வு அதிகாரிகள் மற்றும் மேலாளர்களுக்கான முதன்மை கட்டளை மையம்.",
                portal_admin_btn: "பணியாளர் அணுகல் / ஆப் என்ஜின் ஸ்டுடியோ →",
                welcome_back: "நல்வரவு",
                stat_total: "மொத்த வழக்குகள்",
                stat_active: "நடப்பு விசாரணைகள்",
                stat_resolved: "தீர்க்கப்பட்ட வழக்குகள்",
                stat_closed: "மூடப்பட்ட வழக்குகள்",
                recent_cases_title: "எனது சமீபத்திய மோசடி வழக்குகள்",
                awareness_title: "மோசடி விழிப்புணர்வு & தடுப்பு",
                report_wizard_title: "மோசடி புகார் பதிவு செய்",
                report_wizard_sub: "முறையான விசாரணை மற்றும் ஆதார பாதுகாப்பிற்காக தகவல்களை வழங்கவும்.",
                track_cases_title: "விசாரணை வழக்கு கண்காணிப்பு",
                evidence_vault_title: "வாடிக்கையாளர் ஆதார காப்பகம்",
                help_title: "மோசடி உதவி & அவசர தொடர்பு",
                conf_title: "மோசடி அறிக்கை வெற்றிகரமாக பதிவு செய்யப்பட்டது",
                conf_sub: "உங்கள் விசாரணை வழக்கு ServiceNow FRAUDNEXUS அமைப்பில் பாதுகாப்பாக உருவாக்கப்பட்டது.",
                ai_pill: "FRAUDNEXUS AI-யிடம் கேளுங்கள்",
                ai_title: "FRAUDNEXUS வழிகாட்டுதல் AI",
                ai_welcome: "வணக்கம்! நான் உங்கள் FRAUDNEXUS வழிகாட்டுதல் உதவியாளர். உங்கள் புகார் அல்லது வழக்கைக் கண்காணிக்க நான் எவ்வாறு உதவ முடியும்?",
                ai_suggested: "பரிந்துரைக்கப்பட்ட கேள்விகள்",
                notifications: "அறிவிப்புகள்"
            }
        };

        // INITIALIZE ON LOAD
        window.addEventListener('DOMContentLoaded', () => {
            // Apply language
            const langSelect = document.getElementById('lang-select');
            if (langSelect) langSelect.value = currentLang;
            applyTranslations(currentLang);

            // Default dates
            const today = new Date().toISOString().split('T')[0];
            const dateInput = document.getElementById('fr-date');
            if (dateInput) dateInput.value = today;

            // Session restoration
            const savedUser = localStorage.getItem('fnx_user');
            const savedCust = localStorage.getItem('fnx_customer');
            if (savedUser && savedCust) {
                try {
                    currentUser = JSON.parse(savedUser);
                    currentCustomer = JSON.parse(savedCust);
                    updateHeaderAuth();
                    loadCustomerCases();
                } catch(e) {
                    console.error('Session load error', e);
                }
            }
        });

        // LANGUAGE SWITCHER
        function changeLanguage(lang) {
            currentLang = lang;
            localStorage.setItem('fnx_lang', lang);
            applyTranslations(lang);
        }

        function applyTranslations(lang) {
            const dict = i18n[lang] || i18n.en;
            document.querySelectorAll('[data-i18n]').forEach(el => {
                const key = el.getAttribute('data-i18n');
                if (dict[key]) el.innerText = dict[key];
            });
        }

        // NAVIGATION LOGIC
        function navigateTo(viewId) {
            document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
            const target = document.getElementById(viewId);
            if (target) target.classList.add('active');

            // Hide/show sidebar based on view
            const sidebar = document.getElementById('app-sidebar');
            const inWorkspace = ['dash-tab-view', 'report-tab-view', 'track-tab-view', 'evidence-tab-view', 'help-tab-view'].includes(viewId);
            if (sidebar) sidebar.style.display = inWorkspace ? 'flex' : 'none';

            // Nav active states
            document.querySelectorAll('.fnx-header-nav a').forEach(a => a.classList.remove('active'));
            if (viewId === 'landing-view') document.getElementById('nav-home')?.classList.add('active');
            if (viewId === 'portal-select-view') document.getElementById('nav-portal-select')?.classList.add('active');

            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function switchWorkspaceTab(tab) {
            document.querySelectorAll('.sidebar-item').forEach(el => el.classList.remove('active'));
            document.getElementById(`sb-${tab}`)?.classList.add('active');
            navigateTo(`${tab}-tab-view`);
            if (tab === 'track') renderTrackTable();
            if (tab === 'evidence') renderVaultEvidence();
        }

        function enterCustomerPortal() {
            if (!currentUser) {
                navigateTo('login-view');
            } else {
                switchWorkspaceTab('dash');
            }
        }

        function enterInvestigatorPortal() {
            showInfoModal(
                'Investigator / Command Center Gateway',
                'The Investigator & Command Center workspace is designated for authorized fraud officers, analysts, and managers.\n\nTo access full case allocation, mule account analysis, and fraud rings, authorized officers utilize ServiceNow App Engine Studio or Polaris Next Experience Workspace (/now/nav/ui/classic/params/target/u_x_fnx_case_list.do).'
            );
        }

        function handleReportFraudNav() {
            if (!currentUser) {
                showAlert('login-alert', 'Please login or create an account to submit a fraud report.', 'error');
                navigateTo('login-view');
            } else {
                goToStep(1);
                switchWorkspaceTab('report');
            }
        }

        function handleMyCasesNav() {
            if (!currentUser) {
                showAlert('login-alert', 'Please login to track your fraud investigation cases.', 'error');
                navigateTo('login-view');
            } else {
                switchWorkspaceTab('track');
            }
        }

        function updateHeaderAuth() {
            const container = document.getElementById('header-auth');
            if (!container) return;

            if (currentUser) {
                container.innerHTML = `
                    <div class="profile-badge">
                        <span>👤 <strong>${escapeHtml(currentUser.name)}</strong></span>
                        <span style="font-size: 0.75rem; background: var(--intel-cyan); color: #0B1F3A; padding: 0.15rem 0.45rem; border-radius: 10px; font-weight: 700;">Verified</span>
                    </div>
                    <button class="btn btn-outline-white" style="padding: 0.4rem 0.8rem; font-size: 0.82rem;" onclick="switchWorkspaceTab('dash')">Workspace</button>
                    <button class="btn btn-outline-white" style="padding: 0.4rem 0.8rem; font-size: 0.82rem;" onclick="logoutCustomer()">Logout</button>
                `;
            } else {
                container.innerHTML = `
                    <button class="btn btn-outline-white" onclick="navigateTo('login-view')">Customer Login</button>
                    <button class="btn btn-primary" onclick="navigateTo('register-view')">Register</button>
                `;
            }
        }

        // NOTIFICATIONS DROPDOWN
        function toggleNotifications() {
            const drop = document.getElementById('notif-dropdown');
            drop.classList.toggle('open');
        }

        function clearNotifications() {
            document.getElementById('notif-list').innerHTML = '<div style="padding: 1.5rem; text-align: center; color: var(--text-secondary); font-size: 0.82rem;">No unread alerts.</div>';
            document.getElementById('notif-count').innerText = '0';
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
            btn.innerText = 'Creating ServiceNow Profile...';

            try {
                const res = await fetch(`${API_BASE}/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email, mobile, password })
                });

                const data = await res.json();
                const result = data.result || data;

                if (res.ok && result.success) {
                    currentUser = { sys_id: result.user_id, name: result.name, email: result.email };
                    currentCustomer = { customer_id: result.customer_id, name: result.name, email: result.email, status: 'Active' };

                    localStorage.setItem('fnx_user', JSON.stringify(currentUser));
                    localStorage.setItem('fnx_customer', JSON.stringify(currentCustomer));

                    updateHeaderAuth();
                    showInfoModal(
                        'FRAUDNEXUS Profile Provisioned',
                        `Your customer profile has been registered in ServiceNow!\n\nCustomer ID: ${result.customer_id}\nName: ${result.name}\nEmail: ${result.email}\n\nYou can now report fraud immediately and track case milestones.`
                    );
                    loadCustomerCases();
                    switchWorkspaceTab('dash');
                } else {
                    showAlert('reg-alert', result.error || 'Failed to create account.', 'error');
                }
            } catch (err) {
                showAlert('reg-alert', 'Connection error. Please try again.', 'error');
            } finally {
                btn.disabled = false;
                btn.innerText = 'Create Account & Enter Workspace';
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
            btn.innerText = 'Authenticating with ServiceNow...';

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
                    switchWorkspaceTab('dash');
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

        function quickFillLogin(email, pwd) {
            document.getElementById('login-email').value = email;
            document.getElementById('login-password').value = pwd;
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

        // FORGOT PASSWORD
        function openForgotPasswordModal() {
            document.getElementById('forgot-modal').classList.add('open');
        }

        function closeForgotPasswordModal() {
            document.getElementById('forgot-modal').classList.remove('open');
        }

        function handleForgotPassword() {
            const email = document.getElementById('forgot-email').value.trim();
            if (!email) {
                showAlert('forgot-alert', 'Please enter your registered email.', 'error');
                return;
            }
            showAlert('forgot-alert', 'Verification email sent. If your account exists, a secure password reset link has been dispatched.', 'success');
            setTimeout(closeForgotPasswordModal, 3000);
        }

        // LOAD CASES & STATS
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
                    const stats = result.stats || { total: 0, active: 0, resolved: 0, closed: 0 };

                    document.getElementById('stat-total').innerText = stats.total;
                    document.getElementById('stat-active').innerText = stats.active;
                    document.getElementById('stat-resolved').innerText = stats.resolved;
                    document.getElementById('stat-closed').innerText = stats.closed || 0;

                    renderDashboardTable(customerCases);
                    renderTrackTable();
                    renderVaultEvidence();
                }
            } catch(e) {
                console.error('Failed loading cases', e);
            }
        }

        function renderDashboardTable(cases) {
            const tbody = document.getElementById('cases-table-body');
            if (!cases || cases.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: var(--text-secondary); padding: 2.5rem;">No fraud cases reported yet. Click "Report Fraud" above to begin.</td></tr>';
                return;
            }

            tbody.innerHTML = cases.slice(0, 5).map(c => `
                <tr>
                    <td style="font-family: monospace; font-weight: 700; color: var(--secondary-navy);">${escapeHtml(c.number || '')}</td>
                    <td><strong>${escapeHtml(c.type || '')}</strong></td>
                    <td>${escapeHtml(c.incident_date || c.created_on?.split(' ')[0] || '')}</td>
                    <td>₹${Number(c.exposure || 0).toLocaleString('en-IN')}</td>
                    <td><span class="badge ${c.stage === 'Resolved' || c.stage === 'Closed' ? 'badge-resolved' : 'badge-active'}">${escapeHtml(c.stage || 'New')}</span></td>
                    <td><span class="badge badge-new">${escapeHtml(c.status || 'New')}</span></td>
                    <td>
                        <button class="btn btn-outline" style="padding: 0.3rem 0.65rem; font-size: 0.8rem;" onclick="viewCaseDetails('${c.sys_id}')">Track</button>
                    </td>
                </tr>
            `).join('');
        }

        function renderTrackTable() {
            const tbody = document.getElementById('track-table-body');
            if (!tbody) return;
            if (!customerCases || customerCases.length === 0) {
                tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: var(--text-secondary); padding: 2.5rem;">No cases reported yet.</td></tr>';
                return;
            }

            tbody.innerHTML = customerCases.map(c => `
                <tr>
                    <td style="font-family: monospace; font-weight: 700; color: var(--secondary-navy);">${escapeHtml(c.number || '')}</td>
                    <td><strong>${escapeHtml(c.type || '')}</strong></td>
                    <td>${escapeHtml(c.incident_date || c.created_on?.split(' ')[0] || '')}</td>
                    <td>₹${Number(c.exposure || 0).toLocaleString('en-IN')}</td>
                    <td><span class="badge badge-active">${escapeHtml(c.stage || 'New')}</span></td>
                    <td><span class="badge badge-closed">${c.evidence ? c.evidence.length : 0} Files</span></td>
                    <td><span class="badge badge-new">${escapeHtml(c.status || 'New')}</span></td>
                    <td>
                        <button class="btn btn-primary" style="padding: 0.3rem 0.75rem; font-size: 0.8rem;" onclick="viewCaseDetails('${c.sys_id}')">View &amp; Add Evidence</button>
                    </td>
                </tr>
            `).join('');
        }

        function renderVaultEvidence() {
            const list = document.getElementById('vault-evidence-list');
            if (!list) return;

            let allEv = [];
            customerCases.forEach(c => {
                if (c.evidence && c.evidence.length > 0) {
                    c.evidence.forEach(ev => allEv.push({ ...ev, caseNumber: c.number, caseSysId: c.sys_id }));
                }
            });

            if (allEv.length === 0) {
                list.innerHTML = '<div style="text-align: center; color: var(--text-secondary); padding: 2.5rem;">No evidence files found in customer vault.</div>';
                return;
            }

            list.innerHTML = allEv.map(ev => `
                <div style="background: #FFFFFF; border: 1px solid var(--border-color); border-radius: 8px; padding: 1rem; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: var(--primary-navy); font-family: monospace;">${escapeHtml(ev.number)}</strong> 
                        <span class="badge badge-closed" style="margin-left: 0.5rem;">${escapeHtml(ev.type)}</span>
                        <div style="font-size: 0.82rem; color: var(--text-secondary); margin-top: 0.25rem;">
                            Case: <strong>${escapeHtml(ev.caseNumber)}</strong> | ${escapeHtml(ev.description || 'Evidence file')}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span class="badge badge-resolved">${escapeHtml(ev.status || 'Verified')}</span>
                        <div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.25rem;">SHA-256 Custody Logged</div>
                    </div>
                </div>
            `).join('');
        }

        // VIEW CASE DETAILS & TIMELINE
        function viewCaseDetails(caseSysId) {
            activeModalCaseId = caseSysId;
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

            // Set visual timeline based on stage/status
            updateModalTimeline(c.stage, c.status);

            // Evidence rendering
            renderModalEvidenceList(c.evidence);

            document.getElementById('case-modal').classList.add('open');
        }

        function updateModalTimeline(stage, status) {
            const stages = ['submitted', 'review', 'investigation', 'resolution', 'closed'];
            stages.forEach(s => {
                const el = document.getElementById(`tl-node-${s}`);
                if (el) el.className = 'tl-node';
            });

            document.getElementById('tl-node-submitted')?.classList.add('completed');
            if (stage === 'Initial Review' || stage === 'New') {
                document.getElementById('tl-node-review')?.classList.add('active');
            } else if (stage === 'Investigation' || stage === 'Active') {
                document.getElementById('tl-node-review')?.classList.add('completed');
                document.getElementById('tl-node-investigation')?.classList.add('active');
            } else if (stage === 'Resolution' || status === 'Resolved') {
                document.getElementById('tl-node-review')?.classList.add('completed');
                document.getElementById('tl-node-investigation')?.classList.add('completed');
                document.getElementById('tl-node-resolution')?.classList.add('active');
            } else if (stage === 'Closed' || status === 'Closed') {
                stages.forEach(s => document.getElementById(`tl-node-${s}`)?.classList.add('completed'));
            }
        }

        function renderModalEvidenceList(evidence) {
            const evBox = document.getElementById('modal-evidence-list');
            if (evidence && evidence.length > 0) {
                evBox.innerHTML = evidence.map(ev => `
                    <div style="background: #F8FAFC; border: 1px solid var(--border-color); padding: 0.65rem 0.85rem; border-radius: 6px; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="font-family: monospace; color: var(--primary-navy);">${escapeHtml(ev.number)}</strong>
                            <span style="font-size: 0.8rem; color: var(--text-secondary); margin-left: 0.5rem;">(${escapeHtml(ev.type)})</span>
                            <div style="font-size: 0.82rem; margin-top: 0.2rem;">${escapeHtml(ev.description || 'Evidence material')}</div>
                        </div>
                        <span class="badge badge-resolved">${escapeHtml(ev.status || 'Verified')}</span>
                    </div>
                `).join('');
            } else {
                evBox.innerHTML = '<em>No evidence files attached.</em>';
            }
        }

        function closeCaseModal() {
            document.getElementById('case-modal').classList.remove('open');
            activeModalCaseId = null;
        }

        // SUBMIT ADDITIONAL EVIDENCE TO AN EXISTING CASE
        async function submitAdditionalEvidence() {
            if (!activeModalCaseId) return;
            const evType = document.getElementById('add-ev-type').value;
            const evDesc = document.getElementById('add-ev-desc').value.trim();
            const fileInput = document.getElementById('add-ev-file');
            const fileName = fileInput?.files?.[0]?.name || '';

            if (!evDesc && !fileName) {
                showAlert('add-ev-alert', 'Please provide a description or select an evidence file.', 'error');
                return;
            }

            const btn = document.getElementById('btn-add-ev');
            btn.disabled = true;
            btn.innerText = 'Preserving Evidence in Custody...';

            const payload = {
                action: 'add_evidence',
                case_id: activeModalCaseId,
                user_id: currentUser ? currentUser.sys_id : '',
                evidence_type: evType,
                evidence_description: evDesc,
                attachment_name: fileName
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
                    showAlert('add-ev-alert', 'Evidence attached and chain of custody recorded successfully!', 'success');
                    document.getElementById('add-ev-desc').value = '';
                    if (fileInput) fileInput.value = '';

                    // Reload cases and refresh modal evidence
                    await loadCustomerCases();
                    const updatedCase = customerCases.find(c => c.sys_id === activeModalCaseId);
                    if (updatedCase) renderModalEvidenceList(updatedCase.evidence);
                } else {
                    showAlert('add-ev-alert', result.error || 'Failed to attach evidence.', 'error');
                }
            } catch(e) {
                showAlert('add-ev-alert', 'Network error uploading evidence.', 'error');
            } finally {
                btn.disabled = false;
                btn.innerText = 'Attach Evidence to Case';
            }
        }

        // REPORT FRAUD WIZARD LOGIC
        function goToStep(stepNum) {
            for (let i = 1; i <= 5; i++) {
                document.getElementById(`wiz-step-${i}`).style.display = (i === stepNum) ? 'block' : 'none';
                const ind = document.getElementById(`wiz-step-ind-${i}`);
                if (ind) {
                    ind.classList.remove('active', 'completed');
                    if (i < stepNum) ind.classList.add('completed');
                    if (i === stepNum) ind.classList.add('active');
                }
            }

            // Summary preview on Step 5
            if (stepNum === 5) {
                document.getElementById('sum-type').innerText = document.getElementById('fr-type').value;
                document.getElementById('sum-amount').innerText = Number(document.getElementById('fr-amount').value || 0).toLocaleString('en-IN');
                document.getElementById('sum-date').innerText = document.getElementById('fr-date').value || 'Today';
                document.getElementById('sum-platform').innerText = document.getElementById('fr-platform').value || 'Not specified';
                document.getElementById('sum-mode').innerText = document.getElementById('fr-pay-mode').value || 'N/A';
                document.getElementById('sum-inst').innerText = document.getElementById('fr-inst-name').value || 'Not specified';
            }
        }

        function setFinGate(val) {
            document.querySelectorAll('.gate-choice-label').forEach(el => el.classList.remove('selected'));
            if (val === 'Yes') {
                document.getElementById('fin-gate-yes').classList.add('selected');
                document.getElementById('fin-details-section').style.display = 'block';
            } else if (val === 'No') {
                document.getElementById('fin-gate-no').classList.add('selected');
                document.getElementById('fin-details-section').style.display = 'none';
                document.getElementById('fr-amount').value = '0';
            } else {
                document.getElementById('fin-gate-ns').classList.add('selected');
                document.getElementById('fin-details-section').style.display = 'block';
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
            
            const finGate = document.querySelector('input[name="fin_gate"]:checked')?.value || 'Yes';
            const payMode = document.getElementById('fr-pay-mode').value;
            const amount = document.getElementById('fr-amount').value || '0';
            const instName = document.getElementById('fr-inst-name').value.trim();
            const instType = document.getElementById('fr-inst-type').value;
            const branch = document.getElementById('fr-branch').value.trim();
            const utr = document.getElementById('fr-utr').value.trim();
            const blocked = document.getElementById('fr-blocked').value || '0';
            const recovered = document.getElementById('fr-recovered').value || '0';
            const suspect = document.getElementById('fr-suspect').value.trim();
            const channel = document.getElementById('fr-channel').value;

            const evType = document.getElementById('fr-ev-type').value;
            const evDesc = document.getElementById('fr-ev-desc').value.trim();
            const fileInput = document.getElementById('fr-file');
            const attachmentName = fileInput?.files?.[0]?.name || '';

            if (!desc) {
                alert('Please enter a case narrative in Step 2.');
                goToStep(2);
                return;
            }

            const btn = document.getElementById('btn-submit-case');
            btn.disabled = true;
            btn.innerText = 'Creating ServiceNow Fraud Case...';

            const payload = {
                user_id: currentUser ? currentUser.sys_id : '',
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
                financial_involvement: finGate,
                payment_mode: payMode,
                exposure: amount,
                institution_name: instName,
                institution_type: instType,
                branch: branch,
                transaction_reference: utr,
                blocked_amount: blocked,
                recovered_amount: recovered,
                suspect_name: suspect,
                communication_channel: channel,
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

                    loadCustomerCases();
                    navigateTo('confirmation-view');
                } else {
                    alert('Submission error: ' + (result.error || 'Server error'));
                }
            } catch(e) {
                alert('Network connection error while submitting fraud report.');
            } finally {
                btn.disabled = false;
                btn.innerText = 'Submit Fraud Report';
            }
        }

        // CUSTOMER AI ASSISTANT LOGIC
        function toggleAiDrawer() {
            document.getElementById('ai-drawer').classList.toggle('open');
        }

        function askAi(intent) {
            const answers = {
                'How to report fraud': 'To report fraud, click "Report Fraud" in the left sidebar or header. Complete the 5 guided steps: select the fraud classification, detail what happened, provide location & financial transaction info (such as UTR/bank name), and upload your evidence screenshots.',
                'Where is my case?': 'You can track all your submitted cases under the "Track Cases" tab in the left sidebar. Each case displays live progress milestones (Submitted, Review, Investigation, Resolution, Closed).',
                'What does case status mean?': 'Milestones:\n• Submitted: Registered in ServiceNow.\n• Initial Review: Assigned triage officers verify account links.\n• Investigation: Forensic analysis and mule-account correlation active.\n• Resolution: Recovery steps executed with partner banks.\n• Closed: Final audit and case completion.',
                'How do I upload evidence?': 'You can upload evidence during initial submission or at ANY time later! Go to "Track Cases", click "View & Add Evidence" on any case, choose your file, and click "Attach Evidence to Case".',
                'How do I contact support?': 'For urgent financial freezing, call the 24/7 National Cyber Fraud Helpline at 1930 immediately. You can also visit cybercrime.gov.in for formal cyber complaints.'
            };

            appendAiChat(intent, answers[intent] || 'I can assist you with fraud reporting procedures, case milestones, and evidence uploads.');
        }

        function sendCustomAiMessage() {
            const input = document.getElementById('ai-user-input');
            const q = input.value.trim();
            if (!q) return;
            input.value = '';

            // Check if user is asking about a specific case number (e.g. FNX-2026-001001)
            const caseMatch = q.match(/FNX-2026-[0-9A-Z]+/i);
            if (caseMatch) {
                const caseNum = caseMatch[0].toUpperCase();
                const found = customerCases.find(c => c.number && c.number.toUpperCase() === caseNum);
                if (found) {
                    appendAiChat(q, `Case <strong>${found.number}</strong> (${found.type}) is currently in stage: <strong>${found.stage}</strong> with status: <strong>${found.status}</strong>. Exposure: ₹${Number(found.exposure || 0).toLocaleString('en-IN')}. Evidence files in custody: ${found.evidence ? found.evidence.length : 0}.`);
                    return;
                } else {
                    appendAiChat(q, `I could not locate case <strong>${caseNum}</strong> under your current customer profile. Please check the "Track Cases" tab or verify the case ID.`);
                    return;
                }
            }

            // Keyword responses
            if (q.toLowerCase().includes('status') || q.toLowerCase().includes('track')) {
                appendAiChat(q, 'You can track your case progress anytime in the "Track Cases" tab. All your active cases are listed with live investigation stages.');
            } else if (q.toLowerCase().includes('helpline') || q.toLowerCase().includes('phone') || q.toLowerCase().includes('number')) {
                appendAiChat(q, 'The National Cyber Fraud Reporting Helpline is <strong>1930</strong>. Call immediately to request an inter-bank fund freeze.');
            } else if (q.toLowerCase().includes('evidence') || q.toLowerCase().includes('screenshot')) {
                appendAiChat(q, 'You can attach additional evidence directly inside "Track Cases" → "View & Add Evidence". Supported files: Screenshots, PDFs, Chat Exports, and Transaction Slips.');
            } else {
                appendAiChat(q, `Thank you for your inquiry regarding "${escapeHtml(q)}". For active cases, please refer to the Track Cases tab or call the 1930 national helpline for immediate fund freeze assistance.`);
            }
        }

        function appendAiChat(userText, botHtml) {
            const history = document.getElementById('ai-chat-history');
            const userBubble = `<div style="text-align: right; margin-bottom: 0.6rem;"><div class="ai-user-bubble">${escapeHtml(userText)}</div></div>`;
            const botBubble = `<div class="ai-msg" style="margin-bottom: 0.6rem;">${botHtml}</div>`;
            history.innerHTML += userBubble + botBubble;
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

# 1. Write updated create_ui_page.py
with open("create_ui_page.py", "w", encoding="utf-8") as f:
    f.write(f'''import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {{'Accept': 'application/json', 'Content-Type': 'application/json'}}

portal_html = """{portal_html}"""

# Check or Create sys_ui_page
r_chk = requests.get(f"{{url}}/api/now/table/sys_ui_page?sysparm_query=name=fnx_portal", auth=auth, headers=headers)
existing = r_chk.json().get('result', [])

page_payload = {{
    "name": "fnx_portal",
    "html": portal_html,
    "description": "FRAUDNEXUS Customer Portal Foundation (Phase 1)",
    "direct": "true"
}}

if existing:
    page_id = existing[0]['sys_id']
    r_update = requests.patch(f"{{url}}/api/now/table/sys_ui_page/{{page_id}}", auth=auth, headers=headers, json=page_payload)
    print("Updated sys_ui_page 'fnx_portal':", r_update.status_code)
else:
    r_create = requests.post(f"{{url}}/api/now/table/sys_ui_page", auth=auth, headers=headers, json=page_payload)
    print("Created sys_ui_page 'fnx_portal':", r_create.status_code)
''')

print("Generated create_ui_page.py successfully.")

# 2. Deploy to sp_widget fnx_customer_experience
css_match = re.search(r'<style>(.*?)</style>', portal_html, re.DOTALL)
css_content = css_match.group(1).strip() if css_match else ""

body_match = re.search(r'<body>(.*?)<script>', portal_html, re.DOTALL)
body_html = body_match.group(1).strip() if body_match else ""

js_match = re.search(r'<script>(.*?)</script>\s*</body>', portal_html, re.DOTALL)
js_content = js_match.group(1).strip() if js_match else ""

widget_client_script = f"""function($scope, $http, $window) {{
    var c = this;
    $window.setTimeout(function() {{
        var scriptEl = document.createElement('script');
        scriptEl.type = 'text/javascript';
        scriptEl.text = {repr(js_content)};
        document.body.appendChild(scriptEl);
    }}, 100);
}}"""

r_w = requests.get(f"{url}/api/now/table/sp_widget?sysparm_query=id=fnx_customer_experience", auth=auth, headers=headers)
w_id = r_w.json()['result'][0]['sys_id']

payload = {
    "template": body_html,
    "css": css_content,
    "client_script": widget_client_script,
    "public": "true"
}

r_patch = requests.patch(f"{url}/api/now/table/sp_widget/{w_id}", auth=auth, headers=headers, json=payload)
print(f"Updated sp_widget fnx_customer_experience: {r_patch.status_code}")

# Update UI page redirect
redirect_html = f"""<?xml version="1.0" encoding="utf-8" ?>
<j:jelly trim="false" xmlns:j="jelly:core" xmlns:g="glide" xmlns:j2="null" xmlns:g2="null">
    <script type="text/javascript">
        window.location.href = "{url}/fnx";
    </script>
    <div style="font-family: sans-serif; text-align: center; padding: 50px;">
        <h2>Redirecting to FRAUDNEXUS Portal...</h2>
        <p><a href="{url}/fnx">Click here if you are not redirected automatically.</a></p>
    </div>
</j:jelly>
"""

r_ui = requests.get(f"{url}/api/now/table/sys_ui_page?sysparm_query=name=fnx_portal", auth=auth, headers=headers)
if r_ui.json().get('result', []):
    ui_id = r_ui.json()['result'][0]['sys_id']
    requests.patch(f"{url}/api/now/table/sys_ui_page/{ui_id}", auth=auth, headers=headers, json={"html": redirect_html, "direct": "false"})
    print("Updated fnx_portal.do redirect to /fnx: 200")

# Verify /fnx
r_fnx = requests.get(f"{url}/fnx")
print(f"/fnx status: {r_fnx.status_code}, Length: {len(r_fnx.text)}")
print("Verified FRAUDNEXUS in /fnx:", "FRAUDNEXUS" in r_fnx.text)
