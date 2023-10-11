# @author Steven CHU

class player:
    # Record if the player or cell visited the coordinates or not.
    def __init__(cell, x, y):
        cell.x = x
        cell.y = y
        cell.visited = False 

#Check if player visited the coordinates.
if player.visited:
    print("Player has visited the corrdinates.")
else:
    print("Player has not visited the coordinates.")
