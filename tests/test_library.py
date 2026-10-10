import os
import unittest
from library import Library, load_books

ROOT = os.path.dirname(os.path.dirname(__file__))


class LibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library(load_books(os.path.join(ROOT, "data", "books.json")))

    def test_search(self):
        results = self.library.search("python")
        self.assertTrue(any(book["id"] == "B1" for book in results))

    def test_category(self):
        self.assertEqual(len(self.library.by_category("Programming")), 3)

    def test_bfs_and_dfs(self):
        self.assertTrue(self.library.related_bfs("B1"))
        self.assertTrue(self.library.related_dfs("B1"))
        self.assertEqual(self.library.related_bfs("INVALID"), [])

    def test_dijkstra(self):
        result = self.library.dijkstra("B1", "B2")
        self.assertIsNotNone(result)
        self.assertEqual(result[1][0], "B1")
        self.assertEqual(result[1][-1], "B2")

    def test_floyd_warshall(self):
        distances = self.library.floyd_warshall()
        self.assertEqual(distances["B1"]["B1"], 0)

    def test_lcs(self):
        self.assertEqual(Library.lcs_length("python basics", "python guide"), 1)

    def test_knapsack(self):
        chosen = self.library.recommend_knapsack(60)
        self.assertLessEqual(sum(b["reading_time"] for b in chosen), 60)

    def test_resource_allocation(self):
        chosen = self.library.resource_allocation(4)
        self.assertEqual(len(chosen), 4)
        self.assertEqual(len({b["category"] for b in chosen}), 4)


if __name__ == "__main__":
    unittest.main()
