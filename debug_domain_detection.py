#!/usr/bin/env python3
"""
Quick test to debug the domain detection and FRD generation
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'react-python-auth', 'backend', 'app'))

from services.ai_service import _detect_domain_from_inputs, _generate_enhanced_fallback_frd

def test_domain_detection():
    print("🔍 Testing Domain Detection...")
    
    # Insurance test input
    insurance_inputs = {
        "project": "Insurance Management System",
        "briefRequirements": """Quote & Bind: rate and rules, proposal, KYC, payment, and policy issuance.
Policy Admin: endorsements, renewals, cancellations, reinstatements, and documents.
Claims: FNOL intake, triage, assignment, reserves, investigation, approvals, and payouts.
Billing: invoices, reminders, dunning, autopay, refunds, reconciliation.
Distribution: agent/partner portal, lead tracking, commissions, and dashboards.
Compliance & Reporting: audit logs, regulatory reports, bordereaux, and MI.""",
        "scope": "priority products (motor/health/life), underwriting rules engine, policy issuance",
        "objectives": "Increase digital quote to bind rate, reduce time to issue policies"
    }
    
    # Test domain detection
    detected_domain = _detect_domain_from_inputs(insurance_inputs)
    print(f"✅ Detected Domain: {detected_domain}")
    
    # Test if it should be insurance
    expected_keywords = ["policy", "claim", "premium", "coverage", "underwriting", "actuarial"]
    found_keywords = []
    all_text = str(insurance_inputs).lower()
    for keyword in expected_keywords:
        if keyword in all_text:
            found_keywords.append(keyword)
    
    print(f"📊 Insurance Keywords Found: {found_keywords}")
    
    if detected_domain == "insurance":
        print("🎉 CORRECT: Domain correctly detected as insurance")
    else:
        print(f"❌ WRONG: Domain detected as '{detected_domain}' instead of 'insurance'")
    
    return detected_domain

def test_frd_generation():
    print("\n🚀 Testing FRD Generation...")
    
    brd_text = """Executive Summary
This document captures business requirements for Insurance.

Project Scope  
quote and bind for priority products, underwriting rules engine, policy issuance

Business Requirements
Quote & Bind: rate and rules, proposal, KYC, payment, and policy issuance.
Policy Admin: endorsements, renewals, cancellations, reinstatements, and documents.
Claims: FNOL intake, triage, assignment, reserves, investigation, approvals, and payouts."""
    
    # Generate FRD using fallback
    frd_html = _generate_enhanced_fallback_frd("Insurance System", brd_text, 1)
    
    print(f"📄 Generated FRD Length: {len(frd_html)} characters")
    
    # Check for insurance-specific content
    insurance_terms = ["policy", "claim", "underwriter", "premium", "coverage"]
    telecom_terms = ["sim", "billing", "charging", "subscriber", "telecom"]
    
    insurance_found = sum(1 for term in insurance_terms if term.lower() in frd_html.lower())
    telecom_found = sum(1 for term in telecom_terms if term.lower() in frd_html.lower())
    
    print(f"📊 Insurance Terms Found: {insurance_found}")
    print(f"📊 Telecom Terms Found: {telecom_found}")
    
    if insurance_found > telecom_found:
        print("🎉 SUCCESS: FRD contains more insurance terms than telecom")
    else:
        print("❌ PROBLEM: FRD contains more telecom terms than insurance")
    
    # Save output for inspection
    with open("debug_frd_output.html", "w", encoding="utf-8") as f:
        f.write(frd_html)
    print("💾 FRD saved to debug_frd_output.html")

if __name__ == "__main__":
    print("🐛 DEBUG: Domain Detection & FRD Generation")
    print("=" * 50)
    
    detected = test_domain_detection()
    test_frd_generation()
    
    print("\n📋 SUMMARY:")
    print(f"  Domain Detection: {'✅ PASS' if detected == 'insurance' else '❌ FAIL'}")
    print("  Check debug_frd_output.html for detailed FRD content")