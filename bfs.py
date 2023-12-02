from maze import maze
from agent import agent
from textLabel import textLabel
from COLOR import COLOR
from collections import deque

def breadthFirstSearch(maze, start=None):
    """
    Finds the shortest path in a maze using Breadth-First Search (BFS) algorithm.

    Args:
    - maze: The maze instance.
    - start: The starting point for the BFS search. Defaults to the maze's dimensions if not provided.

    Returns:
    - A tuple containing three dictionaries representing the search path, BFS path, and forward path.
    """
    if start is None:
        start = (maze.rows, maze.cols)
    frontier = deque()
    frontier.append(start)
    bfsPath = {}
    explored = [start]
    searchPath = []

    while len(frontier) > 0:
        currentCell = frontier.popleft()
        if currentCell == maze._goal:
            break
        for direction in 'ESNW':
            if maze.maze_map[currentCell][direction] == True:
                if direction == 'E':
                    childCell = (currentCell[0], currentCell[1]+1)
                elif direction == 'W':
                    childCell = (currentCell[0], currentCell[1]-1)
                elif direction == 'S':
                    childCell = (currentCell[0]+1, currentCell[1])
                elif direction == 'N':
                    childCell = (currentCell[0]-1, currentCell[1])
                if childCell in explored:
                    continue
                frontier.append(childCell)
                explored.append(childCell)
                bfsPath[childCell] = currentCell
                searchPath.append(childCell)
    
    forwardPath = {}
    cell = maze._goal
    while cell != (maze.rows, maze.cols):
        forwardPath[bfsPath[cell]] = cell
        cell = bfsPath[cell]
    
    return searchPath, bfsPath, forwardPath

if __name__ == '__main__':
    maze_instance = maze(10, 10)
    maze_instance.CreateMaze(loopPercent=10, theme='light')
    
    # Perform breadth-first search to get paths
    searchPath, bfsPath, fwdPath = breadthFirstSearch(maze_instance)
    
    # Create agents
    agent_a = agent(maze_instance, footprints=True, color=COLOR.yellow, shape='square', filled=True)
    agent_b = agent(maze_instance, footprints=True, color=COLOR.red, shape='square', filled=False)
    agent_c = agent(maze_instance, 1, 1, footprints=True, color=COLOR.green, shape='square', filled=True, goal=(maze_instance.rows, maze_instance.cols))
    
    # Trace paths obtained from search algorithms
    maze_instance.tracePath({agent_a: searchPath}, delay=100)
    maze_instance.tracePath({agent_c: bfsPath}, delay=100)
    maze_instance.tracePath({agent_b: fwdPath}, delay=100)
    
    path = breadthFirstSearch(maze_instance)
    label = textLabel(maze_instance, 'BFS', len(path) + 1)

    # Run the maze
    maze_instance.run()
