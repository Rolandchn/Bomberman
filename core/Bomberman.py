import pygame

class Game():

    def __init__(self, width, height):
        pygame.init()

        #--------------------
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = width, height
        self.SCREEN_SIZE = self.SCREEN_WIDTH, self.SCREEN_HEIGHT
        #--------------------

        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)

        #############################################################

        self.background = None

        self.set_background("background.jpg")                          

        #################################################

        self.player = MyPlayer("ball1.png", 100, 200)

        self.sprites_list = []

        self.add_sprite(MySprite("ball2.png", 100, 400))
        self.add_sprite(MySprite("ball2.png", 300, 500))
        self.add_sprite(MySprite("ball2.png", 300, 200))

        self.remove_last_sprite()

        #-----------------------------

        # red text "PAUSE"
        font = pygame.font.SysFont("", 72)
        self.text_pause = font.render("PAUSE", True, (255, 0, 0))

        # center text on screen
        screen_center = self.screen.get_rect().center
        self.text_pause_rect = self.text_pause.get_rect(center=screen_center) 

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

    def draw_background(self, screen:pygame.Surface):
        screen.fill((0,64,0)) # clear screen to green
        if self.background:
            screen.blit(self.background, (0,0))

    #--------------------------

    def draw_world(self, image):
        temp = pygame.Surface(self.SCREEN_SIZE, pygame.SRCALPHA, 32).convert_alpha()
        image_rect = image.get_rect()

        for x in range(0, self.SCREEN_WIDTH, 60):
            for y in range(0,self.SCREEN_WIDTH, 60):
                temp.blit(image,(x,y))

        return temp


    #--------------------------

    def set_background(self, image=None):
        if image: 
            self.background = pygame.image.load(image)

    #--------------------------

    def run(self):

        clock = pygame.time.Clock()

        RUNNING = True
        PAUSED = False

        while RUNNING:

            #--- events ---

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    RUNNING = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        RUNNING = False
                    elif event.key == pygame.K_SPACE:
                        PAUSED = not PAUSED

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

            #--- changes ----

            if not PAUSED:
                # change elements position
                self.player.update()

            #--- draws ---

            self.draw_background(self.screen)
            self.draw_sprites(self.screen) 
            self.player.draw(self.screen)

            if PAUSED:
                # draw pause string
                self.screen.blit(self.text_pause, self.text_pause_rect.topleft)

            pygame.display.update()

            #--- FPS ---

            clock.tick(25) # 25 Frames Per Seconds

        #--- finish ---

        pygame.quit()