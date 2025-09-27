#!/usr/bin/env python3
"""Test script to check if AI service imports correctly."""

import sys
import os

# Add the backend path
backend_path = os.path.join(os.getcwd(), 'react-python-auth', 'backend')
sys.path.insert(0, backend_path)

print("🔍 Testing AI Service Import...")
print(f"Backend path: {backend_path}")

try:
    from app.services.ai_service import generate_frd_html_from_brd
    print("✅ AI Service imported successfully!")
    
    # Test basic function call
    test_brd = "Simple test BRD with product and checkout requirements."
    result = generate_frd_html_from_brd("Test Project", test_brd, 1)
    print(f"✅ Function call successful! Output length: {len(result)}")
    
    # Check for intelligent features
    if "Acceptance Criteria" in result and "Validation Rules" in result:
        print("✅ Intelligent features detected!")
    else:
        print("⚠️  Intelligent features not found in output")
        
except Exception as e:
    print(f"❌ Import/execution failed: {e}")
    import traceback
    traceback.print_exc()