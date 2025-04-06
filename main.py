import pygame
import sys
from data.texture.config import *
from core.Bomberman import Game

""" # Game loop
running = True
while running:

    prepare.wall_group.draw(prepare.SCREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    prepare.CLOCK.tick(60)
    pygame.display.update()

else:
    pygame.quit() """


# Active Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bomberman")
clock = pygame.time.Clock()

game = Game()

while True:
    screen.fill(WHITE)
    game.update()
    game.render(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        game.handle_event(event)

    pygame.display.update()
    clock.tick(10)