from pygame.math import Vector2
from asteroids.constants import BULLET_RANGE, BULLET_SCREEN_FRACTION
from asteroids.utils import blit_rotated, load_sprite, scale_sprite, window_scale
from models.models import GameObject


class Bullet(GameObject):
    _sprite = None
    _sprite_size = None

    def __init__(self, position, velocity, screen):
        super().__init__(position, self.sprite_for(screen), Vector2(velocity))
        self.distance_traveled = 0
        self.max_range = BULLET_RANGE * window_scale(screen)

    @classmethod
    def sprite_for(cls, screen):
        size = screen.get_size()
        if cls._sprite is None or cls._sprite_size != size:
            cls._sprite = scale_sprite(
                load_sprite("bullet"), screen, BULLET_SCREEN_FRACTION
            )
            cls._sprite_size = size
        return cls._sprite

    def rescale(self, screen):
        new_range = BULLET_RANGE * window_scale(screen)
        if self.max_range:
            self.distance_traveled *= new_range / self.max_range
        self.max_range = new_range
        self.sprite = self.sprite_for(screen)
        self.radius = self.sprite.get_width() / 2

    def move(self, surface):
        self.position += self.velocity
        self.distance_traveled += self.velocity.length()

    def expired(self, surface):
        if self.distance_traveled >= self.max_range:
            return True
        reach = self.sprite.get_height() / 2
        visible = surface.get_rect().inflate(reach * 2, reach * 2)
        return not visible.collidepoint(self.position)

    def draw(self, surface):
        direction = self.velocity if self.velocity.length_squared() else GameObject.UP
        blit_rotated(surface, self.sprite, self.position, direction)

    def collides_with(self, other):
        direction = self.velocity
        if not direction.length_squared():
            return super().collides_with(other)

        direction = direction.normalize()
        half_length = self.sprite.get_height() / 2
        half_width = self.sprite.get_width() / 2
        start = self.position - direction * half_length
        segment = direction * (half_length * 2)
        t = (other.position - start).dot(segment) / segment.length_squared()
        t = max(0.0, min(1.0, t))
        closest = start + segment * t
        return closest.distance_to(other.position) < half_width + other.radius
