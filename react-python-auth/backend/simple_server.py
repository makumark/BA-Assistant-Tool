"""
Simple standalone FastAPI server for testing FRD generation
Bypasses import path issues by being self-contained
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sys
import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(env_path, override=True)  # Force override existing env vars
    print(f"✅ Loaded .env from: {env_path}")
    
    # Check if API key is loaded (OpenAI or Perplexity)
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ API key loaded: {api_key[:10]}...{api_key[-5:]}")
        if api_key.startswith("sk-"):
            print("✅ Valid OpenAI API key format detected")
        elif api_key.startswith("pplx-"):
            print("✅ Valid Perplexity API key format detected")
        else:
            print("❓ Unknown API key format")
    else:
        print("❌ API key not found in environment")
except ImportError:
    print("❌ python-dotenv not available, using system environment variables")
except Exception as e:
    print(f"❌ Error loading .env: {e}")

# Add the app directory to Python path
app_dir = os.path.join(os.path.dirname(__file__), 'app')
sys.path.insert(0, app_dir)

# Now import the AI service
try:
    from services.ai_service import generate_frd_html_from_brd, generate_brd_html, prioritize_frd_requirements
    from services.wireframe_service import generate_wireframe_from_frd, generate_wireframe_from_user_stories
    from services.prototype_service import generate_prototype_from_frd, generate_prototype_from_user_stories
    print("✅ AI service imported successfully (with Agentic RAG support)")
    print("✅ Wireframe service imported successfully")
    print("✅ Prototype service imported successfully")
except Exception as e:
    print(f"❌ Failed to import AI service: {e}")
    generate_frd_html_from_brd = None
    generate_brd_html = None
    prioritize_frd_requirements = None
    generate_wireframe_from_frd = None
    generate_prototype_from_frd = None
    generate_prototype_from_user_stories = None
    generate_wireframe_from_user_stories = None

app = FastAPI(title="Simple FRD Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FRDRequest(BaseModel):
    project: str
    brd: str
    version: int = 1

class ExpandRequest(BaseModel):
    project: str
    inputs: dict = {}
    version: int = 1

class PrioritizeRequest(BaseModel):
    project: str
    frd_html: str
    version: int = 1

@app.get("/")
def read_root():
    return {
        "message": "Simple FRD Server is running", 
        "ai_service_available": generate_frd_html_from_brd is not None,
        "prioritization_available": prioritize_frd_requirements is not None,
        "endpoints": {
            "expand_brd": "/ai/expand",
            "generate_frd": "/ai/frd/generate", 
            "prioritize_frd": "/ai/frd/prioritize"
        }
    }

@app.post("/ai/expand")
def expand_brd(req: ExpandRequest):
    print(f"📥 Received expand request: {req.project}")
    print(f"📥 Inputs: {req.inputs}")
    
    if not req.project:
        print("❌ No project name provided")
        raise HTTPException(status_code=400, detail="Project name is required")
    
    if generate_brd_html is None:
        print("❌ AI service not available")
        raise HTTPException(status_code=500, detail="AI service not available")
    
    try:
        print(f"🔄 Generating BRD for project: {req.project}")
        print(f"🔄 Calling generate_brd_html...")
        
        # Wrap in another try-catch to prevent server crashes
        try:
            html = generate_brd_html(req.project, req.inputs or {}, req.version or 1)
            print(f"✅ Generated BRD with {len(html)} characters")
            
            # Check if it's using enhanced fallback (good) vs basic fallback (error)
            if "enhanced fallback" in html:
                print("✅ Using enhanced domain-specific fallback")
            elif "AI expansion failed" in html:
                print("❌ Using basic error fallback")
            else:
                print("✅ Generated with AI enhancement")
                
            return {"html": html}
            
        except Exception as inner_e:
            print(f"❌ Inner AI service error: {inner_e}")
            # If AI service completely fails, return a basic fallback
            basic_fallback = f"""
            <h1>Business Requirements Document (BRD)</h1>
            <h2>{req.project} — Version {req.version}</h2>
            <p><strong>Note:</strong> AI service temporarily unavailable — saved basic BRD</p>
            <h3>Executive Summary</h3>
            <p>This document outlines the business requirements for {req.project}.</p>
            <h3>Business Requirements</h3>
            <p>Core business functionality and essential system capabilities.</p>
            """
            return {"html": basic_fallback}
            
    except Exception as e:
        print(f"❌ Outer error generating BRD: {e}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        # Return a simple fallback BRD
        fallback_html = f"""
        <h1>Business Requirements Document (BRD)</h1>
        <h2>{req.project} — Version {req.version}</h2>
        <p>Error occurred during AI generation: {str(e)}</p>
        <p><strong>Note:</strong> AI expansion failed — saved basic BRD</p>
        <h3>Executive Summary</h3>
        <p>This document outlines the business requirements for {req.project}.</p>
        <h3>Business Requirements</h3>
        <p>Core business functionality and essential system capabilities.</p>
        """
        return {"html": fallback_html}

@app.get("/ai/frd/test")
def test_frd():
    return {"message": "FRD endpoint is working", "ai_service_available": generate_frd_html_from_brd is not None}

@app.post("/ai/frd")
def generate_frd_simple(req: FRDRequest):
    """Main FRD endpoint that frontend calls"""
    if not req.project or not req.brd:
        raise HTTPException(status_code=400, detail="project and brd are required")
    
    if generate_frd_html_from_brd is None:
        raise HTTPException(status_code=500, detail="AI service not available")
    
    try:
        print(f"🔄 Generating FRD for project: {req.project}")
        html = generate_frd_html_from_brd(req.project, req.brd, req.version or 1)
        print(f"✅ Generated FRD with {len(html)} characters")
        return {"html": html}
    except Exception as e:
        print(f"❌ Error generating FRD: {e}")
        # For debugging, return a simple fallback
        fallback_html = f"""
        <h1>FRD for {req.project}</h1>
        <p>Error occurred during generation: {str(e)}</p>
        <p>BRD Content: {req.brd[:200]}...</p>
        <h2>Fallback User Stories</h2>
        <p>User Story 1: As a user, I want to test the FRD generation functionality.</p>
        <p>User Story 2: As a developer, I want to see error messages when generation fails.</p>
        """
        return {"html": fallback_html}

@app.post("/ai/frd/prioritize")
def prioritize_frd(req: PrioritizeRequest):
    """Prioritize FRD requirements using MoSCoW methodology"""
    print(f"📥 Received prioritization request: {req.project}")
    
    if not req.project or not req.frd_html:
        print("❌ Missing required fields: project and frd_html")
        raise HTTPException(status_code=400, detail="Project name and FRD HTML are required")
    
    if prioritize_frd_requirements is None:
        print("❌ Prioritization service not available")
        raise HTTPException(status_code=500, detail="Prioritization service not available")
    
    try:
        print(f"🔄 Prioritizing requirements for project: {req.project}")
        print(f"🔄 FRD HTML length: {len(req.frd_html)} characters")
        
        prioritization_result = prioritize_frd_requirements(req.project, req.frd_html, req.version or 1)
        
        print(f"✅ Prioritization completed:")
        print(f"   Domain: {prioritization_result['domain']}")
        print(f"   Total Requirements: {prioritization_result['total_requirements']}")
        print(f"   MoSCoW Distribution: {prioritization_result['moscow_distribution']['counts']}")
        
        return prioritization_result
        
    except Exception as e:
        print(f"❌ Error during prioritization: {e}")
        import traceback
        traceback.print_exc()
        
        # Return fallback prioritization
        fallback_result = {
            "project": req.project,
            "domain": "general",
            "version": req.version or 1,
            "total_requirements": 0,
            "moscow_distribution": {
                "counts": {"Must Have": 0, "Should Have": 0, "Could Have": 0, "Won't Have (this time)": 0},
                "percentages": {"Must Have": 0, "Should Have": 0, "Could Have": 0, "Won't Have (this time)": 0},
                "total_requirements": 0
            },
            "prioritized_requirements": [],
            "dependencies": {"dependency_graph": {}, "critical_path": [], "total_dependencies": 0, "isolated_requirements": []},
            "report_html": f"<h1>Prioritization Error</h1><p>Error occurred: {str(e)}</p>",
            "error": str(e)
        }
        return fallback_result

@app.post("/ai/frd/generate")
def generate_frd(req: FRDRequest):
    if not req.project or not req.brd:
        raise HTTPException(status_code=400, detail="project and brd are required")
    
    if generate_frd_html_from_brd is None:
        raise HTTPException(status_code=500, detail="AI service not available")
    
    try:
        print(f"🔄 Generating FRD for project: {req.project}")
        html = generate_frd_html_from_brd(req.project, req.brd, req.version or 1)
        print(f"✅ Generated FRD with {len(html)} characters")
        return {"html": html}
    except Exception as e:
        print(f"❌ Error generating FRD: {e}")
        # For debugging, return a simple fallback
        fallback_html = f"""
        <h1>FRD for {req.project}</h1>
        <p>Error occurred during generation: {str(e)}</p>
        <p>BRD Content: {req.brd[:200]}...</p>
        <h2>Fallback User Stories</h2>
        <p>User Story 1: As a user, I want to test the FRD generation functionality.</p>
        <p>User Story 2: As a developer, I want to see error messages when generation fails.</p>
        """
        return {"html": fallback_html}

# Wireframe generation models
class WireframeRequest(BaseModel):
    project: str
    frd_content: str = None  # FRD content to extract user stories from
    user_stories: list = None  # Direct user stories list
    domain: str = "generic"
    version: int = 1

@app.post("/ai/wireframes")
def generate_wireframes(req: WireframeRequest):
    """Generate wireframes from FRD content or user stories"""
    if not req.project:
        raise HTTPException(status_code=400, detail="project name is required")
    
    if not req.frd_content and not req.user_stories:
        raise HTTPException(status_code=400, detail="Either frd_content or user_stories is required")
    
    if generate_wireframe_from_frd is None or generate_wireframe_from_user_stories is None:
        raise HTTPException(status_code=500, detail="Wireframe service not available")
    
    try:
        print(f"🎨 Generating wireframes for project: {req.project}")
        print(f"🎨 Domain: {req.domain}")
        
        if req.frd_content:
            # Generate from FRD content
            print(f"🔄 Extracting user stories from FRD content ({len(req.frd_content)} chars)")
            html = generate_wireframe_from_frd(req.project, req.frd_content, req.domain)
        else:
            # Generate from user stories directly
            print(f"🔄 Generating from {len(req.user_stories)} user stories")
            html = generate_wireframe_from_user_stories(req.project, req.user_stories, req.domain)
        
        print(f"✅ Generated wireframes with {len(html)} characters")
        return {"html": html, "domain": req.domain}
        
    except Exception as e:
        print(f"❌ Error generating wireframes: {e}")
        import traceback
        traceback.print_exc()
        
        # Return fallback wireframe
        fallback_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Wireframes: {req.project}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .error {{ background: #fee; border: 1px solid #fcc; padding: 20px; border-radius: 8px; }}
                .wireframe {{ border: 2px dashed #ccc; margin: 20px 0; padding: 20px; }}
            </style>
        </head>
        <body>
            <h1>🎨 Wireframes for {req.project}</h1>
            <div class="error">
                <h3>⚠️ Generation Error</h3>
                <p>Error occurred during wireframe generation: {str(e)}</p>
            </div>
            <div class="wireframe">
                <h3>📱 Login Page</h3>
                <div style="border: 1px solid #ddd; padding: 10px; margin: 10px 0;">
                    [Logo] <br>
                    [Username Field] <br>
                    [Password Field] <br>
                    [Login Button]
                </div>
            </div>
            <div class="wireframe">
                <h3>📊 Dashboard</h3>
                <div style="border: 1px solid #ddd; padding: 10px; margin: 10px 0;">
                    [Navigation Bar] <br>
                    [Key Metrics] <br>
                    [Charts and Graphs] <br>
                    [Quick Actions]
                </div>
            </div>
        </body>
        </html>
        """
        return {"html": fallback_html}

