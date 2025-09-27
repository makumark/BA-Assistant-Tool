#!/usr/bin/env python3
"""
Test Insurance Domain Fix
Quick verification that insurance domain works correctly
"""

import requests
import json

def test_insurance_domain():
    print("🏥 Testing Insurance Domain Fix...")
    
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

    payload = {
        "project": "Insurance Management System",
        "brd": insurance_brd,
        "version": 1
    }
    
    try:
        response = requests.post("http://localhost:8001/ai/frd", json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            frd_html = result.get("html", "")
            
            print(f"✅ FRD Generated: {len(frd_html)} characters")
            
            # Check for insurance-specific content
            insurance_checks = {
                "Domain Detection": "Domain: Insurance" in frd_html,
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
            with open("test_insurance_fix_output.html", "w", encoding="utf-8") as f:
                f.write(frd_html)
            print("💾 Full FRD saved to test_insurance_fix_output.html")
            
            if score >= 80:
                print("🎉 SUCCESS: Insurance domain fix is working!")
                return True
            else:
                print("⚠️ PARTIAL: Some insurance elements missing")
                return False
                
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_insurance_domain()
    print(f"\n📋 RESULT: {'✅ FIXED' if success else '❌ STILL BROKEN'}")