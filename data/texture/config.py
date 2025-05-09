#Taille
from game.GameStatus import GameStatus
from collections import defaultdict

TILE_SIZE = 40
GRID_WIDTH = 15
GRID_HEIGHT = 15
SCREEN_WIDTH = TILE_SIZE * GRID_WIDTH
SCREEN_HEIGHT = TILE_SIZE * GRID_HEIGHT

MAX_TURN = 300
SHRINK_INTERVAL = 20

DESTINATION_POS = {
    GameStatus.P1: [(3, 3), (10, 3), (7, 7)],
    GameStatus.P2: [(11, 11), (3, 11), (7, 7)]
}


current_destination_index = defaultdict(lambda: 0)
