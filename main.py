# @author Steven CHU

class Player:
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
        self.rows = len(maze_data)
        self.cols = len(maze_data[0])
        self.start_position = (0,0)
        self.end_position = (self.rows -1, self.cols -1)
    
    #Check if the player can move on to the next coordinate
    def check_move(self, player, direction):

         #Creating player coordinate
        x, y = player.x, player.y

        if direction == 'up' and x > 0 and self.maze_data[x-1][y] == 0:
            player.x -= 1
        elif direction == 'down' and x < self.rows - 1 and self.maze_data[x+1][y] == 0 :
            player.x += 1
        elif direction == 'left' and y > 0 and self.maze_data[x][y-1] == 0 :
            player.y -= 1
        elif direction == 'right' and y < self.rows - 1 and self.maze_data[x][y+1] == 0 :
            player.y += 1
        else:
            print("Invalid direction. Please retry.")
            return False

        player.visited = True
        return True
    
    #When player is at the ending path
    def at_end(self, player):
        return(player.x, player.y) == self.end_position
    
    #Visualisation in the maze
    def visualise(self, player):
        for i in range(self.rows):
            for j in range(self.cols):
                if (i,j) == self.start_position:
                    print('S', end = ' ')
                elif (i, j) == self.end_position:
                    print('E', end=' ')
                elif self.maze_data[i][j] == 0:
                    if player.x == i and player.y == j:
                        print('P', end = ' ')
                    else:
                        print('.', end = ' ')
                else: 
                    print('.', end = ' ')
            else:
                print('#', end = ' ')
        print()
                
#Example of an open path and walls in a maze
maze_data = [
    [0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
]

#Creating a maze
maze = Maze(maze_data)

#Creating player
player = Player(0, 0)

#Check if the player has visited the coordinates
maze.check_move(player) 

while not maze.at_end(player):
    maze.visualise(player)
    direction = input("Enter a direction (Left, Right, Up, Down): ").lower()
    maze.check_move(player, direction)

print("Congrats! You have reached the end of the maze! ")