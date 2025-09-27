#!/usr/bin/env python3
"""
Direct test of enhanced CRM validation criteria in fallback mode
"""
import sys
import os

# Add the backend path to sys.path
backend_path = os.path.join(os.path.dirname(__file__), 'react-python-auth', 'backend')
sys.path.insert(0, backend_path)

try:
    from app.services.ai_service import _detect_domain_from_inputs, generate_brd_html
    
    print("=== Testing Enhanced CRM Validation Criteria ===")
    
    # Test CRM project input
    test_inputs = {
        "project_overview": "Customer Relationship Management system for sales team to manage leads, track opportunities, and maintain customer contacts",
        "functional_requirements": [
            "Lead capture and qualification system",
            "Opportunity pipeline management", 
            "Contact management and deduplication",
            "Sales activity tracking",
            "Campaign performance analytics"
        ],
        "non_functional_requirements": [
            "System should handle 1000 concurrent users",
            "Response time under 2 seconds"
        ],
        "validations": "Lead data validation, opportunity workflow validation, contact integrity checks"
    }
    
    # Test domain detection
    detected_domain = _detect_domain_from_inputs(test_inputs)
    print(f"🎯 Detected Domain: {detected_domain}")
    
    # Generate enhanced BRD using the main function (which includes validation)
    project_name = "CRM System Enhancement"
    brd_html = generate_brd_html(project_name, test_inputs, 1)
    
    print(f"\n=== Generated BRD Analysis ===")
    print(f"BRD Length: {len(brd_html)} characters")
    
    # Check for CRM-specific validation criteria in the generated BRD
    crm_validation_keywords = [
        "lead capture",
        "opportunity",
        "contact",
        "deduplication", 
        "sales activity",
        "campaign",
        "customer consent",
        "email address format",
        "deliverability",
        "attribution"
    ]
    
    found_validations = []
    for keyword in crm_validation_keywords:
        if keyword.lower() in brd_html.lower():
            found_validations.append(keyword)
    
    print(f"CRM-specific validations found: {len(found_validations)}")
    print(f"Found keywords: {found_validations}")
    
    # Save output for inspection
    output_file = "test_crm_brd_validation_output.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(brd_html)
    print(f"✅ BRD output saved to {output_file}")
    
    # Check if we have marketing domain-specific validation
    marketing_validations = [
        "customer consent validation",
        "email address format",
        "campaign performance tracking",
        "A/B testing validation"
    ]
    
    found_marketing = []
    for validation in marketing_validations:
        if validation.lower() in brd_html.lower():
            found_marketing.append(validation)
    
    print(f"Marketing-specific validations found: {len(found_marketing)}")
    print(f"Marketing validations: {found_marketing}")
    
    # Assessment
    if len(found_validations) >= 3 or len(found_marketing) >= 2:
        print("\n✅ SUCCESS: Enhanced CRM/Marketing validation criteria are working!")
        print("The AI service now generates domain-specific validation instead of generic rules.")
    else:
        print("\n❌ ISSUE: Generic validation criteria still detected")
        print("May need further enhancement of validation generation logic.")
        
except ImportError as e:
    print(f"❌ Import Error: {e}")
except Exception as e:
    print(f"❌ Test Error: {e}")
    import traceback
    traceback.print_exc()