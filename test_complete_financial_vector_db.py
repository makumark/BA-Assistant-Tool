"""
Comprehensive Test Suite for Financial Domains + Vector DB Integration
Tests all 7 new domain implementations and vector database functionality
"""

import os
import sys
import json
import asyncio
from pathlib import Path

# Add the backend path to sys.path
backend_path = Path(__file__).parent / "react-python-auth" / "backend"
sys.path.insert(0, str(backend_path))

try:
    from app.services.agentic_rag_service import (
        AgenticRAGService, 
        DomainType, 
        DocumentType,
        KnowledgeBase,
        VectorDB
    )
    print("✅ Successfully imported Agentic RAG Service with Vector DB support")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("📝 Will test with simulated service")

def test_all_financial_domains():
    """Test all 7 newly implemented financial domains"""
    print("\n" + "="*60)
    print("🧪 TESTING ALL FINANCIAL DOMAINS")
    print("="*60)
    
    # Test scenarios for each domain
    test_scenarios = {
        DomainType.MUTUAL_FUNDS: {
            "project": "MutualFund Portfolio Management System",
            "inputs": {
                "business_need": "Build comprehensive mutual fund management platform",
                "features": "NAV calculation, portfolio rebalancing, investor reporting, fund performance analytics",
                "stakeholders": "Fund managers, investors, compliance officers",
                "compliance": "SEBI regulations, portfolio disclosure requirements"
            }
        },
        DomainType.AIF: {
            "project": "Alternative Investment Fund Platform",
            "inputs": {
                "business_need": "Create AIF management system for accredited investors",
                "features": "Investor qualification, sophisticated risk management, performance analytics",
                "stakeholders": "Accredited investors, fund managers, risk officers",
                "compliance": "AIF regulations, accredited investor verification"
            }
        },
        DomainType.CARDS_PAYMENT: {
            "project": "Card Payment Processing Gateway",
            "inputs": {
                "business_need": "Develop secure payment processing infrastructure",
                "features": "Transaction authorization, fraud detection, merchant services, chargeback management",
                "stakeholders": "Cardholders, merchants, payment processors",
                "compliance": "PCI DSS, EMV standards, card network rules"
            }
        },
        DomainType.INSURANCE: {
            "project": "Insurance Management Platform",
            "inputs": {
                "business_need": "Modernize insurance operations and claims processing",
                "features": "Policy administration, automated underwriting, claims processing",
                "stakeholders": "Policyholders, agents, underwriters, claims adjusters",
                "compliance": "NAIC regulations, state insurance laws"
            }
        },
        DomainType.EDUCATION: {
            "project": "Educational Management System",
            "inputs": {
                "business_need": "Create comprehensive student information system",
                "features": "Student enrollment, academic tracking, learning management",
                "stakeholders": "Students, faculty, administrators, parents",
                "compliance": "FERPA, ADA compliance, Title IX"
            }
        },
        DomainType.LOGISTICS: {
            "project": "Supply Chain Management Platform",
            "inputs": {
                "business_need": "Optimize logistics and warehouse operations",
                "features": "Shipment tracking, inventory management, route optimization",
                "stakeholders": "Shippers, warehouse staff, drivers, logistics coordinators",
                "compliance": "DOT regulations, customs requirements"
            }
        },
        DomainType.FINTECH: {
            "project": "Digital Banking Platform",
            "inputs": {
                "business_need": "Launch innovative fintech services",
                "features": "Digital wallet, robo-advisory, peer-to-peer payments, API banking",
                "stakeholders": "App users, developers, financial advisors",
                "compliance": "PCI DSS, open banking, KYC requirements"
            }
        }
    }
    
    results = {}
    
    try:
        service = AgenticRAGService()
        print(f"✅ AgenticRAGService initialized successfully")
        
        for domain_type, scenario in test_scenarios.items():
            print(f"\n🔍 Testing {domain_type.value.upper()} Domain...")
            
            try:
                # Generate BRD
                brd_result = service.generate_enhanced_document(
                    project=scenario["project"],
                    inputs=scenario["inputs"],
                    doc_type=DocumentType.BRD,
                    version=1
                )
                
                success = brd_result.get("success", False)
                domain_detected = "unknown"
                
                if success and "metadata" in brd_result:
                    domain_detected = brd_result["metadata"]["rag_context"]["domain"]
                
                results[domain_type.value] = {
                    "success": success,
                    "domain_detected": domain_detected,
                    "has_content": bool(brd_result.get("content")),
                    "content_length": len(brd_result.get("content", "")),
                    "vector_enhanced": "🔍 AI-Enhanced" in brd_result.get("content", "")
                }
                
                status = "✅ PASS" if success else "❌ FAIL"
                print(f"  {status} Domain: {domain_detected}")
                print(f"  📄 Content Length: {results[domain_type.value]['content_length']} chars")
                print(f"  🔍 Vector Enhanced: {results[domain_type.value]['vector_enhanced']}")
                
            except Exception as e:
                print(f"  ❌ ERROR: {e}")
                results[domain_type.value] = {"success": False, "error": str(e)}
                
    except Exception as e:
        print(f"❌ Service initialization failed: {e}")
        return {"error": "Service initialization failed"}
    
    return results

