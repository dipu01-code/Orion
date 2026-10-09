"""Interfaces shared by every language-model provider integration."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class ModelRequest:
    """A provider-neutral generation request."""

    prompt: str
    context: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ModelResponse:
    """A provider-neutral generation result with explicit provenance."""

    text: str
    model_id: str
    confidence: float | None = None


class Model(ABC):
    """Contract implemented by cloud, local, and future specialised models."""

    @abstractmethod
    async def generate(self, request: ModelRequest) -> ModelResponse:
        """Generate a response without exposing provider-specific types."""
