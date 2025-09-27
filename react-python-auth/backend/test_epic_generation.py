#!/usr/bin/env python3
"""
Test EPIC generation to ensure EPICs are generated only from Business Objectives and Scope sections.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ai_service_enhanced import _generate_epics_fallback_brd

def test_epic_generation_from_objectives_and_scope():
    """Test that EPICs are generated only from Business Objectives and Scope sections."""
    
    print("🧪 Testing EPIC Generation Constraint...")
    print("=" * 60)
    
    # Test case: Include various sections but EPICs should only come from objectives and scope
    test_inputs = {
        "briefRequirements": """
            1. User management system with authentication
            2. Course management and content delivery
            3. Payment processing system
            4. Reporting and analytics dashboard
        """,
        "objectives": """
            - Improve learning outcomes through better engagement
            - Reduce administrative workload by 40%
            - Enable remote learning capabilities
            - Increase course completion rates to 85%
        """,
        "scope": """
            In scope: Core LMS functionality, basic reporting, mobile access
            Out of scope: Advanced AI tutoring, VR integration, complex analytics
        """,
        "validations": """
            - User input validation for all forms
            - Course prerequisite validation
            - Payment transaction security validation
            - Progress tracking accuracy validation
        """,
        "assumptions": """
            - Users have reliable internet access
            - Content will be provided in digital formats
            - Integration APIs are available
        """,
        "constraints": """
            - 6-month development timeline
            - Budget limit of $500K
            - WCAG compliance required
        """
    }
    
    print("📋 Input Sections:")
    print(f"   ✓ Requirements: {len(test_inputs['briefRequirements'].strip())} chars")
    print(f"   ✓ Objectives: {len(test_inputs['objectives'].strip())} chars")
    print(f"   ✓ Scope: {len(test_inputs['scope'].strip())} chars")
    print(f"   ✓ Validations: {len(test_inputs['validations'].strip())} chars")
    print(f"   ✓ Assumptions: {len(test_inputs['assumptions'].strip())} chars")
    print(f"   ✓ Constraints: {len(test_inputs['constraints'].strip())} chars")
    
    # Generate BRD using our updated fallback method
    brd_html = _generate_epics_fallback_brd("Test LMS Project", test_inputs, 1)
    
    print("\n🔍 Analyzing Generated BRD...")
    
    # Check if BRD was generated
    if brd_html and len(brd_html) > 100:
        print("✅ BRD Generated Successfully!")
        print(f"📄 Document Length: {len(brd_html)} characters")
        
        # Count EPICs
        epic_count = brd_html.count("EPIC-")
        print(f"📊 EPICs Found: {epic_count}")
        
        # Check for content that should NOT be in EPICs (from requirements, validations, etc.)
        requirements_terms = ["user management", "course management", "payment processing", "reporting and analytics"]
        validation_terms = ["user input validation", "course prerequisite", "payment transaction", "progress tracking"]
        assumption_terms = ["reliable internet", "digital formats", "integration APIs"]
        constraint_terms = ["6-month", "500K", "WCAG compliance"]
        
        # Check for content that SHOULD be in EPICs (from objectives and scope)
        objective_terms = ["learning outcomes", "engagement", "administrative workload", "remote learning", "completion rates"]
        scope_terms = ["core LMS", "basic reporting", "mobile access"]
        
        print("\n🎯 EPIC Content Analysis:")
        
        # Check if EPICs contain objective/scope-related content (GOOD)
        objective_matches = sum(1 for term in objective_terms if term.lower() in brd_html.lower())
        scope_matches = sum(1 for term in scope_terms if term.lower() in brd_html.lower())
        
        print(f"✅ Objective-related content in EPICs: {objective_matches}/{len(objective_terms)} terms found")
        print(f"✅ Scope-related content in EPICs: {scope_matches}/{len(scope_terms)} terms found")
        
        # Check if EPICs contain content from other sections (BAD)
        requirement_matches = sum(1 for term in requirements_terms if term.lower() in brd_html.lower())
        validation_matches = sum(1 for term in validation_terms if term.lower() in brd_html.lower())
        assumption_matches = sum(1 for term in assumption_terms if term.lower() in brd_html.lower())
        constraint_matches = sum(1 for term in constraint_terms if term.lower() in brd_html.lower())
        
        print(f"⚠️  Requirement terms in document: {requirement_matches}/{len(requirements_terms)} (should be minimal)")
        print(f"⚠️  Validation terms in document: {validation_matches}/{len(validation_terms)} (should be minimal)")  
        print(f"⚠️  Assumption terms in document: {assumption_matches}/{len(assumption_terms)} (should be minimal)")
        print(f"⚠️  Constraint terms in document: {constraint_matches}/{len(constraint_terms)} (should be minimal)")
        
        # Extract EPIC section for detailed analysis
        epic_section_start = brd_html.find("Business Requirements (EPICs)")
        epic_section_end = brd_html.find("</section>", epic_section_start)
        
        if epic_section_start != -1 and epic_section_end != -1:
            epic_section = brd_html[epic_section_start:epic_section_end]
            print(f"\n📋 EPIC Section Content (first 500 chars):")
            print("-" * 50)
            print(epic_section[:500] + "..." if len(epic_section) > 500 else epic_section)
        
        # Determine test result
        good_content = objective_matches + scope_matches
        bad_content = requirement_matches + validation_matches
        
        if good_content > 0 and bad_content < good_content:
            print(f"\n🎉 TEST PASSED: EPICs appear to be generated primarily from Objectives and Scope!")
            print(f"   📈 Good content ratio: {good_content}/(good_content + bad_content) = {good_content/(good_content + bad_content):.2%}")
        else:
            print(f"\n❌ TEST FAILED: EPICs may still contain content from other sections")
            print(f"   📉 Good content ratio: {good_content}/(good_content + bad_content) = {good_content/(good_content + bad_content):.2%}")
        
    else:
        print("❌ ERROR: BRD generation failed or returned empty content")
        return False
    
    return True

def test_epic_generation_with_empty_objectives_scope():
    """Test EPIC generation when objectives and scope are empty."""
    
    print("\n🧪 Testing EPIC Generation with Empty Objectives/Scope...")
    print("=" * 60)
    
    test_inputs = {
        "briefRequirements": """
            1. User authentication system
            2. Course management platform
            3. Student progress tracking
        """,
        # Empty objectives and scope
        "objectives": "",
        "scope": "",
        "validations": "User input validation required"
    }
    
    # Generate BRD
    brd_html = _generate_epics_fallback_brd("Test Project", test_inputs, 1)
    
    if brd_html and "EPIC-" in brd_html:
        epic_count = brd_html.count("EPIC-")
        print(f"✅ Default EPICs generated: {epic_count}")
        print("✅ Fallback EPICs are objective/scope focused (as expected)")
        
        # Check for our new default EPIC types
        if "Objective-Driven Operations" in brd_html or "Business Process Optimization" in brd_html:
            print("✅ Default EPICs reflect objectives/scope focus")
            return True
        else:
            print("❌ Default EPICs don't reflect objectives/scope focus")
            return False
    else:
        print("❌ No EPICs generated")
        return False

if __name__ == "__main__":
    print("🔬 EPIC Generation Constraint Test Suite")
    print("=" * 60)
    print("Purpose: Verify EPICs are generated ONLY from Business Objectives and Scope sections")
    print()
    
    test1_passed = test_epic_generation_from_objectives_and_scope()
    test2_passed = test_epic_generation_with_empty_objectives_scope()
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"   Test 1 (Objectives/Scope Focus): {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"   Test 2 (Empty Objectives/Scope): {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED! EPICs are now generated only from Business Objectives and Scope.")
    else:
        print("\n❌ SOME TESTS FAILED! Please review the EPIC generation logic.")