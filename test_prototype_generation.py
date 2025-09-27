"""
Test prototype generation with sample FRD content
"""
import requests
import json
import os
from datetime import datetime

# Sample FRD content for testing
sample_frd_content = """
<h2>E-commerce Platform Requirements</h2>

<h3>User Stories</h3>
<p>As a customer, I want to browse products by category, so that I can find items I'm interested in.</p>
<p>As a customer, I want to add items to my cart, so that I can purchase multiple products at once.</p>
<p>As a customer, I want to review my cart before checkout, so that I can verify my order.</p>
<p>As a customer, I want to enter my payment information securely, so that I can complete my purchase.</p>
<p>As a customer, I want to create an account, so that I can track my orders and save my preferences.</p>

<h3>Functional Requirements</h3>
<ul>
<li>Product catalog with search and filtering capabilities</li>
<li>Shopping cart functionality with quantity management</li>
<li>Secure payment processing</li>
<li>User authentication and account management</li>
<li>Order tracking and history</li>
</ul>

<h3>Acceptance Criteria</h3>
<ul>
<li>All functional requirements must be validated against ecommerce domain standards</li>
<li>User acceptance testing must cover all defined user stories</li>
<li>Performance criteria must meet ecommerce-specific requirements</li>
<li>Security and compliance requirements must be validated</li>
</ul>
"""

def test_prototype_generation():
    """Test the prototype generation API endpoint"""
    
    url = "http://localhost:8001/ai/prototype"
    
    payload = {
        "project": "E-commerce Platform Test",
        "frd_content": sample_frd_content,
        "domain": "ecommerce"
    }
    
    try:
        print("🎯 Testing prototype generation...")
        print(f"📋 Project: {payload['project']}")
        print(f"🎨 Domain: {payload['domain']}")
        print(f"📄 FRD Content: {len(sample_frd_content)} characters")
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            html_content = result.get('html', '')
            
            print(f"✅ Prototype generation successful!")
            print(f"📊 Generated HTML: {len(html_content)} characters")
            print(f"🎯 Domain: {result.get('domain', 'unknown')}")
            
            # Save the prototype to a file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_prototype_ecommerce_{timestamp}.html"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"💾 Prototype saved to: {filename}")
            
            # Basic validation
            validation_checks = [
                ("Contains navigation", "nav-button" in html_content or "navigation" in html_content.lower()),
                ("Contains interactive elements", "onclick" in html_content),
                ("Contains e-commerce elements", "product" in html_content.lower()),
                ("Contains login page", "login" in html_content.lower()),
                ("Contains dashboard", "dashboard" in html_content.lower()),
                ("Contains cart functionality", "cart" in html_content.lower()),
                ("Contains proper HTML structure", "<html" in html_content and "</html>" in html_content),
                ("Contains CSS styling", "<style" in html_content)
            ]
            
            passed_checks = sum(1 for name, check in validation_checks if check)
            total_checks = len(validation_checks)
            
            print(f"\n📋 Validation Results: {passed_checks}/{total_checks} checks passed")
            
            for name, check in validation_checks:
                status = "✅" if check else "❌"
                print(f"  {status} {name}")
            
            if passed_checks >= 6:  # At least 75% of checks should pass
                print(f"\n🎉 Prototype quality: EXCELLENT ({passed_checks}/{total_checks} checks passed)")
            elif passed_checks >= 4:
                print(f"\n👍 Prototype quality: GOOD ({passed_checks}/{total_checks} checks passed)")
            else:
                print(f"\n⚠️ Prototype quality: NEEDS IMPROVEMENT ({passed_checks}/{total_checks} checks passed)")
            
            return html_content
            
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Starting Prototype Generation Test")
    print("=" * 50)
    
    # Test prototype generation
    result = test_prototype_generation()
    
    if result:
        print("\n🎯 Prototype generation test completed successfully!")
        print("📝 Open the generated HTML file in your browser to see the interactive prototype.")
    else:
        print("\n❌ Prototype generation test failed!")
        print("🔍 Check that the backend server is running on port 8001.")