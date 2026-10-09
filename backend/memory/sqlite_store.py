"""Persistent local SQLite memory with explicit record metadata."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

from memory.base import MemoryRecord, MemoryStore


class SQLiteMemoryStore(MemoryStore):
    def __init__(self, database_path: str | Path):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.database_path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute(
            """CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY, content TEXT NOT NULL, kind TEXT NOT NULL,
                source TEXT NOT NULL, confidence REAL NOT NULL, importance REAL NOT NULL,
                metadata TEXT NOT NULL, timestamp TEXT NOT NULL
            )"""
        )
        self._connection.commit()

    def write(self, record: MemoryRecord) -> MemoryRecord:
        self._connection.execute(
            "INSERT OR REPLACE INTO memories VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (record.id, record.content, record.kind, record.source, record.confidence,
             record.importance, json.dumps(dict(record.metadata)), record.timestamp.isoformat()),
        )
        self._connection.commit()
        return record

    def search(self, query: str, *, limit: int = 5) -> list[MemoryRecord]:
        terms = [term for term in query.lower().split() if term]
        rows = self._connection.execute("SELECT * FROM memories ORDER BY timestamp DESC").fetchall()
        matches = []
        for row in rows:
            score = sum(term in row["content"].lower() for term in terms)
            if score:
                matches.append((score, row))
        matches.sort(key=lambda item: (item[0], item[1]["timestamp"]), reverse=True)
        return [self._from_row(row) for _, row in matches[:limit]]

    def delete(self, record_id: str) -> bool:
        cursor = self._connection.execute("DELETE FROM memories WHERE id = ?", (record_id,))
        self._connection.commit()
        return cursor.rowcount > 0

    def close(self) -> None:
        self._connection.close()

    @staticmethod
    def _from_row(row: sqlite3.Row) -> MemoryRecord:
        return MemoryRecord(
            id=row["id"], content=row["content"], kind=row["kind"], source=row["source"],
            confidence=row["confidence"], importance=row["importance"],
            metadata=json.loads(row["metadata"]), timestamp=datetime.fromisoformat(row["timestamp"]),
        )
