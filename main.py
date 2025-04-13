from data.texture.config import *
from core.Bomberman import Game

import pygame



if __name__ == "__main__":
    pygame.init()

    game = Game()

    game.run()