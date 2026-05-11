# 🌿 PlantBot — AI Plant Disease Assistant

PlantBot is an image-first plant disease assistant. Upload a leaf photo, and PlantBot's CNN model identifies the disease, then an LLM-powered agent provides treatment and prevention advice.

## Architecture

```
User uploads leaf image
        ↓
CNN Service (PyTorch) → Disease prediction
        ↓
Diagnosis State → Structured diagnosis
        ↓
PlantBot Agent (LLM) → Searches knowledge base
        ↓
Response: Diagnosis + Treatment + Prevention
```

## Modules

| Module | Description |
|--------|-------------|
| `plant_disease/` | Trained CNN model, class labels, training & inference |
| `backend/cnn_service/` | FastAPI routes for model loading & prediction |
| `backend/diagnosis/` | Converts CNN predictions to structured states |
| `backend/agent/` | LLM reasoning agent (TravelPlanner-inspired) |
| `backend/tools/` | LeafSearch, DiseaseSearch, TreatmentSearch, PreventionSearch |
| `backend/knowledge_base/` | Disease profiles, treatment & prevention guides |
| `frontend/` | Next.js UI for image upload and chat |
| `workflows/n8n/` | n8n orchestration workflows |

## Quick Start

```bash
# Install Python dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env

# Start backend (run from project root, NOT from inside backend/)
uvicorn backend.main:app --reload --port 8001

# Start frontend
cd frontend
npm install
npm run dev
```

## Testing

```powershell
# Run all tests (must use python -m to set sys.path correctly)
python -m pytest tests/ -v
```

## Requirements

- Python 3.10+
- Node.js 18+
- PyTorch (with CUDA optional)
- Google Gemini API key (or OpenAI)