# Prototype Request Model
class PrototypeRequest(BaseModel):
    project: str
    frd_content: str = None
    user_stories: List[dict] = None
    domain: str = "generic"

@app.post("/ai/prototype")
def generate_prototype(req: PrototypeRequest):
    """Generate interactive prototype from FRD content or user stories"""
    if not req.project:
        raise HTTPException(status_code=400, detail="project name is required")
    
    if not req.frd_content and not req.user_stories:
        raise HTTPException(status_code=400, detail="Either frd_content or user_stories is required")
    
    if generate_prototype_from_frd is None or generate_prototype_from_user_stories is None:
        raise HTTPException(status_code=500, detail="Prototype service not available")
    
    try:
        print(f"🎯 Generating interactive prototype for project: {req.project}")
        print(f"🎯 Domain: {req.domain}")
        
        if req.frd_content:
            # Generate from FRD content
            print(f"🔄 Extracting user stories from FRD content ({len(req.frd_content)} chars)")
            html = generate_prototype_from_frd(req.project, req.frd_content, req.domain)
        else:
            # Generate from user stories directly
            print(f"🔄 Generating from {len(req.user_stories)} user stories")
            html = generate_prototype_from_user_stories(req.project, req.user_stories, req.domain)
        
        print(f"✅ Generated interactive prototype with {len(html)} characters")
        return {"html": html, "domain": req.domain}
        
    except Exception as e:
        print(f"❌ Error generating prototype: {e}")
        import traceback
        traceback.print_exc()
        
        # Return fallback prototype
        fallback_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Prototype: {req.project}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f8fafc; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
                .error {{ background: #fee; border: 1px solid #fcc; padding: 15px; border-radius: 4px; margin-bottom: 20px; }}
                .page {{ border: 1px solid #ddd; margin: 20px 0; padding: 15px; border-radius: 4px; }}
                .btn {{ background: #4299e1; color: white; padding: 8px 16px; border: none; border-radius: 4px; margin-right: 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎯 Interactive Prototype: {req.project}</h1>
                <div class="error">
                    <strong>⚠️ Generation Error:</strong> {str(e)}<br>
                    <small>Showing fallback prototype structure</small>
                </div>
                
                <div class="page">
                    <h3>🔐 Login Page</h3>
                    <input type="email" placeholder="Email" style="width: 200px; padding: 8px; margin: 5px;">
                    <input type="password" placeholder="Password" style="width: 200px; padding: 8px; margin: 5px;">
                    <button class="btn">Sign In</button>
                </div>
                
                <div class="page">
                    <h3>📊 Dashboard</h3>
                    <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                        <div style="background: #4299e1; color: white; padding: 15px; border-radius: 4px; flex: 1; text-align: center;">
                            <div style="font-size: 24px; font-weight: bold;">1,234</div>
                            <div>Total Items</div>
                        </div>
                        <div style="background: #48bb78; color: white; padding: 15px; border-radius: 4px; flex: 1; text-align: center;">
                            <div style="font-size: 24px; font-weight: bold;">89%</div>
                            <div>Success Rate</div>
                        </div>
                    </div>
                    <button class="btn">View Reports</button>
                    <button class="btn">Add New</button>
                </div>
            </div>
        </body>
        </html>
        """
        return {"html": fallback_html}

# Project and Document Management Endpoints
class ProjectRequest(BaseModel):
    name: str
    description: str = ""

class DocumentRequest(BaseModel):
    project_name: str
    doc_type: str
    content: str
    version: int = 1
    approved: bool = False

@app.get("/api/projects")
def get_projects():
    """Get all projects"""
    try:
        # This would typically read from a database
        # For now, return sample data
        projects = {
            "Ecommerce": {
                "name": "Ecommerce",
                "description": "E-commerce platform development",
                "documents": []
            },
            "Banking": {
                "name": "Banking", 
                "description": "Banking system modernization",
                "documents": []
            }
        }
        return {"projects": projects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving projects: {str(e)}")

@app.post("/api/projects")
def create_project(req: ProjectRequest):
    """Create a new project"""
    try:
        # This would typically save to a database
        print(f"📁 Creating project: {req.name}")
        return {"message": f"Project '{req.name}' created successfully", "project": {"name": req.name, "description": req.description}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating project: {str(e)}")

@app.get("/api/projects/{project_name}/documents")
def get_project_documents(project_name: str):
    """Get all documents for a specific project"""
    try:
        # This would typically read from a database
        print(f"📄 Getting documents for project: {project_name}")
        
        # Sample documents for demonstration
        sample_documents = [
            {
                "id": f"BRD_{project_name}_1",
                "type": "BRD",
                "version": 1,
                "content": f"<h1>Business Requirements Document V1 - {project_name}</h1><p>Sample BRD content...</p>",
                "approved": True,
                "created_at": "2025-09-25T10:00:00Z"
            },
            {
                "id": f"BRD_{project_name}_2", 
                "type": "BRD",
                "version": 2,
                "content": f"<h1>Business Requirements Document V2 - {project_name}</h1><p>Updated BRD content...</p>",
                "approved": True,
                "created_at": "2025-09-25T14:00:00Z"
            },
            {
                "id": f"FRD_{project_name}_1",
                "type": "FRD",
                "version": 1,
                "content": f"<h1>Functional Requirements Document V1 - {project_name}</h1><p>Sample FRD content...</p>",
                "approved": True,
                "created_at": "2025-09-25T16:00:00Z"
            }
        ]
        
        return {"documents": sample_documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving documents: {str(e)}")

@app.post("/api/projects/{project_name}/documents")
def create_document(project_name: str, req: DocumentRequest):
    """Create a new document for a project"""
    try:
        print(f"📝 Creating {req.doc_type} document for project: {project_name}")
        
        document = {
            "id": f"{req.doc_type}_{project_name}_{req.version}",
            "type": req.doc_type,
            "version": req.version,
            "content": req.content,
            "approved": req.approved,
            "created_at": "2025-09-26T00:00:00Z"
        }
        
        return {"message": f"{req.doc_type} document created successfully", "document": document}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating document: {str(e)}")

@app.put("/api/projects/{project_name}/documents/{document_id}/approve")
def approve_document(project_name: str, document_id: str):
    """Approve a document"""
    try:
        print(f"✅ Approving document {document_id} for project: {project_name}")
        return {"message": f"Document {document_id} approved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error approving document: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Simple FRD Server...")
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)