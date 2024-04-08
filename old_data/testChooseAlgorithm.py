from maze_data import small_maze_data, medium_maze_data, large_maze_data
from old_data.a_star_search import Algorithms
from dfs_bfs import bfs, dfs
from main import Maze, Player

if __name__ == "__main__":
    while True:
        maze_size = input("Choose the maze size (small, medium, large): ").strip().lower()
        if maze_size in ["small", "medium", "large"]:
            break
        else:
            print("Invalid maze size choice. Please enter small, medium, or large.")

    if maze_size == "small":
        maze_data = small_maze_data
    elif maze_size == "medium":
        maze_data = medium_maze_data
    else:
        maze_data = large_maze_data

    player = Player(0, 0)
    maze = Maze(maze_data)

    while True:
        algorithm_choice = input("Choose an algorithm (a_star, bfs, dfs): ").strip().lower()
        if algorithm_choice in ["a_star", "bfs", "dfs"]:
            break
        else:
            print("Invalid algorithm choice. Please enter a_star, bfs, or dfs.")

    alg = Algorithms(maze_data, maze.start_position, maze.end_position)

    if algorithm_choice == "a_star":
        path = alg.find_path_a_star()
    elif algorithm_choice == "bfs":
        path = alg.bfs()
    else:
        path = alg.dfs()

    if path:
        print("Path found:", path)
    else:
        print("No Path Found")
