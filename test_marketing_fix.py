#!/usr/bin/env python3
"""
Test script to verify marketing automation domain detection and validation fixes.
"""

import requests
import json

def test_marketing_automation_brd():
    """Test marketing automation BRD generation with domain-specific stakeholders and validation."""
    
    url = "http://localhost:8001/ai/expand"
    
    # Marketing automation project data - same as user's example
    payload = {
        "project": "Marketing Automation System",
        "inputs": {
            "projectName": "Marketing Automation System",
            "projectDescription": "Advanced marketing automation platform for managing multi-channel campaigns, customer segmentation, and marketing analytics",
            "businessRequirements": [
                "Customer segmentation based on behavior and demographics",
                "Multi-channel campaign management (email, SMS, push notifications)",
                "A/B testing capabilities for content optimization",
                "Real-time analytics and attribution reporting", 
                "Marketing automation workflows and triggers",
                "Content and asset management system",
                "Integration with CRM and data sources"
            ],
            "businessObjectives": [
                "Increase customer engagement through personalized campaigns",
                "Improve marketing ROI with data-driven insights",
                "Automate repetitive marketing tasks",
                "Enable omnichannel customer experiences"
            ],
            "assumptions": [
                "Marketing team will be trained on the new system",
                "Data quality from CRM is sufficient for segmentation",
                "Email deliverability infrastructure is available"
            ],
            "budget": "Budget range: $500K-$750K",
            "outOfScope": [
                "Social media content creation",
                "Sales lead qualification processes"
            ]
        },
        "version": 1
    }
    
    print("🧪 Testing Marketing Automation BRD Generation...")
    print("=" * 60)
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            html_content = result.get("html", "")
            
            # Check for marketing domain detection
            print("✅ BRD Generation successful!")
            print("\n🔍 Checking for Marketing Domain-Specific Content:")
            print("-" * 50)
            
            # Check stakeholders
            if "Marketing managers" in html_content:
                print("✅ Marketing stakeholders detected (Marketing managers)")
            else:
                print("❌ Marketing stakeholders missing")
                
            if "Campaign managers" in html_content:
                print("✅ Campaign managers found")
            else:
                print("❌ Campaign managers missing")
                
            if "Email specialists" in html_content:
                print("✅ Email specialists found") 
            else:
                print("❌ Email specialists missing")
                
            # Check for wrong banking stakeholders
            if "Branch staff" in html_content or "Bank tellers" in html_content:
                print("❌ Banking stakeholders incorrectly detected!")
            else:
                print("✅ No incorrect banking stakeholders")
                
            # Check for marketing-specific validation
            if "Email inbox rate" in html_content:
                print("✅ Email deliverability validation found")
            else:
                print("❌ Email deliverability validation missing")
                
            if "SMS delivery rate" in html_content:
                print("✅ SMS delivery validation found")
            else:
                print("❌ SMS delivery validation missing")
                
            # Check for generic validation
            if "System response time shall be less than 3 seconds" in html_content:
                print("❌ Generic validation rules still present")
            else:
                print("✅ No generic validation rules detected")
                
            # Check for segmentation-specific criteria
            if "Audience size: minimum" in html_content:
                print("✅ Segmentation validation criteria found")
            else:
                print("❌ Segmentation validation criteria missing")
                
            # Check for campaign-specific criteria  
            if "Campaign names: 5-100 characters" in html_content:
                print("✅ Campaign validation criteria found")
            else:
                print("❌ Campaign validation criteria missing")
                
            print(f"\n📊 Summary:")
            print(f"Response Status: {response.status_code}")
            print(f"Content Length: {len(html_content)} characters")
            
            # Save response for manual inspection
            with open("test_marketing_brd_output.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            print("💾 Full response saved to: test_marketing_brd_output.html")
            
        else:
            print(f"❌ BRD Generation failed!")
            print(f"Status Code: {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

def test_frd_generation():
    """Test FRD generation for marketing automation."""
    
    url = "http://localhost:8001/ai/frd"
    
    # Simple BRD content for FRD generation
    brd_content = """
    <h3>Business Requirements</h3>
    <div class="epic">
        <h4>EPIC-01: Customer Segmentation</h4>
        <p>The system shall provide customer segmentation based on behavior and demographics</p>
    </div>
    <div class="epic">
        <h4>EPIC-02: Campaign Management</h4>
        <p>The system shall support multi-channel campaign management</p>
    </div>
    """
    
    payload = {
        "project": "Marketing Automation System",
        "brd": brd_content,
        "version": 1
    }
    
    print("\n🧪 Testing Marketing FRD Generation...")
    print("=" * 60)
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            html_content = result.get("html", "")
            print("✅ FRD Generation successful!")
            
            # Check for marketing-specific acceptance criteria
            if "Email inbox rate" in html_content or "deliverability" in html_content.lower():
                print("✅ Marketing-specific acceptance criteria found")
            else:
                print("❌ Marketing-specific acceptance criteria missing")
                
            # Check for segmentation criteria
            if "Audience size" in html_content:
                print("✅ Segmentation acceptance criteria found")
            else:
                print("❌ Segmentation acceptance criteria missing")
                
            # Save FRD output
            with open("test_marketing_frd_output.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            print("💾 FRD response saved to: test_marketing_frd_output.html")
            
        else:
            print(f"❌ FRD Generation failed!")
            print(f"Status Code: {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_marketing_automation_brd()
    test_frd_generation()