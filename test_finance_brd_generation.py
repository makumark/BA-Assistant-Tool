#!/usr/bin/env python3
"""
Real-world test of mutual fund BRD generation using the AI service
"""

import sys
import os
import json

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'react-python-auth', 'backend')
sys.path.insert(0, backend_path)

from app.services.ai_service import generate_brd_html

def test_mutual_fund_brd():
    print("=== Testing Mutual Fund BRD Generation ===\n")
    
    # Mutual fund project inputs
    mutual_fund_inputs = {
        "project_name": "SmartFund Investment Platform",
        "description": "A comprehensive mutual fund investment platform that enables retail and institutional investors to discover, invest in, and manage their mutual fund portfolios with advanced analytics and automated SIP features.",
        "objectives": [
            "Enable seamless mutual fund discovery and investment",
            "Provide real-time NAV tracking and portfolio analytics", 
            "Automate SIP investments and dividend management",
            "Ensure regulatory compliance with SEBI guidelines"
        ],
        "features": [
            "Mutual fund search and filtering",
            "SIP (Systematic Investment Plan) automation",
            "Portfolio tracking with performance analytics",
            "NAV calculation and real-time updates",
            "KYC verification and compliance",
            "Dividend management and reinvestment",
            "Risk profiling and investment recommendations",
            "Tax reporting and capital gains calculation"
        ],
        "stakeholders": "Investors, Fund managers, Distributors, AMC teams",
        "scope": "Web and mobile platform for mutual fund investments"
    }
    
    print("Input Project Details:")
    print(f"Project: {mutual_fund_inputs['project_name']}")
    print(f"Description: {mutual_fund_inputs['description']}")
    print(f"Key Features: {', '.join(mutual_fund_inputs['features'][:3])}...")
    print()
    
    try:
        # Generate BRD using the enhanced AI service
        print("Generating BRD using AI service...")
        brd_html = generate_brd_html(
            project="SmartFund Investment Platform",
            inputs=mutual_fund_inputs,
            version=1
        )
        
        # Check if BRD was generated successfully
        if brd_html and len(brd_html) > 1000:
            print("✅ BRD Generated Successfully!")
            print(f"Generated BRD length: {len(brd_html)} characters")
            
            # Check for mutual fund specific content
            mf_keywords = ["mutual fund", "NAV", "SIP", "portfolio", "investment", "AMC", "distributor"]
            found_keywords = [kw for kw in mf_keywords if kw.lower() in brd_html.lower()]
            print(f"Mutual fund keywords found: {found_keywords}")
            
            # Check for proper stakeholders
            stakeholder_keywords = ["investor", "fund manager", "distributor", "compliance"]
            found_stakeholders = [sk for sk in stakeholder_keywords if sk.lower() in brd_html.lower()]
            print(f"Expected stakeholders found: {found_stakeholders}")
            
            # Save the BRD to file for inspection
            output_file = "test_mutual_fund_brd_output.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(brd_html)
            print(f"BRD saved to: {output_file}")
            
            # Check for EPIC structure
            epic_count = brd_html.lower().count("epic-")
            print(f"EPICs generated: {epic_count}")
            
            return True
            
        else:
            print("❌ BRD generation failed or returned minimal content")
            print(f"Returned content length: {len(brd_html) if brd_html else 0}")
            return False
            
    except Exception as e:
        print(f"❌ Error during BRD generation: {str(e)}")
        return False

def test_aif_brd():
    print("\n=== Testing AIF BRD Generation ===\n")
    
    # AIF project inputs
    aif_inputs = {
        "project_name": "AlphaFund AIF Management System",
        "description": "Alternative Investment Fund management platform for hedge funds, private equity, and venture capital with sophisticated investor management and regulatory compliance.",
        "objectives": [
            "Manage alternative investment fund operations",
            "Provide sophisticated investor onboarding and KYC",
            "Ensure SEBI AIF regulatory compliance",
            "Deliver superior risk-adjusted returns tracking"
        ],
        "features": [
            "Fund administration and operations",
            "Qualified investor onboarding",
            "Performance attribution and analytics",
            "Regulatory reporting to SEBI",
            "Risk management and monitoring",
            "Investor portal and communications",
            "Portfolio valuation and NAV calculation",
            "Capital calls and distribution management"
        ],
        "stakeholders": "Qualified investors, Fund managers, Compliance officers",
        "scope": "Enterprise platform for AIF management and operations"
    }
    
    print("Input Project Details:")
    print(f"Project: {aif_inputs['project_name']}")
    print(f"Key Features: {', '.join(aif_inputs['features'][:3])}...")
    print()
    
    try:
        print("Generating AIF BRD using AI service...")
        brd_html = generate_brd_html(
            project="AlphaFund AIF Management System",
            inputs=aif_inputs,
            version=1
        )
        
        if brd_html and len(brd_html) > 1000:
            print("✅ AIF BRD Generated Successfully!")
            
            # Check for AIF specific content
            aif_keywords = ["alternative investment", "hedge fund", "private equity", "qualified investor", "SEBI"]
            found_keywords = [kw for kw in aif_keywords if kw.lower() in brd_html.lower()]
            print(f"AIF keywords found: {found_keywords}")
            
            # Save the BRD
            output_file = "test_aif_brd_output.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(brd_html)
            print(f"AIF BRD saved to: {output_file}")
            
            return True
        else:
            print("❌ AIF BRD generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during AIF BRD generation: {str(e)}")
        return False

if __name__ == "__main__":
    # Test mutual fund BRD generation
    mf_success = test_mutual_fund_brd()
    
    # Test AIF BRD generation  
    aif_success = test_aif_brd()
    
    print(f"\n=== FINAL RESULTS ===")
    print(f"Mutual Fund BRD: {'✅ SUCCESS' if mf_success else '❌ FAILED'}")
    print(f"AIF BRD: {'✅ SUCCESS' if aif_success else '❌ FAILED'}")
    
    if mf_success and aif_success:
        print("🎉 All finance domain BRD generation working perfectly!")
    else:
        print("⚠️  Some issues found with finance domain BRD generation")