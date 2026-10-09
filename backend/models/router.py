"""Configurable model selection boundary.

The initial policy intentionally selects one local fallback.  Provider adapters
can be registered here later without changing the brain.
"""

from models.base import Model
from models.local import LocalFallbackModel


class ModelRouter:
    def __init__(self, default_model: Model | None = None):
        self._default_model = default_model or LocalFallbackModel()

    def select(self, task_type: str = "general") -> Model:
        del task_type  # Reserved for future capability/cost/latency policy.
        return self._default_model
