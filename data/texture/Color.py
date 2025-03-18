

from enum import Enum

class Color(Enum):
    WHITE = (255, 255, 255)  # Player 1 color (high contrast)
    BLACK = (0, 0, 0)  # Player 2 color (high contrast)

    GREEN = (92, 184, 92)  # Ground color, a more balanced light green
    SPAWN = (72, 170, 72)  # Spawn zone, a slightly darker green for differentiation

    OBSTACLE = (128, 128, 128)  # Solid, neutral gray for indestructible blocks
    BRICK = (190, 65, 55)  # Warmer red tone to make destructible bricks pop

    BOMBE = (20, 80, 120)  # A deep teal for a distinct bomb appearance
    EXPLOSION = (255, 90, 0)  # Fiery orange-red for a more dynamic explosion effect
