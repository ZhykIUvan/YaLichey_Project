class GameStats:
    def __init__(self, settings):
        self.settings = settings
        self.game_active = False

        self.reset()

    def reset(self):
        # инициализация настроек
        self.settings.ALIEN_SPEED_X = 1
        self.settings.BULLETS_RECHARGE = 3
        self.lives = self.settings.ships_amount
        self.level = self.settings.ALIEN_SPEED_X
        self.score = 0
