import pygame
from pygame.math import Vector2
from pygame.transform import smoothscale
from models.asteroid import Asteroid
from models.spaceship import Spaceship
from asteroids.constants import (
    LEVEL_ASTEROID_BASE,
    LEVEL_ASTEROID_CAP,
    LEVEL_ASTEROID_STEP,
    LEVEL_SPEED_CAP,
    LEVEL_SPEED_MAX,
    LEVEL_SPEED_MIN,
    LEVEL_SPEED_STEP,
    MIN_ASTEROID_DISTANCE,
    SCREEN_REFERENCE,
    WAVE_CLEAR_FRAMES,
    WINDOW_SIZE,
)
from asteroids.scoring import Score
from asteroids.utils import get_random_position, load_sprite, print_text, window_scale


class AsteroidsGame:
    def __init__(self):
        self._init_pygame()
        self._fullscreen = False
        self._windowed_size = WINDOW_SIZE
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
        self._display_size = self.screen.get_size()
        self._background_image = load_sprite("space", False)
        self.background = None
        self.clock = pygame.time.Clock()
        self.font = None
        self.score_font = None
        self._fit_display()
        self.message = ""
        self.score = Score()
        self.level = 1
        self._game_over = False
        self._paused = False
        self._wave_delay = 0

        self.asteroids = []
        self.bullets = []
        self.spaceship = None
        self._begin_level(1)

    def main_loop(self):
        while True:
            self._handle_input()
            self._sync_display_size()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Asteroids")

    def _fit_display(self):
        self.background = smoothscale(self._background_image, self.screen.get_size())
        scale = window_scale(self.screen)
        self.font = pygame.font.Font(None, max(1, round(64 * scale)))
        self.score_font = pygame.font.Font(None, max(1, round(36 * scale)))

    def _toggle_fullscreen(self):
        self._fullscreen = not self._fullscreen
        if self._fullscreen:
            self._windowed_size = self.screen.get_size()
            flags = pygame.FULLSCREEN
        else:
            flags = pygame.RESIZABLE
        size = (0, 0) if self._fullscreen else self._windowed_size
        self.screen = pygame.display.set_mode(size, flags)

    def _sync_display_size(self):
        size = self.screen.get_size()
        if size[0] < 1 or size[1] < 1 or size == self._display_size:
            return

        old = Vector2(self._display_size)
        new = Vector2(size)
        self._display_size = size
        old_scale = min(old.x, old.y) / SCREEN_REFERENCE
        speed_ratio = window_scale(self.screen) / old_scale if old_scale else 1
        Asteroid.clear_sprite_cache()

        for game_object in self._get_game_objects():
            game_object.position.x *= new.x / old.x
            game_object.position.y *= new.y / old.y
            game_object.velocity *= speed_ratio
            game_object.rescale(self.screen)

        self._fit_display()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit()
            elif event.type == pygame.KEYDOWN and (
                event.key == pygame.K_F11
                or (event.key == pygame.K_RETURN and event.mod & pygame.KMOD_ALT)
            ):
                self._toggle_fullscreen()
            elif (
                self._game_over
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_r
            ):
                self._restart()
            elif (
                not self._game_over
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_p
            ):
                self._paused = not self._paused
            elif (
                self.spaceship
                and not self._paused
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()
            elif (
                event.type in (pygame.VIDEORESIZE, pygame.WINDOWRESIZED)
                and not self._fullscreen
            ):
                self.screen = pygame.display.get_surface()

        if not self.spaceship or self._paused:
            return

        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_RIGHT]:
            self.spaceship.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            self.spaceship.rotate(clockwise=False)
        if is_key_pressed[pygame.K_UP]:
            self.spaceship.accelerate()

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]
        if self.spaceship:
            game_objects.append(self.spaceship)
        return game_objects

    def _restart(self):
        self._game_over = False
        self._paused = False
        self._wave_delay = 0
        self.message = ""
        self.score.reset()
        self.bullets.clear()
        self.asteroids.clear()
        self._begin_level(1)

    def _begin_level(self, level):
        self.level = level
        self.bullets.clear()
        self.asteroids.clear()
        self.spaceship = Spaceship(
            Vector2(self._display_size) / 2,
            self.bullets.append,
            self.screen,
        )
        self._spawn_asteroids()

    def _speed_range(self):
        bonus = (self.level - 1) * LEVEL_SPEED_STEP
        low = min(LEVEL_SPEED_MIN + bonus, LEVEL_SPEED_CAP - 1)
        high = min(LEVEL_SPEED_MAX + bonus * 1.5, LEVEL_SPEED_CAP)
        return (low, high)

    def _spawn_asteroids(self):
        count = min(
            LEVEL_ASTEROID_BASE + (self.level - 1) * LEVEL_ASTEROID_STEP,
            LEVEL_ASTEROID_CAP,
        )
        min_asteroid_distance = MIN_ASTEROID_DISTANCE * window_scale(self.screen)
        speed_range = self._speed_range()

        for _ in range(count):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > min_asteroid_distance
                ):
                    break
            self.asteroids.append(
                Asteroid(
                    position,
                    self.asteroids.append,
                    self.screen,
                    speed_range=speed_range,
                )
            )

    def _process_game_logic(self):
        if self._paused or self._game_over:
            return

        if self._wave_delay > 0:
            self._wave_delay -= 1
            if self._wave_delay == 0:
                self.message = ""
                self._begin_level(self.level + 1)
            return

        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    self._game_over = True
                    self.message = "You lost!"
                    return

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if bullet.collides_with(asteroid):
                    self.score.award(asteroid)
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break

        for bullet in self.bullets[:]:
            if bullet.expired(self.screen):
                self.bullets.remove(bullet)

        if not self.asteroids and self.spaceship:
            self.message = f"Level {self.level} cleared!"
            self._wave_delay = WAVE_CLEAR_FRAMES

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        self.score.draw(self.screen, self.score_font, self.level)

        if self._paused:
            print_text(self.screen, "Paused", self.font)
            print_text(
                self.screen,
                "Press P to continue",
                self.score_font,
                pygame.Color("white"),
                y_offset=round(72 * window_scale(self.screen)),
            )
        elif self.message:
            print_text(self.screen, self.message, self.font)
        if self._game_over:
            print_text(
                self.screen,
                "Press R to restart",
                self.score_font,
                pygame.Color("white"),
                y_offset=round(72 * window_scale(self.screen)),
            )

        pygame.display.flip()
        self.clock.tick(60)
