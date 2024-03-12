from character import Character
from wall import Wall
from collections import deque
from random import random
from heapq import heappush, heappop


class Agent(Character):
    inky = 5
    blinky = 6
    pinky = 7
    clyde = 8

    def __init__(self, x, y, enemy_type, images, algorithm,  direction=None,):
        ''' Initializes an Enemy class that inherits from the Character Class. The enemy class
            is one of the two classes that has movement involved, and different attributes to
            represent the state. The enemy_type is given by argument, and there are 4 different enemy
            types because each enemy is unique. '''
        Character.__init__(self, x, y, direction)
        self.enemy_type = enemy_type
        self.invulnerable = True
        self.slowed_down = False
        self.determine_image(enemy_type, images)
        self.pickup_memory = None
        self.algorithm = algorithm

        if enemy_type == Agent.inky or enemy_type == Agent.clyde:  # Only Inky and Clyde require these Attributes
            self.movement_turns = 15
            self.last_choice = None

    def discard_pickup(self) -> None:
        ''' This function is called when an enemy was holding a pickup and then discards
            it, and is used as memory. '''
        self.pickup_memory = None

    def determine_image(self, enemy_type, images) -> None:
        ''' Image display to player is determined by which type of enemy it is. If the enemy
            is not invulnerable, then they all have the same common vulnerable ghost image. '''
        if self.invulnerable:
            if enemy_type == Agent.inky:
                self._image = images.return_image('inky')

            elif enemy_type == Agent.blinky:
                self._image = images.return_image('blinky')

            elif enemy_type == Agent.pinky:
                self._image = images.return_image('pinky')

            elif enemy_type == Agent.clyde:
                self._image = images.return_image('clyde')

        else:
            self._image = images.return_image('vulnerable_ghost')

    def determine_path(self, board, start, endpoint_y, endpoint_x) -> deque:
        if self.invulnerable:
            # Use A* search algorithm
            if self.algorithm == "AStar":
                return self.astar_search(board, start, endpoint_y, endpoint_x)
            # Use Depth-first search algorithm
            elif self.algorithm == "DFS":
                return self.dfs_search(board, start, endpoint_y, endpoint_x)
            # Use Dijkstra's algorithm
            elif self.algorithm == "Dijkstra":
                return self.dijkstra_search(board, start, endpoint_y, endpoint_x)
            # Use Breadth First Search's algorithm
            elif self.algorithm == "BFS":
                return self.breadth_first_search(board, start, endpoint_y, endpoint_x)
            else:
                raise ValueError
        else:
            return self.breadth_first_search(board, start, self.start_location[1], self.start_location[0])[:-1]

    def determineDirection(self, board, powers) -> None:
        ''' Direction is determined by the enemy type. Since each enemy type
            has their own unique game movement. '''
        start = self.x, self.y

        if self.enemy_type == Agent.blinky:
            self.blinky_movement(board, start, powers)

        elif self.enemy_type == Agent.inky:
            self.inky_movement(board, start, powers)

        if self.enemy_type == Agent.pinky:
            self.pinky_movement(board, start, powers)

        elif self.enemy_type == Agent.clyde:
            self.clyde_movement(board)

    # Inky Movement Functions #
    def blinky_movement(self, board, start, powers) -> None:
        ''' Blinky's movement is to directly chase Pacman on the board. '''
        path = self.determine_path(board, start, powers.y, powers.x)
        self.path_finding_direction(path)

    # Blinky Movement Functions #
    def inky_movement(self, board, start, powers) -> None:
        ''' Inky's movement differentiates between the other three ghost. So we use
            random() from the random library to determine which movement he will follow,
            and it will constantly be changing as time goes on. '''
        choice = self.random_choice()
        self._inky_and_clyde_movement_turns()

        if choice <= .33:
            self.blinky_movement(board, start, powers)

        elif choice <= .75:
            self.clyde_movement(board)

        elif choice <= 1:
            self.pinky_movement(board, start, powers)

    # Pinky Movement Functions #

    def pinky_movement(self, board, start, powers):
        ''' Pinky's movement is meant to ambush, so we have the entire pacman object
            so that are we able to look at his direction and coordinates. '''
        endpoint_y, endpoint_x = self.pinky_endpoints(board, powers)
        path = self.determine_path(board, start, endpoint_y, endpoint_x)

        self.path_finding_direction(path)

    def pinky_endpoints(self, board, powers) -> tuple:
        ''' This function primarily just returns the endpoints from the method
            pinky_avoiding_wall. The difference is that it accounts for the direction
            and adds a change in x or y depending on that direction. '''
        if powers.direction == 'Left':
            return self.pinky_ambush(board, powers, 0, -1)

        elif powers.direction == 'Right':
            return self.pinky_ambush(board, powers, 0, 1)

        elif powers.direction == 'Up':
            return self.pinky_ambush(board, powers, -1, 0)

        elif powers.direction == 'Down':
            return self.pinky_ambush(board, powers, 1, 0)

    def pinky_ambush(self, board, powers, dy, dx) -> tuple:
        ''' This function is used to get ahead of Pacman to ambush him.
            The max distance to get ahead is set in the local variable
            ambush_limit. The ambush limit is less if ahead of Pacman
            is a wall, or the distance is not within board boundaries. '''
        ambush_limit = 7
        endpoint_y, endpoint_x = powers.return_location()

        if self.pacman_within_pinky_proximity(endpoint_y, endpoint_x, ambush_limit):
            return endpoint_y, endpoint_x

        else:
            return self.ambush_loop(board, dy, dx, endpoint_y, endpoint_x, ambush_limit)

    def pacman_within_pinky_proximity(self, end_y, end_x, limit):
        ''' This function checks if an ambush is necessary depending on the distance between
            Pinky and Pacman. '''
        return abs(self.y - end_y) < limit and abs(self.x - end_x) < limit

    def ambush_loop(self, board, dy, dx, endpoint_y, endpoint_x, ambush_limit):
        ''' If the distance between Pinky and Pacman is too great, than this function is called to
            find a distance within ambush_limit ahead of Pacman so that Pinky can ambush him. '''
        for i in range(1, ambush_limit):
            # If the loop can not be completed, then Pinky's endpoints are the slightly adjusted endpoints
            if self.pinkys_movement_not_within_board(board, endpoint_y + dy, endpoint_x + dx) or \
                    type(board[endpoint_y + dy][endpoint_x + dx]) == Wall:
                break

            # Else, the endpoints are getting ahead of Pacman
            else:
                endpoint_y += dy
                endpoint_x += dx

        return endpoint_y, endpoint_x

    def pinkys_movement_not_within_board(self, board, endpoint_dy, endpoint_dx) -> bool:
        ''' Returns a boolean if the endpoints are not within the board boundaries. '''
        return not ((0 <= endpoint_dy <= len(board) - 1) and (0 <= endpoint_dx <= board.board_width() - 1))

    # Clyde Movement Functions #

    def clyde_movement(self, board) -> None:
        ''' Clyde's movement is random, and he does not chase or ambush. That
            is why it is not required for him to have any endpoint arguments. '''
        choice = self.random_choice()
        self._inky_and_clyde_movement_turns()
        self.random_direction(choice)

        if self.valid_direction(board):
            self.enemy_moved()
        else:
            self.clydes_wrong_direction()

    def clydes_wrong_direction(self) -> None:
        ''' If clyde has a wrong direction, then his movement_turns are automatically
            set to 0 so that he can make a random choice on which direction to go.
            Must specific if enemy is clyde, because Inky can have any three of the
            other enemy's directions, and this is not the case for him. '''
        if self.enemy_type == Agent.clyde:
            self.movement_turns = 0
            self.last_choice = None

        self.last_location = self.return_location()

    def _inky_and_clyde_movement_turns(self) -> None:
        ''' Inky and clyde are the only enemy with movement_turns attribute, because
            their movement is based off a random choice that last for 15 updates. '''
        self._decrement_movement_turns()

        if self.movement_turns == 0:
            self.movement_turns = 15
            self.last_choice = None

    def _decrement_movement_turns(self) -> None:
        ''' Decrements the attribute movement_turns by 1 until it reaches 0,
            but will never stay at 0, or be less than 0. '''
        self.movement_turns -= 1

    # Direction and Movement Functions #
    def random_direction(self, choice) -> None:
        ''' Splits the chances into 1/4 for each direction, and is randomly chosen. '''
        if choice <= .25:
            self.direction = 'Left'

        elif choice <= .50:
            self.direction = 'Right'

        elif choice <= .75:
            self.direction = 'Down'

        elif choice <= 1:
            self.direction = 'Up'

    def valid_direction(self, board) -> bool:
        ''' Validates if the direction on the board will bump them into a wall.
            If it is not a wall, it returns true and is a valid direction, otherwise
            returns false. '''
        y, x = self.return_location()

        if self.direction == 'Left':
            return type(board[y][x - 1]) != Wall

        elif self.direction == 'Right':
            return type(board[y][x + 1]) != Wall

        elif self.direction == 'Down':
            return type(board[y + 1][x]) != Wall

        elif self.direction == 'Up':
            return type(board[y - 1][x]) != Wall

    def random_choice(self) -> int or float:
        ''' Inky and clyde have unstable movement, but the movement choices occur every 15 updates.
            So the last choice is saved to keep it going for 15 updates in a row. '''
        if self.movement_turns == 15 or self.last_choice == None:
            self.last_choice = random()

        return self.last_choice

    def enemy_moved(self) -> None:
        ''' Once an enemy has moved, their current location is saved, and
            then movement is called that places them in a new location. '''
        self.last_location = self.return_location()

        if self.invulnerable:
            self.movement()

        else:
            self.slowed_movement()

    def slowed_movement(self) -> None:
        ''' This movement is made so that it will move a board square ever other update. This will
            immitate a slowed down movement, and Pacman will be capable of catching up and eating
            an enemy at this speed. This function skips a movement call every other update. '''
        if self.slowed_down:
            self.slowed_down = False

        else:
            self.movement()

    # Pathfinding Functions #
    def path_finding_direction(self, path):
        ''' This function is what changes the direction depending on the next location
            the enemy needs to go. Only one case will follow each time and then once that
            direction is set, the location is saved, and movement() is called to move the
            enemy. '''
        if self.not_empty_path(path):
            distance = self._path_length(path)

            if self.y < path[distance][1]:
                self.direction = 'Down'

            elif self.y > path[distance][1]:
                self.direction = 'Up'

            elif self.x < path[distance][0]:
                self.direction = 'Right'

            elif self.x > path[distance][0]:
                self.direction = 'Left'

            self.enemy_moved()

    def breadth_first_search(self, board, start, endpoint_y, endpoint_x) -> deque:
        ''' The bfs algorithm is required in order to transverse through the
            2d board and find the quickest path that leads directly to the endpoint
            locations. '''
        queue = deque([[start]])
        seen = set([start])
        gamestate = board.Gamestate

        while queue:
            path = queue.popleft()
            x, y = path[-1]

            if (y, x) == (endpoint_y, endpoint_x):
                return path

            for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if self.wanted_path_indexes(board, gamestate, seen, x2, y2):
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))

    def astar_search(self, board, start, endpoint_y, endpoint_x) -> deque:
        # Implementation of A* search algorithm
        came_from = {}
        open_list = [(start, 0)]  # Priority queue (node, f_score)
        g_score = {start: 0}  # Cost from start node to each explored node

        while open_list:
            current, _ = heappop(open_list)

            if current == (endpoint_y, endpoint_x):
                # Reconstruct path from start to endpoint
                path = deque()
                while current in came_from:
                    path.appendleft(current)
                    current = came_from[current]
                return path

            for neighbor in board.get_valid_neighbors(current[0], current[1]):
                # Calculate tentative g score
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # This path to the neighbor is better than any previous one
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + board.heuristic(neighbor, (endpoint_y, endpoint_x))
                    heappush(open_list, (neighbor, f_score))

        # No path found
        return deque()

    def dfs_search(self, board, start, endpoint_y, endpoint_x) -> deque:
    # Implementation of Depth-First Search algorithm
        came_from = {}
        stack = [(start, None)]  # Stack (node, parent)

        while stack:
            current, parent = stack.pop()

            if current == (endpoint_y, endpoint_x):
                # Reconstruct path from start to endpoint
                path = deque()
                while current is not None:
                    path.appendleft(current)
                    current = came_from[current]
                return path

            for neighbor in board.get_valid_neighbors(current[0], current[1]):
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    stack.append((neighbor, current))

        # No path found
        return deque()

    def dijkstra_search(self, board, start, endpoint_y, endpoint_x) -> deque:
        # Implementation of Dijkstra's Algorithm
        came_from = {}
        open_set = {(start, 0)}  # Priority queue (node, cost)
        g_score = {start: 0}  # Cost from start node to each explored node

        while open_set:
            current, _ = min(open_set, key=lambda x: x[1])
            open_set.remove((current, g_score[current]))

            if current == (endpoint_y, endpoint_x):
                # Reconstruct path from start to endpoint
                path = deque()
                while current is not None:
                    path.appendleft(current)
                    current = came_from[current]
                return path

            for neighbor in board.get_valid_neighbors(current[0], current[1]):
                tentative_g_score = g_score[current] + 1  # Assuming uniform edge cost of 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    open_set.add((neighbor, tentative_g_score))

        # No path found
        return deque()

    def wanted_path_indexes(self, board, gamestate, seen, x, y) -> bool:
        ''' To be a wanted index, x and y have to be within the board boundaries.
            The position of y, x on the board also can not be a wall, since we need
            a valid path. And (x, y) can not be duplicated, so must not be in the set seen. '''
        return 0 <= x < board.board_width() and \
            0 <= y < len(board) and \
            type(gamestate[y][x]) != Wall and \
            (x, y) not in seen

    def _path_length(self, path) -> int:
        ''' This function is a helper function to avoid index errors depending on
            how large the path is. If the path is larger than 1, we can just get
            the [1] index of the list for the next location. Otherwise, if it is
            only 1, we do [0] since a list of length 1 only has that index value. '''
        if len(path) > 1:
            return 1
        else:
            return 0

    def not_empty_path(self, path) -> bool:
        ''' Returns a boolean if the path is not empty. '''
        return path is not None and path != []
