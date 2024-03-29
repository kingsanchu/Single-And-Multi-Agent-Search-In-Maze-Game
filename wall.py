class Wall:
    wall = 0

    def __init__(self, x, y, images):
        """
        Initialize a Wall object.

        Args:
            x (int): X-coordinate of the wall.
            y (int): Y-coordinate of the wall.
            images: Images used for game objects.
        """
        self.x = x
        self.y = y
        self.images = images