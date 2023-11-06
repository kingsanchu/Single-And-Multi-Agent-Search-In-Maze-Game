from collections import deque
import maze_data  # Import the maze data from maze_data.py

# Define directions (up, down, left, right)
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def is_valid(x, y, maze):
    return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] == 0

def dfs(maze, start, end):
    def dfs_helper(current):
        visited.add(current)

        if current == end:
            return [current]

        for dx, dy in directions:
            new_x, new_y = current[0] + dx, current[1] + dy
            if is_valid(new_x, new_y, maze) and (new_x, new_y) not in visited:
                path = dfs_helper((new_x, new_y))
                if path:
                    return [current] + path

        return []

    visited = set()
    return dfs_helper(start)

def bfs(maze, start, end):
    queue = deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()

        if current == end:
            path = []
            while current:
                path.insert(0, current)
                current = came_from[current]
            return path

        for dx, dy in directions:
            new_x, new_y = current[0] + dx, current[1] + dy
            if is_valid(new_x, new_y, maze) and (new_x, new_y) not in came_from:
                queue.append((new_x, new_y))
                came_from[(new_x, new_y)] = current

    return None

def display_maze(maze):
    for row in maze:
        row_str = ''.join(['S' if cell == 0 else 'X' if cell == 1 else 'E' for cell in row])
        print(row_str)

def display_path(path):
    if path:
        print(f"Path found: {path}")
    else:
        print("No path found")

# Ask the user to choose the maze size
while True:
    print("Choose a maze size:")
    print("1. Small Maze")
    print("2. Medium Maze")
    print("3. Large Maze")
    
    choice = input("Enter the number of your choice (1/2/3): ")
    
    if choice in ["1", "2", "3"]:
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

if choice == "1":
    maze = maze_data.small_maze_data
elif choice == "2":
    maze = maze_data.medium_maze_data
elif choice == "3":
    maze = maze_data.large_maze_data

start = (0, 0)
end = (len(maze) - 1, len(maze[0]) - 1)

# Ask the user to choose the search algorithm
while True:
    print("Choose a search algorithm:")
    print("1. DFS (Depth-First Search)")
    print("2. BFS (Breadth-First Search)")
    
    search_choice = input("Enter the number of your choice (1/2): ")
    
    if search_choice in ["1", "2"]:
        break
    else:
        print("Invalid choice. Please enter 1 for DFS or 2 for BFS.")

if search_choice == "1":
    search_algorithm = "DFS"
    path = dfs(maze, start, end)
elif search_choice == "2":
    search_algorithm = "BFS"
    path = bfs(maze, start, end)

print("Maze:")
display_maze(maze)

print(f"{search_algorithm}:")
display_path(path)
