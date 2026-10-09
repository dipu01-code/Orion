"""Standard tool contract used by future tool adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class ToolResult:
    success: bool
    message: str
    data: Mapping[str, Any] | None = None


class Tool(ABC):
    name: str
    description: str
    input_schema: Mapping[str, str]
    permission: str

    @abstractmethod
    def execute(self, **input_data: Any) -> ToolResult:
        """Run the tool after permission policy has approved it."""
