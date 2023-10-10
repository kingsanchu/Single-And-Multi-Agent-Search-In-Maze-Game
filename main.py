class player:
    # Record if the player or cell visited the coordinates or not.
    def __init__(cell, x, y):
        cell.x = x
        cell.y = y
        cell.visited = False 
