# PlantBot Workflow Documentation

## Full Pipeline

```
User → Upload Image → CNN Predict → Diagnosis State → Agent → Response
```

## Step-by-Step

### Step 1: Image Upload
- User selects a leaf image (JPEG/PNG) in the frontend
- Frontend sends `POST /api/predict` with multipart form data

### Step 2: CNN Prediction
- `cnn_service/preprocess.py` resizes and normalises the image
- `cnn_service/predictor.py` runs the model and returns top-5 predictions
- Result: `PredictionResult` with `raw_label`, `confidence`, `status`

### Step 3: Diagnosis State Creation
- `diagnosis/diagnosis_formatter.py` parses the raw label into `plant` + `disease`
- `diagnosis/severity_estimator.py` assigns a severity level
- Result: `DiagnosisState` ready for the agent

### Step 4: Agent Execution
- `agent/planner.py` creates a list of `PlanStep` objects
- `agent/plantbot_agent.py` iterates over the plan and calls each tool
- Tools (leaf_search, disease_search, treatment_search, prevention_search) populate the state

### Step 5: Response Generation
- `agent/response_generator.py` calls the LLM (Gemini/OpenAI)
- Falls back to a template response if no API key is configured
- Result: Markdown-formatted diagnosis + treatment + prevention plan

### Step 6: Storage & Return
- Result saved to the database (DiagnosisRecord)
- JSON response returned to frontend
