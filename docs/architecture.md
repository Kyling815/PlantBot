# PlantBot System Architecture

## Overview

PlantBot is a two-stage AI system:
1. **Stage 1 — Vision**: A CNN model classifies leaf images into one of 38 disease/healthy classes.
2. **Stage 2 — Reasoning**: An LLM agent takes the CNN diagnosis and produces a full treatment & prevention plan.

## Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                      Frontend (Next.js)                  │
│   ImageUploader → DiagnosisCard → ChatBox               │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP POST /api/predict
┌──────────────────────▼──────────────────────────────────┐
│                   FastAPI Backend                        │
│                                                          │
│  ┌─────────────┐    ┌──────────────┐    ┌───────────┐   │
│  │ CNN Service │───▶│  Diagnosis   │───▶│   Agent   │   │
│  │  /predict   │    │  Formatter   │    │ (LLM loop)│   │
│  └─────────────┘    └──────────────┘    └─────┬─────┘   │
│         │                                      │         │
│  ┌──────▼──────┐                     ┌─────────▼──────┐  │
│  │  PyTorch    │                     │    Tools        │  │
│  │  CNN Model  │                     │ ├ leaf_search   │  │
│  │  (98% acc.) │                     │ ├ disease_search│  │
│  └─────────────┘                     │ ├ treatment_src │  │
│                                      │ └ prevention_src│  │
│                                      └────────┬────────┘  │
│                                               │           │
│                                      ┌────────▼────────┐  │
│                                      │ Knowledge Base  │  │
│                                      │ (Markdown files)│  │
│                                      └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

1. User uploads a leaf image via the frontend
2. `POST /api/predict` receives the image
3. `cnn_service/predictor.py` runs inference → returns `PredictionResult`
4. `diagnosis/diagnosis_formatter.py` converts it to a `DiagnosisState`
5. `agent/plantbot_agent.py` builds a plan and calls tools
6. Tools query `knowledge_base/` for domain-specific information
7. `agent/response_generator.py` synthesises the final answer (via LLM or template)
8. The enriched `DiagnosisState` is saved to the database
9. The response is returned to the frontend

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14, TypeScript |
| API | FastAPI, Python 3.10+ |
| ML Model | PyTorch CNN (custom architecture) |
| LLM | Google Gemini 1.5 Flash / OpenAI GPT-4o-mini |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Orchestration | n8n workflows |