from character import Character
from wall import Wall
from collections import deque
from random import random
from heapq import heappush, heappop


class Agent(Character):
    inky = 5
    blinky = 6
    pinky = 7
    clyde = 8

    def __init__(self, x, y, enemy_type, images, algorithm,  direction=None,):
        ''' Initializes an Enemy class that inherits from the Character Class. The enemy class
            is one of the two classes that has movement involved, and different attributes to
            represent the state. The enemy_type is given by argument, and there are 4 different enemy
            types because each enemy is unique. '''
        Character.__init__(self, x, y, direction)
        self.enemy_type = enemy_type
        self.invulnerable = True
        self.slowed_down = False
        self.determine_image(enemy_type, images)
        self.pickup_memory = None
        self.algorithm = algorithm

        if enemy_type == Agent.inky or enemy_type == Agent.clyde:  # Only Inky and Clyde require these Attributes
            self.movement_turns = 15
            self.last_choice = None

    def discard_pickup(self) -> None:
        ''' This function is called when an enemy was holding a pickup and then discards
            it, and is used as memory. '''
        self.pickup_memory = None

    def determine_image(self, enemy_type, images) -> None:
        ''' Image display to player is determined by which type of enemy it is. If the enemy
            is not invulnerable, then they all have the same common vulnerable ghost image. '''
        if self.invulnerable:
            if enemy_type == Agent.inky:
                self._image = images.return_image('inky')

            elif enemy_type == Agent.blinky:
                self._image = images.return_image('blinky')

            elif enemy_type == Agent.pinky:
                self._image = images.return_image('pinky')

            elif enemy_type == Agent.clyde:
                self._image = images.return_image('clyde')

        else:
            self._image = images.return_image('vulnerable_ghost')

    def determine_path(self, board, start, endpoint_y, endpoint_x) -> deque:
        if self.invulnerable:
            # Use A* search algorithm
            if self.algorithm == "AStar":
                return self.astar_search(board, start, endpoint_y, endpoint_x)
            # Use Depth-first search algorithm
            elif self.algorithm == "DFS":
                return self.dfs_search(board, start, endpoint_y, endpoint_x)
            # Use Dijkstra's algorithm
            elif self.algorithm == "Dijkstra":
                return self.dijkstra_search(board, start, endpoint_y, endpoint_x)
            # Use Breadth First Search's algorithm
            elif self.algorithm == "BFS":
                return self.breadth_first_search(board, start, endpoint_y, endpoint_x)
            else:
                raise ValueError
        else:
            return self.breadth_first_search(board, start, self.start_location[1], self.start_location[0])[:-1]

    def determineDirection(self, board, powers) -> None:
        ''' Direction is determined by the enemy type. Since each enemy type
            has their own unique game movement. '''
        start = self.x, self.y

        if self.enemy_type == Agent.blinky:
            self.blinky_movement(board, start, powers)

        elif self.enemy_type == Agent.inky:
            self.inky_movement(board, start, powers)

        if self.enemy_type == Agent.pinky:
            self.pinky_movement(board, start, powers)

        elif self.enemy_type == Agent.clyde:
            self.clyde_movement(board)

    # Inky Movement Functions #
    def blinky_movement(self, board, start, powers) -> None:
        ''' Blinky's movement is to directly chase Pacman on the board. '''
        path = self.determine_path(board, start, powers.y, powers.x)
        self.path_finding_direction(path)

    # Blinky Movement Functions #
    def inky_movement(self, board, start, powers) -> None:
        ''' Inky's movement differentiates between the other three ghost. So we use
            random() from the random library to determine which movement he will follow,
            and it will constantly be changing as time goes on. '''
        choice = self.random_choice()
        self._inky_and_clyde_movement_turns()

        if choice <= .33:
            self.blinky_movement(board, start, powers)

        elif choice <= .75:
            self.clyde_movement(board)

        elif choice <= 1:
            self.pinky_movement(board, start, powers)

    # Pinky Movement Functions #

    def pinky_movement(self, board, start, powers):
        ''' Pinky's movement is meant to ambush, so we have the entire pacman object
            so that are we able to look at his direction and coordinates. '''
        endpoint_y, endpoint_x = self.pinky_endpoints(board, powers)
        path = self.determine_path(board, start, endpoint_y, endpoint_x)

        self.path_finding_direction(path)

    def pinky_endpoints(self, board, powers) -> tuple:
        ''' This function primarily just returns the endpoints from the method
            pinky_avoiding_wall. The difference is that it accounts for the direction
            and adds a change in x or y depending on that direction. '''
        if powers.direction == 'Left':
            return self.pinky_ambush(board, powers, 0, -1)

        elif powers.direction == 'Right':
            return self.pinky_ambush(board, powers, 0, 1)

        elif powers.direction == 'Up':
            return self.pinky_ambush(board, powers, -1, 0)

        elif powers.direction == 'Down':
            return self.pinky_ambush(board, powers, 1, 0)

    def pinky_ambush(self, board, powers, dy, dx) -> tuple:
        ''' This function is used to get ahead of Pacman to ambush him.
            The max distance to get ahead is set in the local variable
            ambush_limit. The ambush limit is less if ahead of Pacman
            is a wall, or the distance is not within board boundaries. '''
        ambush_limit = 7
        endpoint_y, endpoint_x = powers.return_location()

        if self.pacman_within_pinky_proximity(endpoint_y, endpoint_x, ambush_limit):
            return endpoint_y, endpoint_x

        else:
            return self.ambush_loop(board, dy, dx, endpoint_y, endpoint_x, ambush_limit)

    def pacman_within_pinky_proximity(self, end_y, end_x, limit):
        ''' This function checks if an ambush is necessary depending on the distance between
            Pinky and Pacman. '''
        return abs(self.y - end_y) < limit and abs(self.x - end_x) < limit

    def ambush_loop(self, board, dy, dx, endpoint_y, endpoint_x, ambush_limit):
        ''' If the distance between Pinky and Pacman is too great, than this function is called to
            find a distance within ambush_limit ahead of Pacman so that Pinky can ambush him. '''
        for i in range(1, ambush_limit):
            # If the loop can not be completed, then Pinky's endpoints are the slightly adjusted endpoints
            if self.pinkys_movement_not_within_board(board, endpoint_y + dy, endpoint_x + dx) or \
                    type(board[endpoint_y + dy][endpoint_x + dx]) == Wall:
                break

            # Else, the endpoints are getting ahead of Pacman
            else:
                endpoint_y += dy
                endpoint_x += dx

        return endpoint_y, endpoint_x

    def pinkys_movement_not_within_board(self, board, endpoint_dy, endpoint_dx) -> bool:
        ''' Returns a boolean if the endpoints are not within the board boundaries. '''
        return not ((0 <= endpoint_dy <= len(board) - 1) and (0 <= endpoint_dx <= board.board_width() - 1))

    # Clyde Movement Functions #

    def clyde_movement(self, board) -> None:
        ''' Clyde's movement is random, and he does not chase or ambush. That
            is why it is not required for him to have any endpoint arguments. '''
        choice = self.random_choice()
        self._inky_and_clyde_movement_turns()
        self.random_direction(choice)

        if self.valid_direction(board):
            self.enemy_moved()
        else:
            self.clydes_wrong_direction()

    def clydes_wrong_direction(self) -> None:
        ''' If clyde has a wrong direction, then his movement_turns are automatically
            set to 0 so that he can make a random choice on which direction to go.
            Must specific if enemy is clyde, because Inky can have any three of the
            other enemy's directions, and this is not the case for him. '''
        if self.enemy_type == Agent.clyde:
            self.movement_turns = 0
            self.last_choice = None

        self.last_location = self.return_location()

    def _inky_and_clyde_movement_turns(self) -> None:
        ''' Inky and clyde are the only enemy with movement_turns attribute, because
            their movement is based off a random choice that last for 15 updates. '''
        self._decrement_movement_turns()

        if self.movement_turns == 0:
            self.movement_turns = 15
            self.last_choice = None

    def _decrement_movement_turns(self) -> None:
        ''' Decrements the attribute movement_turns by 1 until it reaches 0,
            but will never stay at 0, or be less than 0. '''
        self.movement_turns -= 1

    # Direction and Movement Functions #
    def random_direction(self, choice) -> None:
        ''' Splits the chances into 1/4 for each direction, and is randomly chosen. '''
        if choice <= .25:
            self.direction = 'Left'

        elif choice <= .50:
            self.direction = 'Right'

        elif choice <= .75:
            self.direction = 'Down'

        elif choice <= 1:
            self.direction = 'Up'

    def valid_direction(self, board) -> bool:
        ''' Validates if the direction on the board will bump them into a wall.
            If it is not a wall, it returns true and is a valid direction, otherwise
            returns false. '''
        y, x = self.return_location()

        if self.direction == 'Left':
            return type(board[y][x - 1]) != Wall

        elif self.direction == 'Right':
            return type(board[y][x + 1]) != Wall

        elif self.direction == 'Down':
            return type(board[y + 1][x]) != Wall

        elif self.direction == 'Up':
            return type(board[y - 1][x]) != Wall

    def random_choice(self) -> int or float:
        ''' Inky and clyde have unstable movement, but the movement choices occur every 15 updates.
            So the last choice is saved to keep it going for 15 updates in a row. '''
        if self.movement_turns == 15 or self.last_choice == None:
            self.last_choice = random()

        return self.last_choice

    def enemy_moved(self) -> None:
        ''' Once an enemy has moved, their current location is saved, and
            then movement is called that places them in a new location. '''
        self.last_location = self.return_location()

        if self.invulnerable:
            self.movement()

        else:
            self.slowed_movement()

    def slowed_movement(self) -> None:
        ''' This movement is made so that it will move a board square ever other update. This will
            immitate a slowed down movement, and Pacman will be capable of catching up and eating
            an enemy at this speed. This function skips a movement call every other update. '''
        if self.slowed_down:
            self.slowed_down = False

        else:
            self.movement()

    # Pathfinding Functions #
    def path_finding_direction(self, path):
        ''' This function is what changes the direction depending on the next location
            the enemy needs to go. Only one case will follow each time and then once that
            direction is set, the location is saved, and movement() is called to move the
            enemy. '''
        if self.not_empty_path(path):
            distance = self._path_length(path)

            if self.y < path[distance][1]:
                self.direction = 'Down'

            elif self.y > path[distance][1]:
                self.direction = 'Up'

            elif self.x < path[distance][0]:
                self.direction = 'Right'

            elif self.x > path[distance][0]:
                self.direction = 'Left'

            self.enemy_moved()

    def breadth_first_search(self, board, start, endpoint_y, endpoint_x) -> deque:
        ''' The bfs algorithm is required in order to transverse through the
            2d board and find the quickest path that leads directly to the endpoint
            locations. '''
        queue = deque([[start]])
        seen = set([start])
        gamestate = board.Gamestate

        while queue:
            path = queue.popleft()
            x, y = path[-1]

            if (y, x) == (endpoint_y, endpoint_x):
                return path

            for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if self.wanted_path_indexes(board, gamestate, seen, x2, y2):
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))

    def astar_search(self, board, start, endpoint_y, endpoint_x) -> deque:
        # Implementation of A* search algorithm
        came_from = {}
        open_list = [(start, 0)]  # Priority queue (node, f_score)
        g_score = {start: 0}  # Cost from start node to each explored node

        while open_list:
            current, _ = heappop(open_list)

            if current == (endpoint_y, endpoint_x):
                # Reconstruct path from start to endpoint
                path = deque()
                while current in came_from:
                    path.appendleft(current)
                    current = came_from[current]
                return path

            for neighbor in board.get_valid_neighbors(current[0], current[1]):
                # Calculate tentative g score
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # This path to the neighbor is better than any previous one
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + board.heuristic(neighbor, (endpoint_y, endpoint_x))
                    heappush(open_list, (neighbor, f_score))

        # No path found
        return deque()

    def dfs_search(self, board, start, endpoint_y, endpoint_x) -> deque:
    # Implementation of Depth-First Search algorithm
        came_from = {}
        stack = [(start, None)]  # Stack (node, parent)

        while stack:
            current, parent = stack.pop()

            if current == (endpoint_y, endpoint_x):
                # Reconstruct path from start to endpoint
                path = deque()
                while current is not None:
                    path.appendleft(current)
                    current = came_from[current]
                return path

            for neighbor in board.get_valid_neighbors(current[0], current[1]):
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    stack.append((neighbor, current))

        # No path found
        return deque()

    def dijkstra_search(self, board, start, endpoint_y, endpoint_x) -> deque:
        # Implementation of Dijkstra's Algorithm
        came_from = {}
        open_set = {(start, 0)}  # Priority queue (node, cost)
        g_score = {start: 0}  # Cost from start node to each explored node

        while open_set:
            current, _ = min(open_set, key=lambda x: x[1])
            open_set.remove((current, g_score[current]))

            if current == (endpoint_y, endpoint_x):
                # Reconstruct path from start to endpoint
                path = deque()
                while current is not None:
                    path.appendleft(current)
                    current = came_from[current]
                return path

            for neighbor in board.get_valid_neighbors(current[0], current[1]):
                tentative_g_score = g_score[current] + 1  # Assuming uniform edge cost of 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    open_set.add((neighbor, tentative_g_score))

        # No path found
        return deque()

    def wanted_path_indexes(self, board, gamestate, seen, x, y) -> bool:
        ''' To be a wanted index, x and y have to be within the board boundaries.
            The position of y, x on the board also can not be a wall, since we need
            a valid path. And (x, y) can not be duplicated, so must not be in the set seen. '''
        return 0 <= x < board.board_width() and \
            0 <= y < len(board) and \
            type(gamestate[y][x]) != Wall and \
            (x, y) not in seen

    def _path_length(self, path) -> int:
        ''' This function is a helper function to avoid index errors depending on
            how large the path is. If the path is larger than 1, we can just get
            the [1] index of the list for the next location. Otherwise, if it is
            only 1, we do [0] since a list of length 1 only has that index value. '''
        if len(path) > 1:
            return 1
        else:
            return 0

    def not_empty_path(self, path) -> bool:
        ''' Returns a boolean if the path is not empty. '''
        return path is not None and path != []
