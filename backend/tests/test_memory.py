import unittest

from memory import InMemoryStore, MemoryRecord


class InMemoryStoreTests(unittest.TestCase):
    def test_search_and_delete(self):
        store = InMemoryStore()
        record = store.write(MemoryRecord(content="ORION uses modular interfaces"))

        self.assertEqual(store.search("modular")[0], record)
        self.assertTrue(store.delete(record.id))
        self.assertEqual(store.search("modular"), [])
