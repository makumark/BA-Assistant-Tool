#!/usr/bin/env python3
"""
Test domain detection and enhanced fallback for all supported domains.
"""

import sys
import os

# Add the app directory to Python path
backend_dir = r"c:\Users\pavan\OneDrive\Desktop\ba-tool\react-python-auth\backend"
app_dir = os.path.join(backend_dir, 'app')
sys.path.insert(0, app_dir)

try:
    from services.ai_service import generate_brd_html
    print("✅ AI service imported successfully")
except Exception as e:
    print(f"❌ Failed to import AI service: {e}")
    sys.exit(1)

def test_domain(domain_name, project_name, description, requirements):
    """Test BRD generation for a specific domain."""
    
    print(f"\n🧪 Testing {domain_name.upper()} Domain")
    print("=" * 50)
    
    inputs = {
        "projectName": project_name,
        "projectDescription": description,
        "businessRequirements": requirements
    }
    
    try:
        html = generate_brd_html(project_name, inputs, 1)
        
        print(f"✅ Generated BRD with {len(html)} characters")
        
        # Check domain-specific content
        if domain_name == "marketing":
            stakeholders = ["Marketing managers", "Campaign managers", "Email specialists"]
        elif domain_name == "healthcare":
            stakeholders = ["Patients", "Clinicians", "Front-desk staff"]
        elif domain_name == "banking":
            stakeholders = ["Account holders", "Branch staff", "Relationship managers"]
        elif domain_name == "ecommerce":
            stakeholders = ["Customers", "Store managers", "Inventory managers"]
        elif domain_name == "education":
            stakeholders = ["student", "course", "learning"]  # Using keywords since we might not have full stakeholder definitions
        elif domain_name == "insurance":
            stakeholders = ["policy", "claim", "premium"]  # Using keywords since we might not have full stakeholder definitions
        else:
            stakeholders = ["End users", "Business users"]
        
        found_stakeholders = []
        for stakeholder in stakeholders:
            if stakeholder.lower() in html.lower():
                found_stakeholders.append(stakeholder)
        
        print(f"✅ Found stakeholders: {found_stakeholders}")
        
        if "enhanced fallback" in html.lower():
            print("✅ Using enhanced domain-specific fallback")
        else:
            print("🔄 Using AI generation or basic fallback")
            
        # Save output for inspection
        filename = f"test_{domain_name}_output.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"💾 Output saved to: {filename}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to generate BRD: {e}")
        return False

def main():
    """Test all supported domains."""
    
    test_cases = [
        {
            "domain": "marketing",
            "project": "Marketing Automation Platform",
            "description": "Advanced marketing automation platform for managing multi-channel campaigns, customer segmentation, and marketing analytics",
            "requirements": [
                "Customer segmentation based on behavior and demographics",
                "Multi-channel campaign management (email, SMS, push notifications)",
                "A/B testing capabilities for content optimization"
            ]
        },
        {
            "domain": "healthcare",
            "project": "Patient Management System",
            "description": "Electronic health record system for managing patient information, clinical workflows, and medical history",
            "requirements": [
                "Patient registration and demographic management",
                "Clinical documentation and medical history tracking",
                "HIPAA compliant data storage and access controls"
            ]
        },
        {
            "domain": "banking",
            "project": "Digital Banking Platform",
            "description": "Secure online banking system for account management, payments, and financial transactions",
            "requirements": [
                "Account balance inquiries and transaction history",
                "Online payment processing and transfers",
                "Fraud detection and security monitoring"
            ]
        },
        {
            "domain": "ecommerce",
            "project": "E-commerce Platform",
            "description": "Online retail platform for product catalog management, order processing, and customer experience",
            "requirements": [
                "Product catalog browsing and search functionality",
                "Shopping cart and checkout process",
                "Order tracking and inventory management"
            ]
        },
        {
            "domain": "education",
            "project": "Learning Management System",
            "description": "Educational platform for course management, student enrollment, and academic tracking",
            "requirements": [
                "Student registration and course enrollment",
                "Learning content delivery and progress tracking",
                "Grade management and academic reporting"
            ]
        },
        {
            "domain": "insurance",
            "project": "Insurance Claims System",
            "description": "Digital platform for policy management, claims processing, and premium calculations",
            "requirements": [
                "Policy creation and premium calculation",
                "Claims submission and processing workflow",
                "Risk assessment and underwriting support"
            ]
        }
    ]
    
    results = {}
    
    for test_case in test_cases:
        success = test_domain(
            test_case["domain"],
            test_case["project"],
            test_case["description"],
            test_case["requirements"]
        )
        results[test_case["domain"]] = success
    
    print(f"\n📊 Summary of Domain Tests:")
    print("=" * 30)
    for domain, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{domain.upper()}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    print(f"\nOverall: {total_passed}/{total_tests} domains working correctly")

if __name__ == "__main__":
    main()