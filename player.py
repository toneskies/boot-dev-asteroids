import pygame
from constants import *
from circleshape import *
from shot import *
from weapon import *


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.immunity_timer = 0
        self.velocity = pygame.Vector2(0, 0)
        self.weapon = Weapon()
        self.shield_timer = 0
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def collides_with_asteroid(self, asteroid):
        points = self.triangle()

        for point in points:
            if asteroid.position.distance_to(point) < asteroid.radius:
                return True
         
        for i in range(3):
            p1 = points[i]
            p2 = points[(i + 1) % 3]

            line_vec = p2 - p1
            if line_vec.length_squared() == 0:
                continue
            point_vec = asteroid.position - p1

            t = line_vec.dot(point_vec) / line_vec.length_squared()
            t = max(0, min(1, t))

            closest_point = p1 + t * line_vec
            
            if closest_point.distance_to(asteroid.position) < asteroid.radius:
                return True
        
        return False

    def draw(self, screen):
        if self.shield_timer > 0:
            shield_radius = self.radius + 8
            shield_surface = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, (255, 255, 0, 100), (shield_radius, shield_radius), shield_radius)
            screen.blit(shield_surface, (self.position.x - shield_radius, self.position.y - shield_radius))
        
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
        

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt        
    
    def shoot(self):
        self.timer = self.weapon.get_cooldown()
        self.weapon.shoot(self.position, self.rotation)

    def activate_shield(self):
        self.shield_timer = SHIELD_DURATION


    def respawn(self):
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.rotation = 0
        self.immunity_timer = PLAYER_IMMUNITY_TIMER
        self.velocity = pygame.Vector2(0, 0)


    def update(self, dt):
        self.timer -= dt
        if self.immunity_timer > 0:
            self.immunity_timer -= dt
        if self.shield_timer > 0:
            self.shield_timer -= dt
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

        self.wrap_around_screen()

        if keys[pygame.K_SPACE]:
            if self.timer <= 0:
                self.shoot()

        