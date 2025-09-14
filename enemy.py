import pygame
from circleshape import *

class Enemy(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_RADIUS)
        self.velocity = pygame.Vector2(ENEMY_SPEED, 0)

    def draw(self, screen):
        # A Trapezoid for a ship
        points = [
            (self.position.x - self.radius / 2, self.position.y - self.radius),
            (self.position.x + self.radius / 2, self.position.y - self.radius),
            (self.position.x + self.radius, self.position.y + self.radius),
            (self.position.x - self.radius, self.position.y + self.radius)
        ]
        pygame.draw.polygon(screen, "red", points, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        if self.position.x < 0 or self.position.x > SCREEN_WIDTH:
            self.velocity *= -1
        
    def get_score(self):
        return ENEMY_SCORE
    
    def get_position(self):
        return self.position
    
    def get_radius(self):
        return self.radius