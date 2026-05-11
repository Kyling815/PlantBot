# n8n Workflow Documentation

## Overview

n8n is used to orchestrate the PlantBot pipeline in a visual, no-code-friendly way.

## Workflows

### `plantbot_main_workflow.json`
Main orchestration flow:
1. **Webhook Trigger** — Receives image upload from frontend
2. **HTTP Request** — Calls `POST /api/predict` on the FastAPI backend
3. **IF Node** — Checks if disease detected
4. **Agent Execution** — Triggers agent sub-workflow
5. **Respond to Webhook** — Returns final response to frontend

### `cnn_diagnosis_workflow.json`
Isolated CNN prediction flow for testing:
1. **Manual Trigger** — Start manually with a test image
2. **HTTP Request** — `POST /api/predict`
3. **Set Node** — Formats the response
4. **Debug Output** — Logs the result

## Setup

1. Install n8n: `npm install -g n8n`
2. Start n8n: `n8n start`
3. Import workflows from `workflows/n8n/*.json`
4. Configure credentials: Set `BACKEND_URL` in n8n environment

## Webhook URL
```
http://localhost:5678/webhook/plantbot
```
