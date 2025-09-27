#!/usr/bin/env python3
"""
Quick Cross-Domain AI Enhancement Test
Tests one domain to verify AI enhancements are working
"""

import requests
import json

BASE_URL = "http://localhost:8001"
AI_ENDPOINT = f"{BASE_URL}/ai/frd"

def quick_test():
    print("🚀 Quick Cross-Domain AI Enhancement Test")
    print("Testing Healthcare Domain...")
    
    payload = {
        "project": "Healthcare Management System",
        "brd": """Patient registration and medical record management
Appointment scheduling with clinical workflow optimization
Prescription management with drug interaction checking
Insurance claim processing and HIPAA compliance""",
        "version": 1
    }
    
    try:
        response = requests.post(AI_ENDPOINT, json=payload, timeout=30)
        if response.status_code == 200:
            response_data = response.json()
            content = response_data.get("html", "")
            
            # Check for AI enhancements
            has_epics = "EPIC-" in content
            has_acceptance = "Acceptance Criteria" in content
            has_validation = "Validation Criteria" in content
            has_healthcare_terms = any(term in content.lower() for term in ['hipaa', 'patient', 'clinical', 'medical'])
            has_healthcare_personas = any(persona in content for persona in ['Patient', 'Physician', 'Clinical'])
            
            print(f"✅ Has EPICs: {has_epics}")
            print(f"✅ Has Acceptance Criteria: {has_acceptance}")
            print(f"✅ Has Validation Criteria: {has_validation}")
            print(f"✅ Has Healthcare Terms: {has_healthcare_terms}")
            print(f"✅ Has Healthcare Personas: {has_healthcare_personas}")
            
            # Save output
            with open("quick_healthcare_test.html", "w", encoding="utf-8") as f:
                f.write(content)
            
            if all([has_epics, has_acceptance, has_validation, has_healthcare_terms]):
                print("🎉 SUCCESS: Healthcare domain shows AI enhancement!")
                return True
            else:
                print("⚠️ PARTIAL: Some enhancements missing")
                return False
                
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        return False

if __name__ == "__main__":
    quick_test()