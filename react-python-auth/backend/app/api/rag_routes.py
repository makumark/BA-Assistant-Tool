"""
Enhanced RAG API Routes for FastAPI
Provides endpoints for RAG-enhanced document generation and knowledge search
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

# Import our enhanced RAG integration
try:
    from app.services.enhanced_rag_integration import (
        generate_enhanced_brd,
        generate_enhanced_frd,
        get_rag_service_status,
        search_rag_knowledge_base
    )
    RAG_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Enhanced RAG integration not available: {e}")
    RAG_AVAILABLE = False

logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic models for request/response
class BRDRequest(BaseModel):
    project: str = "Untitled Project"
    inputs: Dict[str, Any]
    version: int = 1

class FRDRequest(BaseModel):
    project: str = "Untitled Project"
    inputs: Dict[str, Any]
    brd_content: Optional[str] = None
    version: int = 1

class EnhancedDocumentsRequest(BaseModel):
    project: str = "Untitled Project"
    inputs: Dict[str, Any]
    version: int = 1
    generate_both: bool = False

class SearchRequest(BaseModel):
    query: str
    domain: Optional[str] = None
    k: int = 5

@router.get("/status")
async def get_service_status():
    """Get RAG service status and capabilities"""
    try:
        if not RAG_AVAILABLE:
            return {
                'success': False,
                'error': 'Enhanced RAG integration not available',
                'status': {
                    'agentic_rag_available': False,
                    'traditional_ai_available': True,
                    'vector_db_available': False
                }
            }
        
        status = get_rag_service_status()
        return {
            'success': True,
            'status': status
        }
    except Exception as e:
        logger.error(f"Error getting RAG status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate/brd")
async def generate_brd_enhanced(request: BRDRequest):
    """Generate BRD using enhanced RAG approach"""
    try:
        if not RAG_AVAILABLE:
            raise HTTPException(
                status_code=503, 
                detail="Enhanced RAG integration not available"
            )
        
        logger.info(f"🚀 Enhanced BRD generation request for: {request.project}")
        
        result = generate_enhanced_brd(request.project, request.inputs, request.version)
        
        if result.get('success'):
            return result
        else:
            raise HTTPException(status_code=500, detail=result.get('error', 'Generation failed'))
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enhanced BRD generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate/frd")
async def generate_frd_enhanced(request: FRDRequest):
    """Generate FRD using enhanced RAG approach"""
    try:
        if not RAG_AVAILABLE:
            raise HTTPException(
                status_code=503, 
                detail="Enhanced RAG integration not available"
            )
        
        logger.info(f"🚀 Enhanced FRD generation request for: {request.project}")
        
        result = generate_enhanced_frd(
            request.project, 
            request.inputs, 
            request.brd_content, 
            request.version
        )
        
        if result.get('success'):
            return result
        else:
            raise HTTPException(status_code=500, detail=result.get('error', 'Generation failed'))
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enhanced FRD generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search")
async def search_knowledge(request: SearchRequest):
    """Search the RAG knowledge base"""
    try:
        if not RAG_AVAILABLE:
            raise HTTPException(
                status_code=503, 
                detail="Enhanced RAG integration not available"
            )
        
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        logger.info(f"🔍 Knowledge base search: {request.query[:50]}...")
        
        result = search_rag_knowledge_base(request.query, request.domain, request.k)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Knowledge base search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate/enhanced")
async def generate_enhanced_documents(request: EnhancedDocumentsRequest):
    """Generate both BRD and FRD with enhanced RAG in sequence"""
    try:
        if not RAG_AVAILABLE:
            raise HTTPException(
                status_code=503, 
                detail="Enhanced RAG integration not available"
            )
        
        logger.info(f"🚀 Enhanced document generation request for: {request.project}")
        
        # Generate BRD first
        brd_result = generate_enhanced_brd(request.project, request.inputs, request.version)
        
        result = {
            'success': brd_result.get('success', False),
            'brd': brd_result
        }
        
        # Generate FRD if requested and BRD was successful
        if request.generate_both and brd_result.get('success'):
            logger.info("📝 Generating FRD from BRD...")
            frd_result = generate_enhanced_frd(
                request.project, 
                request.inputs, 
                brd_result.get('content'), 
                request.version
            )
            result['frd'] = frd_result
            result['success'] = result['success'] and frd_result.get('success', False)
        
        # Add summary information
        result['summary'] = {
            'project': request.project,
            'version': request.version,
            'brd_method': brd_result.get('method', 'unknown'),
            'frd_method': result.get('frd', {}).get('method', 'not_generated'),
            'enhanced_features_used': brd_result.get('enhanced_features', {}),
            'total_generation_time': (
                brd_result.get('metadata', {}).get('generation_time', 0) +
                result.get('frd', {}).get('metadata', {}).get('generation_time', 0)
            )
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enhanced document generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test")
async def test_rag_service():
    """Test RAG service with sample data"""
    try:
        # Sample test data
        test_data = {
            'project': 'RAG Test Project',
            'inputs': {
                'project_name': 'Test Mutual Fund Platform',
                'description': 'Testing RAG capabilities with mutual fund domain',
                'features': ['portfolio management', 'NAV calculation', 'investor reporting']
            }
        }
        
        logger.info("🧪 Testing RAG service...")
        
        if not RAG_AVAILABLE:
            return {
                'success': False,
                'error': 'Enhanced RAG integration not available',
                'message': '❌ RAG service test failed - dependencies missing'
            }
        
        # Test BRD generation
        brd_result = generate_enhanced_brd(
            test_data['project'], 
            test_data['inputs']
        )
        
        # Get service status
        status = get_rag_service_status()
        
        # Test knowledge search if available
        search_result = None
        if status['agentic_rag_available']:
            search_result = search_rag_knowledge_base(
                "mutual fund portfolio management best practices",
                "mutual_funds",
                3
            )
        
        return {
            'success': True,
            'test_results': {
                'brd_generation': {
                    'success': brd_result.get('success', False),
                    'method': brd_result.get('method', 'unknown'),
                    'domain': brd_result.get('metadata', {}).get('domain', 'unknown')
                },
                'knowledge_search': search_result,
                'service_status': status,
                'rag_integration_available': RAG_AVAILABLE
            },
            'message': '🎉 RAG service test completed successfully!'
        }
        
    except Exception as e:
        logger.error(f"RAG service test error: {e}")
        raise HTTPException(status_code=500, detail=f"RAG service test failed: {str(e)}")