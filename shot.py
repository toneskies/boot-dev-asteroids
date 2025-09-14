import pygame
from circleshape import *
from constants import *


class Shot(CircleShape):
    def __init__(self, position, rotation):
        super().__init__(position.x, position.y, SHOT_RADIUS)
        self.velocity = pygame.Vector2(0, 1).rotate(rotation) * PLAYER_SHOOT_SPEED

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.position.x, self.position.y), self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_around_screen()