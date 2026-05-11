"""Tests for the CNN predictor."""

import pytest
import io
from PIL import Image
from backend.cnn_service.schemas import PredictionResult


def _make_dummy_image_bytes() -> bytes:
    """Create a small solid-green RGB image as bytes."""
    img = Image.new("RGB", (256, 256), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_predict_returns_result():
    """Predictor should return a PredictionResult for any valid image."""
    from backend.cnn_service.predictor import predict
    result = predict(_make_dummy_image_bytes())
    assert isinstance(result, PredictionResult)
    assert result.raw_label != ""
    assert 0 <= result.confidence <= 100
    assert result.status in ("Healthy", "Disease detected")
    assert len(result.top5) == 5


def test_predict_invalid_image_raises():
    """Predictor should raise ValueError for garbage bytes."""
    from backend.cnn_service.predictor import predict
    with pytest.raises(Exception):
        predict(b"not an image")
