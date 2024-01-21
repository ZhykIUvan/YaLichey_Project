import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, settings):
        super(Player, self).__init__()
        self.image = pygame.image.load('img/player.png')
        self.screen = pygame.display.get_surface()
        self.settings = settings

        self.screen_rect = self.screen.get_rect()
        self.rect = self.image.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 10

        self.moving_left = False
        self.moving_right = False

        self.speed = self.settings.PLAYER_SPEED
        self.center = float(self.rect.centerx)

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def moving(self):
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.speed

        self.rect.centerx = self.center

    def move_to_center(self):
        # размещает игрока по центру экрана
        self.center = self.screen_rect.centerx
        self.rect.centerx = self.center
