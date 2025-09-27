#!/usr/bin/env python3
"""
Direct test of AI service - bypass server to understand why frontend sees generic validation
"""

import sys
import os

# Add backend app to path
backend_path = os.path.join("react-python-auth", "backend", "app")
if os.path.exists(backend_path):
    sys.path.insert(0, backend_path)
    print(f"✅ Added {backend_path} to Python path")

# Load environment
try:
    from dotenv import load_dotenv
    env_path = os.path.join("react-python-auth", "backend", ".env")
    load_dotenv(env_path, override=True)
    print(f"✅ Loaded .env from: {env_path}")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print(f"✅ OpenAI API key loaded: {openai_key[:10]}...")
    else:
        print("❌ OpenAI API key not found")
except Exception as e:
    print(f"❌ Error loading .env: {e}")

# Import AI service
try:
    from services.ai_service import generate_brd_html
    print("✅ AI service imported successfully")
except Exception as e:
    print(f"❌ Failed to import AI service: {e}")
    sys.exit(1)

def test_ai_service_directly():
    """Test AI service directly to see what it generates"""
    
    # Marketing automation test data - should detect as marketing domain
    test_inputs = {
        "scope": "Lead generation, email campaigns, customer segmentation, and automated nurturing workflows",
        "objectives": "Increase lead conversion rates by 25%, reduce manual marketing tasks by 60%",
        "briefRequirements": "Email marketing automation, lead scoring system, CRM integration, campaign analytics",
        "assumptions": "CRM system available for integration, marketing team trained",
        "constraints": "6 month development timeline, GDPR compliance required",
        "validations": "Should show marketing-specific validation criteria, not generic ones",
        "budget": "$50,000 development cost"
    }
    
    project = "Marketing Automation Platform"
    version = 1
    
    print(f"🧪 Testing AI service directly...")
    print(f"📤 Project: {project}")
    print(f"📤 Expected domain: Marketing")
    
    try:
        html = generate_brd_html(project, test_inputs, version)
        
        print(f"📥 Generated HTML length: {len(html)} characters")
        
        # Save the output
        with open("test_direct_ai_service_output.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("💾 Saved response to test_direct_ai_service_output.html")
        
        # Check for domain detection
        if "enhanced fallback" in html.lower():
            print("✅ Using enhanced domain-specific fallback")
        elif "ai expansion failed" in html.lower():
            print("❌ Using basic error fallback")
        else:
            print("✅ Generated with AI enhancement")
        
        # Check for marketing-specific content
        if "marketing" in html.lower() or "campaign" in html.lower():
            print("✅ Contains marketing-specific content")
        else:
            print("❌ Missing marketing-specific content")
        
        # Check validation criteria - the key issue
        if "campaign performance" in html.lower():
            print("✅ Contains marketing-specific validation criteria")
        elif "email deliverability" in html.lower():
            print("✅ Contains marketing-specific validation criteria")
        elif "mandatory master data fields" in html.lower():
            print("❌ Contains generic validation criteria (PROBLEM!)")
            # Show the validation section
            print("📄 Extracting validation section:")
            lines = html.split('\n')
            in_validation = False
            for line in lines:
                if "validation" in line.lower() and ("<h2" in line or "<h3" in line):
                    in_validation = True
                    print(f"   {line.strip()}")
                elif in_validation and ("<h2" in line or "<h3" in line):
                    break
                elif in_validation:
                    print(f"   {line.strip()}")
        else:
            print("❓ Validation criteria unclear")
            # Search for validation content
            print("📄 Searching for validation content:")
            lines = html.split('\n')
            for i, line in enumerate(lines):
                if "validation" in line.lower():
                    print(f"   Line {i}: {line.strip()}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI service failed: {e}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    test_ai_service_directly()