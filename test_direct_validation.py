#!/usr/bin/env python3
"""
Simple direct test of enhanced validation logic
"""
import sys
import os

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'react-python-auth', 'backend')
sys.path.insert(0, backend_path)

from app.services.ai_service import _generate_enhanced_fallback_frd

def test_direct_validation():
    """Test validation generation directly"""
    
    # Clean CRM BRD without validation section
    brd_text = """
    <h3>Project Scope</h3>
    <p>Lead management, opportunity pipeline, contact tracking, marketing campaigns</p>
    <h3>Business Requirements (EPIC Format)</h3>
    <p>EPIC-01: Lead Management - capture, qualify, assign leads<br/>
    EPIC-02: Opportunity Pipeline - manage sales opportunities and forecasting<br/>
    EPIC-03: Contact Management - maintain customer relationships<br/>
    EPIC-04: Marketing Campaigns - create and track campaigns</p>
    """
    
    print("🧪 Testing Enhanced Validation Generation DIRECTLY...")
    print("=" * 60)
    
    try:
        frd_html = _generate_enhanced_fallback_frd("CRM System", brd_text, 1)
        
        # Save result
        with open("test_direct_enhanced_validation.html", "w", encoding="utf-8") as f:
            f.write(frd_html)
        print("💾 FRD saved to: test_direct_enhanced_validation.html")
        
        # Check for marketing domain detection
        if "Domain: Marketing" in frd_html:
            print("✅ Domain correctly detected as Marketing")
        else:
            print("❌ Domain detection failed")
            
        # Check for enhanced marketing validations
        enhanced_validations = [
            "customer consent validation for all communication preferences",
            "email address format and deliverability standards", 
            "campaign performance tracking and attribution models",
            "lead scoring and segmentation accuracy",
            "GDPR compliance for customer data processing"
        ]
        
        found_enhanced = 0
        for validation in enhanced_validations:
            if validation.lower() in frd_html.lower():
                print(f"✅ Found enhanced validation: {validation}")
                found_enhanced += 1
            else:
                print(f"❌ Missing enhanced validation: {validation}")
        
        # Check for old generic validations
        if "data validation and integrity checks" in frd_html.lower():
            print("❌ Still contains generic validation")
        else:
            print("✅ No generic validations found")
            
        print(f"\n📊 Enhanced validations found: {found_enhanced}/{len(enhanced_validations)}")
        
        if found_enhanced >= 3:
            print("🎉 SUCCESS: Enhanced validation logic is working!")
        else:
            print("❌ FAILURE: Enhanced validation logic not working")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_direct_validation()