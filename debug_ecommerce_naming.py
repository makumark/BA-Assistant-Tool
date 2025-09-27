#!/usr/bin/env python3
"""
Test E-commerce BRD Generation Issue
Debug why it shows "Insurance" instead of "E-commerce Platform"
"""
import sys
import os

# Add the backend path to sys.path
backend_path = os.path.join(os.path.dirname(__file__), 'react-python-auth', 'backend')
sys.path.insert(0, backend_path)

try:
    from app.services.ai_service import generate_brd_html, _detect_domain_from_inputs
    
    print("=== Testing E-commerce BRD Generation Issue ===")
    
    # Exact E-commerce inputs from the user
    ecommerce_inputs = {
        "scope": "Included: product catalog and search, cart/checkout, payments, shipping/rates, order management, returns/refunds, promotions/coupons, customer accounts, analytics, and admin CMS. Excluded: marketplace multi-vendor onboarding, in-store POS integration, custom warehouse robotics, and cross-border tax automation at launch.",
        "objectives": "Increase online revenue, reduce cart abandonment, improve conversion rate, raise repeat purchase rate, and shorten order fulfillment cycle time.",
        "budget": "Estimated ₹80–₹140 lakh total for design, build, integrations, testing, deployment, and first‑year run/marketing tech; phased by MVP and enhancements.",
        "briefRequirements": "Browse and filter catalog, manage cart, secure checkout with multiple payment methods, real-time shipping options, order tracking, returns workflow, promotions engine, and role-based admin for catalog, pricing, inventory, and content.",
        "assumptions": "Product data, prices, and stock are available via API or batch; payment and shipping accounts are provisioned; core policies (tax, returns, privacy) are approved; environments and SSO are available.",
        "validations": "Mandatory customer and address fields, email/phone formats, postal code and tax/VAT rules by region, inventory availability holds, payment authorization success, coupon eligibility and stack rules, and fraud/risk checks before order confirmation."
    }
    
    # Test domain detection
    detected_domain = _detect_domain_from_inputs(ecommerce_inputs)
    print(f"🎯 Detected Domain: {detected_domain}")
    
    # Test with different project names to see what happens
    test_project_names = [
        "E-commerce Platform",
        "Online Shopping Platform", 
        "E-commerce System",
        "Insurance Management System",  # This to test if it gets confused
        ""  # Empty to see default behavior
    ]
    
    for project_name in test_project_names:
        print(f"\n=== Testing with project name: '{project_name}' ===")
        
        try:
            brd_html = generate_brd_html(project_name, ecommerce_inputs, 2)
            
            # Check the header and executive summary
            if '<h2' in brd_html:
                header_start = brd_html.find('<h2')
                header_end = brd_html.find('</h2>', header_start) + 5
                header_content = brd_html[header_start:header_end]
                print(f"Header: {header_content}")
            
            if 'Executive Summary' in brd_html:
                exec_start = brd_html.find('<h3>Executive Summary</h3>')
                exec_end = brd_html.find('<h3>', exec_start + 1)
                exec_content = brd_html[exec_start:exec_end] if exec_end > 0 else brd_html[exec_start:exec_start+200]
                print(f"Executive Summary: {exec_content}")
            
            # Save for detailed inspection
            filename = f"debug_ecommerce_{project_name.replace(' ', '_').replace('-', '_').lower() or 'empty'}.html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(brd_html)
            print(f"✅ Saved as {filename}")
            
        except Exception as e:
            print(f"❌ Error generating BRD: {e}")
    
    print(f"\n=== Summary ===")
    print(f"Detected domain for E-commerce inputs: {detected_domain}")
    print("Check the saved HTML files to see which project name appears in headers")
            
except ImportError as e:
    print(f"❌ Import Error: {e}")
except Exception as e:
    print(f"❌ Test Error: {e}")
    import traceback
    traceback.print_exc()