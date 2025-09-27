"""
Simple FastAPI Test Server for RAG Testing
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
import sys
import os

# Add paths for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

app = FastAPI(title="BA Tool Enhanced RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import enhanced RAG integration
try:
    from app.services.enhanced_rag_integration import (
        enhanced_rag_integration,
        generate_enhanced_brd,
        generate_enhanced_frd,
        get_rag_service_status,
        search_rag_knowledge_base
    )
    RAG_AVAILABLE = True
    logging.info("✅ Enhanced RAG Integration loaded successfully")
except ImportError as e:
    RAG_AVAILABLE = False
    logging.error(f"❌ Enhanced RAG Integration not available: {e}")

# Pydantic models
class BRDRequest(BaseModel):
    project: str = "Untitled Project"
    inputs: Dict[str, Any]
    version: int = 1

class FRDRequest(BaseModel):
    project: str = "Untitled Project"
    inputs: Dict[str, Any]
    brd_content: Optional[str] = None
    version: int = 1

class SearchRequest(BaseModel):
    query: str
    domain: Optional[str] = None
    k: int = 5

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "BA Tool Enhanced RAG API is running",
        "rag_available": RAG_AVAILABLE,
        "endpoints": [
            "/rag/status",
            "/rag/test", 
            "/rag/generate/brd",
            "/rag/generate/frd",
            "/rag/search"
        ]
    }

@app.get("/rag/status")
async def get_rag_status():
    """Get RAG service status"""
    if not RAG_AVAILABLE:
        return {
            'success': False,
            'error': 'Enhanced RAG integration not available',
            'status': {
                'agentic_rag_available': False,
                'traditional_ai_available': False,
                'vector_db_available': False
            }
        }
    
    try:
        status = get_rag_service_status()
        return {'success': True, 'status': status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rag/generate/brd")
async def generate_brd_enhanced(request: BRDRequest):
    """Generate BRD using enhanced RAG"""
    if not RAG_AVAILABLE:
        raise HTTPException(status_code=503, detail="RAG service not available")
    
    try:
        result = generate_enhanced_brd(request.project, request.inputs, request.version)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rag/generate/frd")
async def generate_frd_enhanced(request: FRDRequest):
    """Generate FRD using enhanced RAG"""
    if not RAG_AVAILABLE:
        raise HTTPException(status_code=503, detail="RAG service not available")
    
    try:
        result = generate_enhanced_frd(
            request.project, 
            request.inputs, 
            request.brd_content, 
            request.version
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rag/search")
async def search_knowledge(request: SearchRequest):
    """Search RAG knowledge base"""
    if not RAG_AVAILABLE:
        raise HTTPException(status_code=503, detail="RAG service not available")
    
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        result = search_rag_knowledge_base(request.query, request.domain, request.k)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/rag/test")
async def test_rag():
    """Test RAG service"""
    if not RAG_AVAILABLE:
        return {
            'success': False,
            'error': 'RAG service not available',
            'message': '❌ RAG service test failed - dependencies missing'
        }
    
    try:
        # Test data
        test_inputs = {
            'project_name': 'Test Mutual Fund Platform',
            'description': 'Testing RAG capabilities',
            'features': ['portfolio management', 'NAV calculation']
        }
        
        # Test BRD generation
        brd_result = generate_enhanced_brd('RAG Test Project', test_inputs)
        
        # Get status
        status = get_rag_service_status()
        
        # Test knowledge search if available
        search_result = None
        if status['agentic_rag_available']:
            search_result = search_rag_knowledge_base(
                "mutual fund portfolio management",
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
                'service_status': status
            },
            'message': '🎉 RAG service test completed successfully!'
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG test failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("rag_test_server:app", host="0.0.0.0", port=8001, reload=True)