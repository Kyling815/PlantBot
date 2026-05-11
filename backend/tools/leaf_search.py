"""
LeafSearch — describes visible symptoms found on the leaf
based on the detected disease label.
"""

from backend.diagnosis.diagnosis_state import DiagnosisState

# Symptom lookup table keyed by partial disease name (lowercase)
SYMPTOM_MAP: dict[str, list[str]] = {
    "early blight": [
        "Dark brown concentric ring spots on older leaves",
        "Yellow halo surrounding the lesion",
        "Lesions typically 1–2 cm in diameter",
        "Affected leaves wither and drop prematurely",
    ],
    "late blight": [
        "Water-soaked lesions that turn dark brown",
        "White powdery mold on the underside of leaves",
        "Rapid wilting across large sections of the plant",
        "Strong, unpleasant odour from infected tissue",
    ],
    "leaf mold": [
        "Pale yellowish spots on upper leaf surface",
        "Olive-green to brown mold on the lower surface",
        "Leaves curl upward and dry out",
    ],
    "bacterial spot": [
        "Small, water-soaked angular spots",
        "Spots turn dark brown with yellow margins",
        "Spots may drop out, giving a shot-hole appearance",
    ],
    "septoria leaf spot": [
        "Circular spots with dark borders and tan/grey centres",
        "Tiny black dots (pycnidia) visible in the centre",
        "Starts on lower leaves and progresses upward",
    ],
    "powdery mildew": [
        "White, powdery fungal coating on leaf surfaces",
        "Leaves may yellow and curl",
        "Stunted growth of new shoots",
    ],
    "black rot": [
        "V-shaped yellow lesions at leaf margins",
        "Blackened leaf veins (blackleg)",
        "Severe wilting and stem rot in advanced stages",
    ],
    "healthy": [
        "Leaf appears uniformly green",
        "No spots, lesions, or discolouration detected",
        "Normal leaf structure and texture",
    ],
}


def leaf_search(state: DiagnosisState, **kwargs) -> str:
    """Return symptom descriptions for the detected disease."""
    disease_lower = state.disease.lower()
    for key, symptoms in SYMPTOM_MAP.items():
        if key in disease_lower:
            return "\n".join(symptoms)
    return f"Symptoms for {state.disease} on {state.plant} (general): spots, discolouration, lesions."
