import requests
import json

# Simple test to debug API response
url = "http://localhost:8001/ai/frd/generate"

payload = {
    "project": "Test E-commerce",
    "brd": "Simple test BRD with product catalog and checkout payment processing requirements.",
    "version": 1
}

print("🔍 Debug API Response...")

try:
    response = requests.post(url, json=payload, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    
    if response.status_code == 200:
        print("Raw Response:")
        print(response.text[:500])  # First 500 chars
        print("\n" + "="*40)
        
        try:
            result = response.json()
            print("JSON keys:", list(result.keys()))
            
            if 'frd_html' in result:
                html = result['frd_html']
                print(f"FRD HTML length: {len(html)}")
                print("First 300 chars of HTML:")
                print(html[:300])
                
                # Check for intelligent features
                print(f"\nIntelligent features check:")
                print(f"- 'FR-' found: {'FR-' in html}")
                print(f"- 'Acceptance Criteria' found: {'Acceptance Criteria' in html}")
                print(f"- 'Validation Rules' found: {'Validation Rules' in html}")
                print(f"- Payment terms: {'payment' in html.lower()}")
                print(f"- Credit card: {'credit' in html.lower()}")
                
        except json.JSONDecodeError:
            print("Failed to parse JSON response")
    else:
        print(f"Error response: {response.text}")
        
except Exception as e:
    print(f"Request failed: {e}")