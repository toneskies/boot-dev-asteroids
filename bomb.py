import pygame
import math
from circleshape import CircleShape
from constants import *

class Bomb(CircleShape):
    def __init__(self, position):
        super().__init__(position.x, position.y, BOMB_RADIUS)
        self.timer = BOMB_DURATION
        self.state = "ticking"
        self.shockwave_radius = 0
        self.font = pygame.font.Font(None, 24)
    
    def update(self, dt):
        if self.state == "ticking":
            self.timer -= dt
            if self.timer < 0:
                self.state = "exploding"
        
        elif self.state == "exploding":
            self.shockwave_radius += BOMB_SHOCKWAVE_SPEED * dt
            if self.shockwave_radius > SCREEN_WIDTH:
                self.kill()
    
    def draw(self, screen):
        if self.state == "ticking":
            pulse_time = pygame.time.get_ticks() / 1000
            pulse_alpha = 128 * (0.5 * math.sin(pulse_time * 8) + 0.5) + 50

            bomb_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(bomb_surface, (255, 0, 0, int(pulse_alpha)), (self.radius, self.radius), self.radius)
            screen.blit(bomb_surface, (self.position.x - self.radius, self.position.y - self.radius))

            timer_text = self.font.render(f"{math.ceil(self.timer)}", True, "white")
            text_rect = timer_text.get_rect(center=self.position)
            screen.blit(timer_text, text_rect)

        elif self.state == "exploding":
            shockwave_surface = pygame.Surface((self.shockwave_radius * 2, self.shockwave_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(shockwave_surface, (255,255,255,80), (self.shockwave_radius, self.shockwave_radius), self.shockwave_radius)
            screen.blit(shockwave_surface, (self.position.x - self.shockwave_radius, self.position.y - self.shockwave_radius))