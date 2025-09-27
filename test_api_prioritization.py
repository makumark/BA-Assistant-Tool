"""
Test the prioritization API endpoint directly
"""

import requests
import json

# Sample E-commerce FRD HTML for testing
ecommerce_frd_html = """
<div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
  <h1>Functional Requirements Document</h1>
  <h2>E-commerce Shopping Platform - Version 1</h2>
  
  <h3>EPIC-01: User Authentication & Account Management</h3>
  <h4>FR-001: User Login System</h4>
  <p><strong>Description:</strong> Users need to authenticate securely to access personalized features</p>
  <p>As a customer, I want to login to my account, so that I can access my personal shopping features</p>
  
  <h4>FR-002: User Registration</h4>
  <p><strong>Description:</strong> New users need to create accounts</p>
  <p>As a new customer, I want to register for an account, so that I can save my preferences and order history</p>
  
  <h3>EPIC-02: Product Discovery & Search</h3>
  <h4>FR-003: Product Search</h4>
  <p><strong>Description:</strong> Users need to find products efficiently</p>
  <p>As a customer, I want to search for products, so that I can find items I'm interested in purchasing</p>
  
  <h4>FR-004: Product Catalog Browsing</h4>
  <p><strong>Description:</strong> Users browse product categories</p>
  <p>As a customer, I want to browse product categories, so that I can discover new items</p>
  
  <h3>EPIC-03: Shopping Cart & Checkout</h3>
  <h4>FR-005: Add to Cart</h4>
  <p><strong>Description:</strong> Users add products to shopping cart</p>
  <p>As a customer, I want to add products to my cart, so that I can collect items for purchase</p>
  
  <h4>FR-006: Checkout Process</h4>
  <p><strong>Description:</strong> Users complete purchase transactions</p>
  <p>As a customer, I want to checkout and pay for my items, so that I can complete my purchase</p>
  
  <h4>FR-007: Payment Processing</h4>
  <p><strong>Description:</strong> Secure payment handling</p>
  <p>As a customer, I want to pay securely with my credit card, so that I can complete transactions safely</p>
  
  <h3>EPIC-04: User Experience Features</h3>
  <h4>FR-008: Wishlist Management</h4>
  <p><strong>Description:</strong> Users save items for later</p>
  <p>As a customer, I want to save items to a wishlist, so that I can purchase them later</p>
  
  <h4>FR-009: Product Reviews</h4>
  <p><strong>Description:</strong> Users read and write product reviews</p>
  <p>As a customer, I want to read product reviews, so that I can make informed purchasing decisions</p>
  
  <h4>FR-010: Recommendation Engine</h4>
  <p><strong>Description:</strong> AI-powered product recommendations</p>
  <p>As a customer, I want to see personalized product recommendations, so that I can discover relevant items</p>
</div>
"""

def test_prioritization_api():
    print("🔄 Testing Prioritization API Endpoint...")
    
    # Test the API endpoint
    url = "http://localhost:8001/ai/frd/prioritize"
    payload = {
        "project": "E-commerce Shopping Platform",
        "frd_html": ecommerce_frd_html,
        "version": 1
    }
    
    try:
        print(f"📡 Sending request to: {url}")
        response = requests.post(url, json=payload, timeout=30)
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prioritization successful!")
            print(f"   Project: {data['project']}")
            print(f"   Domain: {data['domain']}")
            print(f"   Total Requirements: {data['total_requirements']}")
            print(f"   MoSCoW Distribution: {data['moscow_distribution']['counts']}")
            
            print(f"\n🎯 Top 5 Prioritized Requirements:")
            for i, req in enumerate(data['prioritized_requirements'][:5]):
                print(f"   #{req['priority_rank']} {req['id']}: {req['goal'][:40]}...")
                print(f"      Category: {req['moscow_category']}")
                print(f"      Score: {req['priority_score']}")
                print()
            
            # Save the HTML report
            with open("test_api_prioritization_report.html", "w", encoding="utf-8") as f:
                f.write(data['report_html'])
            print(f"📄 HTML report saved to: test_api_prioritization_report.html")
            
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    success = test_prioritization_api()
    
    if success:
        print("\n✅ API endpoint test PASSED!")
        print("🚀 Ready for frontend integration testing!")
    else:
        print("\n❌ API endpoint test FAILED!")
        print("🔧 Check backend server status and configuration.")