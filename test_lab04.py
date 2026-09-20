import unittest
from agent import SearchAgent


class AStarTests(unittest.TestCase):
    def setUp(self):
        self.agent = SearchAgent("AStar")

    def test_distances(self):
        self.assertEqual(self.agent.manhattan_distance((0, 0), (3, 4)), 7)
        self.assertEqual(self.agent.euclidean_distance((0, 0), (3, 4)), 5.0)

    def test_astar_optimal_path(self):
        walls = [(1, 0), (2, 0), (0, 2), (1, 2), (2, 2)]
        path = self.agent.astar_search((0, 0), (3, 3), walls, (4, 4))
        self.assertEqual(len(path), 6)

    def test_astar_unreachable(self):
        walls = [(1, 2), (2, 1), (1, 1)]
        self.assertIsNone(self.agent.astar_search((0, 0), (2, 2), walls, (3, 3)))


if __name__ == "__main__":
    unittest.main()
