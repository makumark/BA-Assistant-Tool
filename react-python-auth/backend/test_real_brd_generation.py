#!/usr/bin/env python3
"""
End-to-end test with the exact fund management input that was failing.
This tests the actual BRD generation function that would be called from the API.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.ai_service_enhanced import generate_brd_html

def test_real_brd_generation():
    """Test real BRD generation with fund management input."""
    
    # Exact problematic input from user
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
        "validations": """
        • System must handle 100+ concurrent users
        • Data must be encrypted at rest and in transit
        • Audit trail required for all transactions
        • Backup and disaster recovery procedures
        """,
        "budget": "Estimated ₹60–₹110 Lakh for full implementation",
        "assumptions": "Sandbox and Production environments will be provided"
    }
    
    print("🧪 Testing Real BRD Generation")
    print("=" * 50)
    
    # Generate BRD using the enhanced service
    brd_html = generate_brd_html("Fund Management Platform", fund_management_input, 1)
    
    print(f"✅ BRD Generated successfully ({len(brd_html)} characters)")
    
    # Check for problematic content that should NOT appear in EPICs
    problematic_patterns = [
        "EPIC-11",  # This was the problematic "Excluded — Full" EPIC
        "EPIC-13",  # This was the budget details EPIC  
        "EPIC-19",  # This was the environment EPIC
        "Excluded — Full",
        "₹60–₹110 Lakh", 
        "Estimated ₹60",
        "Sandbox And Production",
        "sandbox and production"
    ]
    
    brd_lower = brd_html.lower()
    issues_found = []
    
    for pattern in problematic_patterns:
        if pattern.lower() in brd_lower:
            issues_found.append(pattern)
    
    print()
    if issues_found:
        print("❌ Found problematic content in BRD:")
        for issue in issues_found:
            print(f"   - {issue}")
        
        # Show some context around problematic content
        print("\n📝 BRD Content Preview (first 1000 chars):")
        print(brd_html[:1000])
        return False
    else:
        print("✅ No problematic EPIC content found!")
        
        # Show EPICs section to verify they look correct
        epic_start = brd_html.lower().find("epic")
        if epic_start != -1:
            epic_section = brd_html[epic_start:epic_start+800]
            print("\n📋 EPICs Section Preview:")
            print(epic_section)
        
        return True

if __name__ == "__main__":
    success = test_real_brd_generation()
    
    if success:
        print("\n🎉 SUCCESS: Fund management BRD generation is now working correctly!")
        print("   - EPICs only from objectives and included scope")
        print("   - No budget details in EPICs")
        print("   - No excluded items in EPICs") 
        print("   - No environment details in EPICs")
        sys.exit(0)
    else:
        print("\n💥 FAILURE: BRD still contains problematic EPIC content")
        sys.exit(1)