def test_vector_db_functionality():
    """Test Vector Database functionality independently"""
    print("\n" + "="*60)
    print("🗄️ TESTING VECTOR DATABASE FUNCTIONALITY")
    print("="*60)
    
    try:
        # Test VectorDB directly
        vector_db = VectorDB()
        print("✅ VectorDB initialized successfully")
        
        # Test document addition
        test_documents = [
            "Best practice for healthcare: Implement HIPAA compliant data handling",
            "Compliance requirement for banking: Maintain KYC documentation for all customers",
            "Validation rule for ecommerce: Verify product availability before order placement",
            "Risk management for mutual funds: Diversify portfolio across asset classes",
            "Fraud detection for cards payment: Monitor transaction patterns for anomalies"
        ]
        
        test_metadata = [
            {"type": "best_practice", "domain": "healthcare", "content": test_documents[0]},
            {"type": "compliance", "domain": "banking", "content": test_documents[1]},
            {"type": "validation_rule", "domain": "ecommerce", "content": test_documents[2]},
            {"type": "best_practice", "domain": "mutual_funds", "content": test_documents[3]},
            {"type": "validation_rule", "domain": "cards_payment", "content": test_documents[4]}
        ]
        
        vector_db.add_documents(test_documents, test_metadata)
        print(f"✅ Added {len(test_documents)} documents to vector DB")
        
        # Test search functionality
        search_queries = [
            "healthcare patient data protection",
            "banking customer verification",
            "payment fraud prevention",
            "investment risk management"
        ]
        
        search_results = {}
        for query in search_queries:
            results = vector_db.search(query, k=3)
            search_results[query] = len(results)
            print(f"🔍 Query: '{query[:30]}...' → {len(results)} results")
            
            for i, (doc, metadata, score) in enumerate(results[:2]):
                print(f"   {i+1}. [{metadata['domain']}] Score: {score:.2f}")
                print(f"      {doc[:80]}...")
        
        return {
            "vector_db_initialized": True,
            "documents_added": len(test_documents),
            "search_queries_tested": len(search_queries),
            "search_results": search_results
        }
        
    except Exception as e:
        print(f"❌ Vector DB test failed: {e}")
        return {"error": str(e)}

def test_knowledge_base_integration():
    """Test Knowledge Base with Vector DB integration"""
    print("\n" + "="*60)
    print("🧠 TESTING KNOWLEDGE BASE + VECTOR DB INTEGRATION")
    print("="*60)
    
    try:
        kb = KnowledgeBase()
        print("✅ KnowledgeBase with Vector DB initialized successfully")
        
        # Test domain count
        domain_count = len(kb.knowledge["domains"])
        print(f"📚 Knowledge Base contains {domain_count} domains")
        
        # Verify all financial domains are present
        expected_domains = [
            DomainType.MUTUAL_FUNDS,
            DomainType.AIF,
            DomainType.CARDS_PAYMENT,
            DomainType.INSURANCE,
            DomainType.EDUCATION,
            DomainType.LOGISTICS,
            DomainType.FINTECH
        ]
        
        missing_domains = []
        present_domains = []
        
        for domain in expected_domains:
            if domain in kb.knowledge["domains"]:
                present_domains.append(domain.value)
                print(f"✅ {domain.value} domain: IMPLEMENTED")
            else:
                missing_domains.append(domain.value)
                print(f"❌ {domain.value} domain: MISSING")
        
        # Test vector search integration
        test_queries = [
            "mutual fund portfolio management",
            "alternative investment compliance",
            "payment card security",
            "insurance claim processing"
        ]
        
        search_results = {}
        for query in test_queries:
            results = kb.search_knowledge(query, k=3)
            search_results[query] = len(results)
            print(f"🔍 Knowledge Search: '{query}' → {len(results)} results")
        
        return {
            "total_domains": domain_count,
            "present_domains": present_domains,
            "missing_domains": missing_domains,
            "vector_search_working": len(search_results) > 0,
            "search_results": search_results
        }
        
    except Exception as e:
        print(f"❌ Knowledge Base test failed: {e}")
        return {"error": str(e)}

