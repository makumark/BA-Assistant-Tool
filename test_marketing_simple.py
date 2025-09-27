#!/usr/bin/env python3
"""
Simple test to check marketing automation BRD generation.
"""

import requests
import json

def test_marketing_brd():
    """Test marketing automation BRD generation."""
    
    url = "http://localhost:8001/ai/expand"
    
    payload = {
        "project": "Marketing Automation System",
        "inputs": {
            "projectName": "Marketing Automation System",
            "projectDescription": "Advanced marketing automation platform for managing multi-channel campaigns, customer segmentation, and marketing analytics",
            "businessRequirements": [
                "Customer segmentation based on behavior and demographics",
                "Multi-channel campaign management (email, SMS, push notifications)",
                "A/B testing capabilities for content optimization"
            ]
        },
        "version": 1
    }
    
    try:
        print("🧪 Testing Marketing Automation BRD...")
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            html = result.get("html", "")
            
            print(f"Response length: {len(html)} characters")
            
            # Check for marketing content
            has_marketing_managers = "Marketing managers" in html
            has_campaign_managers = "Campaign managers" in html
            has_enhanced_fallback = "enhanced fallback" in html
            has_basic_fallback = "AI expansion failed" in html
            
            print(f"✅ Marketing managers found: {has_marketing_managers}")
            print(f"✅ Campaign managers found: {has_campaign_managers}")
            print(f"✅ Enhanced fallback used: {has_enhanced_fallback}")
            print(f"❌ Basic fallback (error): {has_basic_fallback}")
            
            # Save for inspection
            with open("test_marketing_simple_output.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("💾 Output saved to: test_marketing_simple_output.html")
            
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_marketing_brd()