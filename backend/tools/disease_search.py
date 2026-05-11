"""
DiseaseSearch — retrieves disease profile from the knowledge base.
"""

import os
from backend.diagnosis.diagnosis_state import DiagnosisState

KB_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge_base", "disease_profiles")


def disease_search(state: DiagnosisState, **kwargs) -> str:
    """
    Look up the disease profile markdown file for the detected disease.
    Falls back to a generic summary if no file is found.
    """
    # Build a slug: "Tomato - Early blight" → "tomato_early_blight"
    slug = f"{state.plant}_{state.disease}".lower().replace(" ", "_").replace("-", "_")
    md_path = os.path.join(KB_DIR, f"{slug}.md")

    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            return f.read()

    # Generic fallback
    return (
        f"**{state.disease}** is a disease affecting **{state.plant}** plants. "
        f"It is caused by pathogenic organisms and can significantly reduce crop yield. "
        f"Early detection and treatment are critical for effective management."
    )
