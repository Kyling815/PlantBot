"""
Singleton predictor — loads the model once and reuses it.
"""

import torch
from functools import lru_cache

from backend.cnn_service.model_loader import load_model, PlantDiseaseModel
from backend.cnn_service.preprocess import preprocess_image
from backend.cnn_service.schemas import PredictionResult


@lru_cache(maxsize=1)
def _get_model():
    """Lazily load and cache the model on first call."""
    return load_model()


def clean_label(raw_label: str) -> str:
    return raw_label.replace("___", " - ").replace("_", " ")


def predict(image_bytes: bytes) -> PredictionResult:
    """
    Run inference on raw image bytes.

    Returns a PredictionResult with label, confidence, and status.
    """
    model, class_names, device = _get_model()

    tensor = preprocess_image(image_bytes).to(device)

    with torch.no_grad():
        outputs = model(tensor)
        probs = torch.softmax(outputs, dim=1)[0]
        confidence, idx = torch.max(probs, dim=0)

    raw_label = class_names[idx.item()]
    label = clean_label(raw_label)
    confidence_score = round(float(confidence.item()) * 100, 2)
    status = "Healthy" if "healthy" in raw_label.lower() else "Disease detected"

    # Top-5 probabilities
    top5_probs, top5_idxs = torch.topk(probs, k=5)
    top5 = [
        {"label": clean_label(class_names[i.item()]), "confidence": round(float(p.item()) * 100, 2)}
        for p, i in zip(top5_probs, top5_idxs)
    ]

    return PredictionResult(
        raw_label=raw_label,
        label=label,
        confidence=confidence_score,
        status=status,
        top5=top5,
    )
