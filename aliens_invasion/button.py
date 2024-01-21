import pygame


class Button:
    def __init__(self, screen, settings, text):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # размеры и свойства кнопки
        self.width = 250
        self.height = 70
        self.bg_color = 243, 245, 140
        self.text_color = 10, 10, 10

        # "Вместо courier можно поставить None"
        self.font = pygame.font.SysFont('Courier', 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        if text == 'Играть':
            self.rect.center = self.screen_rect.center
        else:
            self.rect.center = self.screen_rect.centerx, self.screen_rect.centery + 3 * self.rect.centery

        self.creating_text(text)

    def creating_text(self, text):
        # Создание прямоугольника из текста и выравнивание
        self.text_surf = self.font.render(text, True, self.text_color, self.bg_color)
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = self.rect.center

    def draw(self):
        # отрисовка кнопки
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.text_surf, self.text_rect)