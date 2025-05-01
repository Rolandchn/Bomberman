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
        pygame.draw.rect(surface, self.bg_color, self.rect)
        surface.blit(self.text_surf, self.text_surf.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False
