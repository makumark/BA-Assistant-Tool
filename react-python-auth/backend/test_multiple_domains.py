#!/usr/bin/env python3
"""
Test domain-agnostic BRD generation with multiple domains to ensure
the generator doesn't add domain-specific content.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_healthcare_domain():
    """Test with healthcare domain to verify domain-agnostic approach."""
    
    from app.services.ai_service import generate_brd_html
    
    inputs = {
        "scope": """
Included: patient registration and demographics, appointment scheduling, clinical documentation (SOAP notes), prescription management, lab results integration, billing and claims processing, patient portal access.

Excluded: electronic health records (EHR) replacement, radiology PACS integration, advanced clinical decision support, telemedicine platform (phase 2).
        """,
        "objectives": """
Streamline patient intake processes; reduce appointment no-shows; improve clinical documentation quality; enhance prescription accuracy; accelerate billing cycles; increase patient engagement.
        """,
        "briefRequirements": """
Registration: patient demographics; insurance verification; consent forms; emergency contacts.
Scheduling: appointment booking; calendar management; reminders; waitlist management.
Clinical: SOAP notes; vital signs capture; diagnosis codes (ICD-10); treatment plans.
Pharmacy: e-prescribing; drug interaction checks; formulary integration.
Billing: charge capture; claims submission; payment processing; statement generation.
Portal: appointment scheduling; test results viewing; secure messaging; bill payment.
        """,
        "assumptions": """
Patient master data will be cleansed prior to migration; integration with insurance eligibility services will be available; clinical staff have basic computer literacy; existing billing system exports are available.
        """,
        "validations": """
Patient identity verification before records access; duplicate patient detection; appointment conflict checking; prescription allergy checks; insurance coverage validation; claim submission edits; secure messaging encryption.
        """
    }
    
    print("=" * 80)
    print("🧪 Testing Healthcare Domain BRD Generation")
    print("=" * 80)
    print()
    
    project = "Healthcare Practice Management System"
    version = 1
    
    html = generate_brd_html(project, inputs, version)
    
    print(f"✅ BRD Generated: {len(html)} characters")
    print()
    
    # Save output
    output_file = "/tmp/healthcare_domain_agnostic_brd.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"💾 BRD saved to: {output_file}")
    print()
    
    # Verify structure
    print("🔍 Verifying Domain-Agnostic Structure:")
    print("-" * 80)
    
    checks = [
        ("EPIC-", "EPICs with proper IDs"),
        ("OBJ-", "Objectives with proper IDs"),
        ("KPI-", "KPIs with proper IDs"),
        ("RISK-", "Risks with proper IDs"),
        ("TBV", "TBV markers for inferred content"),
        ("Scope of the Project", "Scope section"),
        ("Business Objectives", "Objectives section"),
        ("Success Metrics", "KPIs section"),
        ("Risk Assessment", "Risk section")
    ]
    
    all_passed = True
    for pattern, description in checks:
        if pattern in html:
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ Missing: {description}")
            all_passed = False
    
    print()
    if all_passed:
        print("✅ All domain-agnostic structure checks passed!")
    else:
        print("❌ Some checks failed")
    
    return html


def test_ecommerce_domain():
    """Test with e-commerce domain."""
    
    from app.services.ai_service import generate_brd_html
    
    inputs = {
        "scope": """
Included: product catalog management, shopping cart and checkout, payment processing, order fulfillment, inventory tracking, customer accounts, returns and refunds.

Excluded: warehouse management system replacement, third-party marketplace integrations, advanced recommendation engine (phase 2).
        """,
        "objectives": """
Reduce cart abandonment rates; improve checkout conversion; accelerate order processing; enhance inventory accuracy; increase customer retention; provide real-time order tracking.
        """,
        "briefRequirements": """
Catalog: product information; pricing; categories; search and filters; product images.
Cart: add to cart; quantity updates; saved carts; wish lists.
Checkout: guest checkout; address validation; shipping options; tax calculation; payment processing.
Orders: order confirmation; status tracking; fulfillment workflow; shipping labels.
Inventory: stock levels; reorder points; supplier management; stock adjustments.
Accounts: registration; profile management; order history; preferences.
        """,
        "assumptions": """
Product data will be migrated from existing systems; payment gateway integrations are available; shipping carrier APIs are accessible; SSL certificates for secure transactions.
        """,
        "validations": """
Product SKU uniqueness; inventory level checks before order acceptance; payment authorization before fulfillment; shipping address validation; credit card security (PCI DSS); fraud detection rules.
        """
    }
    
    print("=" * 80)
    print("🧪 Testing E-Commerce Domain BRD Generation")
    print("=" * 80)
    print()
    
    project = "Online Shopping Platform"
    version = 1
    
    html = generate_brd_html(project, inputs, version)
    
    print(f"✅ BRD Generated: {len(html)} characters")
    print()
    
    # Save output
    output_file = "/tmp/ecommerce_domain_agnostic_brd.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"💾 BRD saved to: {output_file}")
    print()
    
    return html


if __name__ == "__main__":
    test_healthcare_domain()
    print("\n\n")
    test_ecommerce_domain()
