"""
TreatmentSearch — retrieves treatment guides from the knowledge base.
"""

import os
from backend.diagnosis.diagnosis_state import DiagnosisState

KB_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge_base", "treatment_guides")

# Map disease keywords → guide filenames
TREATMENT_MAP = {
    "blight": "fungal_disease_control.md",
    "mold": "fungal_disease_control.md",
    "mildew": "fungal_disease_control.md",
    "scab": "fungal_disease_control.md",
    "rust": "fungal_disease_control.md",
    "spot": "fungal_disease_control.md",
    "bacterial": "bacterial_disease_control.md",
    "virus": "viral_disease_control.md",
    "mosaic": "viral_disease_control.md",
    "curl": "viral_disease_control.md",
}


def treatment_search(state: DiagnosisState, **kwargs) -> str:
    """
    Find and return a relevant treatment guide for the detected disease.
    """
    disease_lower = state.disease.lower()
    guide_file = None

    for keyword, filename in TREATMENT_MAP.items():
        if keyword in disease_lower:
            guide_file = filename
            break

    if guide_file:
        path = os.path.join(KB_DIR, guide_file)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()

    return (
        f"For **{state.disease}** on **{state.plant}**:\n"
        "1. Remove and destroy infected leaves immediately.\n"
        "2. Apply appropriate fungicide or bactericide.\n"
        "3. Improve air circulation around the plant.\n"
        "4. Avoid overhead irrigation to reduce moisture.\n"
        "5. Monitor plants closely for 2 weeks."
    )
