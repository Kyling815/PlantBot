"""
PreventionSearch — retrieves prevention guides from the knowledge base.
"""

import os
from backend.diagnosis.diagnosis_state import DiagnosisState

KB_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge_base", "prevention_guides")

# Map plant/disease keywords → guide filenames
PREVENTION_MAP = {
    "water": "watering_practice.md",
    "blight": "watering_practice.md",
    "mold": "watering_practice.md",
    "prune": "pruning_practice.md",
    "scab": "pruning_practice.md",
    "soil": "soil_management.md",
    "root": "soil_management.md",
}


def prevention_search(state: DiagnosisState, **kwargs) -> str:
    """
    Find and return a relevant prevention guide for the detected disease.
    """
    disease_lower = state.disease.lower()
    guide_file = None

    for keyword, filename in PREVENTION_MAP.items():
        if keyword in disease_lower:
            guide_file = filename
            break

    if guide_file is None:
        guide_file = "watering_practice.md"

    path = os.path.join(KB_DIR, guide_file)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    return (
        f"Prevention tips for **{state.disease}** on **{state.plant}**:\n"
        "1. Use certified disease-free seeds and transplants.\n"
        "2. Practice crop rotation (minimum 2–3 years).\n"
        "3. Maintain proper plant spacing for air circulation.\n"
        "4. Water at the base; avoid wetting foliage.\n"
        "5. Apply preventive fungicide sprays during high-risk periods.\n"
        "6. Monitor plants weekly and remove symptomatic material promptly."
    )
