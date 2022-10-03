from random import randint, choice
import pygame as pg
from pygame.sprite import Sprite, Group
from timer import Timer
from sound import Sound

aliens_killed = 0


class Alien(Sprite):
    alien_images0 = [pg.transform.rotozoom(pg.image.load(f'images/alien__0{n}.png'), 0, 0.7) for n in range(2)]
    alien_images1 = [pg.transform.rotozoom(pg.image.load(f'images/alien__1{n}.png'), 0, 0.7) for n in range(2)]
    alien_images2 = [pg.transform.rotozoom(pg.image.load(f'images/alien__2{n}.png'), 0, 0.7) for n in range(2)]

    alien_timers = {0: Timer(image_list=alien_images0),
                    1: Timer(image_list=alien_images1),
                    2: Timer(image_list=alien_images2)}

    alien_scores = {0: 10, 1: 20, 2: 40}

    alien_explosion_images = [pg.image.load(f'images/alienexplode{n}.png') for n in range(7)]

    def __init__(self, game, type):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pg.image.load('images/alien__00.png')
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.type = type
        self.game = game
        self.dying = self.dead = False
        self.timer_normal = Alien.alien_timers[type]
        self.timer_explosion = Timer(image_list=Alien.alien_explosion_images, is_loop=False)
        self.timer = self.timer_normal
        self.sb = game.scoreboard
        self.score = Alien.alien_scores[type]

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def check_bottom_or_ship(self, ship):
        screen_rect = self.screen.get_rect()
        return self.rect.bottom >= screen_rect.bottom or self.rect.colliderect(ship.rect)

    def hit(self):
        if not self.dying:
            self.dying = True
            self.timer = self.timer_explosion

    def update(self):
        global aliens_killed
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
            aliens_killed += 1
            if aliens_killed % 14 == 0:
                self.game.speed_up()
        settings = self.settings
        self.x += (settings.alien_speed_factor * settings.fleet_direction)
        self.rect.x = self.x
        self.draw()

    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)


class Aliens:
    def __init__(self, game, sound):
        self.model_alien = Alien(game=game, type=1)
        self.game = game
        self.sb = game.scoreboard
        self.aliens = Group()
        self.ship_lasers = game.ship_lasers.lasers  # a laser Group
        self.aliens_lasers = game.alien_lasers
        self.screen = game.screen
        self.settings = game.settings
        self.shoot_requests = 0
        self.ship = game.ship
        self.create_fleet()
        self.sound = sound

        # UFO Setup
        self.ufo = pg.sprite.GroupSingle()
        self.ufo_spawn_time = randint(1000, 1600)

    def get_number_aliens_x(self, alien_width):
        available_space_x = self.settings.screen_width - 6 * alien_width
        number_aliens_x = int(available_space_x / (1.2 * alien_width))
        return number_aliens_x

    def get_number_rows(self, ship_height, alien_height):
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = 6
        return number_rows

    def reset(self):
        global aliens_killed
        self.aliens.empty()
        self.create_fleet()
        self.aliens_lasers.reset()
        aliens_killed = 0

    def create_alien(self, alien_number, row_number):
        type = row_number // 2
        alien = Alien(game=self.game, type=type)
        alien_width = alien.rect.width

        alien.x = alien_width + 1.5 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 1.2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def create_fleet(self):
        number_aliens_x = self.get_number_aliens_x(self.model_alien.rect.width)
        number_rows = self.get_number_rows(self.ship.rect.height, self.model_alien.rect.height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, row_number)

    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def check_fleet_bottom(self):
        for alien in self.aliens.sprites():
            if alien.check_bottom_or_ship(self.ship):
                self.ship.hit()
                break

    def check_fleet_empty(self):
        if len(self.aliens.sprites()) == 0:
            print('Aliens all gone!')
            self.game.reset()

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def shoot_from_random_alien(self):
        self.shoot_requests += 1
        if self.shoot_requests % self.settings.aliens_shoot_every != 0:
            return

        num_aliens = len(self.aliens.sprites())
        alien_num = randint(0, num_aliens)
        i = 0
        for alien in self.aliens.sprites():
            if i == alien_num:
                self.aliens_lasers.shoot(game=self.game, x=alien.rect.centerx, y=alien.rect.bottom)
            i += 1

    def check_collisions(self):
        collisions = pg.sprite.groupcollide(self.aliens, self.ship_lasers, False, True)
        if collisions:
            for alien in collisions:
                alien.hit()
                self.sb.increment_score(alien.score)

        collisions = pg.sprite.groupcollide(self.ufo, self.ship_lasers, False, True)
        if collisions:
            for ufo in collisions:
                ufo.hit()
            self.sb.increment_score(randint(100, 200))

        collisions = pg.sprite.spritecollide(self.ship, self.aliens_lasers.lasers, True)
        if collisions:
            self.ship.hit()

        collisions = pg.sprite.groupcollide(self.aliens_lasers.lasers, self.ship_lasers, True, True)
        if collisions:
            print("ship_lasers hitting an aliens_lasers")

    def update(self):
        self.check_fleet_edges()
        self.check_fleet_bottom()
        self.check_collisions()
        self.check_fleet_empty()
        self.shoot_from_random_alien()
        self.ufo_timer()
        self.ufo.update()
        for alien in self.aliens.sprites():
            if alien.dead:  # set True once the explosion animation has completed
                alien.remove()
            alien.update()
        self.aliens_lasers.update()

    def draw(self):
        for alien in self.aliens.sprites():
            alien.draw()

    def ufo_timer(self):
        self.ufo_spawn_time -= 1
        if self.ufo_spawn_time <= 0:
            self.ufo.add(UFO(choice(['right', 'left']), self.game))
            self.sound.ufo()
            self.ufo_spawn_time = randint(1000, 1600)


class UFO(pg.sprite.Sprite):
    ufo_images = [pg.transform.rotozoom(pg.image.load(f'images/alien__06.png'), 0, 1.0)]
    ufo_explosion_images = [pg.transform.rotozoom(pg.image.load(f'images/alienexplode{n}.png'), 0, 1.0) for n in
                            range(6)]

    def __init__(self, side, game):
        super().__init__()
        self.settings = game.settings
        self.screen = game.screen

        self.timer_normal = Timer(image_list=UFO.ufo_images)
        self.timer_explosion = Timer(image_list=UFO.ufo_explosion_images, delay=200, is_loop=False)
        self.timer = self.timer_normal

        self.dying = self.dead = False

        self.image = pg.image.load('images/alien__06.png').convert_alpha()
        if side == 'right':
            x = self.settings.screen_width + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft=(x, 80))

    def update(self):
        self.rect.x += self.speed

        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
        self.draw()

    def hit(self):
        if not self.dying:
            self.dying = True
            self.timer = self.timer_explosion

    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)

    # def display_score(self, score):
    # font = pygame.font.Font('arial.ttf', 32)
    # text = font.render(f'{score}', True, (255, 255, 255))
    # textRext = text.get_rect()
    # self.screen.blit(text, textRext)
