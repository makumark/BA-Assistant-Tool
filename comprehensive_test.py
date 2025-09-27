#!/usr/bin/env python3
"""Comprehensive test of intelligent FRD generation across domains."""

import requests
import json
import time

API_URL = "http://localhost:8001/ai/frd/generate"

# Test cases for different domains
test_cases = [
    {
        "name": "E-commerce Checkout",
        "domain": "E-commerce",
        "payload": {
            "project": "E-commerce Checkout System",
            "brd": """
# Business Requirements Document - E-commerce Checkout System

## Executive Summary
Develop a secure checkout system for online retail that processes customer payments with credit card validation.

## Business Requirements
- Implement secure payment processing with credit card and CVV validation
- Create shopping cart management with real-time item updates
- Develop order confirmation and tracking system
- Establish inventory validation during checkout
- Build customer account management integration

## Business Objectives
- Process payments within 5-10 seconds
- Achieve 99.9% payment success rate
- Reduce cart abandonment by 30%
- Ensure PCI DSS compliance
""",
            "version": 1
        },
        "expected_features": ["16 digits", "CVV", "3 digits", "payment", "cart", "real-time"]
    },
    {
        "name": "Healthcare Patient System", 
        "domain": "Healthcare",
        "payload": {
            "project": "Patient Management System",
            "brd": """
# Business Requirements Document - Patient Management System

## Executive Summary
Develop a HIPAA-compliant patient registration and appointment scheduling system for healthcare providers.

## Business Requirements
- Implement patient registration with medical history capture
- Create appointment scheduling with provider availability
- Develop medical record access with security controls
- Establish insurance verification and billing integration
- Build clinical documentation workflow

## Business Objectives
- Ensure HIPAA compliance for patient data
- Reduce appointment scheduling time by 50%
- Improve patient data accuracy by 90%
- Enable real-time insurance verification
""",
            "version": 1
        },
        "expected_features": ["HIPAA", "patient", "medical", "insurance", "appointment", "verification"]
    },
    {
        "name": "Banking Authentication",
        "domain": "Banking", 
        "payload": {
            "project": "Online Banking Authentication System",
            "brd": """
# Business Requirements Document - Banking Authentication System

## Executive Summary
Develop a secure multi-factor authentication system for online banking with transaction processing capabilities.

## Business Requirements
- Implement multi-factor authentication with biometric support
- Create secure transaction processing with validation
- Develop account balance and statement management
- Establish fraud detection and security monitoring
- Build customer account access controls

## Business Objectives
- Ensure regulatory compliance for financial services
- Reduce authentication time to under 60 seconds
- Achieve 99.99% system availability
- Implement real-time fraud detection
""",
            "version": 1
        },
        "expected_features": ["multi-factor", "authentication", "transaction", "fraud", "60 seconds", "balance"]
    }
]

def run_comprehensive_test():
    print("🧪 Comprehensive Intelligent FRD Generation Test")
    print("=" * 60)
    
    total_tests = len(test_cases)
    passed_tests = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}/{total_tests}: {test_case['name']}")
        print("-" * 40)
        
        try:
            # Make API request
            response = requests.post(API_URL, json=test_case['payload'], timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                frd_html = result.get('html', '')  # Fixed: API returns 'html' not 'frd_html'
                
                print(f"✅ API Success: {len(frd_html)} characters generated")
                
                # Check for domain-specific intelligent features
                feature_checks = []
                for feature in test_case['expected_features']:
                    found = feature.lower() in frd_html.lower()
                    feature_checks.append((feature, found))
                    status = "✅" if found else "❌"
                    print(f"  {status} {feature}")
                
                # Check for general intelligent features
                general_checks = [
                    ("Functional Requirements", "FR-" in frd_html),
                    ("Acceptance Criteria", "Acceptance Criteria" in frd_html),
                    ("Validation Rules", "Validation Rules" in frd_html),
                    ("Domain Detection", test_case['domain'].lower() in frd_html.lower())
                ]
                
                print("  📊 General Features:")
                for check_name, passed in general_checks:
                    status = "✅" if passed else "❌"
                    print(f"    {status} {check_name}")
                
                # Calculate success rate
                all_checks = feature_checks + general_checks
                passed_checks = sum(1 for _, passed in all_checks if passed)
                success_rate = (passed_checks / len(all_checks)) * 100
                
                print(f"  📈 Success Rate: {passed_checks}/{len(all_checks)} ({success_rate:.1f}%)")
                
                if success_rate >= 70:  # 70% threshold for pass
                    print(f"  🎉 PASS: {test_case['name']}")
                    passed_tests += 1
                else:
                    print(f"  ⚠️  PARTIAL: {test_case['name']} needs improvement")
                
                # Save output for manual inspection
                filename = f"test_{test_case['name'].lower().replace(' ', '_')}.html"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(frd_html)
                print(f"  💾 Saved: {filename}")
                
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Test Failed: {e}")
        
        # Small delay between tests
        if i < total_tests:
            time.sleep(1)
    
    # Final results
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS")
    print("=" * 60)
    
    overall_success = (passed_tests / total_tests) * 100
    print(f"Tests Passed: {passed_tests}/{total_tests} ({overall_success:.1f}%)")
    
    if overall_success >= 70:
        print("🎉 SUCCESS: Intelligent FRD generation is working excellently!")
        print("🧠 The system generates context-aware acceptance criteria and validations.")
        print("🌟 Domain-specific intelligence is functioning across multiple industries.")
    elif overall_success >= 50:
        print("⚠️  PARTIAL SUCCESS: Core functionality working, some improvements needed.")
    else:
        print("❌ NEEDS WORK: Significant improvements required for intelligent features.")
    
    print(f"\n📝 Generated files for manual inspection:")
    for test_case in test_cases:
        filename = f"test_{test_case['name'].lower().replace(' ', '_')}.html"
        print(f"  • {filename}")

if __name__ == "__main__":
    run_comprehensive_test()