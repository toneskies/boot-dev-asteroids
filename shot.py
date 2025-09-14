import pygame
from circleshape import *
from constants import *


class Shot(CircleShape):
    def __init__(self, position, rotation, offset=(0,0), angle_offset=0):
        super().__init__(position.x, position.y, SHOT_RADIUS)
        self.velocity = pygame.Vector2(0, 1).rotate(rotation + angle_offset) * PLAYER_SHOOT_SPEED
        self.position += pygame.Vector2(offset).rotate(rotation)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.position.x, self.position.y), self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_around_screen()