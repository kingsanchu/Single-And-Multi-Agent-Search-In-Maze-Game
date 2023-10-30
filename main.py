# @author Steven CHU

import heapq

class Node:
    def __init__(self, position, g_cost, h_cost):
        self.position = position
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        
    def __lt__(self, other):
        return self.f_cost < other.f_cost

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

    #Class Node checks the cost of the search

class Maze:
    #Representing the maze configuration
    def __init__(self, maze_data):
        self.maze_data = maze_data
        self.rows = len(maze_data)
        self.cols = len(maze_data[0])
        self.start_position = (0,0)
        self.end_position = (self.rows -1, self.cols -1)
    
    def find_path(self):
        start = self.start_position
        end = self.end_position
        empty_set = []
        visited = set()
        starting_node = Node(start, 0, self.heuristic(start, end))
        heapq.heappush(empty_set, starting_node)
        came_from={}

        while empty_set:
            current = heapq.heappop(empty_set)

            if current.position == end:
                return self.reconstruct_path(start, end, current, came_from)
            
            visited.add(current.position)

            for neighbor in self.get_neighbor(current.position):
                if neighbor in visited:
                    continue

                g_cost = current.g_cost+1
                h_cost = self.heuristic(neighbor, end)
                neighbor_node = Node(neighbor, g_cost, h_cost)
                came_from[neighbor_node] = current

                if neighbor_node not in empty_set:
                    heapq.heappush(empty_set, neighbor_node)
                    
        return None

    def position(self, node):
        return node.position
    
    def reconstruct_path(self, start, end, current, came_from):
        path = []
        while current.position != start:
            path.append(current.position)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path
    
    def heuristic(self, position, end):
        x1, y1 = position
        x2, y2 = end
        return abs(x1 - x2) + abs(y1 - y2)

    #A* search implementation
    def a_star_search(self, start, end):
        empty_set = [] 
        visited = set()
        starting_node = Node(start, 0, self.heuristic(start, end))
        heapq.heappush(empty_set,  starting_node)

        while empty_set:
            current = heapq.heappop(empty_set)

            if current.position == end :
                return self.reconstruct_path(start, end, current)
            
        visited.add(current.position)

        for neighbor in self.get_neighbor(current.position):
            if neighbor in visited:
                continue

            g_cost = current.g_cost + 1
            h_cost = self.heuristic(neighbor, end)
            neighbor_node = Node(neighbor, g_cost, h_cost)

            if neighbor_node not in empty_set:
                heapq.heappush(empty_set, neighbor_node)

    #Check if the neighbors is an obstacle 
    def get_neighbor(self, position):
        x, y = position
        neighbors = []
        if x > 0 and self.maze_data[x-1][y] == 0:
            neighbors.append((x-1, y))
        if x < self.rows - 1 and self.maze_data[x+1][y] == 0:
            neighbors.append((x+1, y))
        if y > 0 and self.maze_data[x][y-1] == 0:
            neighbors.append((x, y-1))
        if y < self.rows - 1 and self.maze_data[x][y+1] == 0:
            neighbors.append((x, y+1))
        
        return neighbors
         
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

#Creating player position
player = Player(0, 0)

path = maze.find_path()

if path:
    print("Path found : " , path)
else:
    print("No Path Found")
