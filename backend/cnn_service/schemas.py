"""
Pydantic schemas for the CNN service.
"""

from pydantic import BaseModel
from typing import List, Optional


class TopPrediction(BaseModel):
    label: str
    confidence: float


class PredictionResult(BaseModel):
    raw_label: str
    label: str
    confidence: float       # percentage, e.g. 97.43
    status: str             # "Healthy" | "Disease detected"
    top5: List[TopPrediction] = []


class PredictionResponse(BaseModel):
    success: bool
    data: Optional[PredictionResult] = None
    error: Optional[str] = None
