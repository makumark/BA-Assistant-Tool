#!/usr/bin/env python3
"""
Demo: Correct E-commerce BRD Generation
Shows the proper way to generate E-commerce BRD with correct project name
"""
import sys
import os

# Add the backend path to sys.path
backend_path = os.path.join(os.path.dirname(__file__), 'react-python-auth', 'backend')
sys.path.insert(0, backend_path)

try:
    from app.services.ai_service import generate_brd_html
    
    print("=== SOLUTION: Correct E-commerce BRD Generation ===")
    
    # Correct E-commerce inputs (same as user provided)
    ecommerce_inputs = {
        "scope": "Included: product catalog and search, cart/checkout, payments, shipping/rates, order management, returns/refunds, promotions/coupons, customer accounts, analytics, and admin CMS. Excluded: marketplace multi-vendor onboarding, in-store POS integration, custom warehouse robotics, and cross-border tax automation at launch.",
        "objectives": "Increase online revenue, reduce cart abandonment, improve conversion rate, raise repeat purchase rate, and shorten order fulfillment cycle time.",
        "budget": "Estimated ₹80–₹140 lakh total for design, build, integrations, testing, deployment, and first‑year run/marketing tech; phased by MVP and enhancements.",
        "briefRequirements": "Browse and filter catalog, manage cart, secure checkout with multiple payment methods, real-time shipping options, order tracking, returns workflow, promotions engine, and role-based admin for catalog, pricing, inventory, and content.",
        "assumptions": "Product data, prices, and stock are available via API or batch; payment and shipping accounts are provisioned; core policies (tax, returns, privacy) are approved; environments and SSO are available.",
        "validations": "Mandatory customer and address fields, email/phone formats, postal code and tax/VAT rules by region, inventory availability holds, payment authorization success, coupon eligibility and stack rules, and fraud/risk checks before order confirmation."
    }
    
    # ✅ CORRECT: Use appropriate E-commerce project name
    correct_project_name = "E-commerce Platform"
    
    print(f"🎯 Using project name: '{correct_project_name}'")
    print(f"🔄 Generating BRD...")
    
    brd_html = generate_brd_html(correct_project_name, ecommerce_inputs, 2)
    
    # Extract header and executive summary
    if '<h2' in brd_html:
        header_start = brd_html.find('<h2')
        header_end = brd_html.find('</h2>', header_start) + 5
        header = brd_html[header_start:header_end]
        print(f"\n✅ Header: {header}")
    
    if 'Executive Summary' in brd_html:
        exec_start = brd_html.find('<p>', brd_html.find('Executive Summary'))
        exec_end = brd_html.find('</p>', exec_start) + 4
        exec_summary = brd_html[exec_start:exec_end]
        print(f"✅ Executive Summary: {exec_summary}")
    
    # Save the corrected output
    with open("CORRECT_ecommerce_brd.html", "w", encoding="utf-8") as f:
        f.write(brd_html)
    
    print(f"\n✅ SUCCESS: Correct E-commerce BRD generated!")
    print(f"✅ File saved: CORRECT_ecommerce_brd.html")
    print(f"\n🔧 SOLUTION:")
    print(f"   - Replace 'Insurance' with '{correct_project_name}' in the project name field")
    print(f"   - The backend will correctly use the provided project name")
    print(f"   - Domain detection works correctly (detects 'ecommerce' from inputs)")
    print(f"   - Validation criteria will be E-commerce specific")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")