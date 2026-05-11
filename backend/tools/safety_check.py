"""
Safety checker — validates that the agent's response is safe
and appropriate before returning it to the user.
"""


BLOCKED_PATTERNS = [
    "poison",
    "toxic to humans",
    "do not use gloves",
]


def safety_check(response: str) -> tuple[bool, str]:
    """
    Returns (is_safe, reason).
    If not safe, reason explains what was flagged.
    """
    lower = response.lower()
    for pattern in BLOCKED_PATTERNS:
        if pattern in lower:
            return False, f"Response flagged for pattern: '{pattern}'"
    return True, ""
