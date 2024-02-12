from COLOR import COLOR


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

    def rotate_clockwise(self):
        '''
        To Rotate the agent in Clock Wise direction
        '''
        def pointNew(p, newOrigin):
            return (p[0]-newOrigin[0], p[1]-newOrigin[1])
        cell_width = self._parentMaze._cell_width
        x = self.x*cell_width-cell_width+self._parentMaze._LabWidth
        y = self.y*cell_width-cell_width+self._parentMaze._LabWidth
        center = (y+cell_width/2, x+cell_width/2)
        p1 = pointNew((self._coord[0], self._coord[1]), center)
        p2 = pointNew((self._coord[2], self._coord[3]), center)
        p1_cw = (-p1[1], p1[0])
        p2_cw = (-p2[1], p2[0])
        p1 = p1_cw[0]+center[0], p1_cw[1]+center[1]
        p2 = p2_cw[0]+center[0], p2_cw[1]+center[1]
        self._coord = (*p1, *p2)
        self._parentMaze._canvas.coords(self._head, *self._coord)
        self._orient = (self._orient+1) % 4

    def moveRight(self, event):
        if self._parentMaze.maze_map[self.x, self.y]['E'] == True:
            self.y = self.y+1

    def moveLeft(self, event):
        if self._parentMaze.maze_map[self.x, self.y]['W'] == True:
            self.y = self.y-1

    def moveUp(self, event):
        if self._parentMaze.maze_map[self.x, self.y]['N'] == True:
            self.x = self.x-1
            self.y = self.y

    def moveDown(self, event):
        if self._parentMaze.maze_map[self.x, self.y]['S'] == True:
            self.x = self.x+1
            self.y = self.y
