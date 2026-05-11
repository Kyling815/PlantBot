"""Tests for the treatment_search tool."""

from backend.diagnosis.diagnosis_state import DiagnosisState
from backend.tools.treatment_search import treatment_search


def _make_state(plant: str, disease: str) -> DiagnosisState:
    return DiagnosisState(
        raw_label=f"{plant}___{disease}",
        label=f"{plant} - {disease}",
        confidence=85.0,
        status="Disease detected",
        plant=plant,
        disease=disease,
        is_healthy=False,
    )


def test_treatment_search_fungal():
    state = _make_state("Tomato", "Early blight")
    result = treatment_search(state)
    assert isinstance(result, str)
    assert len(result) > 20


def test_treatment_search_bacterial():
    state = _make_state("Pepper", "Bacterial spot")
    result = treatment_search(state)
    assert isinstance(result, str)
    assert len(result) > 20


def test_treatment_search_viral():
    state = _make_state("Tomato", "Tomato mosaic virus")
    result = treatment_search(state)
    assert isinstance(result, str)
    assert len(result) > 20


def test_treatment_search_unknown_returns_fallback():
    state = _make_state("Mars", "Unknown rot")
    result = treatment_search(state)
    assert "Remove" in result or len(result) > 20
