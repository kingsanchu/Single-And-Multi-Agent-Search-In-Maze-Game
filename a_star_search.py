from maze import maze
from agent import agent
from textLabel import textLabel
from queue import PriorityQueue

def heuristic(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)

def aStarPathFinding(self):
    start = (self.rows, self.cols)
    g_scores = {cell: float('inf') for cell in self.grid}
    g_scores[start] = 0
    f_scores = {cell: float('inf') for cell in self.grid}
    f_scores[start] = heuristic(start, (1, 1))

    open_cells = PriorityQueue()
    open_cells.put((heuristic(start, (1, 1)), heuristic(start, (1, 1)), start))
    a_path = {}

    while not open_cells.empty():
        current_cell = open_cells.get()[2]
        if current_cell == (1, 1):
            break
        for direction in 'ESNW':
            if self.maze_map[current_cell][direction] == True:
                if direction == 'E':
                    child_cell = (current_cell[0], current_cell[1] + 1)
                if direction == 'W':
                    child_cell = (current_cell[0], current_cell[1] - 1)
                if direction == 'N':
                    child_cell = (current_cell[0] - 1, current_cell[1])
                if direction == 'S':
                    child_cell = (current_cell[0] + 1, current_cell[1])

                temp_g_score = g_scores[current_cell] + 1
                temp_f_score = temp_g_score + heuristic(child_cell, (1, 1))

                if temp_f_score < f_scores[child_cell]:
                    g_scores[child_cell] = temp_g_score
                    f_scores[child_cell] = temp_f_score
                    open_cells.put((temp_f_score, heuristic(child_cell, (1, 1)), child_cell))
                    a_path[child_cell] = current_cell

    forward_path = {}
    cell = (1, 1)
    while cell != start:
        forward_path[a_path[cell]] = cell
        cell = a_path[cell]
    return forward_path

if __name__ == '__main__':
    maze_instance = maze(10, 10)
    maze_instance.CreateMaze()
    path = aStarPathFinding(maze_instance)

    agent_a = agent(maze_instance, footprints=True)
    maze_instance.tracePath({agent_a: path})
    label = textLabel(maze_instance, 'A Star Path Length', len(path) + 1)

    maze_instance.run()
