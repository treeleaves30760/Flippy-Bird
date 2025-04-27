import pygame
import sys
import random

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()  # Add clock

# Screen dimensions
screen_width = 1024
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flippy Bird')  # Changed caption back

# Bird
bird_surface = pygame.Surface((50, 50))
bird_surface.fill((255, 255, 0))  # Yellow color
bird_rect = bird_surface.get_rect(center=(100, screen_height // 2))

# Pipes
pipe_width = 70
pipe_gap = 400  # Gap between top and bottom pipe
pipe_list = []
# Height doesn't matter much here
pipe_surface = pygame.Surface((pipe_width, 500))
pipe_surface.fill((0, 255, 0))  # Green color
# Possible y-coordinates for the bottom pipe's top
pipe_height = [400, 500, 600, 700, 800]

# Timer for pipes
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)  # Generate a new pipe every 1.2 seconds

# Game variables
gravity = 0.6
bird_movement = 0

# Functions


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(
        midtop=(screen_width + 50, random_pipe_pos))  # Start off-screen right
    top_pipe = pipe_surface.get_rect(midbottom=(
        screen_width + 50, random_pipe_pos - pipe_gap))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5  # Move pipes to the left
    # Filter out pipes that are completely off-screen to the left
    visible_pipes = [pipe for pipe in pipes if pipe.right > 0]
    return visible_pipes


def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe_surface, pipe)


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
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird_movement = 0
                    bird_movement -= 12  # Adjust jump strength as needed
            # Restart game on 'R' key press
            if event.key == pygame.K_r and not game_active:
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
        screen.blit(bird_surface, bird_rect)

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
