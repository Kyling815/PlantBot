# PlantBot TODO

## Phase 1 — Foundation ✅
- [x] Project structure scaffold
- [x] CNN model trained (98% accuracy)
- [x] Inference API (`plant_disease/inference_api.py`)

## Phase 2 — Backend
- [ ] `backend/cnn_service/` — Model loader, preprocessor, predictor, routes
- [ ] `backend/diagnosis/` — Diagnosis state, formatter, severity estimator
- [ ] `backend/agent/` — PlantBot agent, planner, response generator
- [ ] `backend/tools/` — LeafSearch, DiseaseSearch, TreatmentSearch, PreventionSearch
- [ ] `backend/knowledge_base/` — Disease profiles, treatment & prevention guides
- [ ] `backend/database/` — SQLAlchemy models and schema
- [ ] `backend/main.py` — FastAPI app wiring

## Phase 3 — Frontend
- [ ] Next.js project setup
- [ ] ImageUploader component
- [ ] DiagnosisCard component
- [ ] ChatBox component
- [ ] TreatmentPlan component
- [ ] PreventionGuide component

## Phase 4 — Integration
- [ ] n8n workflows
- [ ] End-to-end testing

## Phase 5 — Documentation
- [ ] Architecture docs
- [ ] API documentation
- [ ] Deployment guide
