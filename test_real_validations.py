#!/usr/bin/env python3
"""
Test Healthcare User Story-Specific Validations - Simple Test
"""

import sys
import os

# Add the backend app directory to Python path
backend_dir = r"c:\Users\pavan\OneDrive\Desktop\ba-tool\react-python-auth\backend"
app_dir = os.path.join(backend_dir, 'app')
sys.path.insert(0, app_dir)
sys.path.insert(0, backend_dir)

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = os.path.join(backend_dir, '.env')
    load_dotenv(env_path, override=True)
    print(f"✅ Loaded .env from: {env_path}")
except ImportError:
    print("❌ python-dotenv not available")

# Import AI service
try:
    from services.ai_service import generate_frd_html_from_brd
    print("✅ AI service imported successfully")
except Exception as e:
    print(f"❌ Failed to import AI service: {e}")
    sys.exit(1)

def test_simple_healthcare():
    print("🏥 Testing Healthcare Validation Specificity...")
    
    healthcare_brd = """Executive Summary
This document captures the business requirements for Health Care.

Project Scope
Patient registration, appointment scheduling, electronic health records integration, billing module

Business Requirements (EPIC Format)
EPIC-01 Core Business Requirements
Requirements:
• Ability to create and manage patient profiles, schedule appointments with notifications, store and update patient medical history securely, and generate invoices with insurance claim support
• Enforce prescription and medication safety checks"""

    try:
        frd_html = generate_frd_html_from_brd("Health Care", healthcare_brd, 1)
        print(f"✅ FRD Generated: {len(frd_html)} characters")
        
        # Save and show first validation section
        with open("test_real_validations.html", "w", encoding="utf-8") as f:
            f.write(frd_html)
        
        # Find validation sections
        if "🔍 Validation Criteria:" in frd_html:
            print("\n✅ Found validation criteria sections")
            
            # Extract first validation section
            start = frd_html.find("🔍 Validation Criteria:")
            end = frd_html.find("Priority:", start)
            if end == -1:
                end = start + 1000
            
            validation_section = frd_html[start:end]
            print("\n📋 First validation section:")
            print(validation_section[:800] + "...")
            
            # Check for specific vs generic
            if any(term in validation_section.lower() for term in ["patient", "appointment", "medical", "prescription"]):
                print("✅ Contains healthcare-specific validations")
            else:
                print("❌ Still using generic validations")
        else:
            print("❌ No validation criteria found")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    test_simple_healthcare()