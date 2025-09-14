import pygame
import random
import math
from circleshape import CircleShape
from constants import *

class PowerUp(CircleShape):
    def __init__(self):
        x = random.randint(POWERUP_RADIUS, SCREEN_WIDTH - POWERUP_RADIUS)
        y = random.randint(POWERUP_RADIUS, SCREEN_HEIGHT - POWERUP_RADIUS)
        super().__init__(x, y, POWERUP_RADIUS)
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, screen):
        # Draw outer yellow circle
        pygame.draw.circle(screen, "yellow", self.position, self.radius, 3)

        # Create a pulsing effect
        pulse_time = (pygame.time.get_ticks() - self.spawn_time) / 1000
        pulse_radius = self.radius * 0.6 * (0.5 *math.sin(pulse_time * 4) + 0.5)
        pygame.draw.circle(screen, "white", self.position, int(pulse_radius))

    def update(self, dt):
        pass