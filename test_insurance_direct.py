#!/usr/bin/env python3
"""
Direct Insurance Domain Test
Test the AI service directly without server
"""

import sys
import os

# Add the backend app directory to Python path
backend_dir = r"c:\Users\pavan\OneDrive\Desktop\ba-tool\react-python-auth\backend"
app_dir = os.path.join(backend_dir, 'app')
sys.path.insert(0, app_dir)
sys.path.insert(0, backend_dir)

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = os.path.join(backend_dir, '.env')
    load_dotenv(env_path, override=True)
    print(f"✅ Loaded .env from: {env_path}")
except ImportError:
    print("❌ python-dotenv not available")

# Import AI service
try:
    from services.ai_service import generate_frd_html_from_brd, _detect_domain_from_inputs
    print("✅ AI service imported successfully")
except Exception as e:
    print(f"❌ Failed to import AI service: {e}")
    sys.exit(1)

def test_insurance_domain_direct():
    print("🏥 Testing Insurance Domain Fix (Direct)...")
    
    # Insurance BRD content
    insurance_brd = """Executive Summary
This document captures the business requirements for Insurance Management System.

Project Scope
quote and bind for priority products (motor/health/life), underwriting rules engine, policy issuance and endorsements, billing and payments, claims FNOL-to-settlement workflow, agent/partner portal

Business Objectives  
Increase digital quote to bind rate, reduce time to issue policies, improve first call resolution on claims

Budget Details
₹1.2–₹2.0 crore for discovery, licenses, integrations, build and testing

Business Requirements (EPIC Format)
EPIC-01 Quote & Bind Management
Requirements:
• Quote & Bind: rate and rules, proposal, KYC, payment, and policy issuance
• Policy Admin: endorsements, renewals, cancellations, reinstatements, and documents
• Claims: FNOL intake, triage, assignment, reserves, investigation, approvals, and payouts

EPIC-02 Billing & Distribution  
Requirements:
• Billing: invoices, reminders, dunning, autopay, refunds, reconciliation
• Distribution: agent/partner portal, lead tracking, commissions, and dashboards
• Compliance & Reporting: audit logs, regulatory reports, bordereaux, and MI"""

    # Test domain detection first
    project = "Insurance Management System"
    print(f"\n🔍 Testing domain detection for: {project}")
    # Create a dummy inputs dict with the BRD content for domain detection
    test_inputs = {"project_description": insurance_brd}
    detected_domain = _detect_domain_from_inputs(test_inputs)
    print(f"✅ Detected domain: {detected_domain}")
    
    try:
        print(f"\n🔄 Generating FRD...")
        frd_html = generate_frd_html_from_brd(project, insurance_brd, 1)
        print(f"✅ FRD Generated: {len(frd_html)} characters")
        
        # Check for insurance-specific content
        insurance_checks = {
            "Domain Detection": detected_domain == "insurance",
            "Policy Terms": any(term in frd_html.lower() for term in ["policy", "policyholder", "coverage"]),
            "Claims Terms": any(term in frd_html.lower() for term in ["claim", "fnol", "settlement"]),
            "Agent Terms": any(term in frd_html.lower() for term in ["agent", "underwriter", "actuary"]),
            "Insurance Stakeholders": any(term in frd_html for term in ["Insurance agents", "Underwriters", "Claims adjusters"]),
            "Insurance Validations": any(term in frd_html for term in ["premium", "underwriting", "commission"]),
            "NOT Telecom": not any(term in frd_html.lower() for term in ["sim", "subscriber", "telecom", "billing specialist"])
        }
        
        print("\n📊 Insurance Domain Verification:")
        passed = 0
        for check, result in insurance_checks.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {check:20} | {status}")
            if result:
                passed += 1
        
        score = (passed / len(insurance_checks)) * 100
        print(f"\n🎯 Insurance Domain Score: {score:.1f}%")
        
        # Save output for inspection
        with open("test_insurance_direct_output.html", "w", encoding="utf-8") as f:
            f.write(frd_html)
        print("💾 Full FRD saved to test_insurance_direct_output.html")
        
        # Show first 500 chars for quick verification
        print(f"\n📄 First 500 characters of FRD:")
        print(frd_html[:500] + "...")
        
        if score >= 80:
            print("🎉 SUCCESS: Insurance domain fix is working!")
            return True
        else:
            print("⚠️ PARTIAL: Some insurance elements missing")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = test_insurance_domain_direct()
    print(f"\n📋 RESULT: {'✅ FIXED' if success else '❌ STILL BROKEN'}")