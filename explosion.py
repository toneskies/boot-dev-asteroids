import pygame
import random
from constants import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position, asteroid_radius):
        super().__init__(self.containers)
        self.particles = []
        # for _ in range(EXPLOSION_PARTICLES):
        num_particles = int(EXPLOSION_PARTICLES * (asteroid_radius / ASTEROID_MIN_RADIUS))
        explosion_speed = EXPLOSION_SPEED * (asteroid_radius / ASTEROID_MIN_RADIUS)
        explosion_duration = EXPLOSION_DURATION * (asteroid_radius / ASTEROID_MIN_RADIUS)
        for _ in range(num_particles):
            self.particles.append(
                {
                    "position": pygame.Vector2(position),
                    "velocity": pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * random.uniform(50, explosion_speed),
                    "timer": explosion_duration
                }
            )

    def update(self, dt):
        for particle in self.particles:
            particle["position"] += particle["velocity"] * dt
            particle["timer"] -= dt
        self.particles = [p for p in self.particles if p["timer"] > 0]
        if not self.particles:
            self.kill()
        
    def draw(self, screen):
        particle_radius = EXPLOSION_PARTICLE_RADIUS * (self.particles[0]["timer"] / EXPLOSION_DURATION) if self.particles else 0
        for particle in self.particles:
            pygame.draw.circle(screen, "white", particle["position"], particle_radius)