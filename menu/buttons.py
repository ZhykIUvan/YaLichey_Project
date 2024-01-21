import pygame


class Button:
    def __init__(self, screen, text, x, y, width, height):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = width
        self.height = height
        self.bg_color = 243, 245, 140
        self.text_color = 10, 10, 10

        self.font = pygame.font.SysFont('Courier', 35)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = x, y

        self.creating_text(text)

    def creating_text(self, text):
        self.text_surf = self.font.render(text, True, self.text_color, self.bg_color)
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = self.rect.center

    def draw(self):
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.text_surf, self.text_rect)
