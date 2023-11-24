import unittest
from maze import maze
from agent import agent
from textLabel import textLabel
from queue import PriorityQueue
from a_star_search import aStarPathFinding, heuristic

class TestAStarPathFinding(unittest.TestCase):

    def setUp(self):
        self.maze_instance = maze(10, 10)
        self.maze_instance.CreateMaze()

    def test_heuristic(self):
        cell1 = (1, 1)
        cell2 = (5, 5)
        expected_distance = 8
        self.assertEqual(heuristic(cell1, cell2), expected_distance)

    def test_aStarPathFinding(self):
        path = aStarPathFinding(self.maze_instance)
        self.assertTrue(isinstance(path, dict))

if __name__ == '__main__':
    unittest.main()
