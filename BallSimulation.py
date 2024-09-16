import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ball Shooting Across Screen")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ball settings
ball_radius = 15
ball_x = 50  # Start ball on the left side of the screen
ball_y = screen_height // 2  # Center the ball vertically
ball_speed = 5

# Set up the clock for controlling frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update ball position
    ball_x += ball_speed

    # Check if the ball has gone off the screen
    if ball_x - ball_radius > screen_width:
        ball_x = 50  # Reset the ball to the starting position

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the ball
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

    # Update the screen
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)  # Run at 60 frames per second
