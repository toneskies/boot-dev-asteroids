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
from enemy import *
from shot import *
from enemyshot import *
import ui

def game_loop(screen):
    """This function contains the core gameplay loop."""
    time_clock = pygame.time.Clock()
    background_image = pygame.image.load("space_background.png").convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image.set_alpha(80)

    # Create sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    enemy_shots = pygame.sprite.Group()

    # Assign containers
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)
    Bomb.containers = (bombs, updatable, drawable)
    Enemy.containers = (enemies, drawable)
    EnemyShot.containers = (enemy_shots, updatable, drawable)


    # Create game objects
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    dt = 0
    powerup_spawn_timer = 0
    enemy_spawn_timer = 0
    score = 0
    lives = PLAYER_LIVES
    font = pygame.font.Font(None, 36)

    # GAME LOOP
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    player.weapon.next_weapon()

        # Timers
        powerup_spawn_timer += dt
        if powerup_spawn_timer > POWERUP_SPAWN_RATE:
            powerup_spawn_timer = 0
            powerup_type = random.choice(["shield", "bomb"])
            PowerUp(powerup_type)

        enemy_spawn_timer += dt
        if enemy_spawn_timer > ENEMY_SPAWN_RATE:
            enemy_spawn_timer = 0
            x = random.choice([0 - ENEMY_RADIUS, SCREEN_WIDTH + ENEMY_RADIUS])
            y = random.randint(0, SCREEN_HEIGHT)
            Enemy(x, y)

        # Update
        updatable.update(dt)
        for enemy in enemies:
            enemy.update(dt, player, asteroids)

        # Collisions
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
                        print("Game Over!")
                        return score

        for shot in enemy_shots:
            if shot.collision(player):
                shot.kill()
                if player.shield_timer <= 0 and player.immunity_timer <= 0:
                    if lives > 1:
                        lives -= 1
                        player.respawn()
                    else:
                        return score

        for powerup in powerups:
            if powerup.collision(player):
                if powerup.type == "shield":
                    player.activate_shield()
                elif powerup.type == "bomb":
                    player.add_bomb()
                powerup.kill()

        for bomb in bombs:
            if bomb.state == "exploding":
                for asteroid in asteroids.copy():
                    if asteroid.position.distance_to(bomb.position) < bomb.shockwave_radius:
                        score += asteroid.get_score()
                        Explosion(asteroid.get_position(), asteroid.get_radius())
                        asteroid.kill()

        for enemy_ship in enemies:
            for bullet in shots:
                if bullet.collision(enemy_ship):
                    score += enemy_ship.get_score()
                    Explosion(enemy_ship.get_position(), enemy_ship.get_radius())
                    enemy_ship.kill()
                    bullet.kill()

        for enemy_ship in enemies:
            for asteroid in asteroids:
                if asteroid.collision(enemy_ship):
                    Explosion(enemy_ship.get_position(), enemy_ship.get_radius())
                    enemy_ship.kill()
                    asteroid.split()
                    break

        for asteroid in asteroids:
            for bullet in enemy_shots:
                if bullet.collision(asteroid):
                    Explosion(asteroid.get_position(), asteroid.get_radius())
                    asteroid.split()
                    bullet.kill()


        for asteroid in asteroids:
            for bullet in shots:
                if bullet.collision(asteroid):
                    score += asteroid.get_score()
                    Explosion(asteroid.get_position(), asteroid.get_radius())
                    asteroid.split()
                    bullet.kill()

        # Drawing
        screen.fill("black")
        screen.blit(background_image, (0, 0))

        for obj in drawable:
            obj.draw(screen)

        # UI Text
        score_text = font.render(f"Score: {score}", True, "white")
        screen.blit(score_text, (10, 10))

        lives_text = font.render(f"Lives: {lives}", True, "white")
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

        bomb_icon_rect = pygame.Rect(10, SCREEN_HEIGHT - 40, 30, 30)
        pygame.draw.circle(screen, "blue", bomb_icon_rect.center, 15)
        bomb_font = pygame.font.Font(None, 24)
        bomb_b_text = bomb_font.render("B", True, "white")
        screen.blit(bomb_b_text, bomb_b_text.get_rect(center=bomb_icon_rect.center))
        
        bomb_count_text = font.render(f": {player.bombs}", True, "white")
        screen.blit(bomb_count_text, (bomb_icon_rect.right + 5, bomb_icon_rect.centery - bomb_count_text.get_height() / 2))

        weapon_text = font.render(f"Weapon: {player.weapon.name}", True, "white")
        screen.blit(weapon_text, (10, bomb_icon_rect.top - weapon_text.get_height() - 5))

        pygame.display.flip()
        dt = time_clock.tick(60) / 1000

def main():
    """Main function to control game states."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    background_image = pygame.image.load("space_background.png").convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image.set_alpha(80)

    while True:
        # --- MENU STATE ---
        menu_running = True
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    menu_running = False
            
            screen.fill("black")
            screen.blit(background_image, (0, 0))
            ui.draw_main_menu(screen)
            pygame.display.flip()

        # --- SESSION LOOP (PLAY -> GAME OVER -> RESTART) ---
        while True:
            # --- PLAYING STATE ---
            final_score = game_loop(screen)
            
            # --- GAME OVER STATE ---
            game_over_running = True
            
            # Define the button's rectangle BEFORE the event loop
            restart_button_rect = pygame.Rect(0, 0, 250, 80)
            restart_button_rect.center = (screen.get_width() / 2, screen.get_height() / 2 + 100)

            while game_over_running:
                mouse_pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Use the pre-defined rect for the collision check
                        if restart_button_rect.collidepoint(event.pos):
                            game_over_running = False # Exit the game over screen
                
                screen.fill("black")
                screen.blit(background_image, (0, 0))
                ui.draw_game_over_screen(screen, final_score, mouse_pos)
                pygame.display.flip()
            
            # After the game_over_running loop, the session loop will repeat,
            # effectively restarting the game.

if __name__ == "__main__":
    main()

