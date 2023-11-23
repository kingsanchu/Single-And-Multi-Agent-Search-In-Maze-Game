import random
import datetime
import csv
import os
from tkinter import *
from COLOR import COLOR
from agent import agent
from textLabel import textLabel
from collections import deque




class maze:

    def __init__(self, rows=10, cols=10):

        self.rows = rows
        self.cols = cols
        self.maze_map = {}
        self.grid = []
        self.path = {}
        self._cell_width = 50
        self._win = None
        self._canvas = None
        self._agents = []
        self.markCells = []
        self._LabWidth = 10


    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, n):
        self._grid = []
        y = 0
        for n in range(self.cols):
            x = 1
            y = 1+y
            for m in range(self.rows):
                self.grid.append((x, y))
                self.maze_map[x, y] = {'E': 0, 'W': 0, 'N': 0, 'S': 0}
                x = x + 1

# Removing walls

    def _Open_East(self, x, y):

        self.maze_map[x, y]['E'] = 1
        if y+1 <= self.cols:
            self.maze_map[x, y+1]['W'] = 1

    def _Open_West(self, x, y):
        self.maze_map[x, y]['W'] = 1
        if y-1 > 0:
            self.maze_map[x, y-1]['E'] = 1

    def _Open_North(self, x, y):
        self.maze_map[x, y]['N'] = 1
        if x-1 > 0:
            self.maze_map[x-1, y]['S'] = 1

    def _Open_South(self, x, y):
        self.maze_map[x, y]['S'] = 1
        if x+1 <= self.rows:
            self.maze_map[x+1, y]['N'] = 1

    def CreateMaze(self, x=1, y=1, pattern=None, loopPercent=0, saveMaze=False, loadMaze=None, theme: COLOR = COLOR.dark):

        _stack = []
        _closed = []
        self.theme = theme
        self._goal = (x, y)
        if (isinstance(theme, str)):
            if (theme in COLOR.__members__):
                self.theme = COLOR[theme]
            else:
                raise ValueError(f'{theme} is not a valid theme COLOR!')

        def blockedNeighbours(cell):
            n = []
            for d in self.maze_map[cell].keys():
                if self.maze_map[cell][d] == 0:
                    if d == 'E' and (cell[0], cell[1]+1) in self.grid:
                        n.append((cell[0], cell[1]+1))
                    elif d == 'W' and (cell[0], cell[1]-1) in self.grid:
                        n.append((cell[0], cell[1]-1))
                    elif d == 'N' and (cell[0]-1, cell[1]) in self.grid:
                        n.append((cell[0]-1, cell[1]))
                    elif d == 'S' and (cell[0]+1, cell[1]) in self.grid:
                        n.append((cell[0]+1, cell[1]))
            return n

        def removeWallinBetween(cell1, cell2):

            if cell1[0] == cell2[0]:
                if cell1[1] == cell2[1]+1:
                    self.maze_map[cell1]['W'] = 1
                    self.maze_map[cell2]['E'] = 1
                else:
                    self.maze_map[cell1]['E'] = 1
                    self.maze_map[cell2]['W'] = 1
            else:
                if cell1[0] == cell2[0]+1:
                    self.maze_map[cell1]['N'] = 1
                    self.maze_map[cell2]['S'] = 1
                else:
                    self.maze_map[cell1]['S'] = 1
                    self.maze_map[cell2]['N'] = 1

        def isCyclic(cell1, cell2):

            ans = False
            if cell1[0] == cell2[0]:
                if cell1[1] > cell2[1]:
                    cell1, cell2 = cell2, cell1
                if self.maze_map[cell1]['S'] == 1 and self.maze_map[cell2]['S'] == 1:
                    if (cell1[0]+1, cell1[1]) in self.grid and self.maze_map[(cell1[0]+1, cell1[1])]['E'] == 1:
                        ans = True
                if self.maze_map[cell1]['N'] == 1 and self.maze_map[cell2]['N'] == 1:
                    if (cell1[0]-1, cell1[1]) in self.grid and self.maze_map[(cell1[0]-1, cell1[1])]['E'] == 1:
                        ans = True
            else:
                if cell1[0] > cell2[0]:
                    cell1, cell2 = cell2, cell1
                if self.maze_map[cell1]['E'] == 1 and self.maze_map[cell2]['E'] == 1:
                    if (cell1[0], cell1[1]+1) in self.grid and self.maze_map[(cell1[0], cell1[1]+1)]['S'] == 1:
                        ans = True
                if self.maze_map[cell1]['W'] == 1 and self.maze_map[cell2]['W'] == 1:
                    if (cell1[0], cell1[1]-1) in self.grid and self.maze_map[(cell1[0], cell1[1]-1)]['S'] == 1:
                        ans = True
            return ans

        def BFS(cell):

            frontier = deque()
            frontier.append(cell)
            path = {}
            visited = {(self.rows, self.cols)}
            while len(frontier) > 0:
                cell = frontier.popleft()
                if self.maze_map[cell]['W'] and (cell[0], cell[1]-1) not in visited:
                    nextCell = (cell[0], cell[1]-1)
                    path[nextCell] = cell
                    frontier.append(nextCell)
                    visited.add(nextCell)
                if self.maze_map[cell]['S'] and (cell[0]+1, cell[1]) not in visited:
                    nextCell = (cell[0]+1, cell[1])
                    path[nextCell] = cell
                    frontier.append(nextCell)
                    visited.add(nextCell)
                if self.maze_map[cell]['E'] and (cell[0], cell[1]+1) not in visited:
                    nextCell = (cell[0], cell[1]+1)
                    path[nextCell] = cell
                    frontier.append(nextCell)
                    visited.add(nextCell)
                if self.maze_map[cell]['N'] and (cell[0]-1, cell[1]) not in visited:
                    nextCell = (cell[0]-1, cell[1])
                    path[nextCell] = cell
                    frontier.append(nextCell)
                    visited.add(nextCell)
            fwdPath = {}
            cell = self._goal
            while cell != (self.rows, self.cols):
                try:
                    fwdPath[path[cell]] = cell
                    cell = path[cell]
                except:
                    print('Path to goal not found!')
                    return
            return fwdPath

        # if maze is to be generated randomly
        if not loadMaze:
            _stack.append((x, y))
            _closed.append((x, y))
            biasLength = 2  # if pattern is 'v' or 'h'
            if (pattern is not None and pattern.lower() == 'h'):
                biasLength = max(self.cols//10, 2)
            if (pattern is not None and pattern.lower() == 'v'):
                biasLength = max(self.rows//10, 2)
            bias = 0

            while len(_stack) > 0:
                cell = []
                bias += 1
                if (x, y + 1) not in _closed and (x, y+1) in self.grid:
                    cell.append("E")
                if (x, y-1) not in _closed and (x, y-1) in self.grid:
                    cell.append("W")
                if (x+1, y) not in _closed and (x+1, y) in self.grid:
                    cell.append("S")
                if (x-1, y) not in _closed and (x-1, y) in self.grid:
                    cell.append("N")
                if len(cell) > 0:
                    if pattern is not None and pattern.lower() == 'h' and bias <= biasLength:
                        if ('E' in cell or 'W' in cell):
                            if 'S' in cell:
                                cell.remove('S')
                            if 'N' in cell:
                                cell.remove('N')
                    elif pattern is not None and pattern.lower() == 'v' and bias <= biasLength:
                        if ('N' in cell or 'S' in cell):
                            if 'E' in cell:
                                cell.remove('E')
                            if 'W' in cell:
                                cell.remove('W')
                    else:
                        bias = 0
                    current_cell = (random.choice(cell))
                    if current_cell == "E":
                        self._Open_East(x, y)
                        self.path[x, y+1] = x, y
                        y = y + 1
                        _closed.append((x, y))
                        _stack.append((x, y))

                    elif current_cell == "W":
                        self._Open_West(x, y)
                        self.path[x, y-1] = x, y
                        y = y - 1
                        _closed.append((x, y))
                        _stack.append((x, y))

                    elif current_cell == "N":
                        self._Open_North(x, y)
                        self.path[(x-1, y)] = x, y
                        x = x - 1
                        _closed.append((x, y))
                        _stack.append((x, y))

                    elif current_cell == "S":
                        self._Open_South(x, y)
                        self.path[(x+1, y)] = x, y
                        x = x + 1
                        _closed.append((x, y))
                        _stack.append((x, y))

                else:
                    x, y = _stack.pop()

            # Multiple Path Loops
            if loopPercent != 0:

                x, y = self.rows, self.cols
                pathCells = [(x, y)]
                while x != self.rows or y != self.cols:
                    x, y = self.path[(x, y)]
                    pathCells.append((x, y))
                notPathCells = [i for i in self.grid if i not in pathCells]
                random.shuffle(pathCells)
                random.shuffle(notPathCells)
                pathLength = len(pathCells)
                notPathLength = len(notPathCells)
                count1, count2 = pathLength/3*loopPercent/100, notPathLength/3*loopPercent/100

                # remove blocks from shortest path cells
                count = 0
                i = 0
                while count < count1:  # these many blocks to remove
                    if len(blockedNeighbours(pathCells[i])) > 0:
                        cell = random.choice(blockedNeighbours(pathCells[i]))
                        if not isCyclic(cell, pathCells[i]):
                            removeWallinBetween(cell, pathCells[i])
                            count += 1
                        i += 1

                    else:
                        i += 1
                    if i == len(pathCells):
                        break
                # remove blocks from outside shortest path cells
                if len(notPathCells) > 0:
                    count = 0
                    i = 0
                    while count < count2:  # these many blocks to remove
                        if len(blockedNeighbours(notPathCells[i])) > 0:
                            cell = random.choice(
                                blockedNeighbours(notPathCells[i]))
                            if not isCyclic(cell, notPathCells[i]):
                                removeWallinBetween(cell, notPathCells[i])
                                count += 1
                            i += 1

                        else:
                            i += 1
                        if i == len(notPathCells):
                            break
                self.path = BFS((self.rows, self.cols))
        else:
            # Load maze from CSV file
            with open(loadMaze, 'r') as f:
                last = list(f.readlines())[-1]
                c = last.split(',')
                c[0] = int(c[0].lstrip('"('))
                c[1] = int(c[1].rstrip(')"'))
                self.rows = c[0]
                self.cols = c[1]
                self.grid = []

            with open(loadMaze, 'r') as f:
                r = csv.reader(f)
                next(r)
                for i in r:
                    c = i[0].split(',')
                    c[0] = int(c[0].lstrip('('))
                    c[1] = int(c[1].rstrip(')'))
                    self.maze_map[tuple(c)] = {'E': int(i[1]), 'W': int(
                        i[2]), 'N': int(i[3]), 'S': int(i[4])}
            self.path = BFS((self.rows, self.cols))
        self._drawMaze(self.theme)
        agent(self, *self._goal, shape='square',
              filled=True, color=COLOR.green)
        if saveMaze:
            dt_string = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
            with open(f'maze--{dt_string}.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['  cell  ', 'E', 'W', 'N', 'S'])
                for k, v in self.maze_map.items():
                    entry = [k]
                    for i in v.values():
                        entry.append(i)
                    writer.writerow(entry)
                f.seek(0, os.SEEK_END)
                f.seek(f.tell()-2, os.SEEK_SET)
                f.truncate()

    def _drawMaze(self, theme):
        '''
        Creation of Tkinter window and maze lines
        '''

        self._LabWidth = 26  # Space from the top for Labels
        self._win = Tk()
        self._win.state('zoomed')

        scr_width = self._win.winfo_screenwidth()
        scr_height = self._win.winfo_screenheight()
        self._win.geometry(f"{scr_width}x{scr_height}+0+0")
        # 0,0 is top left corner
        self._canvas = Canvas(
            width=scr_width, height=scr_height, bg=theme.value[0])
        self._canvas.pack(expand=YES, fill=BOTH)
        # Some calculations for calculating the width of the maze cell
        k = 3.25
        if self.rows >= 95 and self.cols >= 95:
            k = 0
        elif self.rows >= 80 and self.cols >= 80:
            k = 1
        elif self.rows >= 70 and self.cols >= 70:
            k = 1.5
        elif self.rows >= 50 and self.cols >= 50:
            k = 2
        elif self.rows >= 35 and self.cols >= 35:
            k = 2.5
        elif self.rows >= 22 and self.cols >= 22:
            k = 3
        self._cell_width = round(min(((scr_height-self.rows-k*self._LabWidth)/(
            self.rows)), ((scr_width-self.cols-k*self._LabWidth)/(self.cols)), 90), 3)

        # Creating Maze lines
        if self._win is not None:
            if self.grid is not None:
                for cell in self.grid:
                    x, y = cell
                    w = self._cell_width
                    x = x*w-w+self._LabWidth
                    y = y*w-w+self._LabWidth
                    if self.maze_map[cell]['E'] == False:
                        l = self._canvas.create_line(
                            y + w, x, y + w, x + w, width=2, fill=theme.value[1], tag='line')
                    if self.maze_map[cell]['W'] == False:
                        l = self._canvas.create_line(
                            y, x, y, x + w, width=2, fill=theme.value[1], tag='line')
                    if self.maze_map[cell]['N'] == False:
                        l = self._canvas.create_line(
                            y, x, y + w, x, width=2, fill=theme.value[1], tag='line')
                    if self.maze_map[cell]['S'] == False:
                        l = self._canvas.create_line(
                            y, x + w, y + w, x + w, width=2, fill=theme.value[1], tag='line')

    def _redrawCell(self, x, y, theme):

        w = self._cell_width
        cell = (x, y)
        x = x*w-w+self._LabWidth
        y = y*w-w+self._LabWidth
        if self.maze_map[cell]['E'] == False:
            self._canvas.create_line(
                y + w, x, y + w, x + w, width=2, fill=theme.value[1])
        if self.maze_map[cell]['W'] == False:
            self._canvas.create_line(
                y, x, y, x + w, width=2, fill=theme.value[1])
        if self.maze_map[cell]['N'] == False:
            self._canvas.create_line(
                y, x, y + w, x, width=2, fill=theme.value[1])
        if self.maze_map[cell]['S'] == False:
            self._canvas.create_line(
                y, x + w, y + w, x + w, width=2, fill=theme.value[1])

    def enableArrowKey(self, a):

        self._win.bind('<Left>', a.moveLeft)
        self._win.bind('<Right>', a.moveRight)
        self._win.bind('<Up>', a.moveUp)
        self._win.bind('<Down>', a.moveDown)

    def enableWASD(self, a):

        self._win.bind('<a>', a.moveLeft)
        self._win.bind('<d>', a.moveRight)
        self._win.bind('<w>', a.moveUp)
        self._win.bind('<s>', a.moveDown)

    _tracePathList = []

    def trace_path_single(self, agent, path, kill, show_marked, delay):

        def kill_agent(agent):
            for i in range(len(agent._body)):
                self._canvas.delete(agent._body[i])
            self._canvas.delete(agent._head)

        cell_width = self._cell_width

        if ((agent.x, agent.y) in self.markCells and show_marked):
            x = agent.x * cell_width - cell_width + self._LabWidth
            y = agent.y * cell_width - cell_width + self._LabWidth
            self._canvas.create_oval(y + cell_width/2.5 + cell_width/20, x + cell_width/2.5 + cell_width/20,
                                     y + cell_width/2.5 + cell_width/4 - cell_width/20, x +
                                     cell_width/2.5 + cell_width/4 - cell_width/20,
                                     fill='red', outline='red', tag='ov')
            self._canvas.tag_raise('ov')

        if (agent.x, agent.y) == agent.goal:
            del maze._tracePathList[0][0][agent]
            if maze._tracePathList[0][0] == {}:
                del maze._tracePathList[0]
                if len(maze._tracePathList) > 0:
                    self.trace_path(
                        maze._tracePathList[0][0], kill=maze._tracePathList[0][1], delay=maze._tracePathList[0][2])
            if kill:
                self._win.after(300, kill_agent, agent)
            return

        if type(path) == dict:
            if len(path) == 0:
                del maze._tracePathList[0][0][agent]
                return
            if agent.shape == 'arrow':
                old = (agent.x, agent.y)
                new = path[(agent.x, agent.y)]
                orientation = agent._orient

                if old != new:
                    if old[0] == new[0]:
                        if old[1] > new[1]:
                            movement = 3  # 'W'
                        else:
                            movement = 1  # 'E'
                    else:
                        if old[0] > new[0]:
                            movement = 0  # 'N'
                        else:
                            movement = 2  # 'S'
                    if movement - orientation == 2:
                        agent.rotate_clockwise()
                    if movement - orientation == -2:
                        agent.rotate_clockwise()
                    if movement - orientation == 1:
                        agent.rotate_clockwise()
                    if movement - orientation == -1:
                        agent.rotate_clockwise()
                    if movement - orientation == 3:
                        agent.rotate_clockwise()
                    if movement - orientation == -3:
                        agent.rotate_clockwise()
                    if movement == orientation:
                        agent.x, agent.y = path[(agent.x, agent.y)]
                else:
                    del path[(agent.x, agent.y)]
            else:
                agent.x, agent.y = path[(agent.x, agent.y)]

        if type(path) == str:
            if len(path) == 0:
                del maze._tracePathList[0][0][agent]
                if maze._tracePathList[0][0] == {}:
                    del maze._tracePathList[0]
                    if len(maze._tracePathList) > 0:
                        self.trace_path(
                            maze._tracePathList[0][0], kill=maze._tracePathList[0][1], delay=maze._tracePathList[0][2])
                if kill:
                    self._win.after(300, kill_agent, agent)
                return
            if agent.shape == 'arrow':
                old = (agent.x, agent.y)
                new = path[0]
                orientation = agent._orient
                if new == 'N':
                    movement = 0
                elif new == 'E':
                    movement = 1
                elif new == 'S':
                    movement = 2
                elif new == 'W':
                    movement = 3

                if movement - orientation == 2:
                    agent.rotate_clockwise()
                if movement - orientation == -2:
                    agent.rotate_clockwise()
                if movement - orientation == 1:
                    agent.rotate_clockwise()
                if movement - orientation == -1:
                    agent.rotate_counter_clockwise()
                if movement - orientation == 3:
                    agent.rotate_counter_clockwise()
                if movement - orientation == -3:
                    agent.rotate_clockwise()

            if agent.shape == 'square' or movement == orientation:
                move = path[0]
                if move == 'E':
                    if agent.y + 1 <= self.cols:
                        agent.y += 1
                elif move == 'W':
                    if agent.y - 1 > 0:
                        agent.y -= 1
                elif move == 'N':
                    if agent.x - 1 > 0:
                        agent.x -= 1
                        agent.y = agent.y
                elif move == 'S':
                    if agent.x + 1 <= self.rows:
                        agent.x += 1
                        agent.y = agent.y
                elif move == 'C':
                    agent.rotate_clockwise()
                elif move == 'A':
                    agent.rotate_counter_clockwise()
                path = path[1:]

        if type(path) == list:
            if len(path) == 0:
                del maze._tracePathList[0][0][agent]
                if maze._tracePathList[0][0] == {}:
                    del maze._tracePathList[0]
                    if len(maze._tracePathList) > 0:
                        self.trace_path(
                            maze._tracePathList[0][0], kill=maze._tracePathList[0][1], delay=maze._tracePathList[0][2])
                if kill:
                    self._win.after(300, kill_agent, agent)
                return
            if agent.shape == 'arrow':
                old = (agent.x, agent.y)
                new = path[0]
                orientation = agent._orient

                if old != new:
                    if old[0] == new[0]:
                        if old[1] > new[1]:
                            movement = 3  # 'W'
                        else:
                            movement = 1  # 'E'
                    else:
                        if old[0] > new[0]:
                            movement = 0  # 'N'
                        else:
                            movement = 2  # 'S'
                    if movement - orientation == 2:
                        agent.rotate_clockwise()
                    elif movement - orientation == -2:
                        agent.rotate_clockwise()
                    elif movement - orientation == 1:
                        agent.rotate_clockwise()
                    elif movement - orientation == -1:
                        agent.rotate_counter_clockwise()
                    elif movement - orientation == 3:
                        agent.rotate_counter_clockwise()
                    elif movement - orientation == -3:
                        agent.rotate_clockwise()
                    elif movement == orientation:
                        agent.x, agent.y = path[0]
                        del path[0]
                else:
                    del path[0]
            else:
                agent.x, agent.y = path[0]
                del path[0]

        self._win.after(delay, self.trace_path_single, agent,
                    path, kill, show_marked, delay)

    def tracePath(self, agents_path, kill=False, delay=300, showMarked=False):

        # A method to trace paths by agents

        self._tracePathList.append((agents_path, kill, delay))
        if self._tracePathList[0][0] == agents_path:
            for agent, path in agents_path.items():
                if agent.goal != (agent.x, agent.y) and len(path) != 0:
                    self.trace_path_single(agent, path, kill, showMarked, delay)

    def run(self):
        '''
        Finally to run the Tkinter Main Loop
        '''
        self._win.mainloop()
