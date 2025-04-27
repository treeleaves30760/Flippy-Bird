import pygame
import sys
import random
import math  # Import math for rotation

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()  # Add clock

# Screen dimensions
screen_width = 1024
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flippy Bird')  # Changed caption back

# Bird
# Add SRCALPHA for transparency
bird_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.ellipse(bird_surface, (255, 255, 0),
                    (0, 0, 50, 50))  # Draw yellow ellipse

# Draw the red beak onto the bird_surface
beak_width = 15
beak_height = 8
# Position the beak relative to the ellipse on the surface
# The ellipse is drawn at (0, 0) on the 50x50 surface
# Position at the right edge of the 50x50 surface
beak_x_on_surface = 50 - beak_width
# Vertically center on the 50x50 surface
beak_y_on_surface = (50 - beak_height) // 2
pygame.draw.rect(bird_surface, (255, 0, 0), (beak_x_on_surface,
                 beak_y_on_surface, beak_width, beak_height))

bird_rect = bird_surface.get_rect(center=(100, screen_height // 2))

# Pipes
pipe_width = 70
pipe_gap = 250  # Increased gap between top and bottom pipe
pipe_list = []
pipe_color = (0, 255, 0)  # Green color
min_pipe_height = 50  # Minimum height for a pipe segment

# Timer for pipes
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)  # Generate a new pipe every 1.2 seconds

# Game variables
gravity = 0.6
bird_movement = 0

# Functions


def create_pipe():
    # Calculate available vertical space for pipes
    available_space = screen_height - pipe_gap
    # Choose a random height for the top pipe segment
    top_pipe_height = random.randint(
        min_pipe_height, available_space - min_pipe_height)
    # Calculate the height of the bottom pipe segment
    bottom_pipe_height = available_space - top_pipe_height

    # Create rectangles for the top and bottom pipes
    top_pipe = pygame.Rect(screen_width + 50, 0, pipe_width, top_pipe_height)
    bottom_pipe = pygame.Rect(
        screen_width + 50, top_pipe_height + pipe_gap, pipe_width, bottom_pipe_height)

    return top_pipe, bottom_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5  # Move pipes to the left
    # Filter out pipes that are completely off-screen to the left
    visible_pipes = [pipe for pipe in pipes if pipe.right > 0]
    return visible_pipes


def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, pipe_color, pipe)  # Draw rectangles directly


def check_collision(pipes):
    # Check pipe collisions
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False  # Collision detected

    # Check screen bounds
    if bird_rect.top <= -100 or bird_rect.bottom >= screen_height:
        return False  # Bird is out of bounds

    return True  # No collision


# Game State Variables
game_active = True
score = 0
font = pygame.font.Font(None, 50)  # Default font, size 50

# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # Debug print
            print(f"KEYDOWN event: key={event.key}, game_active={game_active}")
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird_movement = 0
                    bird_movement -= 12  # Adjust jump strength as needed
            # Restart game on 'R' key press
            if event.key == pygame.K_r and not game_active:
                print("Restarting game...")  # Debug print
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, screen_height // 2)
                bird_movement = 0
                score = 0  # Reset score

        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())

    screen.fill((0, 0, 0))  # Clear screen every frame

    if game_active:
        # Bird movement
        bird_movement += gravity
        bird_rect.centery += bird_movement

        # Pipe movement and drawing
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Collision
        game_active = check_collision(pipe_list)

        # Check for scoring
        for pipe in pipe_list:
            # Check when the pipe passes the bird
            if pipe.centerx < bird_rect.centerx and pipe.centerx > bird_rect.centerx - 5:
                score += 1

        # Drawing (Active Game)
        # Calculate rotation angle based on bird_movement
        # Cap angle between -90 and 45 degrees
        angle = max(-90, min(45, bird_movement * -5))

        # Rotate the bird surface
        rotated_bird_surface = pygame.transform.rotate(bird_surface, angle)
        rotated_bird_rect = rotated_bird_surface.get_rect(
            center=bird_rect.center)

        screen.blit(rotated_bird_surface, rotated_bird_rect)

        # Display score
        score_surface = font.render(
            str(score), True, (255, 255, 255))  # White color
        score_rect = score_surface.get_rect(center=(screen_width // 2, 50))
        screen.blit(score_surface, score_rect)

    else:  # Game is over
        # Display game over message
        game_over_surface = font.render(
            "Game Over", True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect(
            center=(screen_width // 2, screen_height // 2))
        screen.blit(game_over_surface, game_over_rect)

        # Display final score
        score_surface = font.render(
            f"Score: {score}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(
            center=(screen_width // 2, screen_height // 2 + 50))

        screen.blit(score_surface, score_rect)

        # Display restart message
        restart_surface = font.render(
            "Press 'R' to Restart", True, (255, 255, 255))
        restart_rect = restart_surface.get_rect(
            center=(screen_width // 2, screen_height // 2 + 100))
        screen.blit(restart_surface, restart_rect)

    # Update display
    pygame.display.update()
    clock.tick(60)  # Limit frame rate
