#!/usr/bin/env python3
"""
🎯 Cross-Domain AI Enhancement Verification Test
Tests AI-enhanced validation and acceptance criteria across all 6 business domains

This test verifies that healthcare, airline, financial, ecommerce, and marketing domains 
now receive the same high-quality AI contextual intelligence as the telecom domain.

Test Coverage:
✅ Healthcare: Patient management, clinical care, prescriptions, insurance
✅ Airline: Flight booking, operations, baggage handling, loyalty programs  
✅ Financial: Portfolio management, trading, risk assessment, compliance
✅ E-commerce: Product catalog, shopping cart, order fulfillment, reviews
✅ Marketing: Campaign management, lead generation, analytics, automation
✅ Telecom: Subscriber management, billing, customer care, compliance (baseline)
"""

import requests
import json
import time
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:8001"
AI_ENDPOINT = f"{BASE_URL}/ai/frd"

def test_ai_enhancement_quality(domain, project_name, requirements):
    """Test AI enhancement quality for a specific domain"""
    print(f"\n🎯 Testing {domain.upper()} Domain AI Enhancement...")
    
    payload = {
        "project": project_name,
        "projectDescription": f"AI-enhanced {domain} system with comprehensive business requirements",
        "briefRequirements": requirements,
        "version": "1.0"
    }
    
    try:
        response = requests.post(AI_ENDPOINT, json=payload, timeout=30)
        if response.status_code == 200:
            content = response.text
            
            # AI Enhancement Quality Metrics
            metrics = {
                "domain": domain,
                "project": project_name,
                "total_length": len(content),
                "has_epics": "EPIC-" in content and "User Story" in content,
                "has_acceptance_criteria": "Acceptance Criteria" in content,
                "has_validation_criteria": "Validation Criteria" in content,
                "has_domain_personas": check_domain_personas(content, domain),
                "domain_specific_terms": count_domain_terms(content, domain),
                "ai_contextual_filtering": check_contextual_filtering(content, domain),
                "epic_intelligence": check_epic_intelligence(content, domain),
                "comprehensive_coverage": check_comprehensive_coverage(content)
            }
            
            # Calculate enhancement score
            enhancement_score = calculate_enhancement_score(metrics)
            metrics["enhancement_score"] = enhancement_score
            
            print(f"✅ {domain.upper()} Enhancement Score: {enhancement_score:.1f}%")
            print(f"📊 Domain-specific terms: {metrics['domain_specific_terms']}")
            print(f"🎭 Domain personas: {metrics['has_domain_personas']}")
            print(f"🤖 AI contextual filtering: {metrics['ai_contextual_filtering']}")
            print(f"🎯 EPIC intelligence: {metrics['epic_intelligence']}")
            
            # Save detailed output for analysis
            with open(f"test_{domain}_ai_enhancement_output.html", "w", encoding="utf-8") as f:
                f.write(content)
            
            return metrics
            
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        return None

def check_domain_personas(content, domain):
    """Check if domain-specific personas are being used"""
    domain_personas = {
        'healthcare': ['Patient', 'Physician', 'Clinical Nurse', 'Medical Administrator', 'Pharmacist', 'Insurance Coordinator'],
        'airline': ['Passenger', 'Check-in Agent', 'Operations Manager', 'Cabin Crew', 'Baggage Handler', 'Maintenance Engineer'],
        'financial': ['Investor', 'Portfolio Manager', 'Trading Specialist', 'Risk Analyst', 'Compliance Officer'],
        'ecommerce': ['Customer', 'Merchant', 'Store Manager', 'Product Manager', 'Fulfillment Specialist'],
        'marketing': ['Marketing Manager', 'Marketing Analyst', 'Content Manager', 'Email Marketing Specialist', 'Social Media Manager'],
        'telecom': ['Customer', 'Customer Service Representative', 'Technical Support Agent', 'Billing Specialist']
    }
    
    if domain in domain_personas:
        found_personas = [persona for persona in domain_personas[domain] if persona in content]
        return len(found_personas) > 0
    return False

