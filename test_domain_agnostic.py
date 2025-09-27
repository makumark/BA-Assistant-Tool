#!/usr/bin/env python3
"""
Test script to verify domain-agnostic EPIC generation logic
"""

import requests
import json

def test_domain_agnostic_epic_generation():
    """Test that EPIC generation works universally across different domains"""
    
    # Test cases for different domains - same structure should produce consistent EPICs
    test_cases = [
        {
            "name": "E-commerce System",
            "data": {
                "project": "E-commerce Platform",
                "scope": """
                Included:
                • Product catalog management with search and filtering
                • Shopping cart and checkout process
                • User registration and authentication
                • Order tracking and management
                • Payment gateway integration
                
                Excluded:
                • Inventory management system
                • Third-party marketplace integration
                """,
                "objectives": """
                • Improve customer shopping experience
                • Increase online sales conversion rates
                • Reduce cart abandonment rates
                • Streamline order fulfillment process
                """,
                "budget": "₹50 lakhs covering development and licenses",
                "assumptions": "Payment gateway endpoints are stable"
            }
        },
        {
            "name": "Healthcare Management System", 
            "data": {
                "project": "Patient Management System",
                "scope": """
                Included:
                • Patient registration and profile management
                • Appointment scheduling system
                • Medical records storage and retrieval
                • Doctor-patient communication portal
                • Prescription management
                
                Excluded:
                • Billing and insurance processing
                • Medical device integration
                """,
                "objectives": """
                • Improve patient care coordination
                • Reduce appointment waiting times
                • Enhance medical record accessibility
                • Streamline healthcare workflows
                """,
                "budget": "₹75 lakhs covering HIPAA compliance and training",
                "assumptions": "Medical staff will receive adequate training"
            }
        },
        {
            "name": "CRM System",
            "data": {
                "project": "Customer Relationship Management",
                "scope": """
                Included:
                • Lead capture and qualification
                • Contact and account management
                • Sales pipeline tracking
                • Customer communication history
                • Reporting and analytics
                
                Excluded:
                • Marketing automation
                • Social media integration
                """,
                "objectives": """
                • Increase sales team productivity
                • Improve lead conversion rates
                • Enhance customer relationship tracking
                • Optimize sales forecasting accuracy
                """,
                "budget": "₹40 lakhs covering licenses and customization",
                "assumptions": "Sales team will adopt new processes"
            }
        }
    ]
    
    print("🧪 Testing Domain-Agnostic EPIC Generation Logic")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing {test_case['name']}")
        print("-" * 40)
        
        try:
            # Make API call to generate BRD
            response = requests.post(
                "http://localhost:8001/ai/expand",
                json=test_case["data"],
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                html_content = result.get("html", "")
                
                # Extract EPICs from the HTML
                epics = extract_epics_from_html(html_content)
                
                print(f"✅ Generated {len(epics)} EPICs:")
                for j, epic in enumerate(epics, 1):
                    title = epic.get("title", "Unknown")
                    description = epic.get("description", "No description")
                    print(f"  EPIC-{j:02d}: {title}")
                    print(f"    → {description[:80]}...")
                
                # Check for budget-related content in EPICs (should be NONE)
                budget_found = check_for_budget_content(epics)
                if budget_found:
                    print(f"❌ ERROR: Found budget-related content in EPICs!")
                    for item in budget_found:
                        print(f"    ⚠️  {item}")
                else:
                    print("✅ No budget/cost content found in EPICs (CORRECT)")
                
                # Check for excluded scope content (should be NONE)
                excluded_found = check_for_excluded_content(epics)
                if excluded_found:
                    print(f"❌ ERROR: Found excluded scope content in EPICs!")
                    for item in excluded_found:
                        print(f"    ⚠️  {item}")
                else:
                    print("✅ No excluded scope content found in EPICs (CORRECT)")
                    
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception occurred: {e}")
    
    print("\n" + "=" * 60)
    print("🏁 Domain-Agnostic Testing Complete")

def extract_epics_from_html(html_content):
    """Extract EPIC information from HTML content"""
    epics = []
    import re
    
    # Find all EPIC blocks
    epic_pattern = r'<span[^>]*>EPIC-\d+</span>\s*([^<]+)</h4>\s*<p[^>]*><strong>Description:</strong>\s*([^<]+)</p>'
    matches = re.findall(epic_pattern, html_content, re.DOTALL)
    
    for match in matches:
        epics.append({
            "title": match[0].strip(),
            "description": match[1].strip()
        })
    
    return epics

def check_for_budget_content(epics):
    """Check if any EPICs contain budget/cost related content"""
    budget_keywords = ['budget', 'cost', '₹', 'lakh', 'covering', 'licenses', 'estimated', 'phased pilot', 'scale', 'first year', 'support']
    found_issues = []
    
    for epic in epics:
        title = epic.get("title", "").lower()
        description = epic.get("description", "").lower()
        
        for keyword in budget_keywords:
            if keyword in title or keyword in description:
                found_issues.append(f"Found '{keyword}' in EPIC: {epic.get('title', 'Unknown')}")
    
    return found_issues

def check_for_excluded_content(epics):
    """Check if any EPICs contain excluded scope content"""
    excluded_keywords = ['excluded', 'replacement', 'marketplace', 'billing', 'insurance', 'marketing automation', 'social media']
    found_issues = []
    
    for epic in epics:
        title = epic.get("title", "").lower()
        description = epic.get("description", "").lower()
        
        for keyword in excluded_keywords:
            if keyword in title or keyword in description:
                found_issues.append(f"Found '{keyword}' in EPIC: {epic.get('title', 'Unknown')}")
    
    return found_issues

if __name__ == "__main__":
    test_domain_agnostic_epic_generation()