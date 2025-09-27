#!/usr/bin/env python3
"""
Test Fund Management BRD Generation Fixes
Purpose: Validate that EPICs are generated correctly, user stories exclude budget/excluded scope, 
and abbreviations are properly expanded for fund management domain.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ai_service_enhanced import _generate_epics_fallback_brd, _generate_user_stories_fallback_frd, _expand_common_abbreviations

def test_epic_filtering_from_budget_and_excluded_scope():
    """Test that EPICs are NOT generated from budget details or excluded scope items."""
    print("🔬 Test 1: EPIC Filtering from Budget and Excluded Scope")
    print("-" * 60)
    
    # Sample fund management input with budget details and excluded scope
    fund_mgmt_inputs = {
        "objectives": """
        • Streamline investor onboarding with KYC/AML compliance
        • Implement digital capital call management
        • Enhance NAV calculation and reporting
        • Provide secure investor portal access
        """,
        "scope": """
        In Scope:
        • Investor registration and e-sign document workflows
        • KYC/AML verification processes
        • Capital call notifications and tracking
        • Basic NAV reporting and investor statements
        
        Out of Scope:
        • Advanced portfolio analytics with AI/ML
        • Third-party marketplace integrations
        • Legacy system data migration
        • Complex automated trading features
        """,
        "budget": """
        Budget Details:
        • Initial Development: $500,000
        • Annual Maintenance: $100,000
        • Third-party licensing: $50,000
        • Infrastructure costs: $25,000
        """,
        "briefRequirements": """
        • Basic investor management functionality
        • Document storage and retrieval
        • Compliance reporting tools
        """
    }
    
    # Generate BRD using fallback method
    brd_result = _generate_epics_fallback_brd("Fund Management Platform", fund_mgmt_inputs, 1)
    
    # Check that EPICs are derived from objectives and scope, not budget
    print("✅ Generated BRD (checking EPIC sources):")
    
    # Verify EPICs come from objectives/scope
    objectives_keywords = ["investor onboarding", "kyc", "aml", "capital call", "nav", "investor portal"]
    budget_keywords = ["$500,000", "maintenance", "licensing", "infrastructure costs"]
    excluded_keywords = ["advanced portfolio analytics", "ai/ml", "marketplace", "legacy system", "automated trading"]
    
    epic_found_objectives = any(keyword.lower() in brd_result.lower() for keyword in objectives_keywords)
    epic_found_budget = any(keyword in brd_result for keyword in budget_keywords)
    epic_found_excluded = any(keyword.lower() in brd_result.lower() for keyword in excluded_keywords)
    
    print(f"📊 EPICs derived from objectives/scope: {epic_found_objectives}")
    print(f"❌ EPICs include budget details: {epic_found_budget}")
    print(f"❌ EPICs include excluded scope: {epic_found_excluded}")
    
    # Test passes if EPICs come from objectives but NOT from budget or excluded scope
    test_passed = epic_found_objectives and not epic_found_budget and not epic_found_excluded
    
    if test_passed:
        print("✅ TEST PASSED: EPICs correctly sourced from objectives/scope only")
    else:
        print("❌ TEST FAILED: EPICs incorrectly include budget details or excluded scope")
    
    print("\n" + "=" * 60 + "\n")
    return test_passed


def test_user_story_filtering_from_frd():
    """Test that user stories in FRD exclude budget and excluded scope items."""
    print("🔬 Test 2: User Story Filtering in FRD Generation")
    print("-" * 60)
    
    # Sample BRD with budget details and excluded scope in Business Requirements
    sample_brd = """
    <h3>Business Requirements (EPICs)</h3>
    <ul>
        <li><strong>EPIC-01 Investor Onboarding:</strong> Streamlined KYC/AML compliance and e-sign workflows</li>
        <li><strong>EPIC-02 Capital Call Management:</strong> Digital capital call notifications and tracking</li>
        <li><strong>EPIC-03 Budget Processing:</strong> Automated budget allocation and expense tracking</li>
        <li><strong>EPIC-04 Advanced Analytics:</strong> AI/ML-powered portfolio optimization (Out of Scope)</li>
        <li><strong>EPIC-05 NAV Reporting:</strong> Monthly Net Asset Value calculations and investor statements</li>
        <li><strong>EPIC-06 Payment Processing:</strong> Credit card and ACH payment processing</li>
    </ul>
    
    <h3>Budget Details</h3>
    <p>Development costs: $500,000 for initial implementation</p>
    
    <h3>Project Scope</h3>
    <p><strong>Out of Scope:</strong> Advanced analytics, AI/ML features, third-party marketplace integrations</p>
    """
    
    # Generate FRD using fallback method
    frd_result = _generate_user_stories_fallback_frd("Fund Management Platform", sample_brd, 1)
    
    print("✅ Generated FRD (checking user story filtering):")
    
    # Check that user stories exclude budget and excluded scope EPICs
    valid_epics = ["investor onboarding", "capital call", "nav reporting"]
    invalid_epics = ["budget processing", "advanced analytics", "ai/ml", "payment processing"]
    
    valid_found = any(epic.lower() in frd_result.lower() for epic in valid_epics)
    invalid_found = any(epic.lower() in frd_result.lower() for epic in invalid_epics)
    
    print(f"📊 User stories include valid EPICs: {valid_found}")
    print(f"❌ User stories include invalid EPICs (budget/excluded): {invalid_found}")
    
    # Test passes if valid EPICs are included but invalid ones are filtered out
    test_passed = valid_found and not invalid_found
    
    if test_passed:
        print("✅ TEST PASSED: User stories correctly filtered to exclude budget/excluded scope EPICs")
    else:
        print("❌ TEST FAILED: User stories include budget details or excluded scope EPICs")
    
    print("\n" + "=" * 60 + "\n")
    return test_passed


def test_abbreviation_expansion():
    """Test that common fund management abbreviations are properly expanded."""
    print("🔬 Test 3: Abbreviation Expansion")
    print("-" * 60)
    
    test_cases = [
        ("KYC compliance process", "Know Your Customer (KYC) compliance process"),
        ("AML verification required", "Anti-Money Laundering (AML) verification required"),
        ("KYC/AML procedures", "Know Your Customer/Anti-Money Laundering (KYC/AML) procedures"),
        ("e-sign document workflow", "electronic signature (e-sign) document workflow"),
        ("NAV calculation engine", "Net Asset Value (NAV) calculation engine"),
        ("LP investment tracking", "Limited Partner (LP) investment tracking"),
        ("API integration points", "Application Programming Interface (API) integration points"),
        ("UI/UX design standards", "User Interface (UI)/User Experience (UX) design standards")
    ]
    
    all_passed = True
    
    for input_text, expected_output in test_cases:
        expanded = _expand_common_abbreviations(input_text)
        test_passed = expected_output == expanded
        
        print(f"Input:    {input_text}")
        print(f"Expected: {expected_output}")
        print(f"Actual:   {expanded}")
        print(f"Result:   {'✅ PASS' if test_passed else '❌ FAIL'}")
        print()
        
        if not test_passed:
            all_passed = False
    
    if all_passed:
        print("✅ ALL ABBREVIATION TESTS PASSED")
    else:
        print("❌ SOME ABBREVIATION TESTS FAILED")
    
    print("\n" + "=" * 60 + "\n")
    return all_passed


def test_fund_management_end_to_end():
    """Test complete fund management BRD to FRD generation workflow."""
    print("🔬 Test 4: End-to-End Fund Management Workflow")
    print("-" * 60)
    
    # Complete fund management input
    fund_mgmt_inputs = {
        "objectives": """
        • Digitize investor onboarding with KYC/AML compliance
        • Implement e-sign document workflows
        • Provide secure investor portal with NAV reporting
        • Enable digital capital call management
        """,
        "scope": """
        In Scope:
        • Investor registration and verification
        • Document management with e-sign
        • Basic NAV calculations and reporting
        • Capital call notifications
        
        Out of Scope:
        • Advanced portfolio analytics with AI/ML features
        • Automated trading capabilities
        • Third-party marketplace integrations
        """,
        "briefRequirements": """
        • Secure investor authentication
        • Document upload and e-sign capabilities
        • Investment tracking and reporting
        • Communication and notification system
        """,
        "budget": """
        Total project budget: $750,000
        • Development: $500,000
        • Testing and QA: $100,000
        • Infrastructure: $150,000
        """,
    }
    
    # Generate BRD
    brd_result = _generate_epics_fallback_brd("Digital Fund Management Platform", fund_mgmt_inputs, 1)
    
    # Generate FRD from BRD
    frd_result = _generate_user_stories_fallback_frd("Digital Fund Management Platform", brd_result, 1)
    
    print("✅ Generated complete BRD to FRD workflow")
    
    # Validate key requirements
    checks = {
        "BRD has EPICs from objectives": any(term in brd_result.lower() for term in ["kyc", "aml", "e-sign", "nav", "capital call"]),
        "BRD excludes budget from EPICs": "$500,000" not in brd_result and "infrastructure" not in brd_result.lower(),
        "FRD has user stories": "User Story:" in frd_result and "FR-" in frd_result,
        "FRD excludes excluded scope": not any(term in frd_result.lower() for term in ["ai/ml", "automated trading", "marketplace"]),
        "Abbreviations expanded": "Know Your Customer" in brd_result or "electronic signature" in frd_result,
    }
    
    all_checks_passed = True
    for check_name, result in checks.items():
        print(f"{'✅' if result else '❌'} {check_name}: {result}")
        if not result:
            all_checks_passed = False
    
    if all_checks_passed:
        print("\n✅ END-TO-END TEST PASSED: Fund management workflow correctly implemented")
    else:
        print("\n❌ END-TO-END TEST FAILED: Some checks did not pass")
    
    print("\n" + "=" * 60 + "\n")
    return all_checks_passed


if __name__ == "__main__":
    print("🚀 FUND MANAGEMENT BRD GENERATION FIXES TEST SUITE")
    print("=" * 70)
    print("Purpose: Validate EPICs sourcing, user story filtering, and abbreviation expansion")
    print()
    
    # Run all tests
    test1_passed = test_epic_filtering_from_budget_and_excluded_scope()
    test2_passed = test_user_story_filtering_from_frd()
    test3_passed = test_abbreviation_expansion()
    test4_passed = test_fund_management_end_to_end()
    
    # Summary
    total_tests = 4
    passed_tests = sum([test1_passed, test2_passed, test3_passed, test4_passed])
    
    print("=" * 70)
    print("📊 TEST SUMMARY")
    print(f"Tests Passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Fund management BRD generation fixes are working correctly.")
        print("✅ EPICs are correctly sourced from objectives and scope only")
        print("✅ User stories exclude budget and excluded scope items")  
        print("✅ Abbreviations are properly expanded for clarity")
        print("✅ End-to-end workflow maintains data integrity")
    else:
        print("⚠️  Some tests failed. Please review the fixes:")
        if not test1_passed:
            print("❌ EPIC filtering from budget and excluded scope needs improvement")
        if not test2_passed:
            print("❌ User story filtering in FRD generation needs improvement")
        if not test3_passed:
            print("❌ Abbreviation expansion logic needs improvement")
        if not test4_passed:
            print("❌ End-to-end workflow has issues")
    
    print("=" * 70)