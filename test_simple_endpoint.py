#!/usr/bin/env python3
"""
Simple test to call the /ai/expand endpoint while server is running
"""

import requests
import json

def test_endpoint():
    """Test the /ai/expand endpoint"""
    
    # Test data - Marketing Automation
    test_data = {
        "project": "Marketing Automation Platform",
        "inputs": {
            "scope": "Lead generation, email campaigns, customer segmentation",
            "objectives": "Increase lead conversion rates by 25%",
            "briefRequirements": "Email marketing automation, lead scoring system",
            "assumptions": "CRM system available for integration",
            "constraints": "6 month development timeline",
            "validations": "Should show marketing-specific validation criteria",
            "budget": "$50,000 development cost"
        },
        "version": 1
    }
    
    print("🧪 Testing /ai/expand endpoint...")
    
    try:
        response = requests.post(
            "http://localhost:8001/ai/expand",
            headers={"Content-Type": "application/json"},
            json=test_data,
            timeout=60
        )
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            html = data.get("html", "")
            
            print(f"📥 Response HTML length: {len(html)} characters")
            
            # Save the output for inspection
            with open("test_backend_response.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("💾 Saved response to test_backend_response.html")
            
            # Check for marketing-specific content
            if "marketing" in html.lower():
                print("✅ Contains marketing-specific content")
            else:
                print("❌ Missing marketing-specific content")
            
            # Check validation criteria - the key issue
            if "campaign performance" in html.lower() or "email deliverability" in html.lower():
                print("✅ Contains marketing-specific validation criteria")
            elif "mandatory master data fields" in html.lower():
                print("❌ Contains generic validation criteria (PROBLEM!)")
                print("📄 Showing validation section:")
                # Extract validation section
                lines = html.split('\n')
                in_validation = False
                for line in lines:
                    if "validation" in line.lower() and ("h2" in line or "h3" in line):
                        in_validation = True
                    elif in_validation and "<h" in line:
                        break
                    if in_validation:
                        print(f"   {line.strip()}")
            else:
                print("❓ Validation criteria unclear")
            
            return True
            
        else:
            print(f"❌ Error response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - is the backend server running on localhost:8001?")
        return False
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    test_endpoint()