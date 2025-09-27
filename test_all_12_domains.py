#!/usr/bin/env python3
"""
Test script for the new business domains: Logistics, Credit Cards & Airline, and Payment
"""

import sys
import os
import json

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'react-python-auth', 'backend')
sys.path.insert(0, backend_path)

from app.services.ai_service import _detect_domain_from_inputs, _generate_domain_specific_stakeholders, _generate_domain_specific_objectives, _generate_domain_specific_scope

def test_new_business_domains():
    print("=== Testing New Business Domain Support ===\n")
    
    # Test cases for the three new business domains
    test_cases = [
        {
            "domain": "Logistics",
            "project_name": "Smart Logistics Management Platform",
            "description": "Comprehensive supply chain and logistics management system with real-time tracking",
            "inputs": {
                "project_name": "Smart Logistics Management Platform",
                "description": "Platform for supply chain management, warehouse operations, and delivery tracking",
                "features": ["Supply chain optimization", "Warehouse management", "Delivery tracking", "Inventory management", "Distribution network"]
            }
        },
        {
            "domain": "Credit Cards & Airline",
            "project_name": "Airline Rewards Credit Card System",
            "description": "Co-branded credit card platform with airline partnerships and loyalty rewards",
            "inputs": {
                "project_name": "Airline Rewards Credit Card System", 
                "description": "Credit card system with airline partnerships, miles tracking, and loyalty rewards management",
                "features": ["Credit card management", "Airline miles tracking", "Rewards program", "Loyalty benefits", "Co-brand partnerships"]
            }
        },
        {
            "domain": "Payment",
            "project_name": "Digital Payment Gateway Platform",
            "description": "Comprehensive payment processing platform with digital wallet and UPI integration",
            "inputs": {
                "project_name": "Digital Payment Gateway Platform",
                "description": "Payment gateway platform supporting digital wallets, UPI, and merchant payment processing",
                "features": ["Payment gateway", "Digital wallet", "UPI integration", "Merchant services", "Payment security"]
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
            "Smart Logistics Management Platform": "logistics",
            "Airline Rewards Credit Card System": "creditcard", 
            "Digital Payment Gateway Platform": "payment"
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
    print(f"New Business Domain Tests: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All new business domains working correctly!")
    else:
        print("⚠️  Some business domains need attention")
        for result in results:
            if not result['success']:
                print(f"  - {result['test']}: expected {result['expected_domain']}, got {result['detected_domain']}")
    
    return results

def test_all_12_domains_comprehensive():
    """Test all 12 domains to ensure nothing was broken"""
    print("\n=== Comprehensive Test: All 12 Domains ===\n")
    
    all_test_cases = [
        {"name": "Marketing Campaign Platform", "keywords": ["campaign", "email", "automation"], "expected": "marketing"},
        {"name": "Patient Management System", "keywords": ["patient", "medical", "clinical"], "expected": "healthcare"},
        {"name": "Banking Transaction System", "keywords": ["account", "transaction", "banking"], "expected": "banking"},
        {"name": "E-commerce Platform", "keywords": ["product", "cart", "checkout"], "expected": "ecommerce"},
        {"name": "Student Learning Management", "keywords": ["student", "course", "learning"], "expected": "education"},
        {"name": "Insurance Claims System", "keywords": ["policy", "claim", "premium"], "expected": "insurance"},
        {"name": "Mutual Fund Platform", "keywords": ["mutual fund", "nav", "sip"], "expected": "mutualfund"},
        {"name": "AIF Management System", "keywords": ["alternative investment", "hedge fund", "aif"], "expected": "aif"},
        {"name": "Financial Planning Platform", "keywords": ["wealth management", "financial planning", "portfolio"], "expected": "finance"},
        {"name": "Supply Chain Management", "keywords": ["supply chain", "warehouse", "logistics"], "expected": "logistics"},
        {"name": "Airline Credit Card System", "keywords": ["credit card", "airline", "rewards"], "expected": "creditcard"},
        {"name": "Payment Gateway Platform", "keywords": ["payment gateway", "digital wallet", "upi"], "expected": "payment"}
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
    # Test the new business domains
    business_results = test_new_business_domains()
    
    # Test all domains comprehensively
    all_success = test_all_12_domains_comprehensive()
    
    print(f"\n=== FINAL RESULTS ===")
    print(f"New business domains added successfully: {all(r['success'] for r in business_results)}")
    print(f"All 12 domains working: {all_success}")
    
    if all_success:
        print("🎉🎉🎉 COMPLETE SUCCESS: ALL 12 DOMAINS OPERATIONAL! 🎉🎉🎉")
        print("✅ Original 6: Marketing, Healthcare, Banking, E-commerce, Education, Insurance")
        print("✅ Finance 3: Mutual Fund, AIF, Finance")
        print("✅ Business 3: Logistics, Credit Cards & Airline, Payment")
    else:
        print("⚠️  Some domains need attention")