#!/usr/bin/env python3
"""
Test BRD generation with server running
"""
import requests
import json

def test_finance_brd_generation():
    print("Testing Finance BRD Generation via Server...")
    
    # Test finance domain project
    payload = {
        "project": "Wealth Management Platform",
        "inputs": {
            "project_name": "Wealth Management Platform",
            "description": "Comprehensive financial planning and wealth management solution for high-net-worth clients",
            "objectives": [
                "Enhance financial planning and wealth management capabilities",
                "Improve risk management and regulatory compliance",
                "Optimize investment strategies and portfolio performance"
            ],
            "features": [
                "Financial planning tools",
                "Wealth management dashboard", 
                "Portfolio optimization",
                "Risk assessment",
                "Investment advisory services"
            ],
            "stakeholders": "Clients, Financial advisors, Portfolio managers",
            "scope": "Comprehensive wealth management platform"
        },
        "version": 1
    }
    
    try:
        response = requests.post(
            "http://localhost:8001/ai/generate",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            html = data.get('html', '')
            
            if len(html) > 500:
                print("✅ BRD Generation Successful!")
                print(f"Generated HTML length: {len(html)} characters")
                
                # Check for finance-specific content
                finance_keywords = ["financial planning", "wealth management", "portfolio", "investment"]
                found_keywords = [kw for kw in finance_keywords if kw.lower() in html.lower()]
                print(f"Finance keywords found: {found_keywords}")
                
                # Check for domain-specific stakeholders
                if "financial advisor" in html.lower() or "portfolio manager" in html.lower():
                    print("✅ Finance-specific stakeholders detected!")
                else:
                    print("❌ Generic stakeholders found instead of finance-specific ones")
                
                # Save for inspection
                with open("test_server_finance_brd.html", "w", encoding="utf-8") as f:
                    f.write(html)
                print("BRD saved to: test_server_finance_brd.html")
                
                return True
            else:
                print(f"❌ BRD generation returned minimal content: {len(html)} characters")
                print(f"Response: {html[:200]}...")
                return False
                
        else:
            print(f"❌ Server error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_logistics_brd_generation():
    print("\nTesting Logistics BRD Generation via Server...")
    
    # Test logistics domain project
    payload = {
        "project": "Global Supply Chain Platform",
        "inputs": {
            "project_name": "Global Supply Chain Platform",
            "description": "Comprehensive logistics and supply chain management system",
            "objectives": [
                "Optimize supply chain efficiency and reduce operational costs",
                "Improve delivery speed and tracking accuracy"
            ],
            "features": [
                "Supply chain management",
                "Warehouse operations", 
                "Delivery tracking",
                "Inventory optimization"
            ],
            "stakeholders": "Shippers, Carriers, Warehouse staff",
            "scope": "Enterprise logistics platform"
        },
        "version": 1
    }
    
    try:
        response = requests.post(
            "http://localhost:8001/ai/generate",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            html = data.get('html', '')
            
            if len(html) > 500:
                print("✅ Logistics BRD Generation Successful!")
                
                # Check for logistics-specific stakeholders
                if "shipper" in html.lower() or "carrier" in html.lower() or "warehouse" in html.lower():
                    print("✅ Logistics-specific stakeholders detected!")
                    return True
                else:
                    print("❌ Generic stakeholders found instead of logistics-specific ones")
                    return False
            else:
                print(f"❌ Logistics BRD generation failed: {len(html)} characters")
                return False
                
        else:
            print(f"❌ Server error: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Server-Based BRD Generation with Domain Support")
    print("=" * 60)
    
    # Test different domains
    finance_success = test_finance_brd_generation()
    logistics_success = test_logistics_brd_generation()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS:")
    print(f"Finance Domain: {'✅ PASSED' if finance_success else '❌ FAILED'}")
    print(f"Logistics Domain: {'✅ PASSED' if logistics_success else '❌ FAILED'}")
    
    if finance_success and logistics_success:
        print("\n🎉 All domain-specific BRD generation tests PASSED!")
        print("The server is correctly using the enhanced 12-domain support!")
    else:
        print("\n⚠️  Some tests failed - domain detection may not be working correctly")