import pygame
import sys

import aliens_invasion.alien_invasion_py
from buttons import Button


def run_menu():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))

    pygame.display.set_caption('menu')

    aliens_button = Button(screen, 'Вторжение пришельцев', 320, 170, 420, 70)
    exit_button = Button(screen, 'Выход', 960, 360, 210, 70)

    def draw_bg(screen):
        bg = pygame.image.load('img/bg.jpg')
        screen.blit(bg, [0, 0])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if aliens_button.rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    aliens_invasion.alien_invasion_py.run_game_aliens()
                    sys.exit()
                elif exit_button.rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

        draw_bg(screen)
        aliens_button.draw()
        exit_button.draw()

        pygame.display.flip()


run_menu()
