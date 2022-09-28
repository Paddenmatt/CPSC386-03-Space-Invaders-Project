import pygame.font
import pygame as pg

class Button():

    def __init__(self, settings, screen):
        """Initialize button attributes."""
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image = pg.image.load("images/play_game (1).jpg")
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
        self.image = pygame.image.load("images/space_invaders (1).jpg")
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
        self.image = pygame.image.load("images/alien_scores (1).jpg")
        self.rect = self.image.get_rect()
        self.rect.center = (600, 300)
        self.prep_msg()

    def prep_msg(self):
        self.msg_image_rect = self.image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.blit(self.image, self.msg_image_rect)