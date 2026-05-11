"""
Response generator — synthesises the final user-facing answer
from the enriched DiagnosisState.

Uses the LLM configured in settings (Gemini or OpenAI).
Falls back to a template-based response if no API key is set.
"""

import logging
from backend.diagnosis.diagnosis_state import DiagnosisState
from backend.config import settings

logger = logging.getLogger(__name__)


def _template_response(state: DiagnosisState) -> str:
    """Fallback: build a structured response without an LLM."""
    if state.is_healthy:
        return (
            f"## ✅ Your {state.plant} looks healthy!\n\n"
            f"Confidence: **{state.confidence:.1f}%**\n\n"
            "Keep up good gardening practices to maintain plant health."
        )

    sections = [
        f"## 🌿 Diagnosis: {state.plant} — {state.disease}",
        f"**Confidence:** {state.confidence:.1f}%  |  **Severity:** {state.severity.capitalize()}",
    ]
    if state.disease_info:
        sections += ["", "### About this disease", state.disease_info]
    if state.treatment_plan:
        sections += ["", "### Treatment", state.treatment_plan]
    if state.prevention_tips:
        sections += ["", "### Prevention", state.prevention_tips]

    return "\n".join(sections)


def _llm_response(state: DiagnosisState) -> str:
    """Call the configured LLM to produce a polished response."""
    prompt = _build_prompt(state)

    if settings.llm_provider == "gemini" and settings.gemini_api_key:
        from google import genai
        client = genai.Client(api_key=settings.gemini_api_key)
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
        )
        return response.text

    if settings.llm_provider == "openai" and settings.openai_api_key:
        from openai import OpenAI
        client = OpenAI(api_key=settings.openai_api_key)
        completion = client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content

    raise RuntimeError("No LLM API key configured.")


def _build_prompt(state: DiagnosisState) -> str:
    """Assemble the LLM prompt from the enriched state."""
    return f"""You are PlantBot, an expert plant pathologist assistant.

## Diagnosis Result
- Plant: {state.plant}
- Disease: {state.disease}
- Confidence: {state.confidence:.1f}%
- Severity: {state.severity}

## Knowledge Gathered
### Leaf Symptoms
{chr(10).join(f"- {s}" for s in state.leaf_symptoms) or "Not available"}

### Disease Info
{state.disease_info or "Not available"}

### Treatment
{state.treatment_plan or "Not available"}

### Prevention
{state.prevention_tips or "Not available"}

## Task
Write a clear, compassionate, and actionable response for a farmer or gardener.
Use markdown with headers. Be concise (300 words max).
"""


def generate_response(state: DiagnosisState) -> str:
    """
    Try LLM first; fall back to template if unavailable.
    """
    try:
        return _llm_response(state)
    except Exception as exc:
        logger.warning("LLM unavailable (%s), using template response.", exc)
        return _template_response(state)
