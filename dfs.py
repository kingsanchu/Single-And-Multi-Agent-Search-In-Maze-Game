from maze import maze
from agent import agent
from textLabel import textLabel
from COLOR import COLOR

def depthFirstSearch(self, start=None):
    if start is None:
        start = (self.rows, self.cols)
    explored_cells = [start]
    frontier = [start]
    dfs_path = {}
    dfs_search = []

    while len(frontier) > 0:
        current_cell = frontier.pop()
        dfs_search.append(current_cell)

        if current_cell == self._goal:
            break

        possible_directions = 0
        for direction in 'ESNW':
            if self.maze_map[current_cell][direction] == True:
                if direction == 'E':
                    child_cell = (current_cell[0], current_cell[1]+1)
                elif direction == 'W':
                    child_cell = (current_cell[0], current_cell[1]-1)
                elif direction == 'N':
                    child_cell = (current_cell[0]-1, current_cell[1])
                elif direction == 'S':
                    child_cell = (current_cell[0]+1, current_cell[1])

                if child_cell in explored_cells:
                    continue

                possible_directions += 1
                explored_cells.append(child_cell)
                frontier.append(child_cell)
                dfs_path[child_cell] = current_cell

        if possible_directions > 1:
            self.markCells.append(current_cell)

    forward_path = {}
    cell = self._goal
    while cell != start:
        forward_path[dfs_path[cell]] = cell
        cell = dfs_path[cell]

    return dfs_search, dfs_path, forward_path

if __name__ == '__main__':
    maze_instance = maze(10, 10)  # Change to any size
    maze_instance.CreateMaze(2, 4)  # (2,4) is Goal Cell, Change that to any other valid cell

    # (5,1) is Start Cell, Change that to any other valid cell
    dfs_search, dfs_path, forward_path = depthFirstSearch(maze_instance, (5, 1))

    agent_a = agent(maze_instance, 5, 1, goal=(2, 4), footprints=True, shape='square', color=COLOR.green)
    agent_b = agent(maze_instance, 2, 4, goal=(5, 1), footprints=True, filled=True)
    agent_c = agent(maze_instance, 5, 1, footprints=True, color=COLOR.yellow)

    maze_instance.tracePath({agent_a: dfs_search}, showMarked=True)
    maze_instance.tracePath({agent_b: dfs_path})
    maze_instance.tracePath({agent_c: forward_path})
    maze_instance.run()
