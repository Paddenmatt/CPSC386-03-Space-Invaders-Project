import pygame as pg
from settings import Settings
import game_functions as gf

from button import Title, Button, Alien_sheet
from laser import Lasers, LaserType
from alien import Aliens
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
from barrier import Barriers
import sys


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")

        self.sound = Sound(bg_music="sounds/startrek.wav")
        self.play_button = Button(self.settings, self.screen)
        self.title = Title(self.settings, self.screen)
        self.name = Alien_sheet(self.settings, self.screen)
        self.scoreboard = Scoreboard(game=self)

        self.ship_lasers = Lasers(settings=self.settings, type=LaserType.SHIP)
        self.alien_lasers = Lasers(settings=self.settings, type=LaserType.ALIEN)
        
        self.barriers = Barriers(game=self)
        self.ship = Ship(game=self)
        self.aliens = Aliens(game=self)
        self.settings.initialize_speed_settings()

    def reset(self):
        print('Resetting game...')
        # self.lasers.reset()
        self.barriers.reset()
        self.ship.reset()
        self.aliens.reset()
        # self.scoreboard.reset()

    def game_over(self):
        print('All ships gone: game over!')
        self.sound.gameover()
        pg.quit()
        sys.exit()

    def play(self):
        self.sound.play_bg()
        while True:     # at the moment, only exits in gf.check_events if Ctrl/Cmd-Q pressed
            if not self.settings.game_active:
                self.play_button.draw_button()
                self.name.draw_button()
                self.title.draw_button()

            gf.check_events(settings=self.settings, ship=self.ship, play_button=self.play_button)
            if self.settings.game_active:
                self.screen.fill(self.settings.bg_color)
                self.ship.update()
                self.aliens.update()
                self.barriers.update()
                self.scoreboard.update()
            pg.display.flip()


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
