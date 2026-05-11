"""
FastAPI router for CNN prediction — /api/predict
"""

from fastapi import APIRouter, File, UploadFile, HTTPException

from backend.cnn_service.predictor import predict
from backend.cnn_service.schemas import PredictionResponse

router = APIRouter(tags=["CNN Prediction"])


@router.post("/predict", response_model=PredictionResponse)
async def predict_disease(file: UploadFile = File(...)):
    """
    Accept a leaf image and return the disease prediction.

    - **file**: multipart image upload (JPEG / PNG / WebP)
    """
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image")

    image_bytes = await file.read()

    try:
        result = predict(image_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    return PredictionResponse(success=True, data=result)
