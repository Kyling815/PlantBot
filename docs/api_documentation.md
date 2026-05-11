# PlantBot API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### `GET /`
Health check.

**Response:**
```json
{"message": "PlantBot API is running 🌿"}
```

---

### `GET /health`
System status.

**Response:**
```json
{"status": "ok"}
```

---

### `POST /api/predict`
Upload a leaf image and receive a disease prediction.

**Request:** `multipart/form-data`
| Field | Type | Description |
|---|---|---|
| file | File | Leaf image (JPEG, PNG, WebP) |

**Response:**
```json
{
  "success": true,
  "data": {
    "raw_label": "Tomato___Early_blight",
    "label": "Tomato - Early blight",
    "confidence": 94.32,
    "status": "Disease detected",
    "top5": [
      {"label": "Tomato - Early blight", "confidence": 94.32},
      {"label": "Tomato - Target Spot", "confidence": 3.12},
      ...
    ]
  }
}
```

**Error Responses:**
| Code | Reason |
|---|---|
| 400 | Not an image file |
| 422 | Image could not be decoded |
| 500 | Model inference failure |

---

## Models

### PredictionResult
```typescript
{
  raw_label: string;        // e.g. "Tomato___Early_blight"
  label: string;            // e.g. "Tomato - Early blight"
  confidence: number;       // 0–100 (percentage)
  status: "Healthy" | "Disease detected";
  top5: Array<{ label: string; confidence: number }>;
}
```
