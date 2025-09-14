import pygame
from constants import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(self.containers)
        self.position = position
        self.timer = EXPLOSION_DURATION

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.kill()
        
    def draw(self, screen):
        size = 1 - (self.timer / EXPLOSION_DURATION)
        color_1 = (255, 255, 255, 200 * size) # white
        color_2 = (255, 120, 0, 150 * size) #orange
        color_3 = (255, 0, 0, 100*size) #red
        pygame.draw.circle(screen, color_1, self.position, 10 * size)
        pygame.draw.circle(screen, color_2, self.position, 10 * size)
        pygame.draw.circle(screen, color_3, self.position, 10 * size)