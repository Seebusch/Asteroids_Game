from asteroids.constants import ASTEROID_SCREEN_FRACTION
from asteroids.utils import get_random_velocity, load_sprite, scale_sprite, window_scale
from models.models import GameObject


class Asteroid(GameObject):
    _sprites = {}

    def __init__(
        self,
        position,
        create_asteroid_callback,
        screen,
        size=3,
        speed_range=(1, 3),
    ):
        self.create_asteroid_callback = create_asteroid_callback
        self.screen = screen
        self.size = size
        self.speed_range = speed_range

        super().__init__(
            position,
            self._get_sprite(size, screen),
            get_random_velocity(*speed_range) * window_scale(screen),
        )

    @classmethod
    def _get_sprite(cls, size, screen):
        key = (size, screen.get_size())
        if key not in cls._sprites:
            size_to_name = {
                3: "big_asteroid",
                2: "medium_asteroid",
                1: "small_asteroid",
            }
            sprite = load_sprite(size_to_name[size])
            cls._sprites[key] = scale_sprite(
                sprite, screen, ASTEROID_SCREEN_FRACTION[size]
            )
        return cls._sprites[key]

    @classmethod
    def clear_sprite_cache(cls):
        cls._sprites.clear()

    def rescale(self, screen):
        self.screen = screen
        self.sprite = self._get_sprite(self.size, screen)
        self.radius = self.sprite.get_width() / 2

    def split(self):
        if self.size > 1:
            for _ in range(2):
                new_asteroid = Asteroid(
                    self.position,
                    self.create_asteroid_callback,
                    self.screen,
                    self.size - 1,
                    self.speed_range,
                )
                self.create_asteroid_callback(new_asteroid)
