"""Small, transparent in-process memory for the initial vertical slice."""

from memory.base import MemoryRecord, MemoryStore


class InMemoryStore(MemoryStore):
    def __init__(self):
        self._records: list[MemoryRecord] = []

    def write(self, record: MemoryRecord) -> MemoryRecord:
        self._records.append(record)
        return record

    def search(self, query: str, *, limit: int = 5) -> list[MemoryRecord]:
        terms = set(query.lower().split())
        scored = [
            (len(terms.intersection(record.content.lower().split())), index, record)
            for index, record in enumerate(self._records)
        ]
        return [record for score, _, record in sorted(scored, reverse=True) if score][:limit]

    def delete(self, record_id: str) -> bool:
        for index, record in enumerate(self._records):
            if record.id == record_id:
                del self._records[index]
                return True
        return False
