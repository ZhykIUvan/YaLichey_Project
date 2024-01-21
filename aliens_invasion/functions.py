import runpy

import pygame
import sys

from aliens_invasion.bullets import Laser
from aliens_invasion.alien import Alien
from time import sleep


def events_loop(screen, settings, game_stats, player, alien, alien_group, laser_group, play_button, exit_button, score):
    # цикл событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            # обработка нажатий клавиш
            events_keydown(settings, event, player, laser_group)

        elif event.type == pygame.KEYUP:
            # обработка отжатий клавиш
            events_keyup(event, player)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            events_mouse_down(screen, settings, game_stats, player, alien, alien_group, laser_group, play_button,
                              exit_button, score)


def events_keydown(settings, event, player, laser_group):
    # обработка нажатий клавиш, движение и выстрел
    if event.key == pygame.K_a:
        player.moving_left = True
    elif event.key == pygame.K_d:
        player.moving_right = True
    if event.key == pygame.K_SPACE:
        shoot_laser(settings, player, laser_group)


def events_keyup(event, player):
    # обработка отжатий клавиш и движение
    if event.key == pygame.K_a:
        player.moving_left = False
    elif event.key == pygame.K_d:
        player.moving_right = False


def events_mouse_down(screen, settings, game_stats, player, alien, alien_group, laser_group, play_button,
                      exit_button, score):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not game_stats.game_active:
        game_stats.reset()
        game_stats.game_active = True

        alien_group.empty()
        laser_group.empty()
        create_army(screen, settings, alien, alien_group)
        player.move_to_center()

        score.create_score()
        score.create_level()
        score.create_ships()

        pygame.mouse.set_visible(False)
    if exit_button.rect.collidepoint(mouse_x, mouse_y):
        pygame.quit()
        runpy.run_module(mod_name='menu')
        sys.exit()


def shoot_laser(settings, player, laser_group):
    # выстрел
    if len(laser_group) < settings.BULLETS_RECHARGE:
        # если не превышаем допустимое кол-ов лазеров, то создаем новый
        new_laser = Laser(player)
        laser_group.add(new_laser)


def update_laser(screen, settings, game_stats, alien, alien_group, laser_group, score):
    # обработка лазеров

    # обработка столкновений лазеров с пришельцами
    collisions = pygame.sprite.groupcollide(laser_group, alien_group, True, True)

    if collisions:
        # если лазером попали в пришельца, то прибавляем очки
        game_stats.score += len(collisions.values())
        score.create_score()

    if len(alien_group) == 0:
        # если пришельцов нет, то создаем новый флот, увеличиваем скорость и уровень
        laser_group.empty()
        game_stats.level += 1
        score.create_level()
        settings.ALIEN_SPEED_X += 1
        settings.BULLETS_RECHARGE += 1
        create_army(screen, settings, alien, alien_group)

    for laser in laser_group.sprites():
        # отрисовка, движение и удаление лазеров
        laser.draw()
        laser.moving()
        if laser.rect.bottom <= 0:
            laser_group.remove(laser)


def create_army(screen, settings, alien, alien_group):
    # создание флота пришельцев

    # сколько пришельцев поместится по ширине и высоте
    amount_alien_col = (screen.get_width() - (2 * alien.rect.width)) // (2 * alien.rect.width)
    amount_alien_row = (screen.get_height() // 2 + alien.rect.height) // (2 * alien.rect.height)

    for rows_number in range(amount_alien_row):
        for alien_number in range(amount_alien_col):
            # создаем пришельца столько раз, сколько вычислили
            create_alien(settings, alien_group, rows_number, alien_number)


def create_alien(settings, alien_group, rows_number, alien_number):
    # создание пришельца и добавление в группу
    alien = Alien(settings)
    alien.x = alien.rect.width + (2 * alien.rect.width * alien_number)
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + (2 * alien.rect.height * rows_number)
    alien_group.add(alien)


def update_aliens(screen, settings, game_stats, player, alien, alien_group, laser_group, score):
    # обновление пришельцев: отрисовка, проверка достижения края и движение
    alien_group.draw(screen)

    check_army_edges(settings, alien_group)
    alien_group.update()

    if pygame.sprite.spritecollideany(player, alien_group):
        # если игрок столкнулся с каким-либо пришельцем, то уменьшаются жизни
        player_hit(screen, settings, game_stats, player, alien, alien_group, laser_group, score)

    # проверка столкновения с нижним краем
    check_aliens_bottom(screen, settings, game_stats, player, alien, alien_group, laser_group, score)


def player_hit(screen, settings, game_stats, player, alien, alien_group, laser_group, score):
    # столкновение с игроком

    if game_stats.lives > 1:
        # уменьшаем жизни
        game_stats.lives -= 1
        score.create_ships()

        # очистка экрана
        alien_group.empty()
        laser_group.empty()

        # создание нового флота
        create_army(screen, settings, alien, alien_group)
        player.move_to_center()
        sleep(1)
    else:
        game_stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(screen, settings, game_stats, player, alien, alien_group, laser_group, score):
    # проверка столкнулись ли пришельцы с нижнем краем
    screen_rect = screen.get_rect()
    for alien in alien_group.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # если пришелец коснулся края экрана, то происходит то же самое что и в player_hit
            player_hit(screen, settings, game_stats, player, alien, alien_group, laser_group, score)
            break


def check_army_edges(settings, alien_group):
    # проверка достижения края
    for alien in alien_group.sprites():
        if alien.check_edges():
            # если достигли края, то меняем направление флоту и прерываем
            change_army_direction(settings, alien_group)
            break


def change_army_direction(settings, alien_group):
    # смена направления флота и движение вниз
    for alien in alien_group.sprites():
        alien.rect.y += settings.ALIEN_SPEED_Y
    settings.ALIEN_DIRECTION *= -1


def update_screen(screen, settings, game_stats, player, alien, alien_group, bg, laser_group, score):
    # обновление экрана (1 кадр)

    # фон
    screen.blit(bg, (0, 0))

    # счет
    score.draw()

    # обновление игрока: отрисовка и движение
    player.draw()
    player.moving()

    # обновление лазеров
    update_laser(screen, settings, game_stats, alien, alien_group, laser_group, score)

    # обновление пришельцев
    update_aliens(screen, settings, game_stats, player, alien, alien_group, laser_group, score)

    pygame.display.flip()
