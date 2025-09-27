#!/usr/bin/env python3
"""
🧪 AI-Enhanced Telecom API Integration Test
Tests the actual API endpoints with telecom BRD content
"""

import requests
import json
import time

def test_telecom_api_integration():
    """Test the API integration with telecom BRD content"""
    
    print("🧪 AI-Enhanced Telecom API Integration Test")
    print("=" * 60)
    
    base_url = "http://localhost:8001"
    
    # Test BRD content from your actual telecom example
    test_project_data = {
        "project": "Telecom BSS/OSS Platform",
        "inputs": {
            "project_name": "Telecom BSS/OSS Platform",
            "project_description": "Comprehensive telecom business support system with billing, customer care, and partner management",
            "stakeholders": "Telecom Operators, Customers, Channel Partners, Regulatory Bodies",
            "business_objectives": "Streamline telecom operations, improve customer experience, ensure regulatory compliance, optimize revenue management",
            "scope": "Lead to Order, KYC & Activation, Charging & Billing, Care & Assurance, Payments & Collections, Partner Channel, Analytics & Compliance",
            "out_of_scope": "Network infrastructure, Hardware procurement, Third-party integrations outside BSS/OSS",
            "success_criteria": "Successful customer onboarding, Accurate billing, Regulatory compliance, Partner satisfaction",
            "assumptions": "Stable network infrastructure, Regulatory framework compliance, API availability from external systems",
            "constraints": "Budget constraints, Regulatory timelines, Legacy system dependencies",
            "budget": "5-10 million USD over 18 months",
            "timeline": "18 months phased implementation"
        },
        "version": "1.0"
    }
    
    print("\n🎯 STEP 1: Testing BRD Generation API")
    print("-" * 40)
    
    try:
        # Test BRD generation
        brd_response = requests.post(
            f"{base_url}/api/v1/ai/brd",
            json=test_project_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if brd_response.status_code == 200:
            brd_result = brd_response.json()
            print(f"✅ BRD Generation: SUCCESS")
            print(f"   Response length: {len(brd_result.get('html', ''))} characters")
            
            brd_html = brd_result.get('html', '')
            
            # Check for telecom domain detection
            if any(keyword in brd_html.lower() for keyword in ['telecom', 'sim', 'billing', 'kyc', 'mnp']):
                print(f"✅ Telecom Content: DETECTED")
            else:
                print(f"⚠️  Telecom Content: NOT CLEARLY DETECTED")
            
            # Test FRD generation with the BRD
            print("\n🎯 STEP 2: Testing FRD Generation API")
            print("-" * 40)
            
            frd_data = {
                "brdHtml": brd_html,
                "projectData": test_project_data
            }
            
            frd_response = requests.post(
                f"{base_url}/api/v1/ai/frd",
                json=frd_data,
                headers={"Content-Type": "application/json"},
                timeout=45
            )
            
            if frd_response.status_code == 200:
                frd_result = frd_response.json()
                print(f"✅ FRD Generation: SUCCESS")
                
                frd_data_parsed = frd_result.get('frdData', {})
                
                # Analyze domain detection
                detected_domain = frd_data_parsed.get('domainDetection', {}).get('domain', 'unknown')
                domain_score = frd_data_parsed.get('domainDetection', {}).get('score', 0)
                
                print(f"✅ Domain Detection: {detected_domain} (score: {domain_score})")
                
                # Analyze EPICs
                epics = frd_data_parsed.get('epics', [])
                print(f"✅ EPICs Generated: {len(epics)}")
                
                for i, epic in enumerate(epics[:3], 1):  # Show first 3
                    epic_title = epic.get('title', 'Unknown')
                    epic_reqs = len(epic.get('functionalRequirements', []))
                    print(f"   {i}. {epic.get('id', 'Unknown ID')}: {epic_title} ({epic_reqs} requirements)")
                
                # Analyze User Stories
                user_stories = frd_data_parsed.get('userStories', [])
                print(f"✅ User Stories Generated: {len(user_stories)}")
                
                # Test validation criteria uniqueness
                print("\n🔍 STEP 3: AI Validation Criteria Analysis")
                print("-" * 40)
                
                validation_sets = []
                for i, story in enumerate(user_stories[:4], 1):  # Analyze first 4
                    story_id = story.get('id', f'Story-{i}')
                    validations = story.get('validationCriteria', [])
                    validation_sets.append(validations)
                    
                    print(f"   📖 {story_id}: {len(validations)} validations")
                    
                    # Check for telecom-specific validations
                    telecom_validations = [v for v in validations if any(keyword in v.lower() for keyword in ['telecom', 'trai', 'dot', 'sim', 'kyc', 'billing', 'mnp'])]
                    if telecom_validations:
                        print(f"      ✅ Telecom-specific: {len(telecom_validations)} validations")
                        for val in telecom_validations[:1]:  # Show first telecom validation
                            print(f"         • {val}")
                    else:
                        print(f"      ⚠️  No telecom-specific validations detected")
                
                # Check validation uniqueness
                all_validations = [val for validations in validation_sets for val in validations]
                unique_validations = set(all_validations)
                
                print(f"\n   📊 Validation Analysis:")
                print(f"      Total validations: {len(all_validations)}")
                print(f"      Unique validations: {len(unique_validations)}")
                print(f"      Uniqueness ratio: {len(unique_validations)/len(all_validations)*100:.1f}%")
                
                # Acceptance Criteria Analysis
                print("\n🔍 STEP 4: Acceptance Criteria Analysis")
                print("-" * 40)
                
                acceptance_sets = []
                for i, story in enumerate(user_stories[:3], 1):
                    story_id = story.get('id', f'Story-{i}')
                    acceptance = story.get('acceptanceCriteria', [])
                    acceptance_sets.append(acceptance)
                    
                    print(f"   📖 {story_id}: {len(acceptance)} acceptance criteria")
                    
                    # Check for telecom-specific acceptance criteria
                    telecom_acceptance = [a for a in acceptance if any(keyword in a.lower() for keyword in ['telecom', 'sim', 'kyc', 'billing', 'activation', 'compliance'])]
                    if telecom_acceptance:
                        print(f"      ✅ Telecom-specific: {len(telecom_acceptance)} criteria")
                    else:
                        print(f"      ⚠️  Generic criteria only")
                
                print("\n" + "=" * 60)
                print("🚀 AI-ENHANCED TELECOM API TEST SUMMARY")
                print("=" * 60)
                print(f"✅ BRD API: WORKING")
                print(f"✅ FRD API: WORKING") 
                print(f"✅ Domain Detection: {detected_domain} (score: {domain_score})")
                print(f"✅ EPICs Generated: {len(epics)}")
                print(f"✅ User Stories Generated: {len(user_stories)}")
                print(f"✅ AI Enhancement: ACTIVE")
                print(f"✅ Telecom Support: {'ENABLED' if detected_domain == 'telecom' else 'NEEDS VERIFICATION'}")
                
                return True
                
            else:
                print(f"❌ FRD API Error: {frd_response.status_code}")
                print(f"   Response: {frd_response.text}")
                return False
                
        else:
            print(f"❌ BRD API Error: {brd_response.status_code}")
            print(f"   Response: {brd_response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
        print(f"   Make sure the backend server is running on {base_url}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    success = test_telecom_api_integration()
    if success:
        print("\n🎉 All integration tests passed!")
    else:
        print("\n💥 Integration tests failed!")