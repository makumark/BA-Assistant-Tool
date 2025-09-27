#!/usr/bin/env python3
"""
Simple test for AI validation criteria via direct API call
"""
import requests
import json
import time

def test_simple_validation():
    print("=== Simple AI Validation Test ===")
    
    # Start with a minimal wait
    time.sleep(2)
    
    # Simple test data
    test_data = {
        "project": "CRM System Enhancement", 
        "brd": """
Business Requirement Document (BRD)
CRM System Enhancement — BRD Version-2

Business Requirements (EPIC Format)
EPIC-01 Lead Management
Requirements:
• Lead capture from web forms
• Lead qualification and scoring
• Lead assignment to sales teams

EPIC-02 Opportunity Tracking  
Requirements:
• Opportunity stage management
• Sales pipeline visualization
• Win/loss analysis
        """,
        "version": 2
    }
    
    try:
        print("🔄 Testing API endpoint...")
        response = requests.post(
            "http://localhost:8001/ai/frd",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            html = result.get("html", "")
            
            print(f"✅ Response received: {len(html)} characters")
            
            # Save for inspection
            with open("simple_validation_test.html", "w", encoding="utf-8") as f:
                f.write(html)
            
            # Check for AI-generated content
            checks = [
                "lead capture forms" in html.lower(),
                "opportunity stage" in html.lower(), 
                "validation" in html.lower(),
                "user story" in html.lower()
            ]
            
            passed = sum(checks)
            print(f"🎯 Basic checks passed: {passed}/4")
            
            if passed >= 3:
                print("✅ SUCCESS: API working, validation content generated!")
                print("📄 Check 'simple_validation_test.html' for full output")
            else:
                print("🟡 PARTIAL: API working but content may need review")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text[:300]}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Server not running on localhost:8001")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_simple_validation()