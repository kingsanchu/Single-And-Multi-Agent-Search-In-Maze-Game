import heapq
from collections import deque

class Node:
    def __init__(self, position):
        self.position = position

class NodeWithCost(Node):
    def __init__(self, position, g_cost=0, h_cost=0):
        super().__init__(position)
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost

    def __lt__(self, other):
        return self.f_cost < other.f_cost

class NodeWithoutCost(Node):
    pass

class Algorithms:
    def __init__(self, maze_data, start_position, end_position):
        self.maze_data = maze_data
        self.start_position = start_position
        self.end_position = end_position
        self.rows = len(maze_data)

    def heuristic(self, position, end):
        x1, y1 = position
        x2, y2 = end
        return abs(x1 - x2) + abs(y1 - y2)

    # Check if the neighbors are obstacles
    def get_neighbor(self, position):
        x, y = position
        neighbors = []
        if x > 0 and self.maze_data[x - 1][y] == 0:
            neighbors.append((x - 1, y))
        if x < self.rows - 1 and self.maze_data[x + 1][y] == 0:
            neighbors.append((x + 1, y))
        if y > 0 and self.maze_data[x][y - 1] == 0:
            neighbors.append((x, y - 1))
        if y < self.rows - 1 and self.maze_data[x][y + 1] == 0:
            neighbors.append((x, y + 1))

        return neighbors

    # A* Search Algorithm
    def find_path_a_star(self):
        start = self.start_position
        end = self.end_position
        empty_set = []
        visited = set()
        starting_node = NodeWithCost(start, 0, self.heuristic(start, end))
        heapq.heappush(empty_set, starting_node)
        came_from = {}

        while empty_set:
            current = heapq.heappop(empty_set)

            if current.position == end:
                return self.reconstruct_path(start, end, current, came_from)

            visited.add(current.position)

            for neighbor in self.get_neighbor(current.position):
                if neighbor in visited:
                    continue

                g_cost = current.g_cost + 1
                h_cost = self.heuristic(neighbor, end)
                neighbor_node = NodeWithCost(neighbor, g_cost, h_cost)
                came_from[neighbor_node] = current

                if neighbor_node not in empty_set:
                    heapq.heappush(empty_set, neighbor_node)

        return None

    # DFS Search Algorithm
    def find_path_dfs(self):
        start = self.start_position
        end = self.end_position
        visited = set()
        stack = [NodeWithoutCost(start)]
        came_from = {}

        while stack:
            current = stack.pop()

            if current.position == end:
                return self.reconstruct_path(start, end, current, came_from)

            visited.add(current.position)

            for neighbor in self.get_neighbor(current.position):
                if neighbor in visited:
                    continue

                stack.append(NodeWithoutCost(neighbor))
                came_from[NodeWithoutCost(neighbor)] = current

        return None

    # BFS Search Algorithm
    def find_path_bfs(self):
        start = self.start_position
        end = self.end_position
        visited = set()
        queue = deque()
        queue.append(NodeWithoutCost(start))
        came_from = {}

        while queue:
            current = queue.popleft()

            if current == end:
                return self.reconstruct_path(start, end, current, came_from)

            visited.add(current)

            for neighbor in self.get_neighbor(current):
                if neighbor in visited:
                    continue
                queue.append(neighbor)
                came_from[neighbor] = current  # Use tuples as keys

        return None

    def reconstruct_path(self, start, end, current, came_from):
        path = []
        while current.position != start:
            path.append(current.position)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path