import pygame
from constants import *

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass
    
    def wrap_around_screen(self):
        if self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        if self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius

    def collision(self, target):
        distance = self.position.distance_to(target.position)
        return (distance <= (self.radius + target.radius))