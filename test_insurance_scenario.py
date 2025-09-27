#!/usr/bin/env python3
"""
Test specific insurance validation scenario
"""

import sys
import os

# Add the backend app directory to Python path
backend_dir = r"c:\Users\pavan\OneDrive\Desktop\ba-tool\react-python-auth\backend"
app_dir = os.path.join(backend_dir, 'app')
sys.path.insert(0, app_dir)
sys.path.insert(0, backend_dir)

# Import AI service validation function directly
try:
    from services.ai_service import _generate_intelligent_validation_rules
    print("✅ Validation function imported successfully")
except Exception as e:
    print(f"❌ Failed to import validation function: {e}")
    sys.exit(1)

def test_insurance_specific_case():
    print("🔍 Testing specific insurance validation case...")
    
    # This matches what the FRD generation would actually pass
    domain = "insurance"
    requirement = "Quote & Bind: rate and rules"  # This is the specific req_text
    context = """Executive Summary
This document captures the business requirements for Insurance System.

Project Scope
quote and bind for priority products, underwriting rules engine, policy issuance

Business Requirements (EPIC Format)
EPIC-01 Quote & Bind Management
Requirements:
• Quote & Bind: rate and rules, proposal, KYC, payment, and policy issuance"""
    
    print(f"Domain: {domain}")
    print(f"Requirement: {requirement}")
    print(f"Context: {context[:200]}...")
    
    # Check what keywords are found
    combined_text = f"{requirement.lower()} {context.lower()}"
    insurance_keywords = ["policy", "claim", "premium", "coverage", "underwriting", "actuarial", "risk", "benefit", "quote", "bind", "policyholder", "agent", "broker", "reinsurance", "fnol", "settlement", "endorsement", "renewal", "cancellation", "reinstatement"]
    
    found_keywords = [kw for kw in insurance_keywords if kw in combined_text]
    print(f"\nFound insurance keywords: {found_keywords}")
    
    result = _generate_intelligent_validation_rules(domain, requirement, context)
    
    print(f"\n📋 Generated Validation Rules:")
    print(result)
    
    # Check if it's specific or generic
    if any(term in result.lower() for term in ["policy", "premium", "coverage", "quote", "bind"]):
        print("\n✅ SUCCESS: Generated insurance-specific validations!")
        return True
    else:
        print("\n❌ FAIL: Still generating generic validations")
        return False

if __name__ == "__main__":
    success = test_insurance_specific_case()
    print(f"\n📋 RESULT: {'✅ SPECIFIC' if success else '❌ GENERIC'}")