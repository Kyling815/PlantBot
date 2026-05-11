"""
Tool registry — maps tool names to their callable functions.
The agent uses this registry to look up tools by name.
"""

from backend.tools.leaf_search import leaf_search
from backend.tools.disease_search import disease_search
from backend.tools.treatment_search import treatment_search
from backend.tools.prevention_search import prevention_search

TOOL_REGISTRY: dict = {
    "leaf_search": leaf_search,
    "disease_search": disease_search,
    "treatment_search": treatment_search,
    "prevention_search": prevention_search,
}
