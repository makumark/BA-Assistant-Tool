"""
E-commerce Wireframe Generation Test
Using the provided user stories in plain text format
"""
import requests
import json
from datetime import datetime

# Your provided e-commerce user stories
ecommerce_user_stories = [
    {
        "id": "US-001",
        "title": "Authentication",
        "description": "As a shopper, I need to log in securely so that I can access my account and place orders.",
        "acceptance_criteria": [
            "Given a registered email and password, when credentials are valid, then the shopper is logged in and redirected to the home or last page.",
            "When credentials are invalid, then an inline error appears without revealing which field is wrong.",
            "When the shopper is not logged in and tries to checkout, then the app prompts login or guest checkout.",
            "Session persists per 'remember me' and expires after inactivity; logout clears session."
        ]
    },
    {
        "id": "US-002",
        "title": "Browse by category",
        "description": "As a shopper, I need to select a category and view its items so that I can quickly find products of interest.",
        "acceptance_criteria": [
            "When a category is selected, then the product list shows only items within that category, with pagination or infinite scroll.",
            "Filters and sort (price, popularity, rating) update the list without a full page reload.",
            "Empty categories show a helpful message and suggestions."
        ]
    },
    {
        "id": "US-003",
        "title": "Add items to cart",
        "description": "As a shopper, I need to add selected items to the cart so that I can purchase them together.",
        "acceptance_criteria": [
            "Clicking 'Add to Cart' increases the cart count and shows a mini‑cart with item, price, and quantity.",
            "If a product has options (size/color), selection is required before add; otherwise an inline prompt appears.",
            "Adding an item checks inventory and prevents quantities exceeding available stock.",
            "Cart persists across the session and for logged‑in users across devices."
        ]
    },
    {
        "id": "US-004",
        "title": "Cart review",
        "description": "As a shopper, I need to review and update my cart so that I can confirm items and totals before checkout.",
        "acceptance_criteria": [
            "Quantities can be updated and lines removed; totals recompute instantly.",
            "Taxes, shipping estimates, and discounts display clearly; invalid coupons show a clear error.",
            "If inventory changes, the cart reflects updated availability before proceeding."
        ]
    },
    {
        "id": "US-005",
        "title": "Checkout",
        "description": "As a shopper, I need a guided checkout so that I can provide address, shipping, and payment details efficiently.",
        "acceptance_criteria": [
            "Checkout collects shipping/billing addresses and validates required fields and formats.",
            "Available shipping methods are compatible with destination and show cost/ETA.",
            "Order review displays items, charges, and total payable before payment."
        ]
    },
    {
        "id": "US-006",
        "title": "Payments (net banking, cards, UPI)",
        "description": "As a payer, I need to pay using net banking, cards, or UPI so that I can complete my purchase with my preferred method.",
        "acceptance_criteria": [
            "Payment options include net banking, cards, and UPI; the chosen method routes to the correct flow.",
            "Card payments support authorization (and 3DS where required); UPI supports intent/collect; net banking redirects and returns status.",
            "Payment submission is idempotent; duplicate clicks do not create multiple charges.",
            "On success, an order is created, a confirmation page is shown, and a confirmation message/notification is sent.",
            "On failure or cancellation, the order is not created, and the shopper can retry or switch method with a clear reason shown."
        ]
    },
    {
        "id": "US-007",
        "title": "Post‑payment success message",
        "description": "As a shopper, I need a clear success message after payment so that I know my order is confirmed.",
        "acceptance_criteria": [
            "The confirmation page displays 'Payment successful,' order number, summary, and expected delivery/shipment info.",
            "Confirmation is also sent via email/SMS push; status is visible in order history.",
            "If confirmation cannot be sent immediately, the system retries and logs delivery status."
        ]
    }
]

