import pygame
import random
from circleshape import *
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.position.x, self.position.y), self.radius, 2 )

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        rand_angle = random.uniform(20, 50)
        asteroid_1 = Asteroid(self.position.x, self.position.y, self.radius / 2)    
        asteroid_2 = Asteroid(self.position.x, self.position.y, self.radius / 2)    
        asteroid_1.velocity = pygame.math.Vector2.rotate(self.velocity, rand_angle) * 1.2
        asteroid_2.velocity = pygame.math.Vector2.rotate(self.velocity, -1 * rand_angle) * 1.2

    def get_score(self):
        return int(100 / (self.radius / 10))
    
    def get_position(self):
        return self.position