#!/usr/bin/env python3
"""
Test the updated domain-specific validation criteria
"""
import sys
import os

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'react-python-auth', 'backend')
sys.path.insert(0, backend_path)

from app.services.ai_service import generate_brd_html

def test_finance_validation_fix():
    print("=== Testing Finance Domain Validation Criteria Fix ===\n")
    
    finance_inputs = {
        "project_name": "Elite Wealth Management Platform",
        "description": "Comprehensive financial planning and investment advisory platform for high-net-worth clients",
        "objectives": [
            "Enhance financial planning and wealth management capabilities",
            "Improve risk management and regulatory compliance",
            "Optimize investment strategies and portfolio performance"
        ],
        "features": [
            "Financial planning tools",
            "Investment portfolio management", 
            "Risk assessment and profiling",
            "Wealth management advisory",
            "Regulatory compliance tracking"
        ],
        "stakeholders": "High-net-worth clients, Financial advisors, Portfolio managers",
        "scope": "Comprehensive wealth management platform for affluent clients"
    }
    
    print("Input Details:")
    print(f"Project: {finance_inputs['project_name']}")
    print(f"Features: {', '.join(finance_inputs['features'][:3])}...")
    print()
    
    try:
        print("Generating finance BRD with enhanced fallback...")
        brd_html = generate_brd_html(
            project="Elite Wealth Management Platform",
            inputs=finance_inputs,
            version=1
        )
        
        if brd_html and len(brd_html) > 1000:
            print("✅ Finance BRD Generated Successfully!")
            print(f"Generated BRD length: {len(brd_html)} characters")
            
            # Check for finance-specific validation criteria
            finance_validation_keywords = [
                "client financial assessment",
                "investment recommendations", 
                "portfolio rebalancing",
                "regulatory compliance",
                "fiduciary standards"
            ]
            
            found_validations = []
            for keyword in finance_validation_keywords:
                if keyword.lower() in brd_html.lower():
                    found_validations.append(keyword)
            
            print(f"Finance-specific validations found: {found_validations}")
            
            # Check for finance stakeholders
            finance_stakeholders = ["financial advisor", "portfolio manager", "client"]
            found_stakeholders = []
            for stakeholder in finance_stakeholders:
                if stakeholder.lower() in brd_html.lower():
                    found_stakeholders.append(stakeholder)
            
            print(f"Finance stakeholders found: {found_stakeholders}")
            
            # Save the output
            with open("test_finance_validation_fix.html", "w", encoding="utf-8") as f:
                f.write(brd_html)
            print("BRD saved to: test_finance_validation_fix.html")
            
            # Check if it's still using generic validations
            if "mandatory master data fields" in brd_html.lower():
                print("❌ Still using generic validation criteria!")
                return False
            elif len(found_validations) >= 2:
                print("✅ Using finance-specific validation criteria!")
                return True
            else:
                print("⚠️  Some finance validations found, but not comprehensive")
                return False
                
        else:
            print(f"❌ BRD generation failed: {len(brd_html) if brd_html else 0} characters")
            return False
            
    except Exception as e:
        print(f"❌ Error during BRD generation: {str(e)}")
        return False

def test_logistics_validation():
    print("\n=== Testing Logistics Domain Validation Criteria ===\n")
    
    logistics_inputs = {
        "project_name": "Global Express Logistics Platform",
        "description": "Advanced supply chain and logistics management system",
        "features": ["supply chain tracking", "warehouse management", "delivery optimization"],
        "objectives": ["Optimize delivery efficiency", "Reduce logistics costs"]
    }
    
    try:
        brd_html = generate_brd_html(
            project="Global Express Logistics Platform", 
            inputs=logistics_inputs,
            version=1
        )
        
        if brd_html and len(brd_html) > 500:
            # Check for logistics-specific validations
            logistics_validations = ["shipment tracking", "delivery confirmation", "warehouse inventory"]
            found = [v for v in logistics_validations if v.lower() in brd_html.lower()]
            
            print(f"Logistics validations found: {found}")
            return len(found) >= 2
        else:
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing Domain-Specific Validation Criteria Fix")
    print("=" * 60)
    
    finance_success = test_finance_validation_fix()
    logistics_success = test_logistics_validation()
    
    print("\n" + "=" * 60)
    print("📊 VALIDATION FIX RESULTS:")
    print(f"Finance validation criteria: {'✅ FIXED' if finance_success else '❌ STILL GENERIC'}")
    print(f"Logistics validation criteria: {'✅ WORKING' if logistics_success else '❌ NOT WORKING'}")
    
    if finance_success and logistics_success:
        print("\n🎉 Domain-specific validation criteria are now working!")
        print("The issue with generic 'mandatory master data fields' is RESOLVED!")
    else:
        print("\n⚠️  Validation criteria still need attention")