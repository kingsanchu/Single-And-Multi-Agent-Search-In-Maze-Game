
def dfs_search(self, board, start, endpoint_y, endpoint_x) -> deque:
    # Implementation of Depth-First Search algorithm
    came_from = {}
    visited = set()
    stack = [((self.y, self.x), None)]  # Stack (node, parent)

    while stack:
        current, _ = stack.pop()

        if current == (endpoint_y, endpoint_x):
            # Reconstruct path from start to endpoint
            path = deque()
            while current in came_from:
                path.appendleft((current[1], current[0]))
                current = came_from[current]
            return path
        
        if current in visited:
            continue
        
        visited.add(current)

        for neighbor in board.get_valid_neighbors(current[0], current[1]):
            if neighbor not in came_from and neighbor not in visited:
                came_from[neighbor] = current
                stack.append((neighbor, current))

    # No path found
    return None


def adversarial_minimax_search(self, board, start, endpoint_y, endpoint_x):
    # Adversarial Minimax search algorithm
    def max_value(board, player):
        if board.is_terminal():
            return board.utility(player)
        v = float("-inf")
        for action in board.actions():
            v = max(v, min_value(board.result(action), player))
        return v

    def min_value(board, player):
        if board.is_terminal():
            return board.utility(player)
        v = float("inf")
        for action in board.actions():
            v = min(v, max_value(board.result(action), player))
        return v

    best_action = None
    best_score = float("-inf")
    for action in board.actions():
        v = min_value(board.result(action), self.player)
        if v > best_score:
            best_score = v
            best_action = action
    return best_action

def alpha_beta_pruning(self, board, start, endpoint_y, endpoint_x):
    # Alpha-beta pruning algorithm
    def max_value(board, player, alpha, beta):
        if board.is_terminal():
            return board.utility(player)
        v = float("-inf")
        for action in board.actions():
            v = max(v, min_value(board.result(action), player, alpha, beta))
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v

    def min_value(board, player, alpha, beta):
        if board.is_terminal():
            return board.utility(player)
        v = float("inf")
        for action in board.actions():
            v = min(v, max_value(board.result(action), player, alpha, beta))
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v

    alpha = float("-inf")
    beta = float("inf")
    best_action = None
    best_score = float("-inf")
    for action in board.actions():
        v = min_value(board.result(action), player, alpha, beta)
        if v > best_score:
            best_score = v
            best_action = action
        alpha = max(alpha, v)
    return best_action

def expectimax(self, board, start, endpoint_y, endpoint_x):
    # Expectimax algorithm
    def max_value(board, player):
        if board.is_terminal():
            return board.utility(player)
        v = float("-inf")
        for action in board.actions():
            v = max(v, expect_value(board.result(action), player))
        return v

    def expect_value(board, player):
        if board.is_terminal():
            return board.utility(player)
        v = 0
        num_actions = len(board.actions())
        for action in board.actions():
            v += max_value(board.result(action), player)
        return v / num_actions

    best_action = None
    best_score = float("-inf")
    for action in board.actions():
        v = expect_value(board.result(action), self.player)
        if v > best_score:
            best_score = v
            best_action = action
    return best_action