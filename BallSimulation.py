import pygame
import random
import math
import os

# Initialize pygame and sound mixer
pygame.init()
pygame.mixer.init()

# Set up display
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Drop Simulation with Rotating Balloons")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Load sound effect for the blip
blip_sound = pygame.mixer.Sound("blip_sound.wav")

# Load the paddle image (dog)
paddle_image = pygame.image.load("Butters.png")

# Resize the paddle image to 200x200
paddle_image = pygame.transform.scale(paddle_image, (200, 200))  # Resize to width 200, height 200

# Ball parameters
BALL_RADIUS = 15
initial_gravity = 0.1  # Start with slower gravity
initial_velocity_factor = 1.0  # Initial velocity for slower movement
num_balls = 30  # Number of balls
ball_add_interval = 300  # Number of frames between adding balls
max_gravity = 0.5  # Max gravity increase

# Load the balloon image for the ball
balloon_image = pygame.image.load("balloon.gif")

# Optional: Resize the balloon image to match the BALL_RADIUS
balloon_image = pygame.transform.scale(balloon_image, (BALL_RADIUS * 2, BALL_RADIUS * 2))

# Paddle parameters
paddle_speed = 10

# Game parameters
max_misses = 10  # End game after 10 misses
min_bounce_height = HEIGHT / 4  # Minimum bounce height for the balloons

# High score file and default high score
high_score_file = "highscore.txt"
high_score = 0

# Font for displaying score and misses
font = pygame.font.SysFont(None, 36)

def load_high_score():
    """Load the high score from a file."""
    global high_score
    if os.path.exists(high_score_file):
        with open(high_score_file, "r") as file:
            try:
                high_score = int(file.read())
            except ValueError:
                high_score = 0
    else:
        high_score = 0

def save_high_score():
    """Save the current high score to a file."""
    with open(high_score_file, "w") as file:
        file.write(str(high_score))

def reset_game():
    global paddle_x, paddle_y, balls, frame_counter, misses, score, GRAVITY, accelerate, ball_spawn_timer, gravity_increase_timer
    # Reset paddle position
    paddle_x = WIDTH // 2 - paddle_image.get_width() // 2  # Centered horizontally
    paddle_y = HEIGHT - 50 - 100  # Move the paddle up by 100 units

    # Reset ball data
    balls = []
    
    # Initial game variables
    frame_counter = 0
    misses = 0
    score = 0
    GRAVITY = initial_gravity  # Start with initial gravity
    ball_spawn_timer = 0  # Timer for adding balls
    gravity_increase_timer = 0  # Timer to increase gravity
    accelerate = False

def draw_button(text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    label = font.render(text, True, text_color)
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))

def add_ball():
    # Adds a new ball with random position, velocity, and angular momentum
    x_position = random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS)
    y_position = -random.randint(50, 150)  # Start above the screen
    angle = random.uniform(-30, 30)  # Random angle
    angular_velocity = random.uniform(-5, 5)  # Random angular velocity for rotation
    ball = {
        "x": x_position,
        "y": y_position,
        "vx": math.sin(math.radians(angle)) * initial_velocity_factor,  # X velocity
        "vy": 0,  # Start with no Y velocity
        "angle": 0,  # Initial rotation angle
        "angular_velocity": angular_velocity,  # Rotation speed
        "active": True  # Ball starts active
    }
    balls.append(ball)

def rotate_image(image, angle):
    """Rotate an image while keeping its center."""
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect().center)
    return rotated_image, new_rect

def main_game():
    global paddle_x, paddle_y, frame_counter, misses, score, accelerate, GRAVITY, running, ball_spawn_timer, gravity_increase_timer, high_score
    
    reset_game()
    load_high_score()  # Load the high score when the game starts

    # Main loop
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_image.get_width():
            paddle_x += paddle_speed

        # Draw the paddle image
        screen.blit(paddle_image, (paddle_x, paddle_y))

        # Drop balls and update their positions
        for ball in balls:
            if ball["active"]:
                # Apply gravity
                ball["vy"] += GRAVITY
                ball["x"] += ball["vx"]
                ball["y"] += ball["vy"]

                # Update the balloon's rotation angle
                ball["angle"] += ball["angular_velocity"]

                # Ball bouncing off the walls
                if ball["x"] <= BALL_RADIUS or ball["x"] >= WIDTH - BALL_RADIUS:
                    ball["vx"] = -ball["vx"]

                # Ball bouncing off the paddle (paddle image's bounding box)
                if (paddle_y - BALL_RADIUS < ball["y"] < paddle_y and
                    paddle_x < ball["x"] < paddle_x + paddle_image.get_width()):
                    
                    # Add a small random angular momentum to the ball when it bounces
                    ball["angular_velocity"] += random.uniform(-2, 2)
                    
                    # Ensure the bounce height is at least 1/4 of the screen
                    ball["vy"] = -max(abs(ball["vy"] * 0.9), min_bounce_height / HEIGHT * 10)
                    
                    blip_sound.play()  # Play blip sound on paddle hit
                    score += 1  # Increase score

                # Rotate and draw the balloon image instead of the ball circle
                rotated_balloon_image, rect = rotate_image(balloon_image, ball["angle"])
                screen.blit(rotated_balloon_image, (int(ball["x"]) - BALL_RADIUS, int(ball["y"]) - BALL_RADIUS))

                # If ball falls off the screen (miss)
                if ball["y"] > HEIGHT:
                    balls.remove(ball)  # Remove the ball once missed
                    misses += 1  # Increment miss counter

        # Add balls over time
        ball_spawn_timer += 1
        if ball_spawn_timer > ball_add_interval:
            add_ball()
            ball_spawn_timer = 0

        # Gradually increase gravity over time
        gravity_increase_timer += 1
        if gravity_increase_timer > 600 and GRAVITY < max_gravity:  # Every 10 seconds (600 frames at 60 FPS)
            GRAVITY += 0.05  # Increase gravity
            gravity_increase_timer = 0

        # Display score, misses, and high score
        score_text = font.render(f"Score: {score}", True, BLACK)
        misses_text = font.render(f"Misses: {misses}/{max_misses}", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(misses_text, (10, 50))
        screen.blit(high_score_text, (10, 90))

        # End the game if max misses reached
        if misses >= max_misses:
            running = False

        # Update the display
        pygame.display.flip()
        frame_counter += 1
        clock.tick(60)

    # If the current score is greater than the high score, update the high score
    if score > high_score:
        high_score = score
        save_high_score()  # Save the new high score to the file

    return game_over()

def game_over():
    # Game over screen with restart button
    while True:
        screen.fill(WHITE)
        game_over_text = font.render(f"Game Over! Final Score: {score}", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 3))
        screen.blit(high_score_text, (WIDTH // 4, HEIGHT // 3 + 50))

        # Draw restart button
        button_width, button_height = 150, 50
        button_x, button_y = (WIDTH - button_width) // 2, (HEIGHT // 2)
        draw_button("Restart", button_x, button_y, button_width, button_height, GREEN, BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if (button_x <= mouse_pos[0] <= button_x + button_width and
                    button_y <= mouse_pos[1] <= button_y + button_height):
                    return main_game()  # Restart the game if button clicked

        pygame.display.flip()

# Start the game
main_game()
pygame.quit()
