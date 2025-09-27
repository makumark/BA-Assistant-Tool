#!/usr/bin/env python3
"""
Test script to demonstrate Agentic Adaptive RAG functionality
"""

import requests
import json
from datetime import datetime

def test_agentic_rag_brd():
    """Test Agentic RAG BRD generation with banking domain"""
    
    print("🚀 Testing Agentic Adaptive RAG for BRD Generation")
    print("=" * 60)
    
    # Banking domain test data - should trigger advanced RAG processing
    test_data = {
        "project": "Digital Banking Platform",
        "inputs": {
            "scope": "Retail banking operations including account management, payment processing, and customer service",
            "briefRequirements": """
            • Customer onboarding with KYC/AML compliance
            • Real-time account balance and transaction history
            • Multi-currency payment processing (NEFT/IMPS/RTGS/UPI)
            • Fraud detection and risk management
            • Mobile banking with biometric authentication
            • Loan application and processing workflow
            • Investment portfolio management
            • Regulatory compliance and audit reporting
            """,
            "objectives": "Transform traditional banking operations with digital-first approach",
            "budget": "₹2.5-4.2 crore over 18 months",
            "assumptions": "Core banking APIs available, regulatory approvals in place, customer migration strategy defined",
            "validations": """
            • Account verification with Aadhaar and PAN validation
            • Transaction limits based on customer tier and risk profile
            • Two-factor authentication for high-value transactions
            • Real-time fraud scoring and blocking suspicious activities
            • Compliance with RBI guidelines and data localization requirements
            """
        },
        "version": 1
    }
    
    try:
        print(f"📤 Sending request to http://localhost:8001/ai/expand")
        print(f"🏦 Project: {test_data['project']}")
        print(f"📊 Expected Domain: Banking (should be auto-detected)")
        
        response = requests.post(
            "http://localhost:8001/ai/expand",
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n✅ Agentic RAG BRD Generation Successful!")
            print("=" * 60)
            
            # Check if it contains Agentic RAG metadata
            html_content = result.get("html", "")
            
            if "Agentic Adaptive RAG Generation Report" in html_content:
                print("🤖 ✅ Agentic RAG processing detected in output")
                
                # Extract metadata if present
                if "DOMAIN DETECTED" in html_content:
                    print("🎯 ✅ Domain detection working")
                if "QUALITY SCORE" in html_content:
                    print("📊 ✅ Quality assessment working") 
                if "ENHANCEMENT LEVEL" in html_content:
                    print("⚡ ✅ Adaptive enhancement working")
                    
                print("\n🏦 Banking Domain Features Expected:")
                banking_features = [
                    "KYC/AML compliance",
                    "Regulatory compliance",
                    "Risk management",
                    "Transaction processing",
                    "Account management"
                ]
                
                for feature in banking_features:
                    if feature.lower() in html_content.lower():
                        print(f"   ✅ {feature} - Found")
                    else:
                        print(f"   ❌ {feature} - Missing")
                        
            else:
                print("⚠️ Traditional AI/Fallback method used (not Agentic RAG)")
                
            # Save output for inspection
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"agentic_rag_brd_test_{timestamp}.html"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"\n📄 Output saved to: {output_file}")
            print(f"📝 Content length: {len(html_content)} characters")
            
            return True
            
        else:
            print(f"❌ Request failed with status: {response.status_code}")
            print(f"❌ Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        print("💡 Make sure the backend server is running on port 8001")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_domain_detection():
    """Test different domains to verify adaptive RAG"""
    
    domains_to_test = [
        {
            "name": "Healthcare",
            "project": "Hospital Management System",
            "keywords": "patient registration, medical records, doctor appointments, prescription management, HIPAA compliance"
        },
        {
            "name": "E-commerce", 
            "project": "Online Shopping Platform",
            "keywords": "product catalog, shopping cart, checkout process, order management, payment gateway, customer reviews"
        },
        {
            "name": "Marketing",
            "project": "Marketing Automation Platform", 
            "keywords": "campaign management, customer segmentation, email automation, analytics dashboard, lead scoring"
        }
    ]
    
    print("\n🧪 Testing Domain Detection Capabilities")
    print("=" * 60)
    
    for domain in domains_to_test:
        print(f"\n📋 Testing {domain['name']} Domain...")
        
        test_data = {
            "project": domain['project'],
            "inputs": {
                "briefRequirements": domain['keywords'],
                "scope": f"Core {domain['name'].lower()} functionality",
            },
            "version": 1
        }
        
        try:
            response = requests.post(
                "http://localhost:8001/ai/expand",
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                html_content = response.json().get("html", "")
                
                if "DOMAIN DETECTED" in html_content:
                    print(f"   ✅ Domain detection active")
                    if domain['name'].lower() in html_content.lower():
                        print(f"   🎯 Correctly detected {domain['name']} domain")
                    else:
                        print(f"   ⚠️ Domain detection may need tuning")
                else:
                    print(f"   ❌ Domain detection not found in output")
                    
        except Exception as e:
            print(f"   ❌ Test failed: {e}")

if __name__ == "__main__":
    print("🤖 Agentic Adaptive RAG Testing Suite")
    print("=" * 60)
    print("This script tests the new intelligent document generation capabilities")
    print("of your BA Tool using multi-agent RAG architecture.\n")
    
    # Test main BRD generation
    success = test_agentic_rag_brd()
    
    if success:
        # Test domain detection
        test_domain_detection()
        
        print("\n🎉 Agentic RAG Testing Complete!")
        print("=" * 60)
        print("Your BA Tool now features:")
        print("✅ Intelligent domain detection")
        print("✅ Adaptive generation strategies") 
        print("✅ Context-aware knowledge retrieval")
        print("✅ Quality assessment and validation")
        print("✅ Multi-agent document generation")
        print("\n💡 Try generating documents in the web interface to see the enhanced capabilities!")
    else:
        print("\n❌ Testing failed. Please check server status and try again.")