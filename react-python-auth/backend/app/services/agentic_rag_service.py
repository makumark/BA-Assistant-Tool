"""
Intelligent Agentic Adaptive RAG Service for BA Tool
Implements multi-agent system for intelligent document generation
"""

import os
import json
import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import pickle
from pathlib import Path

logger = logging.getLogger(__name__)

class DocumentType(Enum):
    BRD = "BRD"
    FRD = "FRD" 
    SRS = "SRS"
    WIREFRAME = "WIREFRAME"
    PROTOTYPE = "PROTOTYPE"

class DomainType(Enum):
    HEALTHCARE = "healthcare"
    BANKING = "banking"
    ECOMMERCE = "ecommerce"
    INSURANCE = "insurance"
    MARKETING = "marketing"
    EDUCATION = "education"
    LOGISTICS = "logistics"
    FINTECH = "fintech"
    MUTUAL_FUNDS = "mutual_funds"
    AIF = "aif"
    CARDS_PAYMENT = "cards_payment"
    GENERAL = "general"

@dataclass
class RAGContext:
    """Context retrieved from knowledge base"""
    domain: DomainType
    document_type: DocumentType
    templates: List[str]
    best_practices: List[str]
    examples: List[str]
    validation_rules: List[str]
    stakeholders: List[str]
    compliance_requirements: List[str]

@dataclass
class GenerationStrategy:
    """Adaptive generation strategy"""
    complexity_level: str  # Low, Medium, High
    enhancement_level: str  # Basic, Advanced, Expert
    template_weight: float  # 0.0 to 1.0
    ai_creativity: float   # 0.0 to 1.0
    validation_strictness: str  # Relaxed, Standard, Strict

class VectorDB:
    """Vector database for semantic document retrieval"""
    
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2", vector_dim: int = 384):
        self.embedding_model_name = embedding_model
        self.vector_dim = vector_dim
        self.model = None
        self.index = None
        self.documents = []
        self.metadata = []
        self.db_path = Path("data/vector_db")
        self.db_path.mkdir(parents=True, exist_ok=True)
        
    def _initialize_model(self):
        """Initialize sentence transformer model with fallback"""
        try:
            self.model = SentenceTransformer(self.embedding_model_name)
            logger.info(f"✅ Vector DB initialized with {self.embedding_model_name}")
        except Exception as e:
            logger.warning(f"⚠️ Could not load SentenceTransformer: {e}")
            logger.info("📝 Vector DB will use simulated embeddings")
            self.model = None
    
    def _create_simulated_embedding(self, text: str) -> np.ndarray:
        """Create simulated embedding when actual model unavailable"""
        # Simple hash-based simulation for consistent results
        try:
            import numpy as np
            text_hash = hash(text) % (2**32)
            np.random.seed(text_hash)
            return np.random.normal(0, 1, self.vector_dim).astype(np.float32)
        except ImportError:
            # Even more basic fallback
            return [0.1] * self.vector_dim
    
    def add_documents(self, texts: List[str], metadata_list: List[Dict[str, Any]]):
        """Add documents to vector database"""
        if not self.model:
            self._initialize_model()
        
        try:
            if self.model:
                embeddings = self.model.encode(texts)
                import faiss
                if self.index is None:
                    self.index = faiss.IndexFlatIP(self.vector_dim)
                faiss.normalize_L2(embeddings)
                self.index.add(embeddings)
            
            self.documents.extend(texts)
            self.metadata.extend(metadata_list)
            
            logger.info(f"📚 Added {len(texts)} documents to vector DB")
            
        except Exception as e:
            logger.error(f"❌ Vector DB add_documents failed: {e}")
            # Fallback: store without embeddings
            self.documents.extend(texts)
            self.metadata.extend(metadata_list)
    
    def search(self, query: str, k: int = 5) -> List[Tuple[str, Dict[str, Any], float]]:
        """Search for similar documents"""
        if not self.documents:
            return []
        
        try:
            if self.model and self.index:
                import faiss
                query_embedding = self.model.encode([query])
                faiss.normalize_L2(query_embedding)
                
                scores, indices = self.index.search(query_embedding, min(k, len(self.documents)))
                
                results = []
                for score, idx in zip(scores[0], indices[0]):
                    if 0 <= idx < len(self.documents):
                        results.append((self.documents[idx], self.metadata[idx], float(score)))
                
                return results
            else:
                # Fallback: simple keyword matching
                query_lower = query.lower()
                results = []
                for i, doc in enumerate(self.documents):
                    score = sum(1 for word in query_lower.split() if word in doc.lower())
                    if score > 0:
                        results.append((doc, self.metadata[i], score / len(query_lower.split())))
                
                return sorted(results, key=lambda x: x[2], reverse=True)[:k]
                
        except Exception as e:
            logger.error(f"❌ Vector search failed: {e}")
            return []

