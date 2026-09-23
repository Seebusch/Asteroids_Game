import pygame
import random
from logger import log_event
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
   def __init__(self, x: float, y: float, radius: float) -> None:
      super().__init__(x, y, radius)

   def draw(self, screen: pygame.Surface) -> None:
      pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

   def update(self, dt: float) -> None:
      self.position += self.velocity*dt

   def split(self) -> None:
      self.kill()
      if self.radius <= ASTEROID_MIN_RADIUS:
         return
      else:
         log_event("asteroid_split")
         rangle = random.uniform(20, 50)
         first_split = self.velocity.rotate(rangle)
         second_split = self.velocity.rotate(rangle*(-1))
         new_radius = self.radius-ASTEROID_MIN_RADIUS
         first_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
         first_asteroid.velocity = first_split*1.2
         second_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
         second_asteroid.velocity = second_split*1.2
