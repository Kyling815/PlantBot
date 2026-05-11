"""
DiagnosisState — intermediate state produced after CNN prediction.
Passed to the PlantBot agent as its initial context.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DiagnosisState:
    # Raw CNN output
    raw_label: str
    label: str
    confidence: float           # 0–100
    status: str                 # "Healthy" | "Disease detected"

    # Parsed fields
    plant: str = ""
    disease: str = ""
    is_healthy: bool = False

    # Severity (set by severity_estimator)
    severity: str = "unknown"   # "mild" | "moderate" | "severe" | "healthy"

    # Agent context (filled during agent reasoning)
    leaf_symptoms: List[str] = field(default_factory=list)
    disease_info: Optional[str] = None
    treatment_plan: Optional[str] = None
    prevention_tips: Optional[str] = None

    # Final response
    agent_response: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "raw_label": self.raw_label,
            "label": self.label,
            "confidence": self.confidence,
            "status": self.status,
            "plant": self.plant,
            "disease": self.disease,
            "is_healthy": self.is_healthy,
            "severity": self.severity,
            "leaf_symptoms": self.leaf_symptoms,
            "disease_info": self.disease_info,
            "treatment_plan": self.treatment_plan,
            "prevention_tips": self.prevention_tips,
            "agent_response": self.agent_response,
        }
