from pygame import Color
from asteroids.utils import window_scale

# Classic Asteroids: smaller rocks are worth more.
POINTS_BY_SIZE = {
    3: 20,
    2: 50,
    1: 100,
}


class Score:
    def __init__(self):
        self.points = 0

    def award(self, asteroid):
        gained = POINTS_BY_SIZE.get(asteroid.size, 0)
        self.points += gained
        return gained

    def reset(self):
        self.points = 0

    def draw(self, surface, font, level, color=Color("white")):
        margin = max(8, round(16 * window_scale(surface)))
        line_gap = max(2, round(4 * window_scale(surface)))
        y = round(margin * 0.75)
        for line in (f"Score: {self.points}", f"Level: {level}"):
            text_surface = font.render(line, True, color)
            surface.blit(text_surface, (margin, y))
            y += text_surface.get_height() + line_gap
