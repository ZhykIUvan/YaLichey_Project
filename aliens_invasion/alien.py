import pygame


class Alien(pygame.sprite.Sprite):
    def __init__(self, settings):
        super(Alien, self).__init__()
        self.image = pygame.image.load('img/alien.png')
        self.screen = pygame.display.get_surface()

        self.screen_rect = self.screen.get_rect()
        self.rect = self.image.get_rect()

        self.rect.x = self.image.get_width()
        self.rect.y = self.image.get_height()

        self.x = float(self.rect.x)

        self.settings = settings

        # self.direction = -1

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= screen_rect.left:
            return True

    def update(self):
        self.x += (self.settings.ALIEN_SPEED_X * self.settings.ALIEN_DIRECTION)
        self.rect.x = self.x
