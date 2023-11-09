from mazeGame import maze, agent, textLabel, COLOR
from collections import deque

def breadthFirstSearch(maze, start=None):
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
    searchPath, bfsPath, fwdPath = breadthFirstSearch(maze_instance)
    
    agent_a = agent(maze_instance, footprints=True, color=COLOR.yellow, shape='square', filled=True)
    agent_b = agent(maze_instance, footprints=True, color=COLOR.red, shape='square', filled=False)
    agent_c = agent(maze_instance, 1, 1, footprints=True, color=COLOR.cyan, shape='square', filled=True, goal=(maze_instance.rows, maze_instance.cols))
    
    maze_instance.tracePath({agent_a: searchPath}, delay=100)
    maze_instance.tracePath({agent_c: bfsPath}, delay=100)
    maze_instance.tracePath({agent_b: fwdPath}, delay=100)

    maze_instance.run()
