import pygame
import random
from circleshape import *
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = 0
        self.rotation_speed = random.uniform(-50, 50)

        self.shape = []
        for i in range(ASTEROID_VERTICES):
            angle = (360 / ASTEROID_VERTICES) * i
            dist = self.radius + random.uniform(-self.radius, self.radius) * ASTEROID_LUMPINESS
            point = pygame.Vector2(0, 1).rotate(angle) * dist
            self.shape.append(point)


    def draw(self, screen):
        points = []
        for point in self.shape:
            rotated_point = point.rotate(self.rotation)
            screen_point = rotated_point + self.position
            points.append(screen_point)
        pygame.draw.polygon(screen, "white", points, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rotation += self.rotation_speed * dt
        self.wrap_around_screen()

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
    
    def get_radius(self):
        return self.radius