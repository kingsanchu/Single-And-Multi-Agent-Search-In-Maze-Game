import unittest
from maze_data import small_maze_data, medium_maze_data, large_maze_data
from algorithms import Algorithms
from main import Player, Maze

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.small_maze = Maze(small_maze_data)
        self.medium_maze = Maze(medium_maze_data)
        self.large_maze = Maze(large_maze_data)

    def validate_path(self, path, maze, start, end):
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
            if maze[x2][y2] == 1:  # If it's not an open path
                return False
        return True

    def search_algorithm(self, maze, algorithm):
        alg = Algorithms(maze.maze_data, maze.start_position, maze.end_position)
        if algorithm == 'bfs':
            path = alg.find_path_bfs()
        elif algorithm == 'dfs':
            path = alg.find_path_dfs()
        elif algorithm == 'a_star':
            path = alg.find_path_a_star()
        else:
            path = None
        return path

    def test_search_small_maze_bfs(self):
        path = self.search_algorithm(self.small_maze, 'bfs')
        self.assertTrue(self.validate_path(path, self.small_maze.maze_data, self.small_maze.start_position, self.small_maze.end_position))

    def test_search_medium_maze_bfs(self):
        path = self.search_algorithm(self.medium_maze, 'bfs')
        self.assertTrue(self.validate_path(path, self.medium_maze.maze_data, self.medium_maze.start_position, self.medium_maze.end_position))

    def test_search_large_maze_bfs(self):
        path = self.search_algorithm(self.large_maze, 'bfs')
        self.assertTrue(self.validate_path(path, self.large_maze.maze_data, self.large_maze.start_position, self.large_maze.end_position))

    def test_search_small_maze_dfs(self):
        path = self.search_algorithm(self.small_maze, 'dfs')
        self.assertTrue(self.validate_path(path, self.small_maze.maze_data, self.small_maze.start_position, self.small_maze.end_position))

    def test_search_medium_maze_dfs(self):
        path = self.search_algorithm(self.medium_maze, 'dfs')
        self.assertTrue(self.validate_path(path, self.medium_maze.maze_data, self.medium_maze.start_position, self.medium_maze.end_position))

    def test_search_large_maze_dfs(self):
        path = self.search_algorithm(self.large_maze, 'dfs')
        self.assertTrue(self.validate_path(path, self.large_maze.maze_data, self.large_maze.start_position, self.large_maze.end_position))

    def test_search_small_maze_a_star(self):
        path = self.search_algorithm(self.small_maze, 'a_star')
        self.assertTrue(self.validate_path(path, self.small_maze.maze_data, self.small_maze.start_position, self.small_maze.end_position))

    def test_search_medium_maze_a_star(self):
        path = self.search_algorithm(self.medium_maze, 'a_star')
        self.assertTrue(self.validate_path(path, self.medium_maze.maze_data, self.medium_maze.start_position, self.medium_maze.end_position))

    def test_search_large_maze_a_star(self):
        path = self.search_algorithm(self.large_maze, 'a_star')
        self.assertTrue(self.validate_path(path, self.large_maze.maze_data, self.large_maze.start_position, self.large_maze.end_position))

if __name__ == "__main__":
    unittest.main()
