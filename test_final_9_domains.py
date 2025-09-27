#!/usr/bin/env python3
"""
Final comprehensive test of all 9 domains with BRD generation
"""

import sys
import os

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'react-python-auth', 'backend')
sys.path.insert(0, backend_path)

from app.services.ai_service import _detect_domain_from_inputs, _generate_domain_specific_stakeholders

def test_all_9_domains_final():
    print("=== FINAL COMPREHENSIVE TEST: All 9 Domains ===\n")
    
    test_projects = [
        {
            "name": "Marketing Campaign Automation",
            "domain": "marketing",
            "inputs": {
                "project_name": "Marketing Campaign Automation",
                "description": "Automated email marketing campaign platform with segmentation",
                "features": ["campaign management", "email automation", "customer segmentation"]
            },
            "expected_stakeholders": ["campaign manager", "marketing", "email"]
        },
        {
            "name": "Patient Care Management System", 
            "domain": "healthcare",
            "inputs": {
                "project_name": "Patient Care Management System",
                "description": "Healthcare platform for patient records and clinical workflows",
                "features": ["patient management", "medical records", "clinical workflows"]
            },
            "expected_stakeholders": ["patient", "clinician", "medical"]
        },
        {
            "name": "Digital Banking Platform",
            "domain": "banking", 
            "inputs": {
                "project_name": "Digital Banking Platform",
                "description": "Online banking with account management and transactions",
                "features": ["account management", "online banking", "transaction processing"]
            },
            "expected_stakeholders": ["account holder", "banking", "branch"]
        },
        {
            "name": "E-commerce Marketplace",
            "domain": "ecommerce",
            "inputs": {
                "project_name": "E-commerce Marketplace", 
                "description": "Online marketplace for product sales and order management",
                "features": ["product catalog", "shopping cart", "order management"]
            },
            "expected_stakeholders": ["customer", "store", "inventory"]
        },
        {
            "name": "Learning Management System",
            "domain": "education",
            "inputs": {
                "project_name": "Learning Management System",
                "description": "Educational platform for student learning and course management", 
                "features": ["student portal", "course management", "learning analytics"]
            },
            "expected_stakeholders": ["student", "teacher", "academic"]
        },
        {
            "name": "Insurance Claims Portal",
            "domain": "insurance",
            "inputs": {
                "project_name": "Insurance Claims Portal",
                "description": "Platform for insurance policy management and claims processing",
                "features": ["policy management", "claims processing", "premium calculations"]
            },
            "expected_stakeholders": ["policyholder", "insurance", "claim"]
        },
        {
            "name": "Mutual Fund Investment Platform", 
            "domain": "mutualfund",
            "inputs": {
                "project_name": "Mutual Fund Investment Platform",
                "description": "Platform for mutual fund investments with SIP and NAV tracking",
                "features": ["mutual fund selection", "SIP automation", "NAV tracking"]
            },
            "expected_stakeholders": ["investor", "fund manager", "distributor"]
        },
        {
            "name": "Alternative Investment Fund System",
            "domain": "aif", 
            "inputs": {
                "project_name": "Alternative Investment Fund System",
                "description": "AIF management platform for hedge funds and private equity",
                "features": ["alternative investment", "hedge fund management", "qualified investor portal"]
            },
            "expected_stakeholders": ["qualified investor", "fund manager", "investment advisor"]
        },
        {
            "name": "Wealth Management Platform",
            "domain": "finance",
            "inputs": {
                "project_name": "Wealth Management Platform", 
                "description": "Financial planning and wealth management solution",
                "features": ["financial planning", "wealth management", "portfolio optimization"]
            },
            "expected_stakeholders": ["client", "financial advisor", "portfolio manager"]
        }
    ]
    
    results = []
    
    for i, project in enumerate(test_projects, 1):
        print(f"Test {i}: {project['name']}")
        print("-" * 60)
        
        # Test domain detection
        detected_domain = _detect_domain_from_inputs(project['inputs'])
        domain_correct = detected_domain == project['domain']
        
        # Test stakeholders generation  
        stakeholders = _generate_domain_specific_stakeholders(detected_domain)
        
        # Check if expected stakeholders are present
        stakeholder_matches = []
        for expected in project['expected_stakeholders']:
            if expected.lower() in stakeholders.lower():
                stakeholder_matches.append(expected)
        
        stakeholders_correct = len(stakeholder_matches) >= 2  # At least 2 expected stakeholders found
        
        print(f"Domain Detection: {detected_domain} {'✅' if domain_correct else '❌'}")
        print(f"Stakeholders: {stakeholders}")
        print(f"Expected stakeholders found: {stakeholder_matches} {'✅' if stakeholders_correct else '❌'}")
        
        success = domain_correct and stakeholders_correct
        results.append(success)
        
        print(f"Overall: {'✅ PASS' if success else '❌ FAIL'}")
        print()
    
    # Summary
    print("=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    domain_names = [p['domain'] for p in test_projects]
    for i, (project, result) in enumerate(zip(test_projects, results)):
        status = "✅" if result else "❌"
        print(f"{status} {project['domain'].upper()}: {project['name']}")
    
    print(f"\nOVERALL RESULTS: {passed}/{total} domains working correctly")
    
    if passed == total:
        print("🎉🎉🎉 ALL 9 DOMAINS WORKING PERFECTLY! 🎉🎉🎉")
        print("✅ Marketing, Healthcare, Banking, E-commerce, Education, Insurance")
        print("✅ NEW: Mutual Fund, Alternative Investment Fund (AIF), Finance")
        print("\nThe BA Tool now supports comprehensive domain-specific content generation")
        print("for all major business verticals including the requested finance domains!")
    else:
        print("⚠️  Some domains need attention")
        failed_domains = [test_projects[i]['domain'] for i, result in enumerate(results) if not result]
        print(f"Failed domains: {failed_domains}")
    
    return passed == total

if __name__ == "__main__":
    success = test_all_9_domains_final()
    print(f"\n{'='*60}")
    print(f"COMPREHENSIVE TEST RESULT: {'SUCCESS' if success else 'NEEDS ATTENTION'}")
    print(f"{'='*60}")