"""End-to-end test for the PlantBot agent pipeline."""

import io
import pytest
from PIL import Image

from backend.cnn_service.schemas import PredictionResult, TopPrediction
from backend.diagnosis.diagnosis_formatter import build_diagnosis_state
from backend.agent.plantbot_agent import PlantBotAgent


def _make_diseased_prediction() -> PredictionResult:
    return PredictionResult(
        raw_label="Tomato___Early_blight",
        label="Tomato - Early blight",
        confidence=92.0,
        status="Disease detected",
        top5=[TopPrediction(label="Tomato - Early blight", confidence=92.0)],
    )


def _make_healthy_prediction() -> PredictionResult:
    return PredictionResult(
        raw_label="Tomato___healthy",
        label="Tomato - healthy",
        confidence=98.0,
        status="Healthy",
        top5=[TopPrediction(label="Tomato - healthy", confidence=98.0)],
    )


def test_agent_runs_on_diseased_plant():
    pred = _make_diseased_prediction()
    state = build_diagnosis_state(pred)
    agent = PlantBotAgent()
    result = agent.run(state)

    assert result.leaf_symptoms is not None
    assert result.disease_info is not None
    assert result.treatment_plan is not None
    assert result.prevention_tips is not None
    assert result.agent_response is not None
    assert len(result.agent_response) > 10


def test_agent_runs_on_healthy_plant():
    pred = _make_healthy_prediction()
    state = build_diagnosis_state(pred)
    agent = PlantBotAgent()
    result = agent.run(state)

    assert result.agent_response is not None
    assert "healthy" in result.agent_response.lower()
