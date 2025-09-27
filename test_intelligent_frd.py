#!/usr/bin/env python3
"""Test script for intelligent FRD generation."""

import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'react-python-auth', 'backend'))

from app.services.ai_service import generate_frd_html_from_brd

# Test BRD for e-commerce domain
test_brd = """
# Business Requirements Document - E-commerce Platform

## Executive Summary
Develop a comprehensive e-commerce platform that enables customers to browse products, manage shopping carts, and complete secure checkout processes.

## Business Requirements
- Implement product catalog with search and filtering capabilities
- Create shopping cart functionality with item management
- Develop secure checkout process with payment integration
- Establish customer account management system
- Build order tracking and management system

## Project Scope
The system will support online retail operations including product management, customer interactions, and order processing.

## Business Objectives
- Increase online sales by 40%
- Improve customer satisfaction through seamless shopping experience
- Reduce cart abandonment rate by implementing streamlined checkout
"""

print("🧪 Testing Intelligent FRD Generation...")
print("=" * 50)

try:
    # Generate FRD using the intelligent system
    frd_html = generate_frd_html_from_brd("E-commerce Platform", test_brd, 1)
    
    print("✅ FRD Generation Successful!")
    print(f"📊 Generated HTML Length: {len(frd_html)} characters")
    
    # Check for intelligent content
    checks = [
        ("FR- codes", "FR-" in frd_html),
        ("Acceptance Criteria", "Acceptance Criteria" in frd_html),
        ("Validation Rules", "Validation Rules" in frd_html),
        ("Domain-specific content", any(term in frd_html for term in ["16 digits", "CVV", "payment", "cart"])),
        ("E-commerce detection", "ecommerce" in frd_html.lower() or "e-commerce" in frd_html.lower())
    ]
    
    print("\n📋 Content Analysis:")
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}")
    
    # Show sample of generated content
    print("\n📄 Sample Content (first 500 chars):")
    print("-" * 40)
    print(frd_html[:500] + "..." if len(frd_html) > 500 else frd_html)
    
    # Save output to file for inspection
    with open('test_frd_output.html', 'w', encoding='utf-8') as f:
        f.write(frd_html)
    print(f"\n💾 Full output saved to: test_frd_output.html")

except Exception as e:
    print(f"❌ Error generating FRD: {e}")
    import traceback
    traceback.print_exc()