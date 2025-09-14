import pygame
import random
from circleshape import *
from constants import *

class EnemyShot(CircleShape):
    def __init__(self, position, target_position):
        super().__init__(position.x, position.y, ENEMY_SHOT_RADIUS)

        # Calculate direction and add random inaccuracy
        direction = (target_position - position).normalize()
        inaccuracy = random.uniform(-ENEMY_SHOT_INACCURACY, ENEMY_SHOT_INACCURACY)
        self.velocity = direction.rotate(inaccuracy) * ENEMY_SHOT_SPEED

    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.radius)

    def update(self, dt):
        self.position += self.velocity * dt
        if (self.position.x < 0 or self.position.x > SCREEN_WIDTH or 
            self.position.y < 0 or self.position.y > SCREEN_HEIGHT):
            self.kill()