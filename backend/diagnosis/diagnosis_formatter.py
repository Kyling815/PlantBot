"""
Converts a PredictionResult into a DiagnosisState.
Parses plant name and disease name from the raw CNN label.
"""

from backend.cnn_service.schemas import PredictionResult
from backend.diagnosis.diagnosis_state import DiagnosisState
from backend.diagnosis.severity_estimator import estimate_severity


def parse_plant_disease(raw_label: str) -> tuple[str, str]:
    """
    Split 'Tomato___Early_blight' → ('Tomato', 'Early blight').
    Returns ('Unknown', 'Unknown') on parse failure.
    """
    parts = raw_label.split("___")
    if len(parts) == 2:
        plant = parts[0].replace("_", " ").strip()
        disease = parts[1].replace("_", " ").strip()
        return plant, disease
    return "Unknown", "Unknown"


def build_diagnosis_state(prediction: PredictionResult) -> DiagnosisState:
    """
    Given a PredictionResult from the CNN, produce a DiagnosisState
    ready for the PlantBot agent.
    """
    plant, disease = parse_plant_disease(prediction.raw_label)
    is_healthy = prediction.status == "Healthy"

    state = DiagnosisState(
        raw_label=prediction.raw_label,
        label=prediction.label,
        confidence=prediction.confidence,
        status=prediction.status,
        plant=plant,
        disease=disease,
        is_healthy=is_healthy,
        severity=estimate_severity(prediction.confidence, is_healthy),
    )
    return state


def format_for_agent(state: DiagnosisState) -> str:
    """
    Returns a natural-language summary suitable for the agent's initial prompt.
    """
    if state.is_healthy:
        return (
            f"The uploaded leaf appears to be from a **{state.plant}** plant "
            f"and looks **healthy** (confidence: {state.confidence:.1f}%)."
        )
    return (
        f"The uploaded leaf is from a **{state.plant}** plant and shows signs of "
        f"**{state.disease}** (confidence: {state.confidence:.1f}%, "
        f"severity: {state.severity})."
    )
