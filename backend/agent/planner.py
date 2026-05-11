"""
Planner — decides which tools to call and in what order,
based on the current DiagnosisState.
"""

from dataclasses import dataclass, field
from typing import Any

from backend.diagnosis.diagnosis_state import DiagnosisState


@dataclass
class PlanStep:
    tool_name: str
    kwargs: dict[str, Any] = field(default_factory=dict)
    rationale: str = ""


def build_plan(state: DiagnosisState) -> list[PlanStep]:
    """
    Produces an ordered list of tool calls for the agent to execute.

    For healthy plants we only call leaf_search.
    For diseased plants we call all four search tools.
    """
    if state.is_healthy:
        return [
            PlanStep(
                tool_name="leaf_search",
                rationale="Confirm the healthy appearance of the leaf.",
            )
        ]

    return [
        PlanStep(
            tool_name="leaf_search",
            rationale="Identify visible symptoms on the leaf.",
        ),
        PlanStep(
            tool_name="disease_search",
            rationale="Retrieve detailed information about the detected disease.",
        ),
        PlanStep(
            tool_name="treatment_search",
            rationale="Find recommended treatments for the disease.",
        ),
        PlanStep(
            tool_name="prevention_search",
            rationale="Find prevention strategies to avoid recurrence.",
        ),
    ]
