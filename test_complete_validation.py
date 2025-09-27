#!/usr/bin/env python3
"""
Test complete FRD validation flow
"""

import sys
import os

backend_dir = r"c:\Users\pavan\OneDrive\Desktop\ba-tool\react-python-auth\backend"
app_dir = os.path.join(backend_dir, 'app')
sys.path.insert(0, app_dir)
sys.path.insert(0, backend_dir)

try:
    from dotenv import load_dotenv
    env_path = os.path.join(backend_dir, '.env')
    load_dotenv(env_path, override=True)
except ImportError:
    pass

try:
    from services.ai_service import _generate_enhanced_fallback_frd, _detect_domain_from_inputs, _generate_intelligent_validation_rules
    print("✅ All functions imported successfully")
except Exception as e:
    print(f"❌ Failed to import functions: {e}")
    sys.exit(1)

def test_full_validation_flow():
    print("🔍 Testing complete FRD validation flow...")
    
    project = "Insurance System"
    brd_text = """Executive Summary
This document captures the business requirements for Insurance System.

Project Scope
quote and bind for priority products, underwriting rules engine, policy issuance and endorsements, billing and payments, claims FNOL-to-settlement workflow, agent/partner portal

Business Requirements (EPIC Format)
EPIC-01 Quote & Bind Management
Requirements:
• Quote & Bind: rate and rules, proposal, KYC, payment, and policy issuance
• Policy Admin: endorsements, renewals, cancellations, reinstatements, and documents
• Claims: FNOL intake, triage, assignment, reserves, investigation, approvals, and payouts"""
    
    # Test domain detection
    domain_inputs = {"project_description": brd_text}
    detected_domain = _detect_domain_from_inputs(domain_inputs)
    print(f"✅ Detected domain: {detected_domain}")
    
    # Test validation generation for first requirement
    req_text = "Quote & Bind: rate and rules, proposal, KYC, payment, and policy issuance"
    validation_rules = _generate_intelligent_validation_rules(detected_domain, req_text, brd_text)
    
    print(f"\n📋 Generated validation rules:")
    print(validation_rules)
    
    # Check if insurance-specific
    is_insurance_specific = any(term in validation_rules.lower() for term in ['policy', 'premium', 'coverage', 'quote'])
    print(f"\n🎯 Insurance-specific: {'✅ YES' if is_insurance_specific else '❌ NO'}")
    
    return is_insurance_specific

if __name__ == "__main__":
    success = test_full_validation_flow()
    print(f"\n📋 RESULT: {'✅ WORKING' if success else '❌ BROKEN'}")