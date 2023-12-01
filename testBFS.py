import unittest
from maze import maze
from bfs import breadthFirstSearch  
from COLOR import COLOR
from agent import agent

class TestBreadthFirstSearch(unittest.TestCase):

    def test_search_with_different_start_and_end_points(self):
        maze_sizes = [(10, 10), (20, 20)]  # Different maze sizes
        start_points = [(1, 1), (5, 5), (8, 8)]  # Different start points
        end_points = [(3, 3), (7, 7), (9, 9)]  # Different end points

        for size in maze_sizes:
            for start in start_points:
                for end in end_points:
                    maze_instance = maze(size[0], size[1])
                    maze_instance.CreateMaze(loopPercent=10, theme='light')

                    search_path, bfs_path, fowardPath = breadthFirstSearch(maze_instance, start)
                    agents = []

                    # Create agents for start and end points
                    agent_start = agent(maze_instance, start[0], start[1], footprints=True, color=COLOR.yellow, shape='square', filled=True)
                    agent_end = agent(maze_instance, end[0], end[1], footprints=True, color=COLOR.red, shape='square', filled=False)
                    agents.append(agent_start)
                    agents.append(agent_end)

                    # Trace paths
                    maze_instance.tracePath({agent_start: search_path}, delay=100)
                    maze_instance.tracePath({agent_end: bfs_path}, delay=100)

                    # Check assertions for each test case
                    self.assertEqual(len(search_path), len(bfs_path))
                    self.assertNotEqual(len(search_path), 0)
                    self.assertNotEqual(len(bfs_path), 0)

                    # Run the maze
                    maze_instance.run()

                    # Clean up agents for the next test
                    for agent_obj in agents:
                        del agent_obj

if __name__ == '__main__':
    unittest.main()
