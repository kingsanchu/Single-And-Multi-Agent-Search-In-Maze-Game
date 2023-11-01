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

class Maze:
    #Representing the maze configuration
    def __init__(self, maze_data):
        self.maze_data = maze_data
        self.rows = len(maze_data)
        self.cols = len(maze_data[0])
        self.start_position = (0,0)
        self.end_position = (self.rows -1, self.cols -1)

    def reconstruct_path(self, start, end, current, came_from): 
        path = []
        while current.position != start:
            path.append(current.position)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path
    
    #2 heuristic functions :

    def heuristic_manhattan(self, position, end):
        x1, y1 = position
        x2, y2 = end
        return abs(x1 - x2) + abs(y1 - y2)
    
    def heuristic_euclidean(self, position, end):
        x1, y1 = position
        x2, y2 = end
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) **0.5
    
    heuristic_fucntions = [heuristic_manhattan, heuristic_euclidean]

    for heuristic in heuristic_fucntions:
        print(f"Using {heuristic.__name__} heuristic: ")

#A* Search algorithms
    def find_path_a_star(self, heuristic_function):
        start = self.start_position
        end = self.end_position
        empty_set = []
        visited = set()
        starting_node = Node(start, 0, heuristic_function(start, end))
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
                h_cost == heuristic_function(neighbor, end)
                neighbor_node = Node(neighbor, g_cost, h_cost)
                came_from[neighbor_node] = current

                if neighbor_node not in empty_set:
                    heapq.heappush(empty_set, neighbor_node)
                    
        return None

    def a_star_search(self, start, end):
        empty_set = [] 
        visited = set()
        starting_node = Node(start, 0, self.heuristic_manhattan(start, end))
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
            h_cost = self.heuristic_manhattan(neighbor, end)
            neighbor_node = Node(neighbor, g_cost, h_cost)

            if neighbor_node not in empty_set:
                heapq.heappush(empty_set, neighbor_node)

#Alpha-beta Pruning algorithms
    def alpha_beta_search(self, node, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.at_end(node):  # Replace with your end condition
            return self.heuristic_manhattan(node.position, self.end_position)

        if maximizing_player:
            max_value = float('-inf')
            for neighbor in self.get_neighbor(node.position):
                max_value = max(max_value, self.alpha_beta_search(Node(neighbor, 0, 0), depth - 1, alpha, beta, False))
                alpha = max(alpha, max_value)
                if beta <= alpha:
                    break  # Pruning
            return max_value
        else:
            min_value = float('inf')
            for neighbor in self.get_neighbor(node.position):
                min_value = min(min_value, self.alpha_beta_search(Node(neighbor, 0, 0), depth - 1, alpha, beta, True))
                beta = min(beta, min_value)
                if beta <= alpha:
                    break  # Pruning
            return min_value
        
    def find_path_alpha_beta(self):
        start = self.start_position
        empty_set = []
        came_from = {}
        depth = 3
        alpha = float('-inf')
        beta = float('inf')
        maximizing_player = True

        player = Player(start[0], start[1])  # Create a Player object for the start position

        while empty_set:
            current = heapq.heappop(empty_set)

            if self.at_end(player):  # Check with the Player object
                return self.reconstruct_path(start, self.end_position, current, came_from)

            for neighbor in self.get_neighbor(current.position):
                neighbor_node = Node(neighbor, 0, self.alpha_beta_search(Node(neighbor, 0, 0), depth, alpha, beta, False))
                came_from[neighbor_node] = current
                heapq.heappush(empty_set, neighbor_node)

        return None

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
    
    def choose_algorithm(self):
        while True:
            choice = input("Type 1 for A* Search, or 2 for Alpha-Beta Pruning in the Maze : ")
            if choice == '1':
                return self.find_path_a_star()
            elif choice == '2':
                return self.find_path_alpha_beta()
            else:
                print("Invalid input, please Type 1 for A* Search, or 2 for Alpha-Beta Pruning in the Maze :")

    #Visualisation in the maze
    #def visualise(self, player):
     #   for i in range(self.rows):
      #      for j in range(self.cols):
       #         if (i,j) == self.start_position:
        #            print('S', end = ' ')
         #       elif (i, j) == self.end_position:
          #          print('E', end=' ')
           #     elif self.maze_data[i][j] == 0:
            #        if player.x == i and player.y == j:
             #           print('P', end = ' ')
              #      else:
               #         print('.', end = ' ')
                #else: 
                 #   print('.', end = ' ')
            #else:
             #   print('#', end = ' ')
        #print()
        
#Example of an open path and walls in a maze
maze_data = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

#Creating a maze
maze = Maze(maze_data)

#Creating player position
player = Player(0, 0)

path = maze.choose_algorithm()

if path:
    print("Path found : " , path)
else:
    print("No Path Found")
