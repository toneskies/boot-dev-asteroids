import pygame
import sys
import random
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from explosion import *
from powerup import *
from bomb import *

def main():
    # INITIALIZATION
    print("Starting Asteroids!")
    print(f'Screen width: {SCREEN_WIDTH}')
    print(f'Screen height: {SCREEN_HEIGHT}')

    # Initialize pygame
    pygame.init()

    # Setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    time_clock = pygame.time.Clock()

    # Background Image
    background_image = pygame.image.load("space_background.png").convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image.set_alpha(80)


    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)
    Bomb.containers = (bombs, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    dt = 0
    powerup_spawn_timer = 0

    # SCORING
    score = 0
    font = pygame.font.Font(None, 36)

    # RESPAWNING
    lives = PLAYER_LIVES

    # GAME LOOP
    while(True):
        # User clicks 'x' closes the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    player.weapon.next_weapon()

        # Powerup logic
        powerup_spawn_timer += dt
        if powerup_spawn_timer > POWERUP_SPAWN_RATE:
            powerup_spawn_timer = 0
            powerup_type = random.choice(["shield", "bomb"])
            PowerUp(powerup_type)


        updatable.update(dt)

        for obj in asteroids:
            if player.collides_with_asteroid(obj):
                if player.shield_timer > 0:
                    score += obj.get_score()
                    Explosion(obj.get_position(), obj.get_radius())
                    obj.split()
                elif player.immunity_timer <= 0:
                    if lives > 1:
                        lives -= 1
                        obj.kill()
                        player.respawn()
                    else:
                        text = font.render(f'Final Score: {score}', True, "white")
                        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT/2))
                        screen.blit(text, text_rect)
                        pygame.display.flip()
                        pygame.time.wait(3000)
                        print("Game Over!")
                        sys.exit()

        for powerup in powerups:
            if powerup.collision(player):
                if powerup.type == "shield":
                    player.activate_shield()
                elif powerup.type == "bomb":
                    player.add_bomb()
                powerup.kill()

        # Bomb Shockwave Collision
        for bomb in bombs:
            if bomb.state == "exploding":
                for asteroid in asteroids.copy():
                    distance = asteroid.position.distance_to(bomb.position)
                    if distance < bomb.shockwave_radius:
                        score += asteroid.get_score()
                        Explosion(asteroid.get_position(), asteroid.get_radius())
                        asteroid.kill()


        for asteroid in asteroids:
            for bullet in shots:
                if bullet.collision(asteroid):
                    score += asteroid.get_score()
                    Explosion(asteroid.get_position(), asteroid.get_radius())
                    asteroid.split()
                    bullet.kill()

        screen.fill("black")
        screen.blit(background_image, (0, 0))

        for obj in drawable:
            obj.draw(screen)

        score_text = font.render(f"Score: {score}", True, "white")
        screen.blit(score_text, (10,10))

        lives_text = font.render(f"Lives: {lives}", True, "white")
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

        weapon_text = font.render(f"Weapon: {player.weapon.name}", True, "white")
        screen.blit(weapon_text, (10, SCREEN_HEIGHT - weapon_text.get_height() - 10))

        # Draw Bomb UI
        bomb_icon_rect = pygame.Rect(10, SCREEN_HEIGHT - 40, 30, 30)
        pygame.draw.circle(screen, "red", bomb_icon_rect.center, 15)
        bomb_font = pygame.font.Font(None, 24)
        bomb_b_text = bomb_font.render("B", True, "white")
        screen.blit(bomb_b_text, bomb_b_text.get_rect(center=bomb_icon_rect.center))

        bomb_count_text = font.render(f": {player.bombs}", True, "white")
        screen.blit(bomb_count_text, (bomb_icon_rect.right + 5, bomb_icon_rect.centery - bomb_count_text.get_height() / 2))


        pygame.display.flip()
        dt = time_clock.tick(60) / 1000


if __name__ == "__main__":
    main()
