#!/usr/bin/env python3
"""
Test with real user validation input vs placeholder text
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
except:
    pass

# Import AI service
from services.ai_service import generate_brd_html

def test_real_vs_placeholder_validations():
    """Test that real user input is preserved while placeholder text triggers domain-specific generation"""
    
    # Test 1: Real user validation input (should be preserved)
    real_inputs = {
        "scope": "Lead generation system",
        "objectives": "Increase conversions",
        "briefRequirements": "Email automation, lead scoring",
        "validations": "All leads must be verified through double opt-in process. Email deliverability must exceed 95%. Campaign ROI must be tracked.",
        "assumptions": "CRM available",
        "constraints": "6 months"
    }
    
    print("🧪 Test 1: Real user validation input")
    html1 = generate_brd_html("Marketing System", real_inputs, 1)
    
    with open("test_real_validations.html", "w", encoding="utf-8") as f:
        f.write(html1)
    
    if "double opt-in process" in html1:
        print("✅ Real user validation input preserved")
    else:
        print("❌ Real user validation input lost")
    
    # Test 2: Placeholder/test input (should trigger domain-specific generation)
    placeholder_inputs = {
        "scope": "Lead generation system",
        "objectives": "Increase conversions", 
        "briefRequirements": "Email automation, lead scoring",
        "validations": "Should show marketing-specific validation criteria",
        "assumptions": "CRM available",
        "constraints": "6 months"
    }
    
    print("🧪 Test 2: Placeholder validation input")
    html2 = generate_brd_html("Marketing System", placeholder_inputs, 1)
    
    with open("test_placeholder_validations.html", "w", encoding="utf-8") as f:
        f.write(html2)
    
    if "campaign performance tracking" in html2 and "Should show marketing" not in html2:
        print("✅ Placeholder input replaced with domain-specific criteria")
    else:
        print("❌ Placeholder input not handled correctly")
    
    # Test 3: Empty validation input (should trigger domain-specific generation)
    empty_inputs = {
        "scope": "Lead generation system",
        "objectives": "Increase conversions",
        "briefRequirements": "Email automation, lead scoring", 
        "validations": "",
        "assumptions": "CRM available",
        "constraints": "6 months"
    }
    
    print("🧪 Test 3: Empty validation input")
    html3 = generate_brd_html("Marketing System", empty_inputs, 1)
    
    if "customer consent validation" in html3:
        print("✅ Empty input generates domain-specific criteria")
    else:
        print("❌ Empty input not handled correctly")

if __name__ == "__main__":
    test_real_vs_placeholder_validations()