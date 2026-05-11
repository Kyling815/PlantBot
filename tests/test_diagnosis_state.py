"""Tests for DiagnosisState creation and formatting."""

import pytest
from backend.cnn_service.schemas import PredictionResult, TopPrediction
from backend.diagnosis.diagnosis_formatter import build_diagnosis_state, format_for_agent
from backend.diagnosis.severity_estimator import estimate_severity


def _make_prediction(raw_label: str, confidence: float, status: str) -> PredictionResult:
    return PredictionResult(
        raw_label=raw_label,
        label=raw_label.replace("___", " - ").replace("_", " "),
        confidence=confidence,
        status=status,
        top5=[TopPrediction(label="test", confidence=confidence)],
    )


def test_healthy_plant_parsed_correctly():
    pred = _make_prediction("Tomato___healthy", 95.0, "Healthy")
    state = build_diagnosis_state(pred)
    assert state.plant == "Tomato"
    assert state.disease == "healthy"
    assert state.is_healthy is True
    assert state.severity == "healthy"


def test_diseased_plant_parsed_correctly():
    pred = _make_prediction("Tomato___Early_blight", 92.0, "Disease detected")
    state = build_diagnosis_state(pred)
    assert state.plant == "Tomato"
    assert "blight" in state.disease.lower()
    assert state.is_healthy is False
    assert state.severity == "severe"


def test_format_for_agent_healthy():
    pred = _make_prediction("Apple___healthy", 98.0, "Healthy")
    state = build_diagnosis_state(pred)
    text = format_for_agent(state)
    assert "healthy" in text.lower()


def test_severity_thresholds():
    assert estimate_severity(95.0, False) == "severe"
    assert estimate_severity(80.0, False) == "moderate"
    assert estimate_severity(50.0, False) == "mild"
    assert estimate_severity(99.0, True) == "healthy"
