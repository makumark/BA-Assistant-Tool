#!/usr/bin/env python3
"""
Debug CRM validation extraction to see what's being parsed from BRD
"""
import sys
import os

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'react-python-auth', 'backend')
sys.path.insert(0, backend_path)

from app.services.ai_service import _extract_section, _br_to_list

def debug_crm_validation():
    """Debug what validation criteria are being extracted from CRM BRD"""
    
    # Your exact BRD content - using the HTML format that actually gets sent
    brd_text = """
    <div style="font-family:Arial,Helvetica,sans-serif;color:#111827;padding:18px;">
      <h1 style="text-align:center;margin-bottom:6px;">Business Requirement Document (BRD)</h1>
      <h2 style="text-align:center;margin-top:2px;">CRM — BRD Version-1</h2>
      <hr/>
      <h3>Executive Summary</h3>
      <p>This document captures the business requirements for the project CRM. It follows standard BA practice aligned to BABOK and provides the scope, objectives, requirements, budget and validations required for delivering the solution.</p>
      <h3>Project Scope</h3>
      <p>Included — lead and account management, contact/interaction tracking, opportunity and pipeline, activities and tasks, case/ticketing, marketing campaigns and segmentation, dashboards and reports, role based admin and security; Excluded — custom CPQ engine at launch, full ERP replacement, on prem telephony switch migration, and field service work order dispatch.</p>
      <h3>Business Objectives</h3>
      <p>Increase qualified lead conversion, improve pipeline visibility and forecast accuracy, reduce response time to inbound inquiries, raise customer retention/NPS, and shorten onboarding time for new sales reps.</p>
      <h3>Budget Details</h3>
      <p>Estimated ₹90–₹160 lakh covering discovery, licenses/subscriptions, data migration, integrations (email, telephony, marketing, ERP), implementation, QA/UAT, training, and first year run/support; phased rollout by sales→service→marketing.</p>
      <h3>Business Requirements (EPIC Format)</h3>
      <p>EPIC-01 Core Business Requirements<br/>
      Requirements:<br/>
      • EPIC 01 Lead & Account: capture, de dupe, qualify, convert to account/contact/opportunity.<br/>
      • EPIC 02 Opportunity & Pipeline: stages, products, quotes light, forecasts, win/loss reasons.<br/>
      • EPIC 03 Activities & Calendar: tasks, calls, meetings, reminders, SLA timers.<br/>
      EPIC Status: Ready for FRD conversion | Priority: Low<br/>
      EPIC-02 Core Business Requirements<br/>
      Requirements:<br/>
      • EPIC 04 Service & Cases: omni channel intake, prioritization, assignment, SLAs, knowledge base.<br/>
      • EPIC 05 Marketing & Journeys: lists/segments, email campaigns, forms, UTMs, attribution.<br/>
      • EPIC 06 Analytics & Reporting: dashboards for funnel, productivity, SLA, and forecast.<br/>
      EPIC Status: Ready for FRD conversion | Priority: Low<br/>
      EPIC-03 Data Management & Storage<br/>
      Requirements:<br/>
      • EPIC 07 Data & Security: roles/profiles, field level security, audit, GDPR consent.<br/>
      • EPIC 08 Integration & Migration: email/SSO/telephony/ERP connectors, one time and incremental loads.<br/>
      EPIC Status: Ready for FRD conversion | Priority: Low</p>
      <h3>Assumptions</h3>
      <p>Master data (accounts/contacts/products) is available and cleansed; email, SSO, and telephony providers expose APIs; sales process and case SLAs are approved; sandbox and prod environments exist; change management and training resources are allocated.</p>
      <h3>Constraints</h3>
      <p></p>
      <h3>Validations & Acceptance Criteria</h3>
      <p>🤖 AI DOMAIN DETECTION ACTIVE - • Enforce customer consent validation for communication preferences<br/>
      • Validate email address format and deliverability standards<br/>
      • Implement campaign performance tracking and attribution models<br/>
      • Enforce A/B testing validation for campaign optimization<br/>
      • Validate lead scoring and segmentation accuracy<br/>
      • Ensure GDPR compliance for customer data processing</p>
    </div>
    """
    
    print("🧪 Debugging CRM Validation Extraction...")
    print("=" * 60)
    
    # Extract validation section
    validations = (
        _extract_section(brd_text, "Validations & Acceptance Criteria")
        or _extract_section(brd_text, "Validations")
        or _extract_section(brd_text, "Acceptance Criteria")
    )
    
    print(f"📋 Raw validation section extracted:")
    print(f"'{validations}'")
    print()
    
    # Process into list
    val_list = _br_to_list(validations)
    print(f"📋 Validation list after processing:")
    for i, val in enumerate(val_list, 1):
        print(f"  {i}. {val}")
    print()
    
    # Generate HTML
    val_html = ""
    for i, val in enumerate(val_list, start=1):
        val_text = val.strip()
        if not val_text.startswith("Enforce"):
            val_text = "Enforce " + val_text
        if not val_text.endswith('.'):
            val_text += '.'
        val_html += f"<li><strong>V-{i:03d}:</strong> {val_text}</li>\n"
    
    print(f"📋 Generated validation HTML:")
    print(val_html)
    
    print(f"🔍 Is val_html empty? {not val_html}")
    print(f"🔍 Will use domain-specific fallback? {not val_html}")

if __name__ == "__main__":
    debug_crm_validation()
