#!/usr/bin/env python3
"""
Test CRM validation criteria through API call to validate enhancement
"""
import requests
import json

def test_crm_validation():
    print("=== Testing CRM Validation via API ===")
    
    # Test data for CRM system
    test_data = {
        "project_overview": "Customer Relationship Management system for sales team to manage leads, track opportunities, and maintain customer contacts",
        "functional_requirements": [
            "Lead capture and qualification system",
            "Opportunity pipeline management",
            "Contact management and deduplication",
            "Sales activity tracking",
            "Campaign performance analytics"
        ],
        "non_functional_requirements": [
            "System should handle 1000 concurrent users",
            "Response time under 2 seconds",
            "99.9% uptime availability"
        ],
        "validations": "Lead data validation, opportunity workflow validation, contact integrity checks"
    }
    
    try:
        # Call the FRD generation API
        print("🔄 Calling FRD API endpoint...")
        response = requests.post(
            "http://localhost:8001/ai/frd",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            frd_html = response.text
            
            # Check for CRM-specific validation criteria
            crm_validations = [
                "lead capture",
                "opportunity",
                "contact",
                "sales",
                "pipeline",
                "deduplication",
                "campaign",
                "customer consent",
                "email address format"
            ]
            
            found_validations = []
            for validation in crm_validations:
                if validation.lower() in frd_html.lower():
                    found_validations.append(validation)
            
            print(f"\n=== Validation Results ===")
            print(f"Response Status: {response.status_code}")
            print(f"CRM-specific validations found: {len(found_validations)}")
            print(f"Found validations: {found_validations}")
            
            # Save the output for inspection
            with open("test_crm_validation_output.html", "w", encoding="utf-8") as f:
                f.write(frd_html)
            print(f"✅ Output saved to test_crm_validation_output.html")
            
            # Check if we have domain-specific content
            if len(found_validations) >= 3:
                print("✅ SUCCESS: Enhanced CRM validation criteria detected!")
            else:
                print("❌ ISSUE: Generic validation criteria still present")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Server not running on localhost:8001")
    except Exception as e:
        print(f"❌ Test Error: {e}")

if __name__ == "__main__":
    test_crm_validation()