class KnowledgeBase:
    """Domain-specific knowledge repository with vector search"""
    
    def __init__(self):
        self.knowledge = self._initialize_knowledge_base()
        self.vector_db = VectorDB()
        self._populate_vector_db()
    
    def _populate_vector_db(self):
        """Populate vector database with domain knowledge"""
        try:
            documents = []
            metadata = []
            
            for domain_type, domain_data in self.knowledge["domains"].items():
                # Add domain best practices
                for practice in domain_data.get("best_practices", []):
                    documents.append(f"Best Practice for {domain_type.value}: {practice}")
                    metadata.append({"type": "best_practice", "domain": domain_type.value, "content": practice})
                
                # Add compliance requirements
                for requirement in domain_data.get("compliance_requirements", []):
                    documents.append(f"Compliance Requirement for {domain_type.value}: {requirement}")
                    metadata.append({"type": "compliance", "domain": domain_type.value, "content": requirement})
                
                # Add validation rules
                for rule in domain_data.get("validation_rules", []):
                    documents.append(f"Validation Rule for {domain_type.value}: {rule}")
                    metadata.append({"type": "validation_rule", "domain": domain_type.value, "content": rule})
            
            if documents:
                self.vector_db.add_documents(documents, metadata)
                logger.info(f"🔍 Vector DB populated with {len(documents)} documents")
                
        except Exception as e:
            logger.error(f"❌ Failed to populate vector DB: {e}")
    
    def search_knowledge(self, query: str, domain: Optional[DomainType] = None, k: int = 5) -> List[Dict[str, Any]]:
        """Search knowledge base using vector similarity"""
        try:
            results = self.vector_db.search(query, k)
            
            # Filter by domain if specified
            if domain:
                results = [r for r in results if r[1].get('domain') == domain.value]
            
            return [{"content": r[0], "metadata": r[1], "score": r[2]} for r in results]
            
        except Exception as e:
            logger.error(f"❌ Knowledge search failed: {e}")
            return []
    
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Initialize comprehensive knowledge base"""
        return {
            "domains": {
                DomainType.HEALTHCARE: {
                    "keywords": ["patient", "medical", "clinical", "hipaa", "ehr", "diagnosis", "treatment", "prescription"],
                    "stakeholders": ["Patients", "Physicians", "Nurses", "Admin Staff", "IT Support", "Compliance Officers"],
                    "compliance": ["HIPAA", "FDA", "Joint Commission", "State Medical Boards"],
                    "templates": {
                        DocumentType.BRD: self._get_healthcare_brd_template(),
                        DocumentType.FRD: self._get_healthcare_frd_template()
                    },
                    "best_practices": [
                        "Ensure patient data privacy and security at all levels",
                        "Implement role-based access control for medical records",
                        "Maintain complete audit trails for all patient interactions",
                        "Comply with HIPAA regulations for data handling"
                    ],
                    "validation_rules": [
                        "All patient identifiers must be encrypted",
                        "Medical data access requires proper authentication",
                        "Clinical decisions must be traceable to authorized personnel",
                        "Patient consent required for all data usage"
                    ]
                },
                DomainType.BANKING: {
                    "keywords": ["account", "transaction", "payment", "compliance", "kyc", "aml", "fraud", "regulatory"],
                    "stakeholders": ["Account Holders", "Branch Staff", "Compliance Officers", "Risk Managers", "IT Security"],
                    "compliance": ["PCI DSS", "SOX", "Basel III", "GDPR", "AML/KYC Regulations"],
                    "templates": {
                        DocumentType.BRD: self._get_banking_brd_template(),
                        DocumentType.FRD: self._get_banking_frd_template()
                    },
                    "best_practices": [
                        "Implement multi-factor authentication for all transactions",
                        "Maintain real-time fraud monitoring and detection",
                        "Ensure regulatory compliance across all jurisdictions",
                        "Implement strong encryption for all financial data"
                    ],
                    "validation_rules": [
                        "Transaction amounts must be validated against limits",
                        "Account verification required before any operations",
                        "All financial operations must be logged and auditable",
                        "Real-time balance validation before transactions"
                    ]
                },
                DomainType.ECOMMERCE: {
                    "keywords": ["product", "order", "cart", "checkout", "inventory", "customer", "shipping", "payment"],
                    "stakeholders": ["Customers", "Store Managers", "Inventory Managers", "Customer Service", "IT Support"],
                    "compliance": ["PCI DSS", "GDPR", "Consumer Protection Laws", "Tax Regulations"],
                    "templates": {
                        DocumentType.BRD: self._get_ecommerce_brd_template(),
                        DocumentType.FRD: self._get_ecommerce_frd_template()
                    },
                    "best_practices": [
                        "Optimize for mobile-first user experience",
                        "Implement secure payment processing",
                        "Ensure real-time inventory synchronization",
                        "Provide comprehensive order tracking"
                    ],
                    "validation_rules": [
                        "Product availability must be validated before ordering",
                        "Payment processing must be PCI compliant",
                        "Order confirmation required before processing",
                        "Customer authentication required for account actions"
                    ]
                },
                DomainType.MARKETING: {
                    "keywords": ["campaign", "segmentation", "automation", "analytics", "lead", "customer journey"],
                    "stakeholders": ["Marketing Managers", "Campaign Specialists", "Data Analysts", "Content Creators"],
                    "compliance": ["GDPR", "CAN-SPAM", "CCPA", "Email Marketing Regulations"],
                    "templates": {
                        DocumentType.BRD: self._get_marketing_brd_template(),
                        DocumentType.FRD: self._get_marketing_frd_template()
                    },
                    "best_practices": [
                        "Implement consent-based marketing communications",
                        "Personalize customer experiences using data insights",
                        "Track campaign performance and ROI metrics",
                        "Maintain customer preference centers"
                    ],
                    "validation_rules": [
                        "Customer consent required for all communications",
                        "Email addresses must be validated before sending",
                        "Campaign performance metrics must be tracked",
                        "Unsubscribe options required in all communications"
                    ]
                },
                DomainType.INSURANCE: {
                    "keywords": ["policy", "claim", "premium", "underwriting", "risk", "coverage", "actuarial", "reinsurance"],
                    "stakeholders": ["Policyholders", "Insurance Agents", "Underwriters", "Claims Adjusters", "Actuaries", "Compliance Officers"],
                    "compliance": ["NAIC Regulations", "Solvency II", "GDPR", "State Insurance Laws", "AML Requirements"],
                    "templates": {
                        DocumentType.BRD: self._get_insurance_brd_template(),
                        DocumentType.FRD: self._get_insurance_frd_template()
                    },
                    "best_practices": [
                        "Implement automated underwriting for standard policies",
                        "Ensure accurate risk assessment and pricing",
                        "Streamline claims processing with digital workflows",
                        "Maintain regulatory compliance across all jurisdictions"
                    ],
                    "validation_rules": [
                        "Policy terms must comply with regulatory requirements",
                        "Claims must be processed within regulatory timeframes",
                        "Premium calculations must be actuarially sound",
                        "Customer data must be protected according to privacy laws"
                    ]
                },
                DomainType.EDUCATION: {
                    "keywords": ["student", "course", "curriculum", "assessment", "learning", "academic", "enrollment", "graduation"],
                    "stakeholders": ["Students", "Faculty", "Administrators", "Parents", "Academic Advisors", "IT Support"],
                    "compliance": ["FERPA", "ADA", "Title IX", "COPPA", "State Education Regulations"],
                    "templates": {
                        DocumentType.BRD: self._get_education_brd_template(),
                        DocumentType.FRD: self._get_education_frd_template()
                    },
                    "best_practices": [
                        "Implement accessible learning management systems",
                        "Ensure student data privacy and security",
                        "Provide comprehensive academic tracking and reporting",
                        "Support diverse learning modalities and requirements"
                    ],
                    "validation_rules": [
                        "Student records must be kept confidential per FERPA",
                        "Academic content must meet accreditation standards",
                        "Assessment methods must be fair and unbiased",
                        "Technology platforms must be ADA compliant"
                    ]
                },
                DomainType.LOGISTICS: {
                    "keywords": ["shipment", "warehouse", "inventory", "tracking", "supply chain", "delivery", "freight", "distribution"],
                    "stakeholders": ["Shippers", "Receivers", "Warehouse Staff", "Drivers", "Logistics Coordinators", "Supply Chain Managers"],
                    "compliance": ["DOT Regulations", "Customs Requirements", "Environmental Regulations", "Safety Standards"],
                    "templates": {
                        DocumentType.BRD: self._get_logistics_brd_template(),
                        DocumentType.FRD: self._get_logistics_frd_template()
                    },
                    "best_practices": [
                        "Implement real-time shipment tracking and visibility",
                        "Optimize warehouse operations and inventory management",
                        "Ensure compliance with transportation regulations",
                        "Provide automated route optimization and planning"
                    ],
                    "validation_rules": [
                        "Shipments must comply with hazardous materials regulations",
                        "Delivery confirmations must be captured and stored",
                        "Inventory levels must be accurately tracked and reported",
                        "Driver hours must comply with DOT regulations"
                    ]
                },
                DomainType.FINTECH: {
                    "keywords": ["digital wallet", "blockchain", "cryptocurrency", "robo-advisor", "peer-to-peer", "neobank", "api", "fintech"],
                    "stakeholders": ["App Users", "Financial Advisors", "Developers", "Product Managers", "Risk Managers", "Compliance Officers"],
                    "compliance": ["PCI DSS", "PSD2", "Open Banking", "KYC", "AML", "GDPR", "Financial Regulations"],
                    "templates": {
                        DocumentType.BRD: self._get_fintech_brd_template(),
                        DocumentType.FRD: self._get_fintech_frd_template()
                    },
                    "best_practices": [
                        "Implement secure API-first architecture",
                        "Ensure real-time transaction processing and monitoring",
                        "Provide intuitive user experiences for financial services",
                        "Maintain regulatory compliance in all jurisdictions"
                    ],
                    "validation_rules": [
                        "All financial transactions must be encrypted and secure",
                        "User identity verification required for account opening",
                        "Transaction limits must be enforced based on risk assessment",
                        "Compliance reporting must be automated and accurate"
                    ]
                },
                DomainType.MUTUAL_FUNDS: {
                    "keywords": ["nav", "portfolio", "fund manager", "asset allocation", "benchmark", "expense ratio", "dividend", "redemption"],
                    "stakeholders": ["Investors", "Fund Managers", "Portfolio Analysts", "Compliance Officers", "Registrar", "Distributors"],
                    "compliance": ["SEBI Regulations", "Mutual Fund Rules", "KYC Requirements", "NAV Calculation", "Portfolio Disclosure"],
                    "templates": {
                        DocumentType.BRD: self._get_mutual_funds_brd_template(),
                        DocumentType.FRD: self._get_mutual_funds_frd_template()
                    },
                    "best_practices": [
                        "Implement automated NAV calculation and publishing",
                        "Ensure accurate portfolio management and rebalancing",
                        "Provide comprehensive investor reporting and statements",
                        "Maintain regulatory compliance with fund operations"
                    ],
                    "validation_rules": [
                        "NAV calculations must be accurate and timely",
                        "Portfolio allocations must comply with fund objectives",
                        "Investor transactions must be processed within regulatory timeframes",
                        "All fund disclosures must be complete and accurate"
                    ]
                },
                DomainType.AIF: {
                    "keywords": ["alternative investment", "hedge fund", "private equity", "venture capital", "accredited investor", "qualified buyer", "fund structure"],
                    "stakeholders": ["Accredited Investors", "Fund Managers", "Investment Analysts", "Risk Officers", "Compliance Teams", "Prime Brokers"],
                    "compliance": ["AIF Regulations", "Accredited Investor Rules", "Disclosure Requirements", "Risk Management", "Reporting Standards"],
                    "templates": {
                        DocumentType.BRD: self._get_aif_brd_template(),
                        DocumentType.FRD: self._get_aif_frd_template()
                    },
                    "best_practices": [
                        "Implement sophisticated risk management and monitoring",
                        "Ensure proper investor accreditation and suitability",
                        "Provide detailed performance reporting and analytics",
                        "Maintain strict regulatory compliance and governance"
                    ],
                    "validation_rules": [
                        "Investor accreditation must be verified before investment",
                        "Risk metrics must be calculated and monitored continuously",
                        "Performance reporting must be accurate and comprehensive",
                        "Compliance documentation must be maintained and auditable"
                    ]
                },
                DomainType.CARDS_PAYMENT: {
                    "keywords": ["credit card", "debit card", "payment processing", "merchant", "pos", "contactless", "tokenization", "chargeback"],
                    "stakeholders": ["Cardholders", "Merchants", "Payment Processors", "Banks", "Card Networks", "Risk Analysts"],
                    "compliance": ["PCI DSS", "EMV Standards", "PSD2", "Card Network Rules", "Consumer Protection Laws", "AML"],
                    "templates": {
                        DocumentType.BRD: self._get_cards_payment_brd_template(),
                        DocumentType.FRD: self._get_cards_payment_frd_template()
                    },
                    "best_practices": [
                        "Implement secure tokenization for card data protection",
                        "Ensure real-time fraud detection and prevention",
                        "Provide seamless payment experiences across channels",
                        "Maintain PCI DSS compliance for all payment operations"
                    ],
                    "validation_rules": [
                        "Card data must be encrypted and tokenized",
                        "Transaction authorization must be real-time",
                        "Fraud scoring must be applied to all transactions",
                        "Chargeback processes must be automated and tracked"
                    ]
                }
            },
            "document_patterns": {
                DocumentType.BRD: {
                    "structure": ["Executive Summary", "Project Scope", "Business Objectives", "Requirements", "Assumptions", "Constraints"],
                    "epic_pattern": "EPIC-{number}: {title}",
                    "requirement_pattern": "The system shall {action}"
                },
                DocumentType.FRD: {
                    "structure": ["Functional Overview", "User Stories", "Acceptance Criteria", "Data Models", "Interfaces"],
                    "story_pattern": "As a {role}, I want {goal}, so that {benefit}",
                    "criteria_pattern": "Given {context}, when {action}, then {outcome}"
                }
            }
        }
    
    def _get_healthcare_brd_template(self) -> str:
        return """
        <h2>Healthcare System BRD Template</h2>
        <h3>Patient Safety & Compliance Focus</h3>
        <p>This BRD addresses healthcare-specific requirements including patient data protection, clinical workflows, and regulatory compliance.</p>
        <h4>Key Areas:</h4>
        <ul>
            <li>Patient Registration & Demographics</li>
            <li>Medical Record Management</li>
            <li>Clinical Decision Support</li>
            <li>Privacy & Security Controls</li>
            <li>Regulatory Compliance</li>
        </ul>
        """
    
    def _get_healthcare_frd_template(self) -> str:
        return """
        <h2>Healthcare System FRD Template</h2>
        <h3>Clinical Workflow & Data Management</h3>
        <p>Detailed functional requirements for healthcare systems with emphasis on patient care and data integrity.</p>
        """
    
    def _get_banking_brd_template(self) -> str:
        return """
        <h2>Banking System BRD Template</h2>
        <h3>Financial Services & Risk Management</h3>
        <p>Banking BRD focusing on financial operations, regulatory compliance, and security requirements.</p>
        <h4>Core Banking Functions:</h4>
        <ul>
            <li>Account Management</li>
            <li>Transaction Processing</li>
            <li>Risk Management</li>
            <li>Regulatory Reporting</li>
            <li>Security & Fraud Prevention</li>
        </ul>
        """
    
    def _get_banking_frd_template(self) -> str:
        return """
        <h2>Banking System FRD Template</h2>
        <h3>Transaction Processing & Security</h3>
        <p>Comprehensive functional requirements for banking systems with security and compliance focus.</p>
        """
    
    def _get_ecommerce_brd_template(self) -> str:
        return """
        <h2>E-commerce Platform BRD Template</h2>
        <h3>Customer Experience & Order Management</h3>
        <p>E-commerce BRD covering customer journey, product management, and order processing.</p>
        <h4>E-commerce Core:</h4>
        <ul>
            <li>Product Catalog Management</li>
            <li>Shopping Cart & Checkout</li>
            <li>Order Processing</li>
            <li>Customer Management</li>
            <li>Payment Integration</li>
        </ul>
        """
    
    def _get_ecommerce_frd_template(self) -> str:
        return """
        <h2>E-commerce Platform FRD Template</h2>
        <h3>User Experience & Transaction Processing</h3>
        <p>Detailed functional requirements for e-commerce platforms with customer-centric design.</p>
        """
    
    def _get_marketing_brd_template(self) -> str:
        return """
        <h2>Marketing Automation BRD Template</h2>
        <h3>Campaign Management & Customer Engagement</h3>
        <p>Marketing platform BRD focusing on automation, analytics, and customer journey optimization.</p>
        <h4>Marketing Capabilities:</h4>
        <ul>
            <li>Campaign Management</li>
            <li>Customer Segmentation</li>
            <li>Marketing Automation</li>
            <li>Analytics & Reporting</li>
            <li>Lead Management</li>
        </ul>
        """
    
    def _get_marketing_frd_template(self) -> str:
        return """
        <h2>Marketing Automation FRD Template</h2>
        <h3>Campaign Execution & Analytics</h3>
        <p>Functional requirements for marketing automation with focus on personalization and performance.</p>
        """
    
    def _get_insurance_brd_template(self) -> str:
        return """
        <h2>Insurance Management System BRD Template</h2>
        <h3>Policy Administration & Claims Processing</h3>
        <p>Insurance BRD covering policy lifecycle, claims management, and regulatory compliance.</p>
        <h4>Core Insurance Functions:</h4>
        <ul>
            <li>Policy Administration</li>
            <li>Underwriting Process</li>
            <li>Claims Processing</li>
            <li>Premium Calculation</li>
            <li>Risk Assessment</li>
        </ul>
        """
    
    def _get_insurance_frd_template(self) -> str:
        return """
        <h2>Insurance Management System FRD Template</h2>
        <h3>Policy & Claims Workflow Management</h3>
        <p>Detailed functional requirements for insurance systems with focus on automation and compliance.</p>
        """
    
    def _get_education_brd_template(self) -> str:
        return """
        <h2>Education Management System BRD Template</h2>
        <h3>Student Information & Learning Management</h3>
        <p>Education BRD covering student lifecycle, academic management, and learning platforms.</p>
        <h4>Educational Core Functions:</h4>
        <ul>
            <li>Student Information System</li>
            <li>Academic Planning</li>
            <li>Learning Management</li>
            <li>Assessment & Grading</li>
            <li>Communication & Collaboration</li>
        </ul>
        """
    
    def _get_education_frd_template(self) -> str:
        return """
        <h2>Education Management System FRD Template</h2>
        <h3>Academic Workflow & Student Services</h3>
        <p>Functional requirements for education systems with focus on accessibility and student success.</p>
        """
    
    def _get_logistics_brd_template(self) -> str:
        return """
        <h2>Logistics Management System BRD Template</h2>
        <h3>Supply Chain & Transportation Management</h3>
        <p>Logistics BRD covering supply chain optimization, warehouse management, and transportation.</p>
        <h4>Logistics Core Functions:</h4>
        <ul>
            <li>Warehouse Management</li>
            <li>Inventory Tracking</li>
            <li>Transportation Planning</li>
            <li>Shipment Tracking</li>
            <li>Supply Chain Optimization</li>
        </ul>
        """
    
    def _get_logistics_frd_template(self) -> str:
        return """
        <h2>Logistics Management System FRD Template</h2>
        <h3>Operations & Distribution Management</h3>
        <p>Functional requirements for logistics systems with focus on efficiency and visibility.</p>
        """
    
    def _get_fintech_brd_template(self) -> str:
        return """
        <h2>Fintech Platform BRD Template</h2>
        <h3>Digital Financial Services & Innovation</h3>
        <p>Fintech BRD covering digital banking, payments, and innovative financial services.</p>
        <h4>Fintech Core Functions:</h4>
        <ul>
            <li>Digital Wallet Services</li>
            <li>Payment Processing</li>
            <li>Robo-Advisory</li>
            <li>Peer-to-Peer Transactions</li>
            <li>API Banking Services</li>
        </ul>
        """
    
    def _get_fintech_frd_template(self) -> str:
        return """
        <h2>Fintech Platform FRD Template</h2>
        <h3>API-First Financial Services</h3>
        <p>Functional requirements for fintech platforms with focus on innovation and user experience.</p>
        """
    
    def _get_mutual_funds_brd_template(self) -> str:
        return """
        <h2>Mutual Funds Management System BRD Template</h2>
        <h3>Fund Administration & Investment Management</h3>
        <p>Mutual Funds BRD covering portfolio management, NAV calculation, and investor services.</p>
        <h4>Mutual Funds Core Functions:</h4>
        <ul>
            <li>Portfolio Management</li>
            <li>NAV Calculation</li>
            <li>Investor Onboarding</li>
            <li>Transaction Processing</li>
            <li>Performance Reporting</li>
        </ul>
        """
    
    def _get_mutual_funds_frd_template(self) -> str:
        return """
        <h2>Mutual Funds Management System FRD Template</h2>
        <h3>Investment Operations & Compliance</h3>
        <p>Functional requirements for mutual funds systems with focus on accuracy and regulatory compliance.</p>
        """
    
    def _get_aif_brd_template(self) -> str:
        return """
        <h2>Alternative Investment Funds BRD Template</h2>
        <h3>AIF Administration & Risk Management</h3>
        <p>AIF BRD covering alternative investments, sophisticated risk management, and accredited investor services.</p>
        <h4>AIF Core Functions:</h4>
        <ul>
            <li>Investor Qualification</li>
            <li>Portfolio Construction</li>
            <li>Risk Management</li>
            <li>Performance Analytics</li>
            <li>Regulatory Reporting</li>
        </ul>
        """
    
    def _get_aif_frd_template(self) -> str:
        return """
        <h2>Alternative Investment Funds FRD Template</h2>
        <h3>Advanced Investment Strategies & Governance</h3>
        <p>Functional requirements for AIF systems with focus on sophisticated investment management and compliance.</p>
        """
    
    def _get_cards_payment_brd_template(self) -> str:
        return """
        <h2>Cards & Payment Processing BRD Template</h2>
        <h3>Payment Gateway & Transaction Management</h3>
        <p>Cards & Payment BRD covering payment processing, fraud prevention, and merchant services.</p>
        <h4>Payment Core Functions:</h4>
        <ul>
            <li>Transaction Authorization</li>
            <li>Fraud Detection</li>
            <li>Merchant Services</li>
            <li>Settlement Processing</li>
            <li>Chargeback Management</li>
        </ul>
        """
    
    def _get_cards_payment_frd_template(self) -> str:
        return """
        <h2>Cards & Payment Processing FRD Template</h2>
        <h3>Secure Payment Infrastructure</h3>
        <p>Functional requirements for payment systems with focus on security, speed, and reliability.</p>
        """

class RetrievalAgent:
    """Intelligent context retrieval from knowledge base"""
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
    
    def detect_domain(self, inputs: Dict[str, Any]) -> DomainType:
        """Detect domain using advanced keyword matching and context analysis"""
        text_content = self._extract_text_content(inputs)
        domain_scores = {}
        
        for domain, domain_data in self.kb.knowledge["domains"].items():
            score = 0
            keywords = domain_data["keywords"]
            
            for keyword in keywords:
                # Weighted scoring based on keyword importance and frequency
                frequency = text_content.lower().count(keyword.lower())
                if frequency > 0:
                    # Important keywords get higher weight
                    weight = 2.0 if keyword in ["patient", "account", "product", "campaign"] else 1.0
                    score += frequency * weight
            
            domain_scores[domain] = score
        
        # Return domain with highest score, default to GENERAL
        if not domain_scores or max(domain_scores.values()) == 0:
            return DomainType.GENERAL
            
        return max(domain_scores, key=domain_scores.get)
    
    def retrieve_context(self, inputs: Dict[str, Any], doc_type: DocumentType) -> RAGContext:
        """Retrieve relevant context from knowledge base with vector search enhancement"""
        domain = self.detect_domain(inputs)
        text_content = self._extract_text_content(inputs)
        
        if domain == DomainType.GENERAL or domain not in self.kb.knowledge["domains"]:
            return self._get_general_context(doc_type)
        
        domain_data = self.kb.knowledge["domains"][domain]
        
        # Enhanced context with vector search
        vector_results = self.kb.search_knowledge(text_content, domain, k=5)
        enhanced_practices = domain_data.get("best_practices", [])
        enhanced_examples = self._get_relevant_examples(domain, doc_type, inputs)
        
        # Add vector search results to practices and examples
        for result in vector_results:
            if result["metadata"]["type"] == "best_practice" and result["score"] > 0.7:
                enhanced_practices.append(f"🔍 AI-Enhanced: {result['metadata']['content']}")
            elif result["metadata"]["type"] == "validation_rule" and result["score"] > 0.7:
                enhanced_examples.append(f"🔍 Validation Insight: {result['metadata']['content']}")
        
        return RAGContext(
            domain=domain,
            document_type=doc_type,
            templates=self._get_templates(domain_data, doc_type),
            best_practices=enhanced_practices,
            examples=enhanced_examples,
            validation_rules=domain_data.get("validation_rules", []),
            stakeholders=domain_data.get("stakeholders", []),
            compliance_requirements=domain_data.get("compliance", [])
        )
    
    def _extract_text_content(self, inputs: Dict[str, Any]) -> str:
        """Extract all text content from inputs for analysis"""
        text_parts = []
        for key, value in inputs.items():
            if isinstance(value, str):
                text_parts.append(value)
            elif isinstance(value, list):
                text_parts.extend([str(item) for item in value])
        return " ".join(text_parts)
    
    def _get_templates(self, domain_data: Dict[str, Any], doc_type: DocumentType) -> List[str]:
        """Get relevant templates for domain and document type"""
        templates = domain_data.get("templates", {})
        return [templates.get(doc_type, "")] if templates.get(doc_type) else []
    
    def _get_relevant_examples(self, domain: DomainType, doc_type: DocumentType, inputs: Dict[str, Any]) -> List[str]:
        """Get relevant examples based on domain and inputs"""
        # This would typically query a vector database or example repository
        # For now, return domain-specific examples
        examples = {
            DomainType.HEALTHCARE: [
                "Patient registration with HIPAA compliance",
                "Medical record access control",
                "Clinical decision support system"
            ],
            DomainType.BANKING: [
                "Account opening with KYC verification",
                "Real-time transaction processing",
                "Fraud detection and prevention"
            ],
            DomainType.ECOMMERCE: [
                "Product catalog management",
                "Shopping cart and checkout flow",
                "Order fulfillment process"
            ]
        }
        return examples.get(domain, [])
    
    def _get_general_context(self, doc_type: DocumentType) -> RAGContext:
        """Get general context when domain is not detected"""
        return RAGContext(
            domain=DomainType.GENERAL,
            document_type=doc_type,
            templates=["General business document template"],
            best_practices=["Follow industry standards", "Ensure clear requirements", "Maintain traceability"],
            examples=["Standard business requirements", "User acceptance criteria"],
            validation_rules=["Validate input completeness", "Ensure requirement clarity"],
            stakeholders=["Business Users", "IT Team", "Project Manager"],
            compliance_requirements=["Data Privacy", "Security Standards"]
        )

class AdaptiveAgent:
    """Determines optimal generation strategy based on context"""
    
    def determine_strategy(self, inputs: Dict[str, Any], context: RAGContext) -> GenerationStrategy:
        """Determine adaptive generation strategy"""
        complexity = self._assess_complexity(inputs, context)
        enhancement_level = self._determine_enhancement_level(inputs, context)
        
        return GenerationStrategy(
            complexity_level=complexity,
            enhancement_level=enhancement_level,
            template_weight=self._calculate_template_weight(complexity, enhancement_level),
            ai_creativity=self._calculate_ai_creativity(complexity, enhancement_level),
            validation_strictness=self._determine_validation_strictness(context.domain)
        )
    
    def _assess_complexity(self, inputs: Dict[str, Any], context: RAGContext) -> str:
        """Assess complexity based on inputs and domain"""
        text_content = " ".join([str(v) for v in inputs.values() if isinstance(v, str)])
        
        # Complexity indicators
        high_complexity_indicators = [
            "integration", "api", "workflow", "automation", "analytics", 
            "machine learning", "ai", "complex business rules"
        ]
        medium_complexity_indicators = [
            "reporting", "dashboard", "user management", "notification", 
            "validation", "approval process"
        ]
        
        high_count = sum(1 for indicator in high_complexity_indicators 
                        if indicator in text_content.lower())
        medium_count = sum(1 for indicator in medium_complexity_indicators 
                          if indicator in text_content.lower())
        
        if high_count >= 3:
            return "High"
        elif high_count >= 1 or medium_count >= 3:
            return "Medium"
        else:
            return "Low"
    
    def _determine_enhancement_level(self, inputs: Dict[str, Any], context: RAGContext) -> str:
        """Determine level of AI enhancement needed"""
        if context.domain in [DomainType.HEALTHCARE, DomainType.BANKING]:
            return "Expert"  # High compliance requirements
        elif len(context.best_practices) > 5:
            return "Advanced"
        else:
            return "Basic"
    
    def _calculate_template_weight(self, complexity: str, enhancement: str) -> float:
        """Calculate how much to rely on templates vs AI creativity"""
        weights = {
            ("Low", "Basic"): 0.8,
            ("Low", "Advanced"): 0.6,
            ("Medium", "Basic"): 0.7,
            ("Medium", "Advanced"): 0.5,
            ("High", "Expert"): 0.4
        }
        return weights.get((complexity, enhancement), 0.5)
    
    def _calculate_ai_creativity(self, complexity: str, enhancement: str) -> float:
        """Calculate AI creativity level"""
        return 1.0 - self._calculate_template_weight(complexity, enhancement)
    
    def _determine_validation_strictness(self, domain: DomainType) -> str:
        """Determine validation strictness based on domain"""
        if domain in [DomainType.HEALTHCARE, DomainType.BANKING]:
            return "Strict"
        elif domain in [DomainType.ECOMMERCE, DomainType.MARKETING]:
            return "Standard"
        else:
            return "Relaxed"

class GenerationAgent:
    """Generates documents using RAG context and AI"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
    
    def generate_document(self, inputs: Dict[str, Any], context: RAGContext, 
                         strategy: GenerationStrategy, doc_type: DocumentType) -> str:
        """Generate document using intelligent RAG approach"""
        
        # Create enhanced prompt using RAG context
        enhanced_prompt = self._create_enhanced_prompt(inputs, context, strategy, doc_type)
        
        # Call AI with adaptive parameters
        ai_response = self._call_ai_with_strategy(enhanced_prompt, strategy)
        
        if ai_response:
            return self._post_process_response(ai_response, context, strategy)
        else:
            # Fallback to template-based generation
            return self._template_based_generation(inputs, context, strategy)
    
    def _create_enhanced_prompt(self, inputs: Dict[str, Any], context: RAGContext, 
                               strategy: GenerationStrategy, doc_type: DocumentType) -> str:
        """Create enhanced prompt using RAG context"""
        
        domain_context = f"""
DOMAIN EXPERTISE: {context.domain.value.title()}
STAKEHOLDERS: {', '.join(context.stakeholders)}
COMPLIANCE: {', '.join(context.compliance_requirements)}

BEST PRACTICES:
{chr(10).join([f"• {bp}" for bp in context.best_practices])}

VALIDATION RULES:
{chr(10).join([f"• {vr}" for vr in context.validation_rules])}
"""
        
        strategy_guidance = f"""
GENERATION STRATEGY:
- Complexity Level: {strategy.complexity_level}
- Enhancement Level: {strategy.enhancement_level}
- Template Weight: {strategy.template_weight}
- AI Creativity: {strategy.ai_creativity}
- Validation Strictness: {strategy.validation_strictness}
"""
        
        user_inputs = f"""
USER INPUTS:
{chr(10).join([f"{k}: {v}" for k, v in inputs.items() if v])}
"""
        
        templates = f"""
RELEVANT TEMPLATES:
{chr(10).join(context.templates)}
""" if context.templates else ""
        
        return f"""
You are a Senior Business Analyst with deep expertise in {context.domain.value} domain.

{domain_context}

{strategy_guidance}

{templates}

{user_inputs}

Generate a comprehensive {doc_type.value} that:
1. Incorporates domain-specific best practices
2. Addresses compliance requirements
3. Uses appropriate stakeholder language
4. Follows industry standards
5. Is tailored to the complexity level specified

Output only clean HTML without code blocks or markdown.
"""
    
    def _call_ai_with_strategy(self, prompt: str, strategy: GenerationStrategy) -> Optional[str]:
        """Call AI with strategy-adapted parameters"""
        try:
            if not self.api_key or not self.api_key.startswith("pplx-"):
                return None
            
            from openai import OpenAI
            client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.perplexity.ai"
            )
            
            # Adapt parameters based on strategy
            temperature = strategy.ai_creativity * 0.8  # Scale creativity
            max_tokens = 3000 if strategy.complexity_level == "High" else 2000
            model = "llama-3.1-sonar-large-128k-online" if strategy.enhancement_level == "Expert" else "llama-3.1-sonar-small-128k-online"
            
            completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            return None
    
    def _post_process_response(self, response: str, context: RAGContext, 
                              strategy: GenerationStrategy) -> str:
        """Post-process AI response for quality and compliance"""
        # Remove code blocks if present
        cleaned_response = re.sub(r'```[a-zA-Z]*\n?|```', '', response)
        
        # Add domain-specific enhancements
        if context.domain != DomainType.GENERAL:
            cleaned_response = self._add_domain_enhancements(cleaned_response, context)
        
        return cleaned_response.strip()
    
    def _add_domain_enhancements(self, content: str, context: RAGContext) -> str:
        """Add domain-specific enhancements to generated content"""
        domain_footer = f"""
        <div style="margin-top: 30px; padding: 15px; background-color: #f0f9ff; border-left: 4px solid #3b82f6;">
            <h4 style="color: #1e40af; margin-top: 0;">🎯 {context.domain.value.title()} Domain Insights</h4>
            <p><strong>Compliance Requirements:</strong> {', '.join(context.compliance_requirements)}</p>
            <p><strong>Key Stakeholders:</strong> {', '.join(context.stakeholders)}</p>
            <p style="font-size: 12px; color: #6b7280; margin-bottom: 0;">
                Generated using Agentic Adaptive RAG | Domain: {context.domain.value} | 
                Enhanced with domain-specific knowledge and best practices
            </p>
        </div>
        """
        
        return content + domain_footer
    
    def _template_based_generation(self, inputs: Dict[str, Any], context: RAGContext, 
                                  strategy: GenerationStrategy) -> str:
        """Fallback template-based generation when AI fails"""
        template = context.templates[0] if context.templates else "<h2>Document Generated</h2>"
        
        # Basic template processing
        processed_content = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            {template}
            <h3>Requirements Overview</h3>
            <ul>
                {chr(10).join([f"<li>{v}</li>" for v in inputs.values() if isinstance(v, str) and v.strip()])}
            </ul>
            <h3>Domain Context</h3>
            <p>Domain: {context.domain.value.title()}</p>
            <p>Stakeholders: {', '.join(context.stakeholders)}</p>
            <div style="margin-top: 20px; padding: 10px; background-color: #fef3c7; border-radius: 5px;">
                <p><strong>Note:</strong> This document was generated using template-based fallback. 
                For enhanced AI-powered generation, ensure proper API configuration.</p>
            </div>
        </div>
        """
        
        return processed_content

class QualityAgent:
    """Validates and improves generated content quality"""
    
    def validate_and_improve(self, content: str, context: RAGContext, 
                            strategy: GenerationStrategy) -> Dict[str, Any]:
        """Validate content quality and suggest improvements"""
        
        quality_metrics = {
            "completeness_score": self._assess_completeness(content, context),
            "domain_relevance": self._assess_domain_relevance(content, context),
            "structure_quality": self._assess_structure_quality(content),
            "compliance_coverage": self._assess_compliance_coverage(content, context),
            "overall_score": 0.0,
            "recommendations": []
        }
        
        # Calculate overall score
        scores = [quality_metrics["completeness_score"], quality_metrics["domain_relevance"], 
                 quality_metrics["structure_quality"], quality_metrics["compliance_coverage"]]
        quality_metrics["overall_score"] = sum(scores) / len(scores)
        
        # Generate recommendations
        quality_metrics["recommendations"] = self._generate_recommendations(quality_metrics, context)
        
        return quality_metrics
    
    def _assess_completeness(self, content: str, context: RAGContext) -> float:
        """Assess content completeness"""
        required_sections = ["summary", "requirements", "scope", "objectives"]
        content_lower = content.lower()
        
        found_sections = sum(1 for section in required_sections if section in content_lower)
        return found_sections / len(required_sections)
    
    def _assess_domain_relevance(self, content: str, context: RAGContext) -> float:
        """Assess domain relevance"""
        if context.domain == DomainType.GENERAL:
            return 0.8  # Default for general domain
        
        domain_data = context.domain.value
        domain_keywords = {
            "healthcare": ["patient", "medical", "clinical", "hipaa"],
            "banking": ["account", "transaction", "compliance", "security"],
            "ecommerce": ["product", "order", "customer", "checkout"]
        }.get(domain_data, [])
        
        content_lower = content.lower()
        found_keywords = sum(1 for keyword in domain_keywords if keyword in content_lower)
        
        return min(found_keywords / len(domain_keywords), 1.0) if domain_keywords else 0.5
    
    def _assess_structure_quality(self, content: str) -> float:
        """Assess document structure quality"""
        structure_indicators = ["<h1>", "<h2>", "<h3>", "<ul>", "<ol>", "<p>"]
        content_lower = content.lower()
        
        found_indicators = sum(1 for indicator in structure_indicators if indicator in content_lower)
        return min(found_indicators / len(structure_indicators), 1.0)
    
    def _assess_compliance_coverage(self, content: str, context: RAGContext) -> float:
        """Assess compliance requirement coverage"""
        if not context.compliance_requirements:
            return 0.8  # Default when no specific compliance requirements
        
        content_lower = content.lower()
        covered_requirements = 0
        
        for requirement in context.compliance_requirements:
            if any(keyword in content_lower for keyword in requirement.lower().split()):
                covered_requirements += 1
        
        return covered_requirements / len(context.compliance_requirements)
    
    def _generate_recommendations(self, metrics: Dict[str, Any], context: RAGContext) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        if metrics["completeness_score"] < 0.7:
            recommendations.append("Add missing sections: Executive Summary, Project Scope, or Business Objectives")
        
        if metrics["domain_relevance"] < 0.6:
            recommendations.append(f"Include more {context.domain.value}-specific terminology and concepts")
        
        if metrics["structure_quality"] < 0.6:
            recommendations.append("Improve document structure with proper headings, lists, and formatting")
        
        if metrics["compliance_coverage"] < 0.5:
            recommendations.append("Address compliance requirements: " + ", ".join(context.compliance_requirements))
        
        if metrics["overall_score"] >= 0.8:
            recommendations.append("✅ Document quality meets high standards")
        
        return recommendations

class AgenticRAGService:
    """Main Agentic Adaptive RAG service orchestrator"""
    
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.retrieval_agent = RetrievalAgent(self.knowledge_base)
        self.adaptive_agent = AdaptiveAgent()
        self.generation_agent = GenerationAgent()
        self.quality_agent = QualityAgent()
        
        logger.info("🤖 Agentic Adaptive RAG Service initialized")
    
    def generate_document(self, project: str, inputs: Dict[str, Any], 
                         doc_type: DocumentType, version: int = 1) -> Dict[str, Any]:
        """Main document generation using Agentic Adaptive RAG"""
        
        start_time = datetime.now()
        
        try:
            logger.info(f"🚀 Starting Agentic RAG generation for {doc_type.value}")
            
            # Step 1: Intelligent Context Retrieval
            logger.info("📚 Retrieving domain context...")
            context = self.retrieval_agent.retrieve_context(inputs, doc_type)
            
            # Step 2: Adaptive Strategy Determination
            logger.info("🎯 Determining generation strategy...")
            strategy = self.adaptive_agent.determine_strategy(inputs, context)
            
            # Step 3: Intelligent Document Generation
            logger.info("✨ Generating document with AI enhancement...")
            generated_content = self.generation_agent.generate_document(inputs, context, strategy, doc_type)
            
            # Step 4: Quality Validation & Improvement
            logger.info("🔍 Validating and improving content quality...")
            quality_metrics = self.quality_agent.validate_and_improve(generated_content, context, strategy)
            
            generation_time = (datetime.now() - start_time).total_seconds()
            
            result = {
                "success": True,
                "content": generated_content,
                "metadata": {
                    "project": project,
                    "version": version,
                    "document_type": doc_type.value,
                    "domain": context.domain.value,
                    "generation_strategy": {
                        "complexity": strategy.complexity_level,
                        "enhancement": strategy.enhancement_level,
                        "template_weight": strategy.template_weight,
                        "ai_creativity": strategy.ai_creativity
                    },
                    "quality_metrics": quality_metrics,
                    "generation_time": generation_time,
                    "rag_context": {
                        "domain": context.domain.value,
                        "stakeholders": context.stakeholders,
                        "compliance": context.compliance_requirements,
                        "best_practices_count": len(context.best_practices)
                    }
                }
            }
            
            logger.info(f"✅ Agentic RAG generation completed in {generation_time:.2f}s")
            logger.info(f"📊 Quality Score: {quality_metrics['overall_score']:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Agentic RAG generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "content": self._emergency_fallback(project, inputs, doc_type, version)
            }
    
    def _emergency_fallback(self, project: str, inputs: Dict[str, Any], 
                           doc_type: DocumentType, version: int) -> str:
        """Emergency fallback when all else fails"""
        return f"""
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            <h1>{doc_type.value} - {project}</h1>
            <h2>Version {version}</h2>
            <div style="background: #fef3c7; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>⚠️ Emergency Fallback Mode</strong></p>
                <p>The Agentic RAG system encountered an issue. This is a basic document structure.</p>
            </div>
            <h3>Requirements</h3>
            <ul>
                {chr(10).join([f"<li>{v}</li>" for v in inputs.values() if isinstance(v, str) and v.strip()])}
            </ul>
            <p><em>Generated using emergency fallback at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
        </div>
        """

# Export main service
agentic_rag_service = AgenticRAGService()