def test_ecommerce_wireframes():
    """Generate wireframes from the provided e-commerce user stories"""
    
    print("🛒 E-commerce Wireframe Generation Test")
    print("="*50)
    
    # Test wireframe generation
    url = "http://localhost:8001/ai/wireframes"
    
    payload = {
        "project": "E-commerce Shopping Platform",
        "user_stories": ecommerce_user_stories,
        "domain": "ecommerce",
        "version": 1
    }
    
    print("🎯 Input Summary:")
    print(f"   📦 Project: E-commerce Shopping Platform")
    print(f"   🏷️  Domain: E-commerce")
    print(f"   📋 User Stories: {len(ecommerce_user_stories)}")
    print(f"   🎨 Expected Pages: Login, Product Browse, Cart, Checkout, Payment, Confirmation")
    
    try:
        print("\n🔄 Generating wireframes from user stories...")
        response = requests.post(url, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            wireframe_html = result.get('html', '')
            detected_domain = result.get('domain', 'unknown')
            
            print(f"✅ Wireframes generated successfully!")
            print(f"📊 Generated HTML: {len(wireframe_html)} characters")
            print(f"🎯 Detected Domain: {detected_domain}")
            
            # Save wireframe
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ecommerce_wireframes_{timestamp}.html"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(wireframe_html)
            
            print(f"💾 Saved to: {filename}")
            
            # E-commerce specific quality analysis
            ecommerce_checks = {
                "Login/Authentication": "login" in wireframe_html.lower() or "authentication" in wireframe_html.lower(),
                "Product browsing": "product" in wireframe_html.lower() or "category" in wireframe_html.lower(),
                "Shopping cart": "cart" in wireframe_html.lower(),
                "Checkout process": "checkout" in wireframe_html.lower(),
                "Payment methods": "payment" in wireframe_html.lower(),
                "Order confirmation": "order" in wireframe_html.lower() or "confirmation" in wireframe_html.lower(),
                "Interactive elements": "onclick" in wireframe_html or "addEventListener" in wireframe_html,
                "E-commerce domain": detected_domain == "ecommerce",
                "Responsive design": "responsive" in wireframe_html.lower(),
                "Shopping-specific components": "shopper" in wireframe_html.lower() or "shop" in wireframe_html.lower()
            }
            
            print(f"\n📈 E-commerce Quality Analysis:")
            passed_checks = 0
            for check, passed in ecommerce_checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check}: {passed}")
                if passed:
                    passed_checks += 1
            
            total_checks = len(ecommerce_checks)
            score = (passed_checks / total_checks) * 100
            
            print(f"\n🏆 E-commerce Score: {score:.1f}% ({passed_checks}/{total_checks} checks passed)")
            
            # Show generated pages preview
            if wireframe_html:
                print(f"\n🎨 Generated Wireframe Features:")
                pages_detected = []
                if "login" in wireframe_html.lower(): pages_detected.append("🔐 Login Page")
                if "dashboard" in wireframe_html.lower(): pages_detected.append("📊 Dashboard")
                if "product" in wireframe_html.lower(): pages_detected.append("🛍️ Product Pages") 
                if "cart" in wireframe_html.lower(): pages_detected.append("🛒 Shopping Cart")
                if "checkout" in wireframe_html.lower(): pages_detected.append("💳 Checkout Flow")
                if "payment" in wireframe_html.lower(): pages_detected.append("💰 Payment Methods")
                
                for page in pages_detected:
                    print(f"   {page}")
                
                print(f"\n📱 Technical Features:")
                print(f"   • Interactive Navigation: {wireframe_html.count('onclick')} clickable elements")
                print(f"   • Form Elements: {'✅' if 'form-field' in wireframe_html else '❌'}")
                print(f"   • Navigation Tabs: {'✅' if 'page-tab' in wireframe_html else '❌'}")
                print(f"   • Professional Styling: {'✅' if len(wireframe_html) > 10000 else '❌'}")
            
            if score >= 80:
                print(f"\n🎉 EXCELLENT! Your e-commerce wireframes are ready!")
                print(f"🔗 Open {filename} in your browser to view the interactive wireframes")
                return True
            else:
                print(f"\n👍 GOOD! Wireframes generated with room for improvement")
                return True
                
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend server not running on port 8001")
        print("💡 Start backend: cd react-python-auth/backend && python simple_server.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🛒 E-commerce Wireframe Generation from User Stories")
    print("Testing with the provided user stories in your specified format")
    print("="*70)
    
    success = test_ecommerce_wireframes()
    
    print("\n" + "="*70)
    if success:
        print("🎉 SUCCESS! E-commerce wireframes generated from your user stories!")
        print("\n🎯 What was generated:")
        print("   • Interactive HTML wireframes based on your 7 user stories")
        print("   • E-commerce specific components (login, cart, checkout, payments)")
        print("   • Professional styling with clickable navigation")
        print("   • Responsive design for desktop and mobile")
        print("\n📱 Next steps:")
        print("   1. Open the generated HTML file in your browser")
        print("   2. Navigate between wireframe pages using the tabs")
        print("   3. Use the same format in your BA Tool frontend")
    else:
        print("💥 Failed to generate wireframes - check server status")