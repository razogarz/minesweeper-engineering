from enum import Enum
# Colors
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (128, 128, 128)

class FieldState(Enum):
    MINED = -3
    NOT_MINED = -2
    POSSIBLE_MINE = -1
    NOT_REVEALED_NOT_NEIGHBOUR = 0
    NOT_REVEALED_NEIGHBOUR = 1
    REVEALED = 2

