#!/usr/bin/env python3

import requests
import time
import re

def test_place_order_functionality():
    """Test that 'Place Order' button correctly navigates to shipping step"""
    print("🧪 Testing 'Place Order' button functionality...")
    
    # Wait for server to be ready
    print("⏳ Waiting for server to start...")
    time.sleep(5)
    
    # Test data
    test_data = {
        "project": "E-commerce Platform",
        "frd_content": """
        <h1>E-commerce Checkout System</h1>
        <h2>User Story: Checkout Process</h2>
        <p>As a customer, I want to complete my purchase through a guided checkout process so that I can securely pay for my items.</p>
        <h3>Acceptance Criteria:</h3>
        <ul>
            <li>Checkout has steps: Cart → Shipping → Payment → Confirmation</li>
            <li>Users can enter shipping information</li>
            <li>Users can select payment method</li>
            <li>Users receive order confirmation</li>
        </ul>
        """,
        "domain": "ecommerce"
    }
    
    try:
        # Make API request
        print("📡 Making API request to generate prototype...")
        response = requests.post('http://localhost:8001/ai/prototype', json=test_data, timeout=30)
        
        if response.status_code == 200:
            print("✅ API Response successful!")
            html_content = response.text
            
            # Save the generated prototype
            filename = "test_place_order_functionality.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"💾 Prototype saved to: {filename}")
            
            # Test specific functionality
            print("\n🔍 Testing Place Order button functionality:")
            
            # Check for proceedToShipping function
            if 'function proceedToShipping()' in html_content:
                print("  ✅ proceedToShipping() function found")
            else:
                print("  ❌ proceedToShipping() function missing")
            
            # Check for Place Order button with correct onclick
            place_order_pattern = r'<button[^>]*onclick=["\']proceedToShipping\(\)["\'][^>]*>Place Order</button>'
            if re.search(place_order_pattern, html_content):
                print("  ✅ 'Place Order' button with proceedToShipping() onclick found")
            else:
                print("  ❌ 'Place Order' button with correct onclick not found")
                # Check for any Place Order button
                any_place_order = re.search(r'<button[^>]*>Place Order</button>', html_content)
                if any_place_order:
                    print(f"  ℹ️  Found Place Order button: {any_place_order.group()}")
                else:
                    print("  ℹ️  No Place Order button found at all")
            
            # Check for shipping step content
            if 'id="step-shipping"' in html_content:
                print("  ✅ Shipping step content area found")
            else:
                print("  ❌ Shipping step content area missing")
            
            # Check for showCheckoutStep function
            if 'function showCheckoutStep(step)' in html_content:
                print("  ✅ showCheckoutStep() navigation function found")
            else:
                print("  ❌ showCheckoutStep() navigation function missing")
                
            print(f"\n🎯 Open {filename} in your browser to test the 'Place Order' functionality!")
            print("   Click 'Place Order' in the Cart section - it should navigate to Shipping step")
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the backend is running on port 8001")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_place_order_functionality()