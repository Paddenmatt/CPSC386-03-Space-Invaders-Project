import pygame as pg
from pygame.sprite import Sprite, Group


class Barrier(Sprite):
    color = 255, 0, 0
    black = 0, 0, 0

    def __init__(self, game, rect):
        super().__init__()
        self.screen = game.screen
        self.rect = rect
        self.settings = game.settings

    def hit(self):
        print("Barrier hit!")

    def update(self):
        self.draw()

    def draw(self):
        pg.draw.rect(self.screen, Barrier.color, self.rect, 0, 20)
        pg.draw.circle(self.screen, self.settings.bg_color, (self.rect.centerx, self.rect.bottom), self.rect.width / 6)


class Barriers:
    def __init__(self, game):
        self.game = game
        self.aliens_lasers = game.alien_lasers.lasers
        self.ship_lasers = game.ship_lasers.lasers
        self.settings = game.settings
        self.bunker = Group()
        self.create_barriers()

    def create_barriers(self):
        width = self.settings.screen_width / 10
        height = 2.0 * width / 4.0
        top = self.settings.screen_height - 2.1 * height
        rects = [pg.Rect(x * 2 * width + 1.5 * width, top, width, height) for x in range(4)]  # SP w  3w  5w  7w  SP
        self.bunker = [Barrier(game=self.game, rect=rects[i]) for i in range(4)]

    def reset(self):
        self.create_barriers()

    def update(self):
        for barrier in self.bunker:
            barrier.update()
            self.check_collisions()

    def check_collisions(self):
        alien_collisions = pg.sprite.groupcollide(self.bunker, self.aliens_lasers, False, True)
        if alien_collisions:
            for barrier in alien_collisions:
                barrier.hit()

        ship_collisions = pg.sprite.groupcollide(self.bunker, self.ship_lasers, False, True)
        if ship_collisions:
            for barrier in ship_collisions:
                barrier.hit()