def count_domain_terms(content, domain):
    """Count domain-specific terminology usage"""
    domain_terms = {
        'healthcare': ['HIPAA', 'HL7', 'ICD-10', 'patient', 'clinical', 'medical', 'prescription', 'diagnosis'],
        'airline': ['IATA', 'PNR', 'GDS', 'flight', 'boarding', 'baggage', 'check-in', 'schedule'],
        'financial': ['portfolio', 'trading', 'settlement', 'compliance', 'risk', 'investment', 'AML', 'margin'],
        'ecommerce': ['product', 'inventory', 'cart', 'checkout', 'shipping', 'order', 'catalog', 'review'],
        'marketing': ['campaign', 'segmentation', 'analytics', 'conversion', 'lead', 'automation', 'ROI', 'GDPR'],
        'telecom': ['TRAI', 'KYC', 'billing', 'subscriber', 'SIM', 'provisioning', 'mediation', 'ARPU']
    }
    
    if domain in domain_terms:
        term_count = sum(1 for term in domain_terms[domain] if term.lower() in content.lower())
        return term_count
    return 0

def check_contextual_filtering(content, domain):
    """Check if AI contextual filtering is working"""
    # Look for intelligent selection of relevant criteria
    contextual_indicators = [
        "contextual", "relevant", "specific", "appropriate", "intelligent",
        "based on", "filtered", "selected", "matched"
    ]
    return any(indicator in content.lower() for indicator in contextual_indicators)

def check_epic_intelligence(content, domain):
    """Check if EPICs show domain-specific intelligence"""
    domain_epic_patterns = {
        'healthcare': ['Patient Registration', 'Clinical Care', 'Prescription', 'Insurance'],
        'airline': ['Flight Booking', 'Check-in', 'Baggage', 'Operations'],
        'financial': ['Portfolio', 'Trading', 'Risk Management', 'Compliance'],
        'ecommerce': ['Product Catalog', 'Shopping Cart', 'Order Management', 'Customer Account'],
        'marketing': ['Campaign', 'Lead Generation', 'Analytics', 'Email Marketing'],
        'telecom': ['Customer Onboarding', 'Billing', 'Service Catalog', 'Customer Care']
    }
    
    if domain in domain_epic_patterns:
        found_patterns = [pattern for pattern in domain_epic_patterns[domain] 
                         if pattern.lower() in content.lower()]
        return len(found_patterns) > 0
    return False

def check_comprehensive_coverage(content):
    """Check for comprehensive coverage of enhancement features"""
    required_elements = [
        "User Story", "Acceptance Criteria", "Validation Criteria",
        "EPIC-", "As a", "I want", "So that", "Given", "When", "Then"
    ]
    coverage = sum(1 for element in required_elements if element in content)
    return coverage >= 8  # At least 8/10 elements should be present

def calculate_enhancement_score(metrics):
    """Calculate overall AI enhancement score"""
    score = 0
    
    # Base functionality (30 points)
    if metrics["has_epics"]: score += 10
    if metrics["has_acceptance_criteria"]: score += 10
    if metrics["has_validation_criteria"]: score += 10
    
    # Domain intelligence (40 points)
    if metrics["has_domain_personas"]: score += 15
    if metrics["domain_specific_terms"] >= 3: score += 15
    if metrics["epic_intelligence"]: score += 10
    
    # AI enhancement quality (30 points)
    if metrics["ai_contextual_filtering"]: score += 15
    if metrics["comprehensive_coverage"]: score += 15
    
    return score

