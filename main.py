# @author Steven CHU

class player:
    # Record if the player or cell visited the coordinates or not.
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False 

    #Check if player visited the coordinates.
    def check_visited(self):
        if self.visited:
            print("Player has visited the corrdinates.")
        else:
            print("Player has not visited the coordinates.")

class Maze:
    #Representing the maze configuration
    def __init__(self, maze_data):
        self.maze_data = maze_data
        self.start_position = (0,0)
        self.end_position = (4,4)
    
    #Check if the player can move on to the next coordinate
    def check_move(self, player):
        next_x, next_y = player.x + 1,  player.y
        #Check if the next coordinate is blocked by a wall
        if next_x < len(self.maze_data) and next_y < len(self.maze_data) and self.maze_data[next_x][next_y] == 0:
            player.x = next_x
            player.y = next_y
            player.visited = True
            return True
        return False

