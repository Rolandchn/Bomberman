import pygame

from core import prepare, Bomberman

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

def main():
    Bomberman.Game

if __name__ == "__main__":
    main()