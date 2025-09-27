#!/usr/bin/env python3
"""
Test actual API endpoint to see what's returned
"""

import requests
import json

def test_api_endpoint():
    print("🔍 Testing actual API endpoint...")
    
    # Healthcare BRD content
    healthcare_brd = """Executive Summary
This document captures the business requirements for Health Care.

Project Scope
Patient registration, appointment scheduling, electronic health records integration, billing module

Business Requirements (EPIC Format)
EPIC-01 Core Business Requirements
Requirements:
• Ability to create and manage patient profiles, schedule appointments with notifications, store and update patient medical history securely, and generate invoices with insurance claim support
• Enforce prescription and medication safety checks"""

    payload = {
        "project": "Health Care",
        "brd": healthcare_brd,
        "version": 1
    }
    
    try:
        print("📡 Calling API endpoint...")
        response = requests.post("http://localhost:8001/ai/frd", json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            frd_html = result.get("html", "")
            
            print(f"✅ API Response received: {len(frd_html)} characters")
            
            # Check for validation sections
            if "🔍 Validation Criteria:" in frd_html or "Validation Rules:" in frd_html:
                print("✅ Contains validation sections")
                
                # Extract validation content
                validation_start = max(
                    frd_html.find("🔍 Validation Criteria:") if "🔍 Validation Criteria:" in frd_html else -1,
                    frd_html.find("Validation Rules:") if "Validation Rules:" in frd_html else -1
                )
                
                if validation_start > -1:
                    validation_section = frd_html[validation_start:validation_start + 800]
                    print(f"\n📋 Validation section:")
                    print(validation_section)
                    
                    # Check specificity
                    if any(term in validation_section.lower() for term in ["patient", "appointment", "medical", "prescription"]):
                        print("\n✅ Contains healthcare-specific validations")
                    else:
                        print("\n❌ Contains generic validations")
                else:
                    print("❌ Could not extract validation section")
            else:
                print("❌ No validation sections found")
            
            # Save for inspection
            with open("test_api_response.html", "w", encoding="utf-8") as f:
                f.write(frd_html)
            print("💾 Full response saved to test_api_response.html")
            
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_api_endpoint()