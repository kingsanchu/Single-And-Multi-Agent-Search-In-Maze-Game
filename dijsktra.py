from maze import maze
from agent import Agent
from textLabel import textLabel
from queue import PriorityQueue
from COLOR import COLOR

def dijkstraPathFinding(self):
    """
    Performs Dijkstra's algorithm to find the shortest path in a maze.

    Returns:
    - Dictionary representing the path found by Dijkstra's algorithm.
    """
    start = (self.rows, self.cols)
    g_scores = {cell: float('inf') for cell in self.grid}
    g_scores[start] = 0

    open_cells = PriorityQueue()
    open_cells.put((0, start))
    d_path = {}

    while not open_cells.empty():
        current_cost, current_cell = open_cells.get()
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

                if temp_g_score < g_scores[child_cell]:
                    g_scores[child_cell] = temp_g_score
                    open_cells.put((temp_g_score, child_cell))
                    d_path[child_cell] = current_cell

    forward_path = {}
    cell = (1, 1)
    while cell != start:
        forward_path[d_path[cell]] = cell
        cell = d_path[cell]
    return forward_path

if __name__ == '__main__':
    maze_instance = maze(10, 10)
    maze_instance.CreateMaze(theme='light')
    path = dijkstraPathFinding(maze_instance)

    agent_a = Agent(maze_instance, footprints=True, color=COLOR.red)
    maze_instance.tracePath({agent_a: path})

    label = textLabel(maze_instance, 'Dijkstra (Path Length)', len(path) + 1)

    maze_instance.run()
