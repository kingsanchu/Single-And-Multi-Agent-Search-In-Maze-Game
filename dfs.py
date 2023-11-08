from mazeGame import maze, agent, COLOR, textLabel

def DFS(self, start=None):
    if start is None:
        start = (self.rows, self.cols)
    explored = [start]
    frontier = [start]
    dfsPath = {}
    dSeacrh = []
    while len(frontier) > 0:
        currCell = frontier.pop()
        dSeacrh.append(currCell)
        if currCell == self._goal:
            break
        poss = 0
        for d in 'ESNW':
            if self.maze_map[currCell][d] == True:
                if d == 'E':
                    child = (currCell[0], currCell[1]+1)
                if d == 'W':
                    child = (currCell[0], currCell[1]-1)
                if d == 'N':
                    child = (currCell[0]-1, currCell[1])
                if d == 'S':
                    child = (currCell[0]+1, currCell[1])
                if child in explored:
                    continue
                poss += 1
                explored.append(child)
                frontier.append(child)
                dfsPath[child] = currCell
        if poss > 1:
            self.markCells.append(currCell)
    fwdPath = {}
    cell = self._goal
    while cell != start:
        fwdPath[dfsPath[cell]] = cell
        cell = dfsPath[cell]
    return dSeacrh, dfsPath, fwdPath


if __name__ == '__main__':
    m = maze(10, 10)  # Change to any size
    # (2,4) is Goal Cell, Change that to any other valid cell
    m.CreateMaze(2, 4)

    # (5,1) is Start Cell, Change that to any other valid cell
    dSeacrh, dfsPath, fwdPath = DFS(m, (5, 1))

    a = agent(m, 5, 1, goal=(2, 4), footprints=True,
              shape='square', color=COLOR.green)
    b = agent(m, 2, 4, goal=(5, 1), footprints=True, filled=True)
    c = agent(m, 5, 1, footprints=True, color=COLOR.yellow)
    m.tracePath({a: dSeacrh}, showMarked=True)
    m.tracePath({b: dfsPath})
    m.tracePath({c: fwdPath})
    m.run()

    # m=maze()
    # m.CreateMaze(loadMaze='dfs.csv')

    # dSeacrh,dfsPath,fwdPath=DFS(m)

    # a=agent(m,footprints=True,shape='square',color=COLOR.green)
    # b=agent(m,1,1,goal=(5,5),footprints=True,filled=True,color=COLOR.cyan)
    # c=agent(m,footprints=True,color=COLOR.yellow)
    # m.tracePath({a:dSeacrh},showMarked=True)
    # m.tracePath({b:dfsPath})
    # m.tracePath({c:fwdPath})
    # m.run()
