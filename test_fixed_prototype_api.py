"""
Test script to generate a new prototype with fixed checkout functionality via API
"""
import requests
import json

def test_prototype_api():
    """Test the prototype generation API with checkout functionality"""
    
    # Sample FRD content for e-commerce
    frd_content = """
    As a customer, I want to browse products so that I can find items I want to purchase.
    As a customer, I want to add products to my cart so that I can buy multiple items.
    As a customer, I want to view my cart so that I can see what I'm purchasing.
    As a customer, I want to enter shipping information so that my order can be delivered.
    As a customer, I want to enter payment details so that I can complete my purchase.
    As a customer, I want to receive order confirmation so that I know my purchase was successful.
    As a customer, I want to track my order so that I know when it will arrive.
    """
    
    # API payload
    payload = {
        "project": "E-commerce Interactive Checkout Test",
        "frd_content": frd_content,
        "domain": "ecommerce",
        "interactive": True,
        "output_type": "prototype"
    }
    
    try:
        print("🚀 Testing prototype API with checkout functionality...")
        response = requests.post(
            "http://localhost:8001/ai/prototype",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            html_content = result.get("html", "")
            
            print(f"✅ API Response successful!")
            print(f"📊 Generated HTML: {len(html_content)} characters")
            
            # Save to file
            filename = "test_fixed_checkout_prototype_api.html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            print(f"💾 Prototype saved to: {filename}")
            
            # Validate checkout functionality
            validation_results = []
            
            # Check for interactive checkout elements
            checks = [
                ("checkout-step", "Clickable checkout steps"),
                ("showCheckoutStep", "Checkout step navigation function"),
                ("step-content", "Step content areas"),
                ("processShipping", "Shipping form processing"),
                ("processPayment", "Payment form processing"),
                ("shippingForm", "Shipping form"),
                ("paymentForm", "Payment form"),
                ("Order Confirmation", "Confirmation page")
            ]
            
            for check_text, description in checks:
                if check_text in html_content:
                    validation_results.append(f"✅ {description}")
                else:
                    validation_results.append(f"❌ {description}")
            
            print("\n📋 Checkout Functionality Validation:")
            for result in validation_results:
                print(f"  {result}")
            
            # Check for duplicate navigation
            nav_count = html_content.count('<div class="prototype-navigation">')
            if nav_count <= 1:
                print("✅ No duplicate navigation headers")
            else:
                print(f"❌ Found {nav_count} navigation headers (should be 1)")
            
            print(f"\n🎯 Open {filename} in your browser to test the interactive checkout!")
            return True
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing prototype API: {e}")
        return False

if __name__ == "__main__":
    test_prototype_api()