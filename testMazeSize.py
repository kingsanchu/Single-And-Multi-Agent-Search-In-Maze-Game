import unittest
from maze_data import small_maze_data, medium_maze_data, large_maze_data
from a_star_search import Algorithms

class TestAStarSearch(unittest.TestCase):

    def validate_path(self, path, maze_data, start, end):
        if path is None:
            return False
        if path[0] != start:
            return False
        if path[-1] != end:
            return False
        for i in range(1, len(path)):
            x1, y1 = path[i - 1]
            x2, y2 = path[i]
            if abs(x1 - x2) > 1 or abs(y1 - y2) > 1:
                return False
            if maze_data[x2][y2] == 1:  # If it's not an open path
                return False
        return True

    def test_a_star_search_small(self):
        alg = Algorithms(small_maze_data, (0, 0), (4, 4))
        path = alg.find_path_a_star()
        self.assertTrue(self.validate_path(path, small_maze_data, (0, 0), (4, 4)))

    def test_a_star_search_medium(self):
        alg = Algorithms(medium_maze_data, (0, 0), (6, 6))
        path = alg.find_path_a_star()
        self.assertTrue(self.validate_path(path, medium_maze_data, (0, 0), (6, 6)))

    def test_a_star_search_large(self):
        alg = Algorithms(large_maze_data, (0, 0), (9, 9))
        path = alg.find_path_a_star()
        self.assertTrue(self.validate_path(path, large_maze_data, (0, 0), (9, 9)))

if __name__ == "__main__":
    unittest.main()