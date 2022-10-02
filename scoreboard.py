import pygame as pg


# import pygame.font

class Scoreboard:
    def __init__(self, game):
        self.score = 0
        self.level = 0

        f = open('high_score.txt', 'r')
        data = f.readline()
        self.high_score = int(data)

        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (30, 30, 30)
        self.font = pg.font.SysFont(None, 48)

        self.score_image = None
        self.score_rect = None
        self.prep_score()
        self.prep_high_score()

    def increment_score(self):
        self.score += self.settings.alien_points
        self.prep_score()

    def prep_score(self):
        score_str = str(self.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def reset(self):
        self.score = 0
        self.update()

    def update(self):
        self.draw()

    def draw(self):
        self.screen.blit(self.score_image, self.score_rect)

    def check_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.prep_high_score()
            filename = 'high_score.txt'
            with open(filename, 'w') as file_object:
                file_object.write(str(self.high_score))

    def prep_high_score(self):
        high_score = int(round(self.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
