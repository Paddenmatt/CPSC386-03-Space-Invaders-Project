import pygame as pg
from settings import Settings
import game_functions as gf
from button import HighScores
from button import Title, Button, Alien_sheet
from laser import Lasers, LaserType
from alien import Aliens
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
import sys
import barrier


class Game:
    soundSpeed = 0

    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")
        self.sound = Sound(bg_music="sounds/game_music0.wav")
        self.play_button = Button(self.settings, self.screen)
        self.title = Title(self.settings, self.screen)
        self.name = Alien_sheet(self.settings, self.screen)
        self.scoreboard = Scoreboard(game=self)
        self.ship_lasers = Lasers(settings=self.settings, type=LaserType.SHIP)
        self.alien_lasers = Lasers(settings=self.settings, type=LaserType.ALIEN)
        self.hs = HighScores(self.settings, self.screen, f'HighScore = {self.scoreboard.high_score}')
        # self.barriers = Barriers(game=self)
        self.ship = Ship(game=self)
        self.aliens = Aliens(game=self, sound=self.sound)
        self.settings.initialize_speed_settings()

        # Obstacle setup
        self.shape = barrier.shape
        self.block_size = 6
        self.blocks = pg.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (self.settings.screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start=self.settings.screen_width / 15, y_start=self.settings.screen_height - 150)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = barrier.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def collision_checks(self):
        # Ship Laser and Barrier collision
        if self.ship_lasers.lasers:
            for laser in self.ship_lasers.lasers:
                # obstacle collisions
                if pg.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

        # Alien Laser and Barrier collision
        if self.alien_lasers.lasers:
            for laser in self.alien_lasers.lasers:
                # obstacle collisions
                if pg.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

    def reset(self):
        print('Resetting game...')
        self.ship.reset()
        self.aliens.reset()
        self.soundSpeed = -1
        self.speed_up()
        self.blocks.empty()
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start=self.settings.screen_width / 15, y_start=480)

    def game_over(self):
        print('All ships gone: game over!')
        self.sound.gameover()
        self.scoreboard.check_high_score()
        pg.quit()
        sys.exit()

    def play(self):
        self.sound.play_bg()
        while True:
            if not self.settings.game_active:
                self.play_button.draw_button()
                self.name.draw_button()
                self.title.draw_button()
                self.hs.draw_button()

            gf.check_events(settings=self.settings, ship=self.ship, play_button=self.play_button)
            if self.settings.game_active:
                self.screen.fill(self.settings.bg_color)
                self.ship.update()
                self.aliens.update()
                self.blocks.draw(self.screen)
                self.collision_checks()
                self.scoreboard.update()
            pg.display.flip()

    def speed_up(self):
        self.soundSpeed += 1
        print(f"Sound sped set to {self.soundSpeed}")
        pg.mixer.music.stop()
        pg.mixer.music.load(f'sounds/game_music{self.soundSpeed}.wav')
        pg.mixer.music.set_volume(0.7)
        pg.mixer.music.play(-1, 0.0)


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
