import pygame

def draw_main_menu(screen):
    """Draws the main menu screen."""
    title_font = pygame.font.Font(None, 100)
    subtitle_font = pygame.font.Font(None, 50)

    # Game Title
    title_text = title_font.render("ASTEROIDS", True, "white")
    title_rect = title_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 100))
    screen.blit(title_text, title_rect)

    # Subtitle / Instructions
    subtitle_text = subtitle_font.render("Press any key to Start", True, "white")
    subtitle_rect = subtitle_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
    screen.blit(subtitle_text, subtitle_rect)

def draw_game_over_screen(screen, score, mouse_pos):
    """Draws teh game over screen and a restart button"""
    title_font = pygame.font.Font(None, 100)
    score_font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 60)

    #Game Over Title
    title_text = title_font.render("GAME OVER", True, "white")
    title_rect = title_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 150))
    screen.blit(title_text, title_rect)

    # Final Score
    score_text = title_font.render(f"Final Score: {score}", True, "white")
    score_rect = title_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 50))
    screen.blit(score_text, score_rect)

    # Restart Button
    button_rect = pygame.Rect(0, 0, 250, 80)
    button_rect.center = (screen.get_width() / 2, screen.get_height() / 2 + 100)
    
    # Hover effect
    button_color = (100, 100, 100) # Dark Grey
    if button_rect.collidepoint(mouse_pos):
        button_color = (150, 150, 150) # Light Grey

    pygame.draw.rect(screen, button_color, button_rect, 0, 10)
    
    button_text = button_font.render("Restart", True, "white")
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)