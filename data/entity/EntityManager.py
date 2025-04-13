

import pygame


class EntityManager:
    def __init__(self):
        self.wall_group = pygame.sprite.Group()
        self.floor_group = pygame.sprite.Group()
        
        self.player_group = pygame.sprite.Group()
    
        self.bomb_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()


    def update(self):
        self.player_group.update()

        self.bomb_group.update()
        self.explosion_group.update()


    def draw(self, screen):
        self.wall_group.draw(screen)
        self.floor_group.draw(screen)
        
        self.player_group.draw(screen)

        self.bomb_group.draw(screen)
        self.explosion_group.draw(screen)
