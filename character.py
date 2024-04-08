class Character():

    def __init__(self, x, y, direction):
        '''Creates a character instance with specified x and y coordinates along with a direction attribute.
        This class is used to represent both Pacman and all the Enemies present on the game board.'''
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 1
        self.start_location = x, y
        self.last_location = None
        self.invulnerable = False
        self._image = None

    def movement(self) -> None:
        '''This function orchestrates the movement of character objects within the game board.
        The coordinates of each character are modified with every update, based on the direction in which the character is moving.'''
        if self.direction == 'Up':
            self.y -= self.speed

        elif self.direction == 'Right':
            self.x += self.speed

        elif self.direction == 'Down':
            self.y += self.speed

        elif self.direction == 'Left':
            self.x -= self.speed

    def invulnerability(self) -> None:
        ''' Inverts the value of the invulnerable attribute from its current state.
            It is invoked twice: once when a boost is consumed, 
            and then again after a certain duration has elapsed to revert it to its default state. '''
        self.invulnerable = not self.invulnerable

    def initial_position(self) -> None:
        ''' Changes the location to the initial spawn location. '''
        self.change_location(self.start_location[0], self.start_location[1])

    def change_direction(self, direction) -> None:
        ''' Makes the attribute direction equal to the direction argument given in the parameters. '''
        self.direction = direction

    def change_location(self, x, y) -> None:
        ''' Changes the location of the character's x and y values to the x and y arguments. '''
        self.x, self.y = x, y

    def return_location(self) -> tuple:
        ''' This function returns y first since the board is a 2D-List. '''
        return self.y, self.x
