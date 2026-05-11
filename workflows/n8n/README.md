# n8n Workflows

## Available Workflows

| File | Description |
|---|---|
| `plantbot_main_workflow.json` | Full PlantBot pipeline (webhook → CNN → agent → response) |
| `cnn_diagnosis_workflow.json` | Standalone CNN prediction test flow |

## Import Instructions

1. Open n8n at `http://localhost:5678`
2. Click **Workflows** → **Import from file**
3. Select the JSON file
4. Configure the `BACKEND_URL` variable to point to your FastAPI server

## Webhook
The main workflow exposes a webhook at:
```
POST http://localhost:5678/webhook/plantbot
```

Send a `multipart/form-data` request with a `file` field containing the leaf image.
