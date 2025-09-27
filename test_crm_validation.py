#!/usr/bin/env python3
"""
Test CRM validation criteria generation
"""
import sys
import os

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'react-python-auth', 'backend')
sys.path.insert(0, backend_path)

from app.services.ai_service import _detect_domain_from_inputs, generate_frd_html_from_brd

def test_crm_domain_detection():
    """Test if CRM BRD is correctly detected as marketing domain"""
    
    # Your exact BRD inputs
    brd_content = """
    1. Executive Summary
    This document captures the business requirements for the project CRM. It follows standard BA practice aligned to BABOK and provides the scope, objectives, requirements, budget and validations required for delivering the solution.
    
    2. Project Scope
    Included — lead and account management, contact/interaction tracking, opportunity and pipeline, activities and tasks, case/ticketing, marketing campaigns and segmentation, dashboards and reports, role based admin and security
    
    3. Business Objectives
    Increase qualified lead conversion, improve pipeline visibility and forecast accuracy, reduce response time to inbound inquiries, raise customer retention/NPS, and shorten onboarding time for new sales reps.
    
    5. Business Requirements (EPIC Format)
    EPIC-01 Core Business Requirements 
    Requirements: 
    •	EPIC 01 Lead & Account: capture, de dupe, qualify, convert to account/contact/opportunity.
    •	EPIC 02 Opportunity & Pipeline: stages, products, quotes light, forecasts, win/loss reasons.
    •	EPIC 03 Activities & Calendar: tasks, calls, meetings, reminders, SLA timers.
    """
    
    test_inputs = {
        'scope': 'lead and account management, contact/interaction tracking, opportunity and pipeline, activities and tasks, case/ticketing, marketing campaigns and segmentation, dashboards and reports',
        'objectives': 'Increase qualified lead conversion, improve pipeline visibility and forecast accuracy, reduce response time to inbound inquiries',
        'briefRequirements': 'lead capture, opportunity management, activities tracking, marketing campaigns, contact management, pipeline forecasting'
    }

    print("🧪 Testing CRM Domain Detection...")
    print("=" * 50)
    
    detected = _detect_domain_from_inputs(test_inputs)
    print(f"🎯 Detected Domain: {detected}")
    print(f"✅ Expected Domain: marketing (CRM falls under marketing domain)")
    
    if detected == "marketing":
        print("✅ Domain detection CORRECT")
    else:
        print("❌ Domain detection INCORRECT")
        print("   This explains why validation criteria are wrong!")
    
    print("\n🧪 Testing FRD Generation...")
    print("=" * 50)
    
    try:
        frd_html = generate_frd_html_from_brd("CRM System", brd_content, 1)
        
        # Save for inspection
        with open("test_crm_frd_output.html", "w", encoding="utf-8") as f:
            f.write(frd_html)
        print("💾 FRD saved to: test_crm_frd_output.html")
        
        # Check validation criteria
        if "lead capture forms collect all required information" in frd_html.lower():
            print("✅ Contains CRM-specific validation criteria")
        elif "customer consent validation" in frd_html.lower():
            print("✅ Contains marketing-specific validation criteria")
        elif "patient" in frd_html.lower():
            print("❌ Contains healthcare validation criteria (WRONG)")
        elif "policy" in frd_html.lower():
            print("❌ Contains insurance validation criteria (WRONG)")
        else:
            print("❓ Validation criteria unclear")
            
        # Check domain consistency
        if "insurance" in frd_html.lower() and "crm" in frd_html.lower():
            print("❌ Domain mismatch: Insurance detected for CRM project")
        elif "marketing" in frd_html.lower():
            print("✅ Marketing domain detected correctly")
            
    except Exception as e:
        print(f"❌ Error generating FRD: {e}")

if __name__ == "__main__":
    test_crm_domain_detection()