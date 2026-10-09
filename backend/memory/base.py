"""Contracts for ORION's memory implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import uuid4


@dataclass(frozen=True)
class MemoryRecord:
    content: str
    kind: str = "working"
    source: str = "orion"
    confidence: float = 1.0
    importance: float = 0.5
    metadata: Mapping[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class MemoryStore(ABC):
    @abstractmethod
    def write(self, record: MemoryRecord) -> MemoryRecord:
        """Persist a memory record."""

    @abstractmethod
    def search(self, query: str, *, limit: int = 5) -> list[MemoryRecord]:
        """Return the most relevant records for a query."""

    @abstractmethod
    def delete(self, record_id: str) -> bool:
        """Delete an explicitly identified record."""
