import pygame
from circleshape import *
from enemyshot import *

class Enemy(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_RADIUS)
        self.velocity = pygame.Vector2(ENEMY_SPEED, 0)

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

    def update(self, dt, player):
        # get player direction
        direction_to_player = player.position - self.position
        distance = direction_to_player.length()
        acceleration_direction = pygame.Vector2(0, 0)

        if distance > 0:
            if distance > ENEMY_ORBIT_RADIUS:
                acceleration_direction += direction_to_player.normalize()
            else:
                # Attraction
                tangential_vector = direction_to_player.rotate(90)
                acceleration_direction += tangential_vector.normalize()

                # Repulsion
                repulsion_force = (ENEMY_ORBIT_RADIUS - distance) / ENEMY_ORBIT_RADIUS
                acceleration_direction -= direction_to_player.normalize() * repulsion_force * 2

        if acceleration_direction.length() > 0:
            acceleration_direction.normalize_ip()

        # accelerate towards player
        self.velocity += acceleration_direction * ENEMY_ACCELERATION * dt

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