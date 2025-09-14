import pygame
import random
import math
from circleshape import CircleShape
from constants import *

class PowerUp(CircleShape):
    def __init__(self, powerup_type):
        x = random.randint(POWERUP_RADIUS, SCREEN_WIDTH - POWERUP_RADIUS)
        y = random.randint(POWERUP_RADIUS, SCREEN_HEIGHT - POWERUP_RADIUS)
        super().__init__(x, y, POWERUP_RADIUS)
        self.spawn_time = pygame.time.get_ticks()
        self.type = powerup_type

    def draw(self, screen):
        if self.type == "shield":
            pygame.draw.circle(screen, "yellow", self.position, self.radius, 3)
            pulse_time = (pygame.time.get_ticks() - self.spawn_time) / 1000
            pulse_radius = self.radius * 0.6 * (0.5 *math.sin(pulse_time * 4) + 0.5)
            pygame.draw.circle(screen, "white", self.position, int(pulse_radius))
        elif self.type == "bomb":
            pygame.draw.circle(screen, "blue", self.position, self.radius, 3)
            font = pygame.font.Font(None, 24)
            text = font.render("B", True, "white")
            text_rect = text.get_rect(center=self.position)
            screen.blit(text, text_rect)
            
    def update(self, dt):
        pass