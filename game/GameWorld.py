import pygame

from data.map.Map import Map



class GameWorld:
    def __init__(self):
        self.wall_group = pygame.sprite.Group()
        self.floor_group = pygame.sprite.Group()
        
        self.player_group = pygame.sprite.Group()
    
        self.bomb_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        
        self.map = Map(self)

        self.turn_status = None
        self.turn = None


    def update(self, game_turn):
        self.player_group.update()

        self.bomb_group.update(game_turn)
        self.explosion_group.update(game_turn)


    def draw(self, screen):
        self.floor_group.draw(screen)
        self.wall_group.draw(screen)
        
        self.player_group.draw(screen)

        for bomb in self.bomb_group:
            bomb.draw(self.turn, screen)
        self.explosion_group.draw(screen)


    def clone(self):
        new_world = GameWorld()
        new_world.turn = self.turn
        new_world.turn_status = self.turn_status

        for sprite, position in self.map.grid.items():
            copy_sprite = sprite.clone(new_world)
            
            new_world.map.grid[copy_sprite] = position

        return new_world

