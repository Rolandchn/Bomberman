import pygame


class Button:
    def __init__(self, x, y, text):
        self.font = pygame.font.SysFont(None, 40)
        
        self.bg_color = (50, 150, 50)
        self.padding = 10

        self.text = text
        self.text_surf = self.font.render(text, True, (255, 255, 255))
        
        text_rect = self.text_surf.get_rect()
        text_rect.width = 100
        
        self.rect = pygame.Rect(x, y, text_rect.width + self.padding * 2, text_rect.height + self.padding * 2)
        self.rect.center = (x, y)  

        self.clicked = False    


    def draw(self, surface: pygame.Surface):
        active = False
        
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                active = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        pygame.draw.rect(surface, self.bg_color, self.rect)
        surface.blit(self.text_surf, self.text_surf.get_rect(center=self.rect.center))

        return active
