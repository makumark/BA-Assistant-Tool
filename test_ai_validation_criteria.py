#!/usr/bin/env python3
"""
Test AI-Enhanced User Story Validation Criteria
Test if the new AI validation generation creates contextual, specific validation criteria
"""
import requests
import json

def test_ai_validation_criteria():
    print("=== Testing AI-Enhanced User Story Validation Criteria ===")
    
    # Test data for CRM system (similar to user's example)
    crm_brd = """
Business Requirement Document (BRD)
CRM System Enhancement — BRD Version-2

Executive Summary
CRM System Enhancement BRD: Customer relationship management system for sales team lead tracking and opportunity management

Project Scope
Included — lead and account management, contact/interaction tracking, opportunity and pipeline, activities and tasks, case/ticketing, marketing campaigns and segmentation, dashboards and reports, role based admin and security

Business Objectives
Increase qualified lead conversion, improve pipeline visibility and forecast accuracy, reduce response time to inbound inquiries, raise customer retention/NPS, and shorten onboarding time for new sales reps.

Business Requirements (EPIC Format)
EPIC-01 Lead & Account Management
Requirements:
• Lead capture, de dupe, qualify, convert to account/contact/opportunity
• Account hierarchy and territory management

EPIC-02 Opportunity & Pipeline Management
Requirements:
• Opportunity stages, products, quotes, forecasts, win/loss reasons
• Pipeline analytics and forecasting dashboards

EPIC-03 Activities & Calendar Management
Requirements:
• Tasks, calls, meetings, reminders, SLA timers
• Calendar integration and activity tracking

EPIC-04 Data & Security Management
Requirements:
• Role/profiles, field level security, audit, GDPR consent
• Data privacy and compliance controls

Validations & Acceptance Criteria
Lead data validation, opportunity workflow validation, contact integrity checks
"""
    
    test_data = {
        "project": "CRM System Enhancement",
        "brd": crm_brd,
        "version": 2
    }
    
    try:
        print("🔄 Calling FRD API endpoint to test AI validation criteria...")
        response = requests.post(
            "http://localhost:8001/ai/frd",
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            frd_html = result.get("html", "")
            
            print(f"✅ FRD Generated: {len(frd_html)} characters")
            
            # Check for AI-generated contextual validation criteria
            ai_validation_checks = {
                "Lead-specific validation": "lead capture forms must validate all required contact information" in frd_html.lower(),
                "Opportunity-specific validation": "opportunity stage progression must follow defined sales workflow" in frd_html.lower(),
                "Contact-specific validation": "contact deduplication algorithms must prevent duplicate customer records" in frd_html.lower(),
                "Activity-specific validation": "activity logging must capture all customer touchpoints" in frd_html.lower(),
                "Security-specific validation": "data privacy controls must comply with gdpr" in frd_html.lower(),
                "Generic validation avoided": "input validation ensures data integrity" not in frd_html.lower()
            }
            
            print(f"\n=== AI Validation Criteria Analysis ===")
            passed_checks = 0
            for check_name, passed in ai_validation_checks.items():
                status = "✅" if passed else "❌"
                print(f"{status} {check_name}")
                if passed:
                    passed_checks += 1
            
            # Save output for inspection
            with open("test_ai_validation_criteria_output.html", "w", encoding="utf-8") as f:
                f.write(frd_html)
            print(f"\n✅ Output saved to test_ai_validation_criteria_output.html")
            
            # Assessment
            success_rate = passed_checks / len(ai_validation_checks) * 100
            print(f"\n🎯 AI Validation Enhancement Score: {success_rate:.1f}%")
            
            if success_rate >= 80:
                print("✅ SUCCESS: AI-Enhanced validation criteria are working!")
                print("🤖 User stories now have contextual, specific validation criteria")
            elif success_rate >= 50:
                print("🟡 PARTIAL: Some AI validation enhancements working")
                print("🔧 May need further tuning of contextual criteria generation")
            else:
                print("❌ ISSUE: Still showing generic validation criteria")
                print("🔍 Need to debug AI validation generation logic")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Server not running on localhost:8001")
        print("💡 Please start the server first:")
        print("   cd react-python-auth/backend && python simple_server.py")
    except Exception as e:
        print(f"❌ Test Error: {e}")

if __name__ == "__main__":
    test_ai_validation_criteria()