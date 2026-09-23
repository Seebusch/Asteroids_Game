import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfields import AsteroidField
from shot import Shot

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    asteroidfield = AsteroidField()
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0
    player = Player((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2),0)
    while True:
       log_state()
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
             return
       screen.fill("black")
       updatable.update(dt)
       for asteroid in asteroids:
          for shot in shots:
             if shot.collides_with(asteroid):
                log_event("asteroid_shot")
                shot.kill()
                asteroid.split()
       for asteroid in asteroids:
          if player.collides_with(asteroid):
             log_event("player_hit")
             print("Game over!")
             sys.exit()
       for figure in drawable:
           figure.draw(screen)
       pygame.display.flip()
       dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
