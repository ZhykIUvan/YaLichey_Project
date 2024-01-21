import pygame
from aliens_invasion.player import Player


class Score:
    def __init__(self, screen, settings, game_stats):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.settings = settings
        self.game_stats = game_stats

        # настройки шрифта
        self.text_color = 243, 245, 140
        self.font = pygame.font.SysFont('Courier', 48)

        self.create_score()
        self.create_level()
        self.create_ships()

    def create_score(self):
        # создание изображения текста
        score = str(self.game_stats.score)
        self.score_surf = self.font.render(score, True, self.text_color)
        self.score_rect = self.score_surf.get_rect()
        self.score_rect.topleft = (20, 20)

    def create_level(self):
        # создание изображения текста
        level = str(self.game_stats.level)
        self.level_surf = self.font.render(level, True, self.text_color)
        self.level_rect = self.level_surf.get_rect()
        self.level_rect.center = self.screen_rect.centerx, 20

    def create_ships(self):
        self.ships = pygame.sprite.Group()
        for ship_number in range(self.game_stats.lives):
            ship = Player(self.settings)
            ship.rect.topleft = self.screen_rect.width - ship.rect.width * (ship_number + 1) - 20, 20
            self.ships.add(ship)

    def draw(self):
        self.screen.blit(self.score_surf, self.score_rect)
        self.screen.blit(self.level_surf, self.level_rect)
        self.ships.draw(self.screen)
