"""
PlantBot reasoning agent.

Inspired by the TravelPlanner framework:
  Observe → Plan → Act (tool call) → Reflect → Respond

The agent receives a DiagnosisState and iteratively uses tools
from the tool registry to gather information, then synthesises
a final response.
"""

import logging
from typing import Optional

from backend.diagnosis.diagnosis_state import DiagnosisState
from backend.diagnosis.diagnosis_formatter import format_for_agent
from backend.agent.planner import build_plan, PlanStep
from backend.agent.response_generator import generate_response
from backend.tools.tool_registry import TOOL_REGISTRY

logger = logging.getLogger(__name__)

MAX_ITERATIONS = 6


class PlantBotAgent:
    """
    Orchestrates tool calls and LLM generation for a single diagnosis session.
    """

    def __init__(self):
        self.tools = TOOL_REGISTRY

    def run(self, state: DiagnosisState) -> DiagnosisState:
        """
        Execute the agent loop and populate the DiagnosisState with results.
        Returns the enriched DiagnosisState.
        """
        logger.info("Agent started for label=%s", state.raw_label)

        # Step 1 — Build plan
        plan: list[PlanStep] = build_plan(state)
        logger.info("Plan: %s", [s.tool_name for s in plan])

        # Step 2 — Execute each planned tool call
        for iteration, step in enumerate(plan[:MAX_ITERATIONS]):
            tool_fn = self.tools.get(step.tool_name)
            if tool_fn is None:
                logger.warning("Unknown tool: %s", step.tool_name)
                continue

            logger.info("[%d] Calling tool: %s", iteration, step.tool_name)
            result: str = tool_fn(state, **step.kwargs)

            # Store result in the appropriate state field
            if step.tool_name == "leaf_search":
                state.leaf_symptoms = result.split("\n") if result else []
            elif step.tool_name == "disease_search":
                state.disease_info = result
            elif step.tool_name == "treatment_search":
                state.treatment_plan = result
            elif step.tool_name == "prevention_search":
                state.prevention_tips = result

        # Step 3 — Generate final response
        state.agent_response = generate_response(state)
        logger.info("Agent finished.")

        return state
