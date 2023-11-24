from enum import Enum

class COLOR(Enum):
    """
    Enum class defining colors with their corresponding color codes.

    Attributes:
    - Color scheme with background and text color.
    """
    dark = ('gray11', 'white')
    light = ('white', 'black')
    black = ('black', 'dim gray')
    red = ('red3', 'tomato')
    cyan = ('cyan4', 'cyan4')
    green = ('green4', 'pale green')
    blue = ('DeepSkyBlue4', 'DeepSkyBlue2')
    yellow = ('yellow2', 'yellow2')