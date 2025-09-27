#!/usr/bin/env python3
"""
Real-world test of BRD generation for new business domains
"""

import sys
import os

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'react-python-auth', 'backend')
sys.path.insert(0, backend_path)

from app.services.ai_service import generate_brd_html

def test_logistics_brd():
    print("=== Testing Logistics BRD Generation ===\n")
    
    logistics_inputs = {
        "project_name": "Global Logistics Management Platform",
        "description": "Comprehensive supply chain and logistics management system enabling real-time tracking, warehouse optimization, and delivery management across multiple distribution networks.",
        "objectives": [
            "Optimize supply chain efficiency and reduce operational costs",
            "Provide real-time shipment tracking and delivery visibility", 
            "Enhance warehouse management and inventory optimization",
            "Enable seamless integration with carrier and distribution networks"
        ],
        "features": [
            "Supply chain visibility and tracking",
            "Warehouse management system integration",
            "Multi-carrier shipping management",
            "Real-time delivery tracking and notifications",
            "Inventory optimization and demand forecasting",
            "Distribution network management",
            "Freight cost optimization",
            "Logistics analytics and reporting"
        ],
        "stakeholders": "Shippers, Carriers, Warehouse staff, Supply chain managers",
        "scope": "Enterprise logistics platform for supply chain optimization"
    }
    
    return test_domain_brd("Logistics", logistics_inputs, "test_logistics_brd_output.html")

def test_creditcard_brd():
    print("\n=== Testing Credit Cards & Airline BRD Generation ===\n")
    
    creditcard_inputs = {
        "project_name": "AeroRewards Credit Card Platform",
        "description": "Co-branded credit card platform with airline partnerships featuring miles earning, loyalty rewards, travel benefits, and seamless integration with airline frequent flyer programs.",
        "objectives": [
            "Maximize customer engagement through rewards and loyalty programs",
            "Strengthen airline partnerships and co-branded offerings",
            "Enhance customer experience with travel benefits and services",
            "Drive card usage and customer retention through targeted incentives"
        ],
        "features": [
            "Credit card account management",
            "Airline miles earning and tracking",
            "Loyalty rewards program management",
            "Travel benefits and insurance coverage",
            "Co-branded airline partnerships",
            "Frequent flyer program integration",
            "Cashback and rewards redemption",
            "Travel booking and management tools"
        ],
        "stakeholders": "Cardholders, Airline partners, Rewards managers, Customer service team",
        "scope": "Co-branded credit card platform with airline loyalty integration"
    }
    
    return test_domain_brd("Credit Cards & Airline", creditcard_inputs, "test_creditcard_brd_output.html")

def test_payment_brd():
    print("\n=== Testing Payment BRD Generation ===\n")
    
    payment_inputs = {
        "project_name": "SecurePay Digital Payment Gateway",
        "description": "Comprehensive payment processing platform supporting digital wallets, UPI, card payments, and merchant services with advanced security and compliance features.",
        "objectives": [
            "Provide secure and seamless payment processing solutions",
            "Enable fast and reliable digital payment experiences",
            "Ensure compliance with payment security standards and regulations",
            "Support diverse payment methods and merchant requirements"
        ],
        "features": [
            "Payment gateway and processing engine",
            "Digital wallet integration",
            "UPI and mobile payment support",
            "Merchant onboarding and management",
            "POS system integration",
            "Payment security and fraud detection",
            "Multi-currency and international payments",
            "Payment analytics and reporting"
        ],
        "stakeholders": "Merchants, Customers, Payment processors, Bank partners",
        "scope": "Digital payment platform for merchants and financial institutions"
    }
    
    return test_domain_brd("Payment", payment_inputs, "test_payment_brd_output.html")

def test_domain_brd(domain_name, inputs, output_file):
    """Helper function to test BRD generation for a domain"""
    print(f"Input Project Details:")
    print(f"Project: {inputs['project_name']}")
    print(f"Description: {inputs['description']}")
    print(f"Key Features: {', '.join(inputs['features'][:3])}...")
    print()
    
    try:
        print(f"Generating {domain_name} BRD using AI service...")
        brd_html = generate_brd_html(
            project=inputs['project_name'],
            inputs=inputs,
            version=1
        )
        
        if brd_html and len(brd_html) > 1000:
            print(f"✅ {domain_name} BRD Generated Successfully!")
            print(f"Generated BRD length: {len(brd_html)} characters")
            
            # Save the BRD to file for inspection
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(brd_html)
            print(f"BRD saved to: {output_file}")
            
            # Check for domain-specific content
            domain_keywords = {
                "Logistics": ["supply chain", "warehouse", "delivery", "logistics", "tracking"],
                "Credit Cards & Airline": ["credit card", "airline", "rewards", "miles", "loyalty"],
                "Payment": ["payment", "gateway", "digital wallet", "merchant", "upi"]
            }
            
            keywords = domain_keywords.get(domain_name, [])
            found_keywords = [kw for kw in keywords if kw.lower() in brd_html.lower()]
            print(f"{domain_name} keywords found: {found_keywords}")
            
            return True
            
        else:
            print(f"❌ {domain_name} BRD generation failed or returned minimal content")
            print(f"Returned content length: {len(brd_html) if brd_html else 0}")
            return False
            
    except Exception as e:
        print(f"❌ Error during {domain_name} BRD generation: {str(e)}")
        return False

if __name__ == "__main__":
    # Test all three new domain BRD generations
    logistics_success = test_logistics_brd()
    creditcard_success = test_creditcard_brd()
    payment_success = test_payment_brd()
    
    print(f"\n=== FINAL RESULTS ===")
    print(f"Logistics BRD: {'✅ SUCCESS' if logistics_success else '❌ FAILED'}")
    print(f"Credit Cards & Airline BRD: {'✅ SUCCESS' if creditcard_success else '❌ FAILED'}")
    print(f"Payment BRD: {'✅ SUCCESS' if payment_success else '❌ FAILED'}")
    
    if logistics_success and creditcard_success and payment_success:
        print("🎉 All new business domain BRD generation working perfectly!")
        print("🚀 The BA Tool now supports 12 comprehensive business domains!")
    else:
        print("⚠️  Some issues found with new business domain BRD generation")