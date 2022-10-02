import pygame as pg
from settings import Settings


class Button():

    def __init__(self, settings, screen):
        """Initialize button attributes."""
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image = pg.image.load("images/play_game.jpg")
        self.rect = self.image.get_rect()

        self.rect.center = (602, 580)

        self.prep_msg()

    def prep_msg(self):
        self.msg_image_rect = self.image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.blit(self.image, self.msg_image_rect)


class Title():
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pg.image.load("images/space_invaders.jpg")
        self.rect = self.image.get_rect()
        self.rect.center = (600, 150)
        self.prep_msg()

    def prep_msg(self):
        self.msg_image_rect = self.image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.blit(self.image, self.msg_image_rect)


class Alien_sheet():
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pg.image.load("images/alien_scores.jpg")
        self.rect = self.image.get_rect()
        self.rect.center = (600, 300)
        self.prep_msg()

    def prep_msg(self):
        self.msg_image_rect = self.image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.blit(self.image, self.msg_image_rect)


class HighScores():
    def __init__(self, settings, screen, msg):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 200, 40
        self.button_color = (0, 0, 0)
        self.text_color = (118, 238, 0)
        self.font = pg.font.SysFont(None, 36)
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = (600, 650)
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_highscore = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_highscore_rect = self.msg_highscore.get_rect()
        self.msg_highscore_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_highscore, self.msg_highscore_rect)
