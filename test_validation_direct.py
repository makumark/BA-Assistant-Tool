#!/usr/bin/env python3
"""
Direct Validation Test - Test validation function in isolation
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

def test_validation_function_directly():
    print("🔍 Testing validation function directly...")
    
    # Test healthcare domain with specific user story content
    domain = "healthcare"
    requirement = "As a Patient, I want implement ability to create and manage patient profiles, schedule appointments with notifications, store and update patient medical history securely, and generate invoices with insurance claim support"
    context = "Patient registration, appointment scheduling, electronic health records integration, billing module"
    
    print(f"Domain: {domain}")
    print(f"Requirement: {requirement[:100]}...")
    print(f"Context: {context}")
    
    result = _generate_intelligent_validation_rules(domain, requirement, context)
    
    print(f"\n📋 Generated Validation Rules:")
    print(result)
    
    # Check if it's specific or generic
    if any(term in result.lower() for term in ["patient", "appointment", "medical", "insurance eligibility"]):
        print("\n✅ SUCCESS: Generated healthcare-specific validations!")
        return True
    else:
        print("\n❌ FAIL: Still generating generic validations")
        return False

if __name__ == "__main__":
    success = test_validation_function_directly()
    print(f"\n📋 RESULT: {'✅ SPECIFIC' if success else '❌ GENERIC'}")