from COLOR import COLOR
from collections import deque
from random import random
from wall import Wall

class agent:

    def __init__(self, parentMaze, x=None, y=None, shape='square', goal=None, filled=False, footprints=False, color: COLOR = COLOR.blue):

        self._parentMaze = parentMaze
        self.color = color
        if (isinstance(color, str)):
            if (color in COLOR.__members__):
                self.color = COLOR[color]
            else:
                raise ValueError(f'{color} is not a valid COLOR!')
        self.filled = filled
        self.shape = shape
        self._orient = 0
        if x is None:
            x = parentMaze.rows
        if y is None:
            y = parentMaze.cols
        self.x = x
        self.y = y
        self.footprints = footprints
        self._parentMaze._agents.append(self)
        if goal == None:
            self.goal = self._parentMaze._goal
        else:
            self.goal = goal
        self._body = []
        self.position = (self.x, self.y)

    def discard_pickup(self) -> None:
        ''' This function is called when an enemy was holding a pickup and then discards
            it, and is used as memory. '''
        self.pickup_memory = None

    def determine_path(self, board, start, endpoint_y, endpoint_x) -> deque:
        ''' Path is towards endpoint destination if the enemy is invulnerable (the normal case).
            Otherwise, the enemy needs to retreat towards the starting location. '''

        if self.invulnerable:
            return self.breadth_first_search(board, start, endpoint_y, endpoint_x)

        else:
            return self.breadth_first_search(board, start, self.start_location[1], self.start_location[0])[:-1]

    def determineDirection(self, board, pacman) -> None:
        ''' Direction is determined by the enemy type. Since each enemy type
            has their own unique game movement. '''
        start = self.x, self.y

    def rotate_counter_clockwise(self):
        '''
        To Rotate the agent in Counter Clock Wise direction
        '''
        def pointNew(p, newOrigin):
            return (p[0]-newOrigin[0], p[1]-newOrigin[1])
        cell_width = self._parentMaze._cell_width
        x = self.x*cell_width-cell_width+self._parentMaze._LabWidth
        y = self.y*cell_width-cell_width+self._parentMaze._LabWidth
        center = (y+cell_width/2, x+cell_width/2)
        p1 = pointNew((self._coord[0], self._coord[1]), center)
        p2 = pointNew((self._coord[2], self._coord[3]), center)
        p1_cw = (p1[1], -p1[0])
        p2_cw = (p2[1], -p2[0])
        p1 = p1_cw[0]+center[0], p1_cw[1]+center[1]
        p2 = p2_cw[0]+center[0], p2_cw[1]+center[1]
        self._coord = (*p1, *p2)
        self._parentMaze._canvas.coords(self._head, *self._coord)
        self._orient = (self._orient-1) % 4

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
            self.slowed_down = True

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
