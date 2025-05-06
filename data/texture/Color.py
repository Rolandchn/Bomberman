from enum import Enum

# Couleurs
class Color(Enum):
    GRAY = (180, 180, 180)
    
    WHITE = (255, 255, 255)
    BLACK = (30, 30, 30)

    GREEN = (92, 184, 92)
    SPAWN = (72, 170, 72)
    
    WALL = (128, 128, 128)
    OBSTACLE = (190, 65, 55)
    OBSTACLE_HIDDEN = (210, 90, 70)
    
    BOMBE = (20, 80, 120)
    EXPLOSION = (255, 90, 0)
