import pygame

from data.texture.Color import Color

# Activate all the pygame functions 
pygame.init()

# Screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)

pygame.display.set_caption("Bomberman")

# Clock (aka FPS)
CLOCK = pygame.time.Clock()


# World data
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, color, size):
        super().__init__()

        self.x = x
        self.y = y
        self.color = color

        self.image = pygame.Surface((size, size))
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.x = self.x * size
        self.rect.y = self.y * size

map_data = []
wall_group = pygame.sprite.Group()

# Read map
with open("map.txt", "r") as game_map:
    for line in game_map:
        map_data.append(line)

MAP_SIZE = len(map_data)
TILE_SIZE = SCREEN_HEIGHT // MAP_SIZE

# Create map
for row, tiles in enumerate(map_data):
    for col, tile in enumerate(tiles):
        if tile == "#":
            wall_group.add(Wall(row, col, Color.OBSTACLE.value, TILE_SIZE))
        
        elif tile == "0":
            wall_group.add(Wall(row, col, Color.GREEN.value, TILE_SIZE))

        elif tile == "S":

            wall_group.add(Wall(row, col, Color.SPAWN.value, TILE_SIZE))

# Game loop
running = True
while running:

    wall_group.draw(SCREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    CLOCK.tick(60)
    pygame.display.update()

else:
    pygame.quit()