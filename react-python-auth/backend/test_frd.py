#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, 'app')

try:
    from services.ai_service import generate_frd_html_from_brd
    print("Testing FRD generation...")
    result = generate_frd_html_from_brd("TestProject", "Test BRD content", 1)
    print(f"Success! Generated {len(result)} characters")
    print("First 200 characters:")
    print(result[:200])
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()