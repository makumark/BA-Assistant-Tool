"""
Production server for BRD/FRD generation
Properly configured with enhanced AI service
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import sys
import os

# Add app directory to path
app_path = os.path.join(os.path.dirname(__file__), 'app')
sys.path.insert(0, app_path)

# Import our enhanced AI service
from services.ai_service import generate_brd_html, generate_frd_html_from_brd

app = FastAPI(title="Business Analysis API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BRDExpandRequest(BaseModel):
    project: str
    inputs: Dict[str, Any] = {}
    version: int = 1


class FRDRequest(BaseModel):
    project: str
    brd: str
    version: int = 1


@app.get("/")
def root():
    """API health check"""
    return {
        "message": "Business Analysis API is running",
        "version": "1.0.0",
        "endpoints": {
            "BRD Generation": "/ai/expand",
            "FRD Generation": "/frd/generate",
            "Health Check": "/"
        }
    }


@app.post("/ai/expand")
def expand_brd(req: BRDExpandRequest):
    """Generate enhanced BRD using AI service with professional fallback"""
    if not req.project:
        raise HTTPException(status_code=400, detail="Project name required")
    
    try:
        print(f"🤖 Generating BRD for project: {req.project}")
        print(f"📊 Input data: {len(str(req.inputs))} characters")
        
        # Call our enhanced AI service
        html = generate_brd_html(req.project, req.inputs or {}, req.version or 1)
        
        print(f"✅ BRD generated successfully: {len(html)} characters")
        
        return {"html": html}
        
    except Exception as e:
        print(f"❌ Error in BRD generation: {str(e)}")
        # Re-raise the exception so the frontend can handle it properly
        # Our enhanced AI service should have its own fallback, so this shouldn't happen
        raise HTTPException(status_code=500, detail=f"BRD generation failed: {str(e)}")


@app.post("/frd/generate")  
def generate_frd(req: FRDRequest):
    """Generate FRD from BRD content"""
    if not req.project or not req.brd:
        raise HTTPException(status_code=400, detail="project and brd are required")
    
    try:
        print(f"📋 Generating FRD for project: {req.project}")
        print(f"📄 BRD content: {len(req.brd)} characters")
        
        html = generate_frd_html_from_brd(req.project, req.brd, req.version or 1)
        
        print(f"✅ FRD generated successfully: {len(html)} characters")
        
        return {"html": html}
        
    except Exception as e:
        print(f"❌ Error in FRD generation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"FRD generation failed: {str(e)}")


@app.get("/health")
def health_check():
    """Detailed health check"""
    try:
        # Test AI service import
        from services.ai_service import generate_brd_html
        ai_service_status = "✅ Available"
    except Exception as e:
        ai_service_status = f"❌ Error: {str(e)}"
    
    return {
        "status": "healthy",
        "ai_service": ai_service_status,
        "endpoints": {
            "BRD Generation": "/ai/expand",
            "FRD Generation": "/frd/generate"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Business Analysis API Server...")
    print("📋 BRD Generation: Enhanced AI with professional fallback")
    print("📄 FRD Generation: Intelligent parsing and user story generation")
    print("🌐 Server will run on http://localhost:8000")
    print("="*60)
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        reload=False  # Disable reload to avoid path issues
    )