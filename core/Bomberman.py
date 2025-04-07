import pygame
from data.entity.Player import Player
from data.entity.Bombe import BombManager
from data.map.Map import Map
from data.entity.Wall import Wall

from data.texture.config import SCREEN_HEIGHT, SCREEN_WIDTH, WHITE



class Game():
    def __init__(self):
        pygame.init()
        # Initialize general
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bomberman")

        # Initialize Game
        self.map = Map()
        self.player = Player(1, 1)
        self.bombs = BombManager(self.map)


    def handle_event(self, event):
        self.player.handle_input(event, self.map, self.bombs)

    def update(self):
        self.bombs.update()

    def render(self, screen):
        self.map.draw(screen)
        self.bombs.draw(screen)
        self.player.draw(screen)

    def run(self):
        clock = pygame.time.Clock()

        RUNNING = True
        while RUNNING:
            self.screen.fill(WHITE)
            self.update()
            self.render(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                self.handle_event(event)

            pygame.display.update()
            
            clock.tick(10)


        """#################################################

         self.player = MyPlayer("ball1.png", 100, 200)

        self.sprites_list = []

        self.add_sprite(MySprite("ball2.png", 100, 400))
        self.add_sprite(MySprite("ball2.png", 300, 500))
        self.add_sprite(MySprite("ball2.png", 300, 200))

        self.remove_last_sprite() 

        #-----------------------------

     self.create_map()

    #--------------------------

     def add_sprite(self, sprite):
        self.sprites_list.append(sprite) 

    #--------------------------

    def remove_last_sprite(self):
        if self.sprites_list:
            del self.sprites_list[-1]

    #--------------------------

    def draw_sprites(self, screen):
        for sprite in self.sprites_list:
            sprite.draw(screen) 

    #--------------------------


    def create_map(self):
        map_data = []
        self.wall_group = pygame.sprite.Group()

        # Read map
        with open("./data/map/map.txt", "r") as game_map:
            for line in game_map:
                map_data.append(line)

        MAP_SIZE = len(map_data)
        TILE_SIZE = self.SCREEN_HEIGHT // MAP_SIZE

        for row, tiles in enumerate(map_data):
            for col, tile in enumerate(tiles):
                if tile == "#":
                    self.wall_group.add(Wall(row, col, Color.OBSTACLE.value, TILE_SIZE))

                elif tile == "0":
                    self.wall_group.add(Wall(row, col, Color.GREEN.value, TILE_SIZE))

                elif tile == "S":

                    self.wall_group.add(Wall(row, col, Color.SPAWN.value, TILE_SIZE))



    def draw_map(self, screen:pygame.Surface):
        self.wall_group.draw(screen)

    #--------------------------

    def draw_world(self, image):
        temp = pygame.Surface(self.SCREEN_SIZE, pygame.SRCALPHA, 32).convert_alpha()
        image_rect = image.get_rect()

        for x in range(0, self.SCREEN_WIDTH, 60):
            for y in range(0,self.SCREEN_WIDTH, 60):
                temp.blit(image,(x,y))

        return temp

    #--------------------------
    def run(self):

        clock = pygame.time.Clock()

        RUNNING = True

        while RUNNING:

            #--- events ---
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    RUNNING = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        RUNNING = False

                    if event.key == pygame.K_UP:
                        self.player.set_speed(0,-10)
                    elif event.key == pygame.K_DOWN:
                        self.player.set_speed(0,10)
                    elif event.key == pygame.K_LEFT:
                        self.player.set_speed(-10,0)
                    elif event.key == pygame.K_RIGHT:
                        self.player.set_speed(10,0)

                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                        self.player.set_speed(0,0)


            #--- draws ---
            self.draw_map(self.SCREEN)

            pygame.display.update()

            #--- FPS ---
            clock.tick(25) # 25 Frames Per Seconds

        #--- finish ---
        pygame.quit()"""