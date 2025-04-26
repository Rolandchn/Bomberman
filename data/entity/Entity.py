import pygame


from data.texture.config import TILE_SIZE



class Entity(pygame.sprite.Sprite):
    def __init__(self, status, position:int, image:pygame.Surface, *groups):
        self.status = status
        super().__init__(*groups)

        self.image = image
        self.life = 1
        
        self.rect = self.image.get_rect(topleft=(position[0] * TILE_SIZE, position[1] * TILE_SIZE))
        
        # Position inside the grip in Map
        self.grid_x = position[0]
        self.grid_y = position[1]


    def update_rect(self):
        self.rect.topleft = (self.grid_x * TILE_SIZE, self.grid_y * TILE_SIZE)


    def is_dead(self):
        '''
        Output: check player life.
        '''
        return self.life <= 0
    

    def __eq__(self, other):
        return isinstance(other, Entity) and other.status == self.status


    def __hash__(self):
        return hash(self.status)