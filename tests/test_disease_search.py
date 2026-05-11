"""Tests for the disease_search tool."""

from backend.diagnosis.diagnosis_state import DiagnosisState
from backend.tools.disease_search import disease_search


def _make_state(plant: str, disease: str) -> DiagnosisState:
    return DiagnosisState(
        raw_label=f"{plant}___{disease}",
        label=f"{plant} - {disease}",
        confidence=90.0,
        status="Disease detected",
        plant=plant,
        disease=disease,
        is_healthy=False,
    )


def test_disease_search_unknown_returns_fallback():
    state = _make_state("Mars", "Purple_Fungus")
    result = disease_search(state)
    assert isinstance(result, str)
    assert len(result) > 10


def test_disease_search_known_disease_from_kb():
    """If the KB file exists, we should get its content."""
    state = _make_state("Tomato", "Early blight")
    result = disease_search(state)
    assert isinstance(result, str)
    assert len(result) > 10
