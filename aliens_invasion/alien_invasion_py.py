import pygame
from aliens_invasion.player import Player
from aliens_invasion.alien import Alien
from aliens_invasion.functions import *
from aliens_invasion.settings import Settings
from aliens_invasion.game_stats import GameStats
from aliens_invasion.button import Button
from aliens_invasion.score import Score


def run_game_aliens():
    pygame.init()
    settings = Settings()

    game_stats = GameStats(settings)

    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))

    pygame.display.set_caption('Alien_Invasion')
    bg = pygame.image.load('img/bg_window.png')
    icon = pygame.image.load('img/player.png')

    pygame.display.set_icon(icon)

    player = Player(settings)
    alien = Alien(settings)

    laser_group = pygame.sprite.Group()
    alien_group = pygame.sprite.Group()

    create_army(screen, settings, alien, alien_group)

    play_button = Button(screen, settings, 'Играть')
    exit_button = Button(screen, settings, 'Выход')

    score = Score(screen, settings, game_stats)

    while True:
        events_loop(screen, settings, game_stats, player, alien, alien_group, laser_group, play_button, exit_button, score)

        if game_stats.game_active:
            update_screen(screen, settings, game_stats, player, alien, alien_group, bg, laser_group, score)
        else:
            # отображение кнопки если игра неактивна
            play_button.draw()
            exit_button.draw()
            pygame.display.flip()
