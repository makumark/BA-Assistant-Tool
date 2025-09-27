"""
Test prioritization for E-commerce example: Login (Priority 1), Search (Priority 2), Checkout (Priority 3)
"""

import sys
import os

# Add the backend directory to Python path
backend_dir = os.path.join(os.path.dirname(__file__), 'react-python-auth', 'backend')
app_dir = os.path.join(backend_dir, 'app')
sys.path.insert(0, app_dir)

try:
    from services.ai_service import prioritize_frd_requirements
    print("✅ AI service imported successfully")
except Exception as e:
    print(f"❌ Failed to import AI service: {e}")
    exit(1)

# Sample E-commerce FRD HTML content
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

def test_ecommerce_prioritization():
    print("🔄 Testing E-commerce requirement prioritization...")
    
    try:
        result = prioritize_frd_requirements("E-commerce Shopping Platform", ecommerce_frd_html, 1)
        
        print(f"\n📊 Prioritization Results:")
        print(f"   Project: {result['project']}")
        print(f"   Domain: {result['domain']}")
        print(f"   Total Requirements: {result['total_requirements']}")
        print(f"   MoSCoW Distribution: {result['moscow_distribution']['counts']}")
        
        print(f"\n🎯 Prioritized Requirements:")
        for req in result['prioritized_requirements']:
            print(f"   #{req['priority_rank']} {req['id']}: {req['goal'][:50]}...")
            print(f"      Category: {req['moscow_category']}")
            print(f"      Score: {req['priority_score']}")
            print(f"      Business Value: {req['business_value']}")
            print(f"      Dependencies: {len(req['dependencies'])}")
            print()
        
        # Check if our expected priorities are correct
        print("🧪 Validating Expected E-commerce Priorities:")
        
        # Find login/authentication requirements
        auth_reqs = [req for req in result['prioritized_requirements'] 
                    if any(keyword in req['goal'].lower() for keyword in ['login', 'authenticate', 'register'])]
        
        # Find search requirements  
        search_reqs = [req for req in result['prioritized_requirements']
                      if any(keyword in req['goal'].lower() for keyword in ['search', 'browse', 'find'])]
        
        # Find checkout requirements
        checkout_reqs = [req for req in result['prioritized_requirements']
                        if any(keyword in req['goal'].lower() for keyword in ['checkout', 'pay', 'payment', 'purchase'])]
        
        print(f"   Authentication Requirements: {len(auth_reqs)}")
        if auth_reqs:
            avg_auth_rank = sum(req['priority_rank'] for req in auth_reqs) / len(auth_reqs)
            print(f"      Average Rank: {avg_auth_rank:.1f}")
            print(f"      Categories: {[req['moscow_category'] for req in auth_reqs]}")
        
        print(f"   Search Requirements: {len(search_reqs)}")
        if search_reqs:
            avg_search_rank = sum(req['priority_rank'] for req in search_reqs) / len(search_reqs)
            print(f"      Average Rank: {avg_search_rank:.1f}")
            print(f"      Categories: {[req['moscow_category'] for req in search_reqs]}")
        
        print(f"   Checkout Requirements: {len(checkout_reqs)}")
        if checkout_reqs:
            avg_checkout_rank = sum(req['priority_rank'] for req in checkout_reqs) / len(checkout_reqs)
            print(f"      Average Rank: {avg_checkout_rank:.1f}")
            print(f"      Categories: {[req['moscow_category'] for req in checkout_reqs]}")
        
        # Validate expected hierarchy: Auth < Search < Checkout (lower rank = higher priority)
        success = True
        if auth_reqs and search_reqs and avg_auth_rank < avg_search_rank:
            print("   ✅ Authentication correctly prioritized over Search")
        else:
            print("   ❌ Authentication should be prioritized over Search")
            success = False
            
        if search_reqs and checkout_reqs and avg_search_rank < avg_checkout_rank:
            print("   ✅ Search correctly prioritized over Checkout")
        else:
            print("   ❌ Search should be prioritized over Checkout") 
            success = False
        
        # Check dependency analysis
        print(f"\n🔗 Dependency Analysis:")
        print(f"   Total Dependencies: {result['dependencies']['total_dependencies']}")
        print(f"   Critical Path: {result['dependencies']['critical_path'][:3]}")
        print(f"   Isolated Requirements: {len(result['dependencies']['isolated_requirements'])}")
        
        if success:
            print("\n✅ E-commerce prioritization test PASSED!")
        else:
            print("\n❌ E-commerce prioritization test FAILED!")
            
        return result
        
    except Exception as e:
        print(f"❌ Error during prioritization test: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = test_ecommerce_prioritization()
    
    if result:
        # Save the HTML report for manual inspection
        with open("test_ecommerce_prioritization_report.html", "w", encoding="utf-8") as f:
            f.write(result['report_html'])
        print(f"\n📄 HTML report saved to: test_ecommerce_prioritization_report.html")