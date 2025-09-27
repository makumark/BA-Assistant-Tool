#!/usr/bin/env python3
"""
Test the ACTUAL FRD generation that your user interface would call
"""
import requests
import json

def test_actual_frd_generation():
    """Test the actual API endpoint that generates FRDs from BRDs"""
    
    # Your exact BRD content
    brd_html = """
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
    
    # Test the FRD generation API endpoint
    url = "http://localhost:8001/ai/frd"
    payload = {
        "project": "CRM",
        "brd": brd_html,
        "version": 1
    }
    
    print("🧪 Testing ACTUAL FRD Generation API...")
    print("=" * 60)
    print(f"📤 Project: {payload['project']}")
    print(f"📤 BRD contains: Lead management, Opportunity pipeline, Marketing campaigns")
    print(f"📤 Expected domain: Marketing/CRM")
    print(f"📤 Expected validation: CRM-specific criteria")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            frd_html = result.get("html", "")
            
            # Save for inspection
            with open("test_actual_frd_generation.html", "w", encoding="utf-8") as f:
                f.write(frd_html)
            print("💾 FRD saved to: test_actual_frd_generation.html")
            
            print(f"📥 FRD HTML length: {len(frd_html)} characters")
            
            # Analyze the content
            print("\n🔍 ANALYSIS OF GENERATED FRD:")
            print("-" * 40)
            
            # Check domain detection
            if "Domain: Marketing" in frd_html:
                print("✅ Domain correctly identified as Marketing")
            elif "Domain: Insurance" in frd_html:
                print("❌ Domain incorrectly identified as Insurance")
            else:
                print("❓ Domain identification unclear")
            
            # Check user stories
            if "As a Marketing Manager" in frd_html:
                print("✅ Contains Marketing Manager user stories")
            if "As a Prospective Customer" in frd_html:
                print("❌ Contains Prospective Customer (wrong for CRM)")
            if "electronically sign documents" in frd_html:
                print("❌ Contains document signing (not CRM-related)")
            if "patient consent" in frd_html:
                print("❌ Contains healthcare concepts (WRONG DOMAIN)")
            
            # Check validation criteria
            if "lead capture forms collect all required information" in frd_html.lower():
                print("✅ Contains CRM-specific validation criteria")
            elif "customer consent validation for communication preferences" in frd_html.lower():
                print("✅ Contains marketing-specific validation criteria")
            elif "input validation ensures data integrity" in frd_html.lower():
                print("❌ Contains generic validation criteria")
            else:
                print("❓ Validation criteria unclear")
                
            # Check for domain mismatches
            domain_mismatches = []
            if "insurance" in frd_html.lower() and "crm" in frd_html.lower():
                domain_mismatches.append("Insurance concepts in CRM system")
            if "patient" in frd_html.lower():
                domain_mismatches.append("Healthcare concepts in CRM system")
            if "policy" in frd_html.lower() and "claim" in frd_html.lower():
                domain_mismatches.append("Insurance policy/claims in CRM system")
                
            if domain_mismatches:
                print(f"❌ Domain mismatches found: {', '.join(domain_mismatches)}")
            else:
                print("✅ No obvious domain mismatches")
                
        else:
            print(f"❌ API call failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Is the backend server running on port 8001?")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_actual_frd_generation()