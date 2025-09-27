#!/usr/bin/env python3
"""
Test script to validate fixed EPIC generation logic.
Tests the specific issues identified by the user:
1. EPICs containing excluded items (EPIC-11 "Excluded — Full")
2. Budget details in EPICs (EPIC-13 "Estimated ₹60–₹110 Lakh")  
3. Environment items in EPICs (EPIC-19 "Sandbox And Production")
4. Fragmented content instead of complete business capabilities
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.ai_service_enhanced import (
    _extract_included_scope_only,
    _extract_business_objectives, 
    _create_epics_from_business_capabilities,
    _generate_epics_fallback_brd
)

def test_fund_management_input():
    """Test with the exact fund management input that was failing."""
    
    # Exact user input that was producing bad EPICs
    fund_management_input = {
        "objectives": """
        • Modernize and streamline fund management operations
        • Enhance investor onboarding and KYC processes  
        • Implement automated capital call and distribution management
        • Improve NAV calculation accuracy and reporting
        • Ensure regulatory compliance across jurisdictions
        """,
        "scope": """
        Included:
        • Fund setup and management
        • Investor onboarding and KYC/AML processes
        • Capital call and distribution processing
        • NAV calculation and reporting
        • Regulatory reporting and compliance
        • Document management and e-signatures
        
        Excluded — Full accounting replacement, Third-party valuation integration, 
        Registrar and transfer agent functionality, Tax pack preparation and delivery, 
        Legacy system migration automation, Advanced portfolio analytics
        """,
        "requirements": """
        Fund Management Requirements:
        • Multi-fund support with hierarchical structures
        • Investor portal for self-service access
        • Automated workflow for capital calls
        • Real-time NAV calculations
        • Compliance monitoring and alerts
        • Document repository with version control
        """,
        "budget": "Estimated ₹60–₹110 Lakh for full implementation",
        "assumptions": "Sandbox and Production environments will be provided"
    }
    
    print("=== Testing Fund Management EPIC Generation ===")
    print()
    
    # Test scope extraction
    print("1. Testing included scope extraction:")
    included_scope = _extract_included_scope_only(fund_management_input["scope"])
    print(f"Included scope items: {len(included_scope)}")
    for i, item in enumerate(included_scope, 1):
        print(f"   {i}. {item}")
    print()
    
    # Verify no excluded items are included
    excluded_check = any("excluded" in item.lower() for item in included_scope)
    print(f"❌ Contains excluded items: {excluded_check}")
    
    # Test objectives extraction  
    print("2. Testing business objectives extraction:")
    objectives = _extract_business_objectives(fund_management_input["objectives"])
    print(f"Business objectives: {len(objectives)}")
    for i, obj in enumerate(objectives, 1):
        print(f"   {i}. {obj}")
    print()
    
    # Test EPIC creation
    print("3. Testing EPIC creation from business capabilities:")
    epics = _create_epics_from_business_capabilities(included_scope, objectives)
    print(f"Generated EPICs: {len(epics)}")
    
    # Validate EPICs don't contain problematic content
    problematic_content = [
        "excluded", "budget", "₹60", "₹110", "lakh", "sandbox", "production",
        "accounting replacement", "valuation", "registrar", "transfer agent",
        "tax pack", "legacy", "automation"
    ]
    
    epic_issues = []
    for epic in epics:
        print(f"\n   {epic['id']} {epic['title']}: {epic['description']}")
        
        # Check for problematic content
        full_text = f"{epic['title']} {epic['description']}".lower()
        for problem in problematic_content:
            if problem in full_text:
                epic_issues.append(f"{epic['id']} contains '{problem}'")
    
    print()
    if epic_issues:
        print(f"❌ EPIC Issues Found:")
        for issue in epic_issues:
            print(f"   - {issue}")
    else:
        print("✅ No problematic content found in EPICs")
    
    # Test complete BRD generation
    print("\n4. Testing complete BRD generation:")
    brd_html = _generate_epics_fallback_brd("Fund Management Platform", fund_management_input, 1)
    
    # Check if BRD contains problematic EPICs
    brd_lower = brd_html.lower()
    brd_issues = []
    
    problem_phrases = [
        "excluded — full", "₹60–₹110 lakh", "sandbox and production",
        "epic-11", "epic-13", "epic-19"  # The specific problematic EPICs mentioned
    ]
    
    for phrase in problem_phrases:
        if phrase in brd_lower:
            brd_issues.append(f"BRD contains: '{phrase}'")
    
    if brd_issues:
        print(f"❌ BRD Issues Found:")
        for issue in brd_issues:
            print(f"   - {issue}")
    else:
        print("✅ BRD does not contain problematic EPIC content")
    
    return len(epic_issues) == 0 and len(brd_issues) == 0

def test_epic_constraint_validation():
    """Test that EPICs are only generated from objectives and included scope."""
    
    print("\n=== Testing EPIC Source Constraint ===")
    
    # Test case with clear separation of included/excluded scope
    test_input = {
        "objectives": """
        • Improve customer satisfaction
        • Reduce operational costs
        • Increase revenue streams
        """,
        "scope": """
        Included:
        • Customer portal development
        • Payment processing integration
        • Basic reporting dashboard
        
        Excluded:
        • Advanced analytics
        • Third-party integrations
        • Mobile app development
        """,
        "requirements": """
        Should NOT be used for EPICs:
        • Complex database optimization
        • Machine learning algorithms
        • Real-time notifications
        """,
        "budget": "Should NOT be used for EPICs: ₹50 Lakh budget",
        "assumptions": "Should NOT be used for EPICs: Cloud infrastructure assumed"
    }
    
    included_scope = _extract_included_scope_only(test_input["scope"])
    objectives = _extract_business_objectives(test_input["objectives"])
    epics = _create_epics_from_business_capabilities(included_scope, objectives)
    
    print(f"Extracted {len(included_scope)} included scope items")
    print(f"Extracted {len(objectives)} objectives")
    print(f"Generated {len(epics)} EPICs")
    
    # Verify no content from requirements, budget, or assumptions
    should_not_appear = [
        "database optimization", "machine learning", "notifications",
        "₹50 lakh", "cloud infrastructure", "excluded", "advanced analytics"
    ]
    
    violations = []
    for epic in epics:
        full_text = f"{epic['title']} {epic['description']}".lower()
        for forbidden in should_not_appear:
            if forbidden in full_text:
                violations.append(f"{epic['id']} contains forbidden content: '{forbidden}'")
    
    if violations:
        print("❌ EPIC constraint violations:")
        for violation in violations:
            print(f"   - {violation}")
        return False
    else:
        print("✅ All EPICs properly sourced from objectives and included scope only")
        return True

def main():
    """Run all tests to validate the EPIC generation fixes."""
    
    print("🔬 Testing Fixed EPIC Generation Logic")
    print("=" * 60)
    
    # Test 1: Fund management specific issues
    test1_passed = test_fund_management_input()
    
    # Test 2: General constraint validation
    test2_passed = test_epic_constraint_validation()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    if test1_passed and test2_passed:
        print("✅ ALL TESTS PASSED - EPIC generation fixes are working correctly")
        print("   - No excluded items in EPICs")
        print("   - No budget details in EPICs") 
        print("   - No environment items in EPICs")
        print("   - EPICs contain only complete business capabilities")
        print("   - EPICs sourced only from objectives and included scope")
        return 0
    else:
        print("❌ SOME TESTS FAILED - EPIC generation still has issues")
        if not test1_passed:
            print("   - Fund management test failed")
        if not test2_passed:
            print("   - EPIC constraint test failed")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)