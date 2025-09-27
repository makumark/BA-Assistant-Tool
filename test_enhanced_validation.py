#!/usr/bin/env python3
"""
Test enhanced CRM validation criteria generation with clean BRD
"""
import requests
import json

def test_enhanced_crm_validation():
    """Test the enhanced CRM validation generation with clean BRD that has no validations"""
    
    # Clean CRM BRD without validation section - should trigger domain-specific fallback
    brd_html = """
    <div style="font-family:Arial,Helvetica,sans-serif;color:#111827;padding:18px;">
      <h1 style="text-align:center;margin-bottom:6px;">Business Requirement Document (BRD)</h1>
      <h2 style="text-align:center;margin-top:2px;">CRM System — BRD Version-1</h2>
      <hr/>
      <h3>Executive Summary</h3>
      <p>This document captures business requirements for a comprehensive CRM system to manage leads, opportunities, contacts, and marketing campaigns.</p>
      <h3>Project Scope</h3>
      <p>Lead management, opportunity pipeline, contact tracking, marketing campaigns, sales activities, and reporting dashboards.</p>
      <h3>Business Objectives</h3>
      <p>Increase lead conversion rates, improve sales pipeline visibility, enhance customer relationship management, and automate marketing processes.</p>
      <h3>Business Requirements (EPIC Format)</h3>
      <p>EPIC-01: Lead Management - capture, qualify, assign, and track leads through sales process<br/>
      EPIC-02: Opportunity Pipeline - manage sales opportunities, stages, forecasting, and win/loss tracking<br/>
      EPIC-03: Contact Management - maintain customer contact information, interaction history, and account relationships<br/>
      EPIC-04: Marketing Campaigns - create, execute, and track marketing campaigns across multiple channels<br/>
      EPIC-05: Sales Activities - manage tasks, meetings, calls, and follow-up activities for sales team<br/>
      EPIC-06: Reporting & Analytics - generate reports and dashboards for sales and marketing performance</p>
      <h3>Assumptions</h3>
      <p>CRM system integrates with existing email and marketing tools. Sales team will receive training on new system.</p>
      <h3>Constraints</h3>
      <p>6-month implementation timeline. GDPR compliance required for customer data processing.</p>
    </div>
    """
    
    # Test the FRD generation API endpoint
    url = "http://localhost:8001/ai/frd"
    payload = {
        "project": "CRM System",
        "brd": brd_html,
        "version": 1
    }
    
    print("🧪 Testing ENHANCED CRM Validation Generation...")
    print("=" * 60)
    print(f"📤 Project: {payload['project']}")
    print(f"📤 BRD: Clean CRM BRD with NO existing validation section")
    print(f"📤 Expected: Domain-specific Marketing/CRM validation criteria")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            frd_html = result.get("html", "")
            
            # Save for inspection
            with open("test_enhanced_frd_validation.html", "w", encoding="utf-8") as f:
                f.write(frd_html)
            print("💾 FRD saved to: test_enhanced_frd_validation.html")
            
            print(f"📥 FRD HTML length: {len(frd_html)} characters")
            
            # Analyze the validation criteria
            print("\n🔍 VALIDATION CRITERIA ANALYSIS:")
            print("-" * 40)
            
            # Check for enhanced marketing-specific validations
            enhanced_validations = [
                "customer consent validation for all communication preferences",
                "email address format and deliverability standards", 
                "campaign performance tracking and attribution models",
                "lead scoring and segmentation accuracy",
                "GDPR compliance for customer data processing"
            ]
            
            enhanced_found = 0
            for validation in enhanced_validations:
                if validation.lower() in frd_html.lower():
                    print(f"✅ Found: {validation}")
                    enhanced_found += 1
                else:
                    print(f"❌ Missing: {validation}")
            
            # Check for generic fallback
            if "data validation and integrity checks" in frd_html.lower():
                print("❌ Still using generic fallback validation")
            
            # Check individual functional requirement validations
            if "Lead capture forms collect all required contact information" in frd_html:
                print("✅ Found CRM-specific functional requirement validation")
            elif "Required fields: all mandatory fields completed" in frd_html:
                print("❌ Still using generic functional requirement validation")
            
            print(f"\n📊 Enhanced validations found: {enhanced_found}/{len(enhanced_validations)}")
            
            if enhanced_found >= 3:
                print("🎉 SUCCESS: Enhanced CRM validation criteria are working!")
            else:
                print("❌ FAILURE: Still using generic validation criteria")
                
        else:
            print(f"❌ API call failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Is the backend server running on port 8001?")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_enhanced_crm_validation()