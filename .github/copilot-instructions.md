# AI Agent Instructions for BA Tool Project

## Project Overview

This is a **Business Analysis (BA) Assistant Tool** - a React + Python application that generates Business Requirements Documents (BRDs) and Functional Requirements Documents (FRDs) using AI enhancement. The project consists of two main directories with different architectural approaches.

## Architecture & Key Components

### Multi-Project Structure
- `react-python-auth/` - Main BA Tool application (React frontend + FastAPI backend)
- `react-python-auth-backend/` - Alternative backend implementation with different auth patterns

### Main Application (`react-python-auth/`)

**Backend (`backend/app/`):**
- **Entry Points**: `main.py` (full FastAPI app) and `simple_server.py` (standalone server)
- **API Structure**: RESTful APIs with `/api/v1/auth`, `/ai`, and `/ai/frd` endpoints
- **Core Services**: 
  - `ai_service.py` - BRD/FRD generation with OpenAI integration + intelligent fallbacks
  - `ai_service_enhanced.py` - Enhanced AI processing with domain-specific logic
- **Data Management**: JSON file-based storage (`data/users.json`)

**Frontend (`frontend/src/`):**
- **React SPA** with routing via React Router
- **Key Pages**: `FRDPage.jsx` (main BRD/FRD interface), `Login.js`
- **Components**: `AuthForm.js`, `FRDEditor.jsx`
- **State Management**: Local component state + axios for API calls

## Critical Business Logic Patterns

### AI-Enhanced Document Generation
The system uses a **dual-strategy approach** for document generation:

1. **Primary**: OpenAI API calls with sophisticated prompts
2. **Fallback**: Local template-based generation when AI fails

**Key Pattern in `ai_service.py`:**
```python
# Always try AI first, then fallback
html = _call_openai_chat(messages, model, temperature, max_tokens)
if html and "<" in html and "EPIC" in html:
    return html
return _generate_enhanced_brd_fallback(project, inputs, version)
```

### EPIC-Based Requirements Structure
- **BRDs**: Organized into EPICs (EPIC-01, EPIC-02, etc.)
- **FRDs**: Convert EPICs to User Stories with acceptance criteria
- **Filtering Logic**: Excludes budget details, out-of-scope items from EPIC generation

### Domain-Specific Intelligence
The AI service detects business domains (Healthcare, E-commerce, Banking, etc.) and applies:
- Domain-specific terminology and abbreviation expansion
- Contextual stakeholder mapping
- Industry-appropriate validation rules

## Development Workflows

### Starting Servers
**Backend**: 
```bash
cd backend
python simple_server.py  # Runs on :8001 (standalone)
# OR
python -m uvicorn app.main:app --reload  # Runs on :8000 (full app)
```

**Frontend**:
```bash
cd frontend
npm start  # Runs on :3000
```

### Testing Patterns
- **Backend Tests**: Extensive test files (`test_*.py`) for different scenarios
- **API Testing**: Direct FastAPI endpoint testing
- **Integration Testing**: BRD → FRD generation workflows

### Configuration
- **Environment**: `.env` files for API keys (OPENAI_API_KEY)
- **CORS**: Configured for localhost:3000 ↔ backend communication
- **Docker**: `docker-compose.yml` available for containerized deployment

## AI Agent Guidelines

### When Working with Document Generation
1. **Understand the Flow**: User Input → BRD (EPICs) → FRD (User Stories)
2. **Test Both Paths**: AI enhancement AND fallback generation
3. **Domain Context**: Always consider the business domain for appropriate terminology
4. **EPIC Filtering**: Exclude budget/cost details when creating functional EPICs

### Common Development Tasks
- **API Changes**: Modify router files (`api/*.py`), test with `simple_server.py`
- **Frontend Updates**: Focus on `FRDPage.jsx` for main business logic
- **AI Enhancement**: Work with prompts in `ai_service.py`, test fallback scenarios

### Key Files for Understanding
- `backend/app/services/ai_service.py` - Core business logic
- `frontend/src/pages/FRDPage.jsx` - Main user interface
- `backend/simple_server.py` - Simplified testing server
- `backend/app/main.py` - Full application entry point

### Environment Setup
- **Python Dependencies**: Install from `requirements.txt`
- **Node Dependencies**: `npm install` in frontend directory
- **OpenAI**: Set `OPENAI_API_KEY` environment variable for AI features

### Testing Strategy
- Use `simple_server.py` for isolated backend testing
- Test document generation with various business domains
- Verify both AI-enhanced and fallback generation paths
- Check CORS and API endpoint connectivity

## Domain-Specific Features

The application has sophisticated domain detection and handles:
- **Healthcare**: HIPAA compliance, patient terminology
- **E-commerce**: Product catalogs, order management
- **Banking**: Regulatory compliance, transaction processing
- **CRM**: Lead management, sales pipelines

When modifying AI prompts or business logic, consider these domain-specific requirements and terminology.