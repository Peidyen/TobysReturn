import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ball Drop Game")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Square (Player) settings
square_width = 100
square_height = 20
square_x = (screen_width - square_width) // 2
square_y = screen_height - square_height - 10
square_speed = 7

# Ball settings
ball_radius = 15
ball_speed_y = 5
ball_list = []  # To keep track of multiple balls

# Game settings
score = 0
high_score = 0
missed_balls = 0
lives = 3
font = pygame.font.Font(None, 36)
game_over = False

# Load sound
hit_sound = pygame.mixer.Sound('blip_sound.wav')  # Replace with your custom sound if available

# Set up the clock for controlling frame rate
clock = pygame.time.Clock()

# Function to drop a new ball at a random position
def drop_ball():
    x = random.randint(ball_radius, screen_width - ball_radius)
    y = -ball_radius  # Start the ball just above the screen
    ball_list.append([x, y])

# Function to check for collision between ball and square
def check_collision(ball_x, ball_y, square_x, square_y, square_width, square_height):
    if (square_x < ball_x < square_x + square_width) and (square_y < ball_y + ball_radius < square_y + square_height):
        return True
    return False

# Timer for dropping balls
drop_event = pygame.USEREVENT + 1
pygame.time.set_timer(drop_event, 2000)  # Drop a ball every 2 seconds

# Function to reset the game
def reset_game():
    global score, missed_balls, lives, ball_list, game_over
    score = 0
    missed_balls = 0
    lives = 3
    ball_list = []
    game_over = False

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == drop_event and not game_over:
            drop_ball()  # Drop a new ball
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            # Restart the game if game over and player clicks mouse
            reset_game()

    # Get key presses for square movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and square_x > 0:
        square_x -= square_speed
    if keys[pygame.K_RIGHT] and square_x < screen_width - square_width:
        square_x += square_speed

    # Update ball positions and check for collisions
    if not game_over:
        for ball in ball_list[:]:
            ball[1] += ball_speed_y  # Move ball down
            if check_collision(ball[0], ball[1], square_x, square_y, square_width, square_height):
                ball_list.remove(ball)  # Remove ball if collision happens
                hit_sound.play()  # Play hit sound when ball hits the square
                score += 1  # Increment score
            elif ball[1] > screen_height:
                ball_list.remove(ball)  # Remove ball if it goes off-screen
                missed_balls += 1
                lives -= 1  # Decrease a life
                if lives <= 0:
                    game_over = True
                    if score > high_score:
                        high_score = score

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the square (player)
    pygame.draw.rect(screen, BLUE, (square_x, square_y, square_width, square_height))

    # Draw the balls
    for ball in ball_list:
        pygame.draw.circle(screen, RED, (ball[0], ball[1]), ball_radius)

    # Display the score and high score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(high_score_text, (10, 50))

    # Display lives
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    screen.blit(lives_text, (screen_width - 120, 10))

    # Game Over Screen
    if game_over:
        game_over_text = font.render("Game Over! Click to Restart", True, BLACK)
        screen.blit(game_over_text, (screen_width // 2 - 200, screen_height // 2))

    # Update the screen
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)  # Run at 60 frames per second