def main():
    """Main test execution"""
    print("🚀 Cross-Domain AI Enhancement Verification Test")
    print("=" * 60)
    print("Testing AI-enhanced validation and acceptance criteria across all domains")
    
    # Test cases for all 6 domains
    test_cases = [
        {
            "domain": "healthcare",
            "project": "AI Enhanced Healthcare Management System",
            "requirements": """Patient registration and medical record management system
Electronic health record integration with HL7 standards
Appointment scheduling and clinical workflow optimization
Prescription management with drug interaction checking
Insurance claim processing and HIPAA compliance validation
Emergency alert system for critical patient conditions"""
        },
        {
            "domain": "airline", 
            "project": "AI Enhanced Airline Operations Platform",
            "requirements": """Flight booking system with real-time seat availability
Passenger check-in and boarding pass generation
Baggage handling and tracking throughout journey
Schedule management and disruption handling procedures
Loyalty program integration with miles tracking
Crew scheduling and aircraft maintenance coordination"""
        },
        {
            "domain": "financial",
            "project": "AI Enhanced Investment Management Platform", 
            "requirements": """Portfolio management with real-time market data integration
Trading execution system with settlement processing
Risk assessment and monitoring across all investments
Regulatory compliance reporting and audit trails
Client onboarding with KYC verification procedures
Performance analytics and investment recommendations"""
        },
        {
            "domain": "ecommerce",
            "project": "AI Enhanced E-commerce Platform",
            "requirements": """Product catalog management with search and filtering
Shopping cart functionality with persistence across sessions
Order fulfillment and shipping integration
Customer account management with order history
Review and rating system for products
Inventory management with automated reordering"""
        },
        {
            "domain": "marketing",
            "project": "AI Enhanced Marketing Automation Platform",
            "requirements": """Campaign management with multi-channel automation
Lead generation and scoring based on behavior
Customer segmentation with personalization rules
Email marketing with deliverability optimization
Analytics dashboard with conversion tracking
Social media integration and engagement monitoring"""
        },
        {
            "domain": "telecom",
            "project": "AI Enhanced Telecom Operations System",
            "requirements": """Subscriber onboarding with KYC verification
Billing and charging system with revenue assurance
Service catalog management and plan recommendations
Customer care platform with diagnostic capabilities
Regulatory compliance and audit reporting
Partner channel management with commission tracking"""
        }
    ]
    
    # Execute tests
    all_results = []
    start_time = time.time()
    
    for test_case in test_cases:
        result = test_ai_enhancement_quality(
            test_case["domain"],
            test_case["project"], 
            test_case["requirements"]
        )
        if result:
            all_results.append(result)
        
        time.sleep(2)  # Prevent overwhelming the server
    
    # Generate comprehensive report
    print("\n" + "=" * 60)
    print("📊 CROSS-DOMAIN AI ENHANCEMENT REPORT")
    print("=" * 60)
    
    if all_results:
        # Summary statistics
        avg_score = sum(r["enhancement_score"] for r in all_results) / len(all_results)
        max_score = max(r["enhancement_score"] for r in all_results)
        min_score = min(r["enhancement_score"] for r in all_results)
        
        print(f"🎯 Average Enhancement Score: {avg_score:.1f}%")
        print(f"📈 Best Performance: {max_score:.1f}%")
        print(f"📉 Minimum Performance: {min_score:.1f}%")
        
        # Individual domain results
        print("\n🏆 DOMAIN-BY-DOMAIN RESULTS:")
        for result in sorted(all_results, key=lambda x: x["enhancement_score"], reverse=True):
            print(f"  {result['domain'].upper():12} | {result['enhancement_score']:5.1f}% | {result['domain_specific_terms']:2d} terms | {'✅' if result['has_domain_personas'] else '❌'} personas")
        
        # Quality assessment
        print(f"\n🤖 AI ENHANCEMENT ASSESSMENT:")
        high_quality = [r for r in all_results if r["enhancement_score"] >= 80]
        print(f"  High Quality (≥80%): {len(high_quality)}/{len(all_results)} domains")
        
        if len(high_quality) == len(all_results):
            print("  🎉 EXCELLENT: All domains achieve high-quality AI enhancement!")
        elif len(high_quality) >= len(all_results) * 0.8:
            print("  ✅ GOOD: Most domains achieve high-quality AI enhancement")
        else:
            print("  ⚠️  NEEDS IMPROVEMENT: Some domains need enhancement tuning")
    
    elapsed_time = time.time() - start_time
    print(f"\n⏱️  Test completed in {elapsed_time:.1f} seconds")
    
    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"cross_domain_ai_enhancement_results_{timestamp}.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"💾 Detailed results saved to cross_domain_ai_enhancement_results_{timestamp}.json")

if __name__ == "__main__":
    main()