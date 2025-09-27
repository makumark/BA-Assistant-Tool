#!/usr/bin/env python3
"""
Simple test to verify enhanced CRM validation criteria generation
"""
import sys
import os

# Add the backend path to sys.path
backend_path = os.path.join(os.path.dirname(__file__), 'react-python-auth', 'backend')
sys.path.insert(0, backend_path)

try:
    from app.services.ai_service import _generate_intelligent_validation_rules, _detect_domain_from_inputs
    
    print("=== Testing Enhanced CRM Validation Criteria ===")
    
    # Test CRM project input
    test_project = {
        "name": "CRM System Enhancement",
        "description": "Customer relationship management system for sales team lead tracking and opportunity management",
        "objectives": ["Improve lead capture", "Track sales pipeline", "Manage customer contacts"]
    }
    
    test_inputs = {
        "project_overview": "CRM system for managing leads and sales opportunities",
        "functional_requirements": [
            "Lead capture and management",
            "Opportunity pipeline tracking", 
            "Contact management and deduplication"
        ]
    }
    
    # Test domain detection
    detected_domain = _detect_domain_from_inputs(test_inputs)
    print(f"Detected Domain: {detected_domain}")
    
    # Test validation criteria generation
    validation_rules = _generate_intelligent_validation_rules(test_project, test_inputs, detected_domain)
    
    print("\n=== Generated Validation Rules ===")
    for i, rule in enumerate(validation_rules, 1):
        print(f"{i}. {rule}")
    
    # Check for CRM-specific criteria
    crm_keywords = ['lead', 'opportunity', 'contact', 'sales', 'pipeline', 'deduplication']
    found_crm_specific = any(any(keyword.lower() in rule.lower() for keyword in crm_keywords) for rule in validation_rules)
    
    print(f"\n=== Validation Results ===")
    print(f"Domain detected: {detected_domain}")
    print(f"CRM-specific validation found: {found_crm_specific}")
    print(f"Total validation rules: {len(validation_rules)}")
    
    if found_crm_specific:
        print("✅ SUCCESS: Enhanced CRM validation criteria are working!")
    else:
        print("❌ ISSUE: Generic validation criteria detected")
        
except ImportError as e:
    print(f"❌ Import Error: {e}")
except Exception as e:
    print(f"❌ Test Error: {e}")