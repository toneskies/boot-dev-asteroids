import pygame
from circleshape import *
from enemyshot import *
from constants import *
import random

class Enemy(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_RADIUS)
        self.velocity = pygame.Vector2(ENEMY_SPEED, 0)
        self.shoot_cooldown = random.uniform(0.5, ENEMY_SHOOT_COOLDOWN)

    def draw(self, screen):
        # A Trapezoid for a ship
        points = [
            (self.position.x - self.radius / 2, self.position.y - self.radius),
            (self.position.x + self.radius / 2, self.position.y - self.radius),
            (self.position.x + self.radius, self.position.y + self.radius),
            (self.position.x - self.radius, self.position.y + self.radius)
        ]
        pygame.draw.polygon(screen, "red", points, 2)

    def shoot(self, player_position):
        self.shoot_cooldown = ENEMY_SHOOT_COOLDOWN
        EnemyShot(self.position, player_position)

    def update(self, dt, player, asteroids):
        self.shoot_cooldown -= dt
        if self.shoot_cooldown <= 0:
            self.shoot(player.position)

        # AI Steering Behavior

        # 1. Player Following/Orbiting Force
        # get player direction
        direction_to_player = player.position - self.position
        distance_to_player = direction_to_player.length()
        player_force = pygame.Vector2(0, 0)

        if distance_to_player > 0:
            if distance_to_player > ENEMY_ORBIT_RADIUS:
                player_force += direction_to_player.normalize()
            else:
                # Attraction
                tangential_vector = direction_to_player.rotate(90).normalize()
                attraction_force = tangential_vector

                # Repulsion
                repulsion_force = (ENEMY_ORBIT_RADIUS - distance_to_player) / ENEMY_ORBIT_RADIUS
                repulsion_vector = direction_to_player.normalize() * repulsion_force * 2

                player_force = attraction_force + repulsion_vector

        # 2. Asteroid Avoidance Force
        avoidance_force = pygame.Vector2(0, 0)
        for asteroid in asteroids:
            direction_to_asteroid = asteroid.position - self.position
            distance_to_asteroid = direction_to_asteroid.length()

            if distance_to_asteroid > 0 and distance_to_asteroid < ENEMY_AVOID_RADIUS:
                repulsion_strength = 1 - (distance_to_asteroid / ENEMY_AVOID_RADIUS)
                avoidance_force -= direction_to_asteroid.normalize() * repulsion_strength
            
        # 3. Combine Forces
        total_force = player_force + (avoidance_force * ENEMY_AVOID_STRENGTH)

        if total_force.length() > 0:
            total_force.normalize_ip()
        
        self.velocity += total_force * ENEMY_ACCELERATION * dt

        # cap speed 
        if self.velocity.length() > ENEMY_MAX_SPEED:
            self.velocity.scale_to_length(ENEMY_MAX_SPEED)
        
        self.position += self.velocity * dt
        self.wrap_around_screen()        
        
    def get_score(self):
        return ENEMY_SCORE
    
    def get_position(self):
        return self.position
    
    def get_radius(self):
        return self.radius