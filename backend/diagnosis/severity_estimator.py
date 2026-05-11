"""
Heuristic severity estimation based on model confidence.

For diseased plants, high confidence often correlates with advanced / clear
symptoms. This is a simple heuristic — replace with a proper model if needed.
"""


def estimate_severity(confidence: float, is_healthy: bool) -> str:
    """
    Returns one of: 'healthy', 'mild', 'moderate', 'severe'.

    Args:
        confidence: CNN confidence percentage (0–100).
        is_healthy: True if the plant is classified as healthy.
    """
    if is_healthy:
        return "healthy"
    if confidence >= 90:
        return "severe"
    if confidence >= 70:
        return "moderate"
    return "mild"
