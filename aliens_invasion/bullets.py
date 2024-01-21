import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, player):
        super(Laser, self).__init__()
        self.width = 3
        self.height = 15
        self.color = 196, 12, 12
        self.speed = 4
        self.screen = pygame.display.get_surface()

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = player.rect.centerx
        self.rect.top = player.rect.top

        self.y = self.rect.y

    def moving(self):
        self.y -= self.speed
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
