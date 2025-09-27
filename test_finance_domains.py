#!/usr/bin/env python3
"""
Test script for the new finance domains: Mutual Fund, AIF, and Finance
"""

import sys
import os
import json

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'react-python-auth', 'backend')
sys.path.insert(0, backend_path)

from app.services.ai_service import _detect_domain_from_inputs, _generate_domain_specific_stakeholders, _generate_domain_specific_objectives, _generate_domain_specific_scope

def test_finance_domains():
    print("=== Testing Finance Domain Support ===\n")
    
    # Test cases for the three new finance domains
    test_cases = [
        {
            "domain": "Mutual Fund",
            "project_name": "Mutual Fund Investment Platform",
            "description": "A comprehensive platform for mutual fund investments, SIP management, and NAV tracking",
            "inputs": {
                "project_name": "Mutual Fund Investment Platform",
                "description": "Platform for mutual fund investments with SIP, portfolio tracking, and NAV calculations",
                "features": ["Portfolio management", "SIP automation", "NAV tracking", "Investment recommendations", "Dividend management"]
            }
        },
        {
            "domain": "Alternative Investment Fund (AIF)",
            "project_name": "AIF Management System",
            "description": "Alternative investment fund management platform for hedge funds and private equity",
            "inputs": {
                "project_name": "AIF Management System", 
                "description": "Platform for managing alternative investment funds, private equity, and hedge fund operations",
                "features": ["Fund administration", "Investor onboarding", "Performance tracking", "Regulatory reporting", "Risk management"]
            }
        },
        {
            "domain": "Finance",
            "project_name": "Wealth Management Platform",
            "description": "Comprehensive financial planning and wealth management solution",
            "inputs": {
                "project_name": "Wealth Management Platform",
                "description": "Platform for financial planning, asset allocation, and wealth management services",
                "features": ["Financial planning", "Risk assessment", "Portfolio optimization", "Client reporting", "Compliance management"]
            }
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['domain']}")
        print("-" * 50)
        
        # Test domain detection
        detected_domain = _detect_domain_from_inputs(test_case['inputs'])
        print(f"Detected Domain: {detected_domain}")
        
        # Test stakeholders generation
        stakeholders = _generate_domain_specific_stakeholders(detected_domain)
        print(f"Stakeholders: {stakeholders}")
        
        # Test objectives generation
        objectives = _generate_domain_specific_objectives(detected_domain)
        print(f"Objectives: {objectives}")
        
        # Test scope generation
        scope = _generate_domain_specific_scope(detected_domain, test_case['project_name'])
        print(f"Scope: {scope}")
        
        # Validate results
        expected_domains = {
            "Mutual Fund Investment Platform": "mutualfund",
            "AIF Management System": "aif", 
            "Wealth Management Platform": "finance"
        }
        
        expected_domain = expected_domains[test_case['project_name']]
        success = detected_domain == expected_domain
        
        results.append({
            "test": test_case['domain'],
            "project": test_case['project_name'],
            "expected_domain": expected_domain,
            "detected_domain": detected_domain,
            "success": success,
            "stakeholders": stakeholders,
            "objectives": objectives,
            "scope": scope
        })
        
        print(f"✅ PASS" if success else f"❌ FAIL (expected {expected_domain}, got {detected_domain})")
        print("\n")
    
    # Summary
    print("=== SUMMARY ===")
    passed = sum(1 for r in results if r['success'])
    total = len(results)
    print(f"Finance Domain Tests: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All finance domains working correctly!")
    else:
        print("⚠️  Some finance domains need attention")
        for result in results:
            if not result['success']:
                print(f"  - {result['test']}: expected {result['expected_domain']}, got {result['detected_domain']}")
    
    return results

def test_all_domains_comprehensive():
    """Test all 9 domains to ensure nothing was broken"""
    print("\n=== Comprehensive Test: All 9 Domains ===\n")
    
    all_test_cases = [
        {"name": "Marketing Campaign Platform", "keywords": ["campaign", "email", "automation"], "expected": "marketing"},
        {"name": "Patient Management System", "keywords": ["patient", "medical", "clinical"], "expected": "healthcare"},
        {"name": "Banking Transaction System", "keywords": ["account", "transaction", "payment"], "expected": "banking"},
        {"name": "E-commerce Platform", "keywords": ["product", "cart", "checkout"], "expected": "ecommerce"},
        {"name": "Student Learning Management", "keywords": ["student", "course", "learning"], "expected": "education"},
        {"name": "Insurance Claims System", "keywords": ["policy", "claim", "premium"], "expected": "insurance"},
        {"name": "Mutual Fund Platform", "keywords": ["mutual fund", "nav", "sip"], "expected": "mutualfund"},
        {"name": "AIF Management System", "keywords": ["alternative investment", "hedge fund", "aif"], "expected": "aif"},
        {"name": "Financial Planning Platform", "keywords": ["wealth management", "financial planning", "portfolio"], "expected": "finance"}
    ]
    
    results = []
    for test_case in all_test_cases:
        inputs = {
            "project_name": test_case["name"],
            "description": f"System involving {', '.join(test_case['keywords'])}",
            "features": test_case["keywords"]
        }
        
        detected = _detect_domain_from_inputs(inputs)
        success = detected == test_case["expected"]
        results.append(success)
        
        status = "✅" if success else "❌"
        print(f"{status} {test_case['name']}: {detected} (expected: {test_case['expected']})")
    
    passed = sum(results)
    total = len(results)
    print(f"\nOverall: {passed}/{total} domains working correctly")
    
    return passed == total

if __name__ == "__main__":
    # Test the new finance domains
    finance_results = test_finance_domains()
    
    # Test all domains comprehensively
    all_success = test_all_domains_comprehensive()
    
    print(f"\n=== FINAL RESULTS ===")
    print(f"Finance domains added successfully: {all(r['success'] for r in finance_results)}")
    print(f"All 9 domains working: {all_success}")