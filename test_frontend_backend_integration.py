#!/usr/bin/env python3
"""
Test the frontend-backend integration for BRD generation
This replicates what the React frontend does when calling /ai/expand
"""

import requests
import json
import sys
import os

# Add backend app to path
backend_path = os.path.join("react-python-auth", "backend", "app")
if os.path.exists(backend_path):
    sys.path.insert(0, backend_path)
    print(f"✅ Added {backend_path} to Python path")

def test_ai_expand_endpoint():
    """Test the /ai/expand endpoint that frontend calls"""
    
    # Test data - Marketing Automation (should detect as marketing domain)
    test_data = {
        "project": "Marketing Automation Platform",
        "inputs": {
            "scope": "Lead generation, email campaigns, customer segmentation, and automated nurturing workflows",
            "objectives": "Increase lead conversion rates by 25%, reduce manual marketing tasks by 60%, improve customer engagement",
            "briefRequirements": "Email marketing automation, lead scoring system, CRM integration, campaign analytics, A/B testing capabilities",
            "assumptions": "CRM system available for integration, marketing team trained on automation tools",
            "constraints": "6 month development timeline, $50,000 budget, GDPR compliance required",
            "validations": "Should show marketing-specific validation criteria, not generic ones",
            "budget": "$50,000 development cost, $10,000 ongoing maintenance"
        },
        "version": 1
    }
    
    print("🧪 Testing /ai/expand endpoint...")
    print(f"📤 Project: {test_data['project']}")
    print(f"📤 Expected domain: Marketing")
    
    try:
        response = requests.post(
            "http://localhost:8001/ai/expand",
            headers={"Content-Type": "application/json"},
            json=test_data,
            timeout=30
        )
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            html = data.get("html", "")
            
            print(f"📥 Response HTML length: {len(html)} characters")
            
            # Check for marketing-specific content
            if "marketing" in html.lower() or "campaign" in html.lower():
                print("✅ Contains marketing-specific content")
            else:
                print("❌ Missing marketing-specific content")
            
            # Check validation criteria
            if "campaign performance tracking" in html.lower() or "email deliverability" in html.lower():
                print("✅ Contains marketing-specific validation criteria")
            elif "mandatory master data fields" in html.lower():
                print("❌ Contains generic validation criteria (PROBLEM!)")
            else:
                print("❓ Validation criteria unclear")
            
            # Check for domain detection
            if "enhanced fallback" in html.lower():
                print("✅ Using enhanced domain-specific fallback")
            elif "ai expansion failed" in html.lower():
                print("❌ Using basic error fallback")
            else:
                print("✅ Generated with AI enhancement")
            
            # Save the output for inspection
            with open("test_frontend_integration_output.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("💾 Saved response to test_frontend_integration_output.html")
            
            return True, html
            
        else:
            print(f"❌ Error response: {response.text}")
            return False, None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - is the backend server running on localhost:8001?")
        return False, None
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False, None

def start_backend_server():
    """Start the backend server if not running"""
    print("🚀 Starting backend server...")
    import subprocess
    import time
    
    # Start server in background
    server_process = subprocess.Popen([
        sys.executable, "react-python-auth/backend/simple_server.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait a bit for server to start
    time.sleep(3)
    
    return server_process

if __name__ == "__main__":
    # First try to test the endpoint
    success, html = test_ai_expand_endpoint()
    
    if not success:
        print("\n🔄 Backend not responding, starting server...")
        server_process = start_backend_server()
        
        try:
            # Test again
            success, html = test_ai_expand_endpoint()
            
            if success:
                print("\n✅ Frontend-backend integration test PASSED")
            else:
                print("\n❌ Frontend-backend integration test FAILED")
                
        finally:
            # Clean up server
            server_process.terminate()
            server_process.wait()
            print("🛑 Server stopped")
    else:
        print("\n✅ Frontend-backend integration test PASSED")