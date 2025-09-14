import pygame
import sys
from constants import *
from player import *
from asteroid import *
from asteroidfield import *

def main():
    # INITIALIZATION
    print("Starting Asteroids!")
    print(f'Screen width: {SCREEN_WIDTH}')
    print(f'Screen height: {SCREEN_HEIGHT}')

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    time_clock = pygame.time.Clock()


    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    dt = 0

    # GAME LOOP
    while(True):
        # User clicks 'x' closes the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return        




        updatable.update(dt)

        for obj in asteroids:
            if obj.collision(player):
                print("Game Over!")
                sys.exit()

        for asteroid in asteroids:
            for bullet in shots:
                if bullet.collision(asteroid):
                    asteroid.split()
                    bullet.kill()

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()
        dt = time_clock.tick(60) / 1000


if __name__ == "__main__":
    main()
