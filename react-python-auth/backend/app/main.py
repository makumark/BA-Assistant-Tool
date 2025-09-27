from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.auth import router as auth_router

try:
    from api.ai import router as ai_router
    _has_ai = True
except Exception:
    ai_router = None
    _has_ai = False

try:
    from api.frd import router as frd_router
    _has_frd = True
except Exception:
    frd_router = None
    _has_frd = False

try:
    from api.rag_routes import router as rag_router
    _has_rag = True
except Exception as e:
    rag_router = None
    _has_rag = False
    logging.warning(f"RAG router not available: {e}")

app = FastAPI(title="BA Assistant Backend")
logger = logging.getLogger("uvicorn.error")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    logger.info("BA Assistant Backend starting")


@app.get("/", tags=["root"])
def read_root():
    return {"message": "BA Assistant Backend is running."}


app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

if _has_ai and ai_router is not None:
    app.include_router(ai_router, prefix="/ai", tags=["ai"])
else:
    logger.info("/ai endpoints disabled (ai router missing).")

if _has_frd and frd_router is not None:
    app.include_router(frd_router, prefix="/ai/frd", tags=["frd"])
else:
    logger.info("/ai/frd endpoints disabled (frd router missing).")

if _has_rag and rag_router is not None:
    app.include_router(rag_router, prefix="/rag", tags=["rag"])
    logger.info("✅ RAG endpoints enabled at /rag")
else:
    logger.info("⚠️  /rag endpoints disabled (rag router missing).")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)