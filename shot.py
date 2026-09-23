from circleshape import CircleShape
from constants import SHOT_RADIUS, LINE_WIDTH
import pygame

class Shot(CircleShape):
   def __init__(self, x: float, y: float) -> None:
      super().__init__(x, y, SHOT_RADIUS)

   def draw(self, screen: pygame.Surface) -> None:
      pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

   def update(self, dt: float) -> None:
      self.position += self.velocity*dt

   def set_velocity(self, velocity: pygame.Vector2) -> None:
      self.velocity = velocity