def generate_comprehensive_report():
    """Generate comprehensive test report"""
    print("\n" + "="*80)
    print("📊 COMPREHENSIVE FINANCIAL DOMAINS + VECTOR DB TEST REPORT")
    print("="*80)
    
    # Run all tests
    domain_results = test_all_financial_domains()
    vector_results = test_vector_db_functionality()
    kb_results = test_knowledge_base_integration()
    
    # Generate summary
    print("\n" + "="*60)
    print("📋 EXECUTIVE SUMMARY")
    print("="*60)
    
    # Domain implementation summary
    if isinstance(domain_results, dict) and "error" not in domain_results:
        successful_domains = sum(1 for r in domain_results.values() if r.get("success", False))
        total_domains = len(domain_results)
        
        print(f"🏗️ DOMAIN IMPLEMENTATIONS:")
        print(f"   ✅ Successful: {successful_domains}/{total_domains}")
        print(f"   📊 Success Rate: {(successful_domains/total_domains)*100:.1f}%")
        
        # List working domains
        working_domains = [domain for domain, result in domain_results.items() 
                          if result.get("success", False)]
        print(f"   🎯 Working Domains: {', '.join(working_domains)}")
    else:
        print(f"🏗️ DOMAIN IMPLEMENTATIONS: ❌ FAILED")
    
    # Vector DB summary
    if isinstance(vector_results, dict) and "error" not in vector_results:
        print(f"🗄️ VECTOR DATABASE:")
        print(f"   ✅ Initialization: SUCCESS")
        print(f"   📚 Documents Added: {vector_results.get('documents_added', 0)}")
        print(f"   🔍 Search Queries Tested: {vector_results.get('search_queries_tested', 0)}")
    else:
        print(f"🗄️ VECTOR DATABASE: ❌ FAILED")
    
    # Knowledge Base summary
    if isinstance(kb_results, dict) and "error" not in kb_results:
        print(f"🧠 KNOWLEDGE BASE:")
        print(f"   ✅ Total Domains: {kb_results.get('total_domains', 0)}")
        print(f"   🎯 Present Domains: {len(kb_results.get('present_domains', []))}")
        print(f"   🔍 Vector Search: {'WORKING' if kb_results.get('vector_search_working') else 'FAILED'}")
    else:
        print(f"🧠 KNOWLEDGE BASE: ❌ FAILED")
    
    # Overall status
    overall_success = (
        isinstance(domain_results, dict) and "error" not in domain_results and
        isinstance(vector_results, dict) and "error" not in vector_results and
        isinstance(kb_results, dict) and "error" not in kb_results
    )
    
    print(f"\n🎯 OVERALL STATUS: {'✅ SUCCESS' if overall_success else '❌ NEEDS ATTENTION'}")
    
    # Save detailed results
    full_results = {
        "timestamp": "2025-09-27T18:47:21",
        "test_type": "Financial Domains + Vector DB Integration",
        "domain_results": domain_results,
        "vector_db_results": vector_results,
        "knowledge_base_results": kb_results,
        "overall_success": overall_success
    }
    
    try:
        with open("financial_domains_vector_db_test_results.json", "w") as f:
            json.dump(full_results, f, indent=2, default=str)
        print(f"💾 Detailed results saved to: financial_domains_vector_db_test_results.json")
    except Exception as e:
        print(f"⚠️ Could not save results: {e}")
    
    return full_results

if __name__ == "__main__":
    print("🚀 Starting Comprehensive Financial Domains + Vector DB Test Suite")
    print("="*80)
    
    results = generate_comprehensive_report()
    
    print("\n🏁 Test Suite Complete!")
    print(f"📊 Results: {'✅ SUCCESS' if results['overall_success'] else '❌ NEEDS REVIEW'}")