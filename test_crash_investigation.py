#!/usr/bin/env python3
"""
Test AI service function directly to identify what's causing server crashes
"""

import sys
import os

# Add backend app to path
backend_path = os.path.join("react-python-auth", "backend", "app")
if os.path.exists(backend_path):
    sys.path.insert(0, backend_path)

# Load environment
try:
    from dotenv import load_dotenv
    env_path = os.path.join("react-python-auth", "backend", ".env")
    load_dotenv(env_path, override=True)
    print(f"✅ Loaded .env")
except Exception as e:
    print(f"❌ Error loading .env: {e}")

# Import AI service
print("🔄 Importing AI service...")
try:
    from services.ai_service import generate_brd_html
    print("✅ AI service imported successfully")
except Exception as e:
    print(f"❌ Failed to import AI service: {e}")
    import traceback
    print(f"Full traceback: {traceback.format_exc()}")
    sys.exit(1)

def test_ai_crash():
    """Test what causes the AI service to crash the server"""
    
    # Same test data that we tried through the API
    test_inputs = {
        "scope": "Lead generation",
        "objectives": "Increase conversions", 
        "briefRequirements": "Email automation",
        "validations": "Should show marketing-specific criteria",
        "assumptions": "CRM available",
        "constraints": "6 months",
        "budget": "$50k"
    }
    
    project = "Marketing Automation"
    version = 1
    
    print(f"🧪 Testing AI service with crash-prone data...")
    print(f"📤 Project: {project}")
    
    try:
        print("🔄 Calling generate_brd_html...")
        html = generate_brd_html(project, test_inputs, version)
        
        print(f"📥 Generated HTML length: {len(html)} characters")
        print("✅ AI service completed without crash")
        
        # Check the validation content
        if "customer consent validation" in html.lower():
            print("✅ Contains marketing-specific validation criteria")
        elif "mandatory master data fields" in html.lower():
            print("❌ Contains generic validation criteria (frontend fallback)")
        else:
            print("❓ Validation criteria unclear")
        
        # Save the output for inspection
        with open("test_crash_investigation.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("💾 Saved response to test_crash_investigation.html")
        
        return True
        
    except Exception as e:
        print(f"❌ AI service crashed: {e}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    print("🔍 Investigating server crash issue...")
    success = test_ai_crash()
    if success:
        print("\n✅ AI service works fine - server crash must be elsewhere")
    else:
        print("\n❌ AI service crashes - need to fix the error")