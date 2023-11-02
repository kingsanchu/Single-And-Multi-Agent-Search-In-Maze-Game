from main import Maze, Node, Player
from maze_data import small_maze_data, medium_maze_data, large_maze_data

if __name__ == "__main__":
    
    maze = Maze(large_maze_data) # Edit the maze size data to search in different maze

#Creating player position
    player = Player(0, 0)

    path = maze.find_path_a_star()

    if path:
        print("Path found : " , path)
    else:
        print("No Path Found")