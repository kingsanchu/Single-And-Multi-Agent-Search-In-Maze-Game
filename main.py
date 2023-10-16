# @author Steven CHU

class player:
    # Record if the player or cell visited the coordinates or not.
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False 

    #Check if player visited the coordinates.
        if player.visited:
            print("Player has visited the corrdinates.")
        else:
            print("Player has not visited the coordinates.")

class Maze:
    #Representing the maze configuration
    def __init__(self, maze_data):
        self.maze_data = maze_data
        self.start_position = (0,0)
        self.end_position = (4,4)
