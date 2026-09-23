from pygame.math import Vector2
from asteroids.constants import *
from asteroids.utils import (
    blit_rotated,
    load_sprite,
    load_sound,
    scale_sprite,
    window_scale,
    wrap_position,
)
from models.bullet import Bullet
from models.models import GameObject


class Spaceship(GameObject):
    def __init__(self, position, create_bullet_callback, screen):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        self.direction = Vector2(GameObject.UP)
        self._screen = screen
        self._scale = window_scale(screen)
        super().__init__(
            position,
            scale_sprite(load_sprite("ship"), screen, SHIP_SCREEN_FRACTION),
            Vector2(0),
        )

    def rescale(self, screen):
        self._screen = screen
        self._scale = window_scale(screen)
        self.sprite = scale_sprite(load_sprite("ship"), screen, SHIP_SCREEN_FRACTION)
        self.radius = self.sprite.get_width() / 2

    def draw(self, surface):
        blit_rotated(surface, self.sprite, self.position, self.direction)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def shoot(self):
        bullet_velocity = (
            self.direction * BULLET_SPEED * self._scale + self.velocity
        )
        bullet = Bullet(self.position, bullet_velocity, self._screen)
        if bullet_velocity.length_squared():
            forward = bullet_velocity.normalize()
        else:
            forward = Vector2(self.direction)
        bullet.position += forward * (
            self.sprite.get_height() / 2 + bullet.sprite.get_height() / 2
        )
        self.create_bullet_callback(bullet)
        self.laser_sound.play()

    def accelerate(self):
        self.velocity += self.direction * ACCELERATION * self._scale

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)