from character import Character
from wall import Wall
from collections import deque
from random import random
from heapq import heappush, heappop


class Agent(Character):
    inky = 5
    blinky = 6
    pinky = 7
    clyde = 8

    def __init__(self, x, y, enemy_type, images, algorithm,  direction=None,):
        ''' Initializes an Enemy class that inherits from the Character Class. The enemy class
            is one of the two classes that has movement involved, and different attributes to
            represent the state. The enemy_type is given by argument, and there are 4 different enemy
            types because each enemy is unique. '''
        Character.__init__(self, x, y, direction)
        self.enemy_type = enemy_type
        self.invulnerable = True
        self.slowed_down = False
        self.determine_image(enemy_type, images)
        self.pickup_memory = None
        self.algorithm = algorithm

        if enemy_type == Agent.inky or enemy_type == Agent.clyde:  # Only Inky and Clyde require these Attributes
            self.movement_turns = 15
            self.last_choice = None

    def discard_pickup(self) -> None:
        ''' This function is called when an enemy was holding a pickup and then discards
            it, and is used as memory. '''
        self.pickup_memory = None

    def determine_image(self, enemy_type, images) -> None:
        ''' Image display to player is determined by which type of enemy it is. If the enemy
            is not invulnerable, then they all have the same common vulnerable ghost image. '''
        if self.invulnerable:
            if enemy_type == Agent.inky:
                self._image = images.return_image('inky')

            elif enemy_type == Agent.blinky:
                self._image = images.return_image('blinky')

            elif enemy_type == Agent.pinky:
                self._image = images.return_image('pinky')

            elif enemy_type == Agent.clyde:
                self._image = images.return_image('clyde')

        else:
            self._image = images.return_image('vulnerable_ghost')

    def determine_path(self, board, start, endpoint_y, endpoint_x) -> deque:
        if self.invulnerable:
            # Use A* search algorithm
            if self.algorithm == "AStar":
                return self.astar_search(board, start, endpoint_y, endpoint_x)
            # Use Depth-first search algorithm
            elif self.algorithm == "DFS":
                return self.dfs_search(board, start, endpoint_y, endpoint_x)
            # Use Dijkstra's algorithm
            elif self.algorithm == "Dijkstra":
                return self.dijkstra_search(board, start, endpoint_y, endpoint_x)
            # Use Breadth First Search's algorithm
            elif self.algorithm == "BFS":
                return self.breadth_first_search(board, start, endpoint_y, endpoint_x)
            else:
                raise ValueError
        else:
            return self.breadth_first_search(board, start, self.start_location[1], self.start_location[0])[:-1]

    def determineDirection(self, board, powers) -> None:
        ''' Direction is determined by the enemy type. Since each enemy type
            has their own unique game movement. '''
        start = self.x, self.y

        if self.enemy_type == Agent.blinky:
            self.blinky_movement(board, start, powers)

        elif self.enemy_type == Agent.inky:
            self.inky_movement(board, start, powers)

        if self.enemy_type == Agent.pinky:
            self.pinky_movement(board, start, powers)

        elif self.enemy_type == Agent.clyde:
            self.clyde_movement(board)

    # Inky Movement Functions #
    def blinky_movement(self, board, start, powers) -> None:
        ''' Blinky's movement is to directly chase Pacman on the board. '''
        path = self.determine_path(board, start, powers.y, powers.x)
        self.path_finding_direction(path)

    # Blinky Movement Functions #
    def inky_movement(self, board, start, powers) -> None:
        ''' Inky's movement differentiates between the other three ghost. So we use
            random() from the random library to determine which movement he will follow,
            and it will constantly be changing as time goes on. '''
        choice = self.random_choice()
        self._inky_and_clyde_movement_turns()

        if choice <= .33:
            self.blinky_movement(board, start, powers)

        elif choice <= .75:
            self.clyde_movement(board)

        elif choice <= 1:
            self.pinky_movement(board, start, powers)

    # Pinky Movement Functions #

    def pinky_movement(self, board, start, powers):
        ''' Pinky's movement is meant to ambush, so we have the entire pacman object
            so that are we able to look at his direction and coordinates. '''
        endpoint_y, endpoint_x = self.pinky_endpoints(board, powers)
        path = self.determine_path(board, start, endpoint_y, endpoint_x)

        self.path_finding_direction(path)

    def pinky_endpoints(self, board, powers) -> tuple:
        ''' This function primarily just returns the endpoints from the method
            pinky_avoiding_wall. The difference is that it accounts for the direction
            and adds a change in x or y depending on that direction. '''
        if powers.direction == 'Left':
            return self.pinky_ambush(board, powers, 0, -1)

        elif powers.direction == 'Right':
            return self.pinky_ambush(board, powers, 0, 1)

        elif powers.direction == 'Up':
            return self.pinky_ambush(board, powers, -1, 0)

        elif powers.direction == 'Down':
            return self.pinky_ambush(board, powers, 1, 0)

    def pinky_ambush(self, board, powers, dy, dx) -> tuple:
        ''' This function is used to get ahead of Pacman to ambush him.
            The max distance to get ahead is set in the local variable
            ambush_limit. The ambush limit is less if ahead of Pacman
            is a wall, or the distance is not within board boundaries. '''
        ambush_limit = 7
        endpoint_y, endpoint_x = powers.return_location()

        if self.pacman_within_pinky_proximity(endpoint_y, endpoint_x, ambush_limit):
            return endpoint_y, endpoint_x

        else:
            return self.ambush_loop(board, dy, dx, endpoint_y, endpoint_x, ambush_limit)

    def pacman_within_pinky_proximity(self, end_y, end_x, limit):
        ''' This function checks if an ambush is necessary depending on the distance between
            Pinky and Pacman. '''
        return abs(self.y - end_y) < limit and abs(self.x - end_x) < limit

    def ambush_loop(self, board, dy, dx, endpoint_y, endpoint_x, ambush_limit):
        ''' If the distance between Pinky and Pacman is too great, than this function is called to
            find a distance within ambush_limit ahead of Pacman so that Pinky can ambush him. '''
        for i in range(1, ambush_limit):
            # If the loop can not be completed, then Pinky's endpoints are the slightly adjusted endpoints
            if self.pinkys_movement_not_within_board(board, endpoint_y + dy, endpoint_x + dx) or \
                    type(board[endpoint_y + dy][endpoint_x + dx]) == Wall:
                break

            # Else, the endpoints are getting ahead of Pacman
            else:
                endpoint_y += dy
                endpoint_x += dx

        return endpoint_y, endpoint_x

    def pinkys_movement_not_within_board(self, board, endpoint_dy, endpoint_dx) -> bool:
        ''' Returns a boolean if the endpoints are not within the board boundaries. '''
        return not ((0 <= endpoint_dy <= len(board) - 1) and (0 <= endpoint_dx <= board.board_width() - 1))

    # Clyde Movement Functions #

    def clyde_movement(self, board) -> None:
        ''' Clyde's movement is random, and he does not chase or ambush. That
            is why it is not required for him to have any endpoint arguments. '''
        choice = self.random_choice()
        self._inky_and_clyde_movement_turns()
        self.random_direction(choice)

        if self.valid_direction(board):
            self.enemy_moved()
        else:
            self.clydes_wrong_direction()

    def clydes_wrong_direction(self) -> None:
        ''' If clyde has a wrong direction, then his movement_turns are automatically
            set to 0 so that he can make a random choice on which direction to go.
            Must specific if enemy is clyde, because Inky can have any three of the
            other enemy's directions, and this is not the case for him. '''
        if self.enemy_type == Agent.clyde:
            self.movement_turns = 0
            self.last_choice = None

        self.last_location = self.return_location()

    def _inky_and_clyde_movement_turns(self) -> None:
        ''' Inky and clyde are the only enemy with movement_turns attribute, because
            their movement is based off a random choice that last for 15 updates. '''
        self._decrement_movement_turns()

        if self.movement_turns == 0:
            self.movement_turns = 15
            self.last_choice = None

    def _decrement_movement_turns(self) -> None:
        ''' Decrements the attribute movement_turns by 1 until it reaches 0,
            but will never stay at 0, or be less than 0. '''
        self.movement_turns -= 1

    # Direction and Movement Functions #
    def random_direction(self, choice) -> None:
        ''' Splits the chances into 1/4 for each direction, and is randomly chosen. '''
        if choice <= .25:
            self.direction = 'Left'

        elif choice <= .50:
            self.direction = 'Right'

        elif choice <= .75:
            self.direction = 'Down'

        elif choice <= 1:
            self.direction = 'Up'

    def valid_direction(self, board) -> bool:
        ''' Validates if the direction on the board will bump them into a wall.
            If it is not a wall, it returns true and is a valid direction, otherwise
            returns false. '''
        y, x = self.return_location()

        if self.direction == 'Left':
            return type(board[y][x - 1]) != Wall

        elif self.direction == 'Right':
            return type(board[y][x + 1]) != Wall

        elif self.direction == 'Down':
            return type(board[y + 1][x]) != Wall

        elif self.direction == 'Up':
            return type(board[y - 1][x]) != Wall

    def random_choice(self) -> int or float:
        ''' Inky and clyde have unstable movement, but the movement choices occur every 15 updates.
            So the last choice is saved to keep it going for 15 updates in a row. '''
        if self.movement_turns == 15 or self.last_choice == None:
            self.last_choice = random()

        return self.last_choice

    def enemy_moved(self) -> None:
        ''' Once an enemy has moved, their current location is saved, and
            then movement is called that places them in a new location. '''
        self.last_location = self.return_location()

        if self.invulnerable:
            self.movement()

        else:
            self.slowed_movement()

    def slowed_movement(self) -> None:
        ''' This movement is made so that it will move a board square ever other update. This will
            immitate a slowed down movement, and Pacman will be capable of catching up and eating
            an enemy at this speed. This function skips a movement call every other update. '''
        if self.slowed_down:
            self.slowed_down = False

        else:
            self.movement()

    # Pathfinding Functions #
    def path_finding_direction(self, path):
        ''' This function is what changes the direction depending on the next location
            the enemy needs to go. Only one case will follow each time and then once that
            direction is set, the location is saved, and movement() is called to move the
            enemy. '''
        if self.not_empty_path(path):
            distance = self._path_length(path)

            if self.y < path[distance][1]:
                self.direction = 'Down'

            elif self.y > path[distance][1]:
                self.direction = 'Up'

            elif self.x < path[distance][0]:
                self.direction = 'Right'

            elif self.x > path[distance][0]:
                self.direction = 'Left'

            self.enemy_moved()

    def breadth_first_search(self, board, start, endpoint_y, endpoint_x) -> deque:
        ''' The bfs algorithm is required in order to transverse through the
            2d board and find the quickest path that leads directly to the endpoint
            locations. '''
        queue = deque([[start]])
        seen = set([start])
        gamestate = board.Gamestate

        while queue:
            path = queue.popleft()
            x, y = path[-1]

            if (y, x) == (endpoint_y, endpoint_x):
                return path

            for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if self.wanted_path_indexes(board, gamestate, seen, x2, y2):
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))

    def astar_search(self, board, start, endpoint_y, endpoint_x) -> deque:
        # Implementation of A* search algorithm
        came_from = {}
        open_list = [(start, 0)]  # Priority queue (node, f_score)
        g_score = {start: 0}  # Cost from start node to each explored node

        while open_list:
            current, _ = heappop(open_list)

            if current == (endpoint_y, endpoint_x):
                # Reconstruct path from start to endpoint
                path = deque()
                while current in came_from:
                    path.appendleft(current)
                    current = came_from[current]
                return path

            for neighbor in board.get_valid_neighbors(current[0], current[1]):
                # Calculate tentative g score
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # This path to the neighbor is better than any previous one
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + board.heuristic(neighbor, (endpoint_y, endpoint_x))
                    heappush(open_list, (neighbor, f_score))

        # No path found
        return deque()

    def dfs_search(self, board, start, endpoint_y, endpoint_x) -> deque:
    # Implementation of Depth-First Search algorithm
        came_from = {}
        stack = [(start, None)]  # Stack (node, parent)

        while stack:
            current, parent = stack.pop()

            if current == (endpoint_y, endpoint_x):
                # Reconstruct path from start to endpoint
                path = deque()
                while current is not None:
                    path.appendleft(current)
                    current = came_from[current]
                return path

            for neighbor in board.get_valid_neighbors(current[0], current[1]):
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    stack.append((neighbor, current))

        # No path found
        return deque()

    def dijkstra_search(self, board, start, endpoint_y, endpoint_x) -> deque:
        # Implementation of Dijkstra's Algorithm
        came_from = {}
        open_set = {(start, 0)}  # Priority queue (node, cost)
        g_score = {start: 0}  # Cost from start node to each explored node

        while open_set:
            current, _ = min(open_set, key=lambda x: x[1])
            open_set.remove((current, g_score[current]))

            if current == (endpoint_y, endpoint_x):
                # Reconstruct path from start to endpoint
                path = deque()
                while current is not None:
                    path.appendleft(current)
                    current = came_from[current]
                return path

            for neighbor in board.get_valid_neighbors(current[0], current[1]):
                tentative_g_score = g_score[current] + 1  # Assuming uniform edge cost of 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    open_set.add((neighbor, tentative_g_score))

        # No path found
        return deque()

    def wanted_path_indexes(self, board, gamestate, seen, x, y) -> bool:
        ''' To be a wanted index, x and y have to be within the board boundaries.
            The position of y, x on the board also can not be a wall, since we need
            a valid path. And (x, y) can not be duplicated, so must not be in the set seen. '''
        return 0 <= x < board.board_width() and \
            0 <= y < len(board) and \
            type(gamestate[y][x]) != Wall and \
            (x, y) not in seen

    def _path_length(self, path) -> int:
        ''' This function is a helper function to avoid index errors depending on
            how large the path is. If the path is larger than 1, we can just get
            the [1] index of the list for the next location. Otherwise, if it is
            only 1, we do [0] since a list of length 1 only has that index value. '''
        if len(path) > 1:
            return 1
        else:
            return 0

    def not_empty_path(self, path) -> bool:
        ''' Returns a boolean if the path is not empty. '''
        return path is not None and path != []
