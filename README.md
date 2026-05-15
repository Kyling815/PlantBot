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

## Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| Python | 3.10+ (recommended 3.11) | Used for the FastAPI backend & CNN inference |
| Node.js | 18+ | Used for the Next.js frontend |
| pip | Latest | Python package manager |
| npm | Bundled with Node.js | Frontend package manager |
| Git | Any | To clone the repository |
| CUDA (optional) | 11.8+ | For GPU-accelerated inference with PyTorch |

You will also need an API key from **one** of the following LLM providers:
- [Google Gemini](https://aistudio.google.com/apikey) (default)
- [OpenAI](https://platform.openai.com/api-keys)

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Kyling815/PlantBot.git
cd PlantBot
```

### 2. Set up the Python environment

Create and activate a virtual environment (recommended):

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

> **Note:** The default `requirements.txt` installs CPU-only PyTorch. If you have an NVIDIA GPU and want faster inference, install the CUDA version of PyTorch instead — see [pytorch.org/get-started](https://pytorch.org/get-started/locally/).

### 3. Configure environment variables

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and fill in your API key:

```dotenv
# Choose your LLM provider: gemini | openai
LLM_PROVIDER=gemini

# Google Gemini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash

# OpenAI (alternative)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

### 4. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

---

## Running the Application

You need **two terminals** — one for the backend and one for the frontend.

### Terminal 1 — Backend (FastAPI)

Run from the **project root** (not from inside `backend/`):

```bash
uvicorn backend.main:app --reload --port 8001
```

The API will be available at **http://localhost:8001**. You can verify it's running by visiting:
- Health check: http://localhost:8001/health
- API docs (Swagger): http://localhost:8001/docs

### Terminal 2 — Frontend (Next.js)

```bash
cd frontend
npm run dev
```

The frontend will be available at **http://localhost:3000**.

> **Tip:** Make sure the `NEXT_PUBLIC_API_URL` in your `.env` matches the backend port you chose (e.g., `http://localhost:8001`).

---

## Testing

Run all tests from the **project root**:

```bash
# Must use python -m to set sys.path correctly
python -m pytest tests/ -v
```

Run a specific test file:

```bash
python -m pytest tests/test_treatment_search.py -v
```
