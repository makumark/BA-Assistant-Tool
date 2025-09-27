from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
import os
import sys

# Add parent directory to Python path for relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_service import generate_brd_html

router = APIRouter()


class ExpandRequest(BaseModel):
    project: str
    inputs: Dict[str, Any] = {}
    version: int = 1


@router.post("/expand")
def expand(req: ExpandRequest):
    if not req.project:
        raise HTTPException(status_code=400, detail="Project name required")
    html = generate_brd_html(req.project, req.inputs or {}, req.version or 1)
    return {"html": html}