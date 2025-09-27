import requests
import json

# Test the enhanced FRD generation API
url = "http://localhost:8001/ai/frd/generate"

# E-commerce test case
test_payload = {
    "project": "E-commerce Checkout System", 
    "brd_text": """
# Business Requirements Document - E-commerce Checkout System

## Executive Summary
Develop a secure and user-friendly checkout system for an e-commerce platform that processes customer payments efficiently.

## Business Requirements
- Implement secure payment processing with credit card validation
- Create shopping cart management with real-time updates
- Develop user authentication and account management
- Establish order confirmation and tracking system
- Build inventory management integration

## Project Scope
The checkout system will handle payment processing, order management, and customer account operations for online retail.

## Business Objectives  
- Reduce cart abandonment rate by 25%
- Process payments within 10 seconds
- Achieve 99.9% payment success rate
- Ensure PCI DSS compliance for credit card processing
""",
    "version": 1
}

print("🧪 Testing Intelligent FRD Generation API...")
print("=" * 60)

try:
    response = requests.post(url, json=test_payload, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        frd_html = result.get('frd_html', '')
        
        print("✅ API Request Successful!")
        print(f"📊 Generated HTML Length: {len(frd_html)} characters")
        
        # Check for intelligent content
        intelligent_checks = [
            ("Functional Requirements", "FR-" in frd_html),
            ("Acceptance Criteria", "Acceptance Criteria" in frd_html),
            ("Validation Rules", "Validation Rules" in frd_html),
            ("Credit Card Validation", "16 digits" in frd_html),
            ("CVV Validation", "CVV" in frd_html and "3 digits" in frd_html),
            ("Payment Timeout", "5-10 seconds" in frd_html or "payment" in frd_html.lower()),
            ("E-commerce Domain", "ecommerce" in frd_html.lower()),
            ("Real-time Updates", "real-time" in frd_html.lower()),
            ("PCI Compliance", "PCI" in frd_html or "security" in frd_html.lower())
        ]
        
        print("\n📋 Intelligent Content Analysis:")
        for check_name, passed in intelligent_checks:
            status = "✅" if passed else "❌"
            print(f"{status} {check_name}")
        
        passed_checks = sum(1 for _, passed in intelligent_checks if passed)
        print(f"\n📈 Intelligence Score: {passed_checks}/{len(intelligent_checks)} ({passed_checks/len(intelligent_checks)*100:.1f}%)")
        
        # Show sample acceptance criteria
        if "Acceptance Criteria" in frd_html:
            start = frd_html.find("Acceptance Criteria")
            sample = frd_html[start:start+300] if start != -1 else ""
            print(f"\n📄 Sample Acceptance Criteria:")
            print("-" * 40)
            print(sample + "..." if len(sample) == 300 else sample)
        
        # Save for manual inspection
        with open('intelligent_frd_test.html', 'w', encoding='utf-8') as f:
            f.write(frd_html)
        print(f"\n💾 Full FRD saved to: intelligent_frd_test.html")
        
        # Success indicators
        if passed_checks >= 6:
            print("\n🎉 SUCCESS: Intelligent FRD generation is working!")
            print("🧠 The system is generating context-aware acceptance criteria and validations.")
        else:
            print("\n⚠️  PARTIAL: Some intelligent features may need adjustment.")
            
    else:
        print(f"❌ API Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ Network Error: {e}")
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    import traceback
    traceback.print_exc()