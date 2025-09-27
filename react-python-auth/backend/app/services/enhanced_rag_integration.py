"""
Enhanced RAG Integration Service
Combines the existing AI service with Agentic RAG and Vector DB capabilities
"""

import os
import logging
from typing import Dict, Any, Optional
from app.services.ai_service import (
    generate_brd_html,
    generate_frd_html_from_brd,
    _detect_domain_from_inputs
)

try:
    from app.services.agentic_rag_service import (
        AgenticRAGService, 
        DocumentType, 
        DomainType
    )
    AGENTIC_RAG_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Agentic RAG Service not available: {e}")
    AGENTIC_RAG_AVAILABLE = False

logger = logging.getLogger(__name__)

class EnhancedRAGIntegration:
    """
    Enhanced RAG Integration combining traditional AI service with Agentic RAG
    """
    
    def __init__(self):
        self.agentic_rag_service = None
        if AGENTIC_RAG_AVAILABLE:
            try:
                self.agentic_rag_service = AgenticRAGService()
                logger.info("🤖 Enhanced RAG Integration initialized with Agentic RAG")
            except Exception as e:
                logger.warning(f"Failed to initialize Agentic RAG: {e}")
                self.agentic_rag_service = None
        else:
            logger.info("📝 Enhanced RAG Integration initialized with traditional AI service only")
    
    def generate_enhanced_brd(self, project: str, inputs: Dict[str, Any], version: int = 1) -> Dict[str, Any]:
        """
        Generate BRD using enhanced RAG approach with intelligent fallback
        """
        logger.info(f"🚀 Starting Enhanced BRD generation for: {project}")
        
        # Try Agentic RAG first if available
        if self.agentic_rag_service:
            try:
                logger.info("🎯 Using Agentic RAG Service...")
                result = self.agentic_rag_service.generate_document(
                    project, inputs, DocumentType.BRD, version
                )
                
                if result.get('success'):
                    logger.info("✅ Agentic RAG BRD generation successful")
                    return {
                        'success': True,
                        'content': result['content'],
                        'method': 'agentic_rag',
                        'metadata': result['metadata'],
                        'enhanced_features': {
                            'vector_search': True,
                            'domain_intelligence': True,
                            'quality_validation': True,
                            'adaptive_generation': True
                        }
                    }
                else:
                    logger.warning("⚠️  Agentic RAG failed, falling back to traditional AI")
            except Exception as e:
                logger.error(f"❌ Agentic RAG error: {e}")
        
        # Fallback to traditional AI service
        logger.info("📝 Using Traditional AI Service...")
        traditional_result = generate_brd_html(project, inputs, version)
        
        return {
            'success': bool(traditional_result),
            'content': traditional_result,
            'method': 'traditional_ai',
            'metadata': {
                'project': project,
                'version': version,
                'domain': _detect_domain_from_inputs(inputs),
                'generation_method': 'traditional_fallback'
            },
            'enhanced_features': {
                'vector_search': False,
                'domain_intelligence': True,
                'quality_validation': False,
                'adaptive_generation': False
            }
        }
    
    def generate_enhanced_frd(self, project: str, inputs: Dict[str, Any], 
                            brd_content: Optional[str] = None, version: int = 1) -> Dict[str, Any]:
        """
        Generate FRD using enhanced RAG approach with intelligent fallback
        """
        logger.info(f"🚀 Starting Enhanced FRD generation for: {project}")
        
        # Try Agentic RAG first if available
        if self.agentic_rag_service:
            try:
                logger.info("🎯 Using Agentic RAG Service for FRD...")
                
                # Enhance inputs with BRD content if available
                enhanced_inputs = inputs.copy()
                if brd_content:
                    enhanced_inputs['brd_context'] = brd_content
                
                result = self.agentic_rag_service.generate_document(
                    project, enhanced_inputs, DocumentType.FRD, version
                )
                
                if result.get('success'):
                    logger.info("✅ Agentic RAG FRD generation successful")
                    return {
                        'success': True,
                        'content': result['content'],
                        'method': 'agentic_rag',
                        'metadata': result['metadata'],
                        'enhanced_features': {
                            'vector_search': True,
                            'domain_intelligence': True,
                            'quality_validation': True,
                            'adaptive_generation': True,
                            'brd_context_aware': bool(brd_content)
                        }
                    }
                else:
                    logger.warning("⚠️  Agentic RAG FRD failed, falling back to traditional AI")
            except Exception as e:
                logger.error(f"❌ Agentic RAG FRD error: {e}")
        
        # Fallback to traditional AI service
        logger.info("📝 Using Traditional AI Service for FRD...")
        
        if brd_content:
            traditional_result = generate_frd_html_from_brd(project, brd_content, version)
        else:
            # Generate FRD from inputs if no BRD content
            traditional_result = generate_brd_html(project, inputs, version)
            # Simple conversion to FRD-like content
            if traditional_result:
                traditional_result = traditional_result.replace(
                    "Business Requirements Document", 
                    "Functional Requirements Document"
                ).replace("BRD", "FRD")
        
        return {
            'success': bool(traditional_result),
            'content': traditional_result,
            'method': 'traditional_ai',
            'metadata': {
                'project': project,
                'version': version,
                'domain': _detect_domain_from_inputs(inputs),
                'generation_method': 'traditional_fallback',
                'brd_context_available': bool(brd_content)
            },
            'enhanced_features': {
                'vector_search': False,
                'domain_intelligence': True,
                'quality_validation': False,
                'adaptive_generation': False,
                'brd_context_aware': bool(brd_content)
            }
        }
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get status of all available services"""
        return {
            'agentic_rag_available': bool(self.agentic_rag_service),
            'traditional_ai_available': True,
            'vector_db_available': AGENTIC_RAG_AVAILABLE,
            'enhanced_features': {
                'intelligent_domain_detection': True,
                'adaptive_generation_strategy': bool(self.agentic_rag_service),
                'quality_metrics': bool(self.agentic_rag_service),
                'vector_search': bool(self.agentic_rag_service),
                'multi_agent_system': bool(self.agentic_rag_service)
            },
            'supported_domains': [
                'Healthcare', 'Banking', 'E-commerce', 'Marketing', 
                'Education', 'Insurance', 'Mutual Funds', 'AIF', 
                'Finance', 'Logistics', 'Credit Cards', 'Payment'
            ]
        }
    
    def search_knowledge_base(self, query: str, domain: Optional[str] = None, k: int = 5) -> Dict[str, Any]:
        """Search the knowledge base using vector similarity"""
        if not self.agentic_rag_service:
            return {
                'success': False,
                'error': 'Agentic RAG Service not available',
                'results': []
            }
        
        try:
            # Convert domain string to DomainType if provided
            domain_type = None
            if domain:
                domain_mapping = {
                    'healthcare': DomainType.HEALTHCARE,
                    'banking': DomainType.BANKING,
                    'ecommerce': DomainType.ECOMMERCE,
                    'marketing': DomainType.MARKETING,
                    'education': DomainType.EDUCATION,
                    'insurance': DomainType.INSURANCE,
                    'mutual_funds': DomainType.MUTUAL_FUNDS,
                    'aif': DomainType.AIF,
                    'cards_payment': DomainType.CARDS_PAYMENT,
                    'logistics': DomainType.LOGISTICS,
                    'fintech': DomainType.FINTECH
                }
                domain_type = domain_mapping.get(domain.lower())
            
            results = self.agentic_rag_service.knowledge_base.search_knowledge(query, domain_type, k)
            
            return {
                'success': True,
                'query': query,
                'domain': domain,
                'results': results,
                'count': len(results)
            }
            
        except Exception as e:
            logger.error(f"Knowledge base search failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'results': []
            }

# Create global instance
enhanced_rag_integration = EnhancedRAGIntegration()

# Export functions for backward compatibility
def generate_enhanced_brd(project: str, inputs: Dict[str, Any], version: int = 1) -> Dict[str, Any]:
    """Generate enhanced BRD with RAG capabilities"""
    return enhanced_rag_integration.generate_enhanced_brd(project, inputs, version)

def generate_enhanced_frd(project: str, inputs: Dict[str, Any], 
                         brd_content: Optional[str] = None, version: int = 1) -> Dict[str, Any]:
    """Generate enhanced FRD with RAG capabilities"""
    return enhanced_rag_integration.generate_enhanced_frd(project, inputs, brd_content, version)

def get_rag_service_status() -> Dict[str, Any]:
    """Get RAG service status"""
    return enhanced_rag_integration.get_service_status()

def search_rag_knowledge_base(query: str, domain: Optional[str] = None, k: int = 5) -> Dict[str, Any]:
    """Search RAG knowledge base"""
    return enhanced_rag_integration.search_knowledge_base(query, domain, k)