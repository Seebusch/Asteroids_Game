import random
from pathlib import Path
from pygame import Color
from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame.transform import rotozoom
from asteroids.constants import SCREEN_REFERENCE

ASSETS = Path(__file__).resolve().parent.parent / "assets"

def load_sprite(name, with_alpha=True):
    path = ASSETS / "sprites" / f"{name}.png"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()

def print_text(surface, text, font, color=Color("tomato"), y_offset=0):
    text_surface = font.render(text, True, color)

    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2 + Vector2(0, y_offset)

    surface.blit(text_surface, rect)

def window_scale(screen):
    return min(screen.get_size()) / SCREEN_REFERENCE

def blit_rotated(surface, sprite, position, direction):
    # Sprites zeigen im Bild nach oben. angle_to liefert die passende Drehung.
    angle = Vector2(direction).angle_to(Vector2(0, -1))
    rotated_surface = rotozoom(sprite, angle, 1.0)
    blit_position = Vector2(position) - Vector2(rotated_surface.get_size()) * 0.5
    surface.blit(rotated_surface, blit_position)

def scale_sprite(sprite, screen, fraction):
    bounds = sprite.get_bounding_rect(min_alpha=32)
    cropped = sprite.subsurface(bounds).copy()
    longest = max(cropped.get_width(), cropped.get_height())
    target = min(screen.get_size()) * fraction
    if longest == 0:
        return cropped
    return rotozoom(cropped, 0, target / longest)

def load_sound(name):
    path = ASSETS / "sounds" / f"{name}.wav"
    return Sound(path)

def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)

def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )

def get_random_velocity(min_speed, max_speed):
    speed = random.uniform(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)

def _handle_input(spaceship, instance):
    for event in instance.event.get():
        if event.type == instance.QUIT or (
            event.type == instance.KEYDOWN and event.key == instance.K_ESCAPE
        ):
            quit()
    is_key_pressed = instance.key.get_pressed()
    if is_key_pressed[instance.K_RIGHT]:
        spaceship.rotate(clockwise=True)
    elif is_key_pressed[instance.K_LEFT]:
        spaceship.rotate(clockwise=False)
    if is_key_pressed[instance.K_UP]:
        spaceship.accelerate()