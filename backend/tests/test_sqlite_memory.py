import tempfile
import unittest
from pathlib import Path

from memory import MemoryRecord, SQLiteMemoryStore


class SQLiteMemoryStoreTests(unittest.TestCase):
    def test_record_is_available_after_reopening_database(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "orion.sqlite3"
            first = SQLiteMemoryStore(path)
            record = first.write(MemoryRecord(content="User prefers concise answers", kind="user"))
            first.close()

            second = SQLiteMemoryStore(path)
            self.assertEqual(second.search("concise")[0], record)
            second.close()
