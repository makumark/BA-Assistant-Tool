#!/usr/bin/env python3
"""
Debug FRD Generation - Find out why it's generating BRD instead of FRD
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
    from services.ai_service import generate_frd_html_from_brd, _generate_enhanced_fallback_frd
    print("✅ AI service imported successfully")
except Exception as e:
    print(f"❌ Failed to import AI service: {e}")
    sys.exit(1)

def debug_frd_generation():
    print("🔍 Debug FRD Generation...")
    
    healthcare_brd = """Executive Summary
This document captures the business requirements for Health Care.

Project Scope
Patient registration, appointment scheduling, electronic health records integration, billing module

Business Requirements (EPIC Format)
EPIC-01 Core Business Requirements
Requirements:
• Ability to create and manage patient profiles, schedule appointments with notifications, store and update patient medical history securely, and generate invoices with insurance claim support"""

    print("🔄 Testing direct fallback function...")
    
    try:
        # Test the fallback function directly
        fallback_html = _generate_enhanced_fallback_frd("Health Care", healthcare_brd, 1)
        print(f"✅ Fallback FRD Generated: {len(fallback_html)} characters")
        
        # Check if it's actually FRD
        if "Functional Requirements Document" in fallback_html:
            print("✅ Generated FRD structure")
        elif "Business Requirements Document" in fallback_html or "Business Requirement Document" in fallback_html:
            print("❌ Generated BRD structure instead of FRD!")
        else:
            print("❓ Unknown document structure")
        
        # Check for validation criteria
        if "🔍 Validation Criteria:" in fallback_html or "Validation Rules:" in fallback_html:
            print("✅ Contains validation sections")
        else:
            print("❌ No validation sections found")
        
        # Save for inspection
        with open("debug_frd_fallback.html", "w", encoding="utf-8") as f:
            f.write(fallback_html)
        print("💾 Saved to debug_frd_fallback.html")
        
        # Show first 500 chars
        print(f"\n📄 First 500 characters:")
        print(fallback_html[:500] + "...")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    debug_frd_generation()