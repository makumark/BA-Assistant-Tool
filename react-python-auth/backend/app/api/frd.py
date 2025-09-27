from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any
import os
import sys

# Add parent directory to Python path for relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_service import generate_frd_html_from_brd

router = APIRouter()


class FRDRequest(BaseModel):
    project: str
    brd: str
    version: int = 1


@router.get("/test")
def test_endpoint():
    """Simple test endpoint to verify the router works"""
    return {"message": "FRD router is working"}


@router.post("/generate")
def generate_frd(req: FRDRequest):
    if not req.project or not req.brd:
        raise HTTPException(status_code=400, detail="project and brd are required")
    
    try:
        html = generate_frd_html_from_brd(req.project, req.brd, req.version or 1)
        return {"html": html}
    except Exception as e:
        print(f"Error generating FRD: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate FRD: {str(e)}")