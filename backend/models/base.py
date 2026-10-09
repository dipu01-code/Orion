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
    system_instruction: str = "You are ORION, a helpful, precise desktop assistant."
    tools: tuple[Mapping[str, Any], ...] = ()


@dataclass(frozen=True)
class ModelResponse:
    """A provider-neutral generation result with explicit provenance."""

    text: str
    model_id: str
    confidence: float | None = None
    tool_calls: tuple["ToolCall", ...] = ()


@dataclass(frozen=True)
class ToolCall:
    """A model-requested action, kept separate from provider wire formats."""

    name: str
    arguments: Mapping[str, Any]
    id: str = ""


class Model(ABC):
    """Contract implemented by cloud, local, and future specialised models."""

    @abstractmethod
    async def generate(self, request: ModelRequest) -> ModelResponse:
        """Generate a response without exposing provider-specific types."""
