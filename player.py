import pygame
from constants import *
from circleshape import *
from shot import *


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.immunity_timer = 0
        self.velocity = pygame.Vector2(0, 0)
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt        
    
    def shoot(self):
        self.timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position, self.rotation)

    def respawn(self):
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.rotation = 0
        self.immunity_timer = PLAYER_IMMUNITY_TIMER
        self.velocity = pygame.Vector2(0, 0)


    def update(self, dt):
        self.timer -= dt
        if self.immunity_timer > 0:
            self.immunity_timer -= dt
        keys = pygame.key.get_pressed()

        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        if keys[pygame.K_a]:
            self.rotate(dt * -1)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.velocity += forward * PLAYER_ACCELERATION * dt
        if keys[pygame.K_s]:
            self.velocity -= forward * PLAYER_ACCELERATION * dt

        if self.velocity.magnitude() > 0:
            self.velocity = pygame.Vector2.normalize(self.velocity) * min(self.velocity.magnitude(), PLAYER_MAX_SPEED)
        else:
            self.velocity = pygame.Vector2(0, 0)
        self.position += self.velocity * dt

        if keys[pygame.K_SPACE]:
            if self.timer <= 0:
                self.shoot()

        