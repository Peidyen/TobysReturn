import pygame
import random
import math

# Initialize pygame and sound mixer
pygame.init()
pygame.mixer.init()

# Set up display
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Drop Simulation with Paddle")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Load sound effect for the blip
blip_sound = pygame.mixer.Sound("blip_sound.wav")

# Load the paddle image
paddle_image = pygame.image.load("Butters.png")

# Optional: Resize the paddle image if necessary
paddle_image = pygame.transform.scale(paddle_image, (200, 200))  # Resize to width 100, height 20

# Ball parameters
BALL_RADIUS = 15  # This needs to be defined before using it to resize the balloon
GRAVITY = 0.2  # Start with slower gravity
initial_velocity_factor = 1.5  # Initial velocity for slower movement
num_balls = 30  # Number of balls
extra_ball_interval = 6  # Extra ball every 6th drop
drop_interval = 60  # Delay between drops in frames

# Load the balloon image for the ball
balloon_image = pygame.image.load("balloon.gif")

# Optional: Resize the balloon image to match the BALL_RADIUS
balloon_image = pygame.transform.scale(balloon_image, (BALL_RADIUS * 2, BALL_RADIUS * 2))

# Paddle parameters
paddle_speed = 10

# Game parameters
max_misses = 10  # End game after 10 misses

# Font for displaying score and misses
font = pygame.font.SysFont(None, 36)

def reset_game():
    global paddle_x, paddle_y, balls, frame_counter, misses, score, GRAVITY, accelerate
    # Reset paddle position
    paddle_x = WIDTH // 2 - paddle_image.get_width() // 2  # Centered horizontally
    paddle_y = HEIGHT - 200  # Move the paddle up by 100 units

    # Reset ball data
    balls = []
    for i in range(num_balls):
        x_position = random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS)
        y_position = -random.randint(50, 150)  # Start above the screen
        angle = random.uniform(-30, 30)  # Random angle
        balls.append({
            "x": x_position,
            "y": y_position,
            "vx": math.sin(math.radians(angle)) * initial_velocity_factor,  # X velocity
            "vy": 0,  # Start with no Y velocity
            "active": False  # Balls will activate based on the timer
        })
        # Add an extra ball every 6th drop
        if (i + 1) % extra_ball_interval == 0:
            balls.append({
                "x": random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS),
                "y": -random.randint(50, 150),
                "vx": math.sin(math.radians(random.uniform(-30, 30))) * initial_velocity_factor,
                "vy": 0,
                "active": False
            })

    # Reset game variables
    frame_counter = 0
    misses = 0
    score = 0
    GRAVITY = 0.2  # Reset gravity
    accelerate = False

def draw_button(text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    label = font.render(text, True, text_color)
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))

def main_game():
    global paddle_x, paddle_y, frame_counter, misses, score, accelerate, GRAVITY, running
    
    reset_game()

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

        # Drop balls at intervals and update their positions
        for i, ball in enumerate(balls):
            if not ball["active"] and frame_counter > i * drop_interval:
                ball["active"] = True

            if ball["active"]:
                # Apply gravity
                ball["vy"] += GRAVITY
                ball["x"] += ball["vx"]
                ball["y"] += ball["vy"]

                # Ball bouncing off the walls
                if ball["x"] <= BALL_RADIUS or ball["x"] >= WIDTH - BALL_RADIUS:
                    ball["vx"] = -ball["vx"]

                # Ball bouncing off the paddle (paddle image's bounding box)
                if (paddle_y - BALL_RADIUS < ball["y"] < paddle_y and
                    paddle_x < ball["x"] < paddle_x + paddle_image.get_width()):
                    ball["vy"] = -abs(ball["vy"]) * 0.9  # Reverse Y velocity with damping
                    blip_sound.play()  # Play blip sound on paddle hit
                    score += 1  # Increase score

                # Draw the balloon image instead of the ball circle
                screen.blit(balloon_image, (int(ball["x"]) - BALL_RADIUS, int(ball["y"]) - BALL_RADIUS))

                # If ball falls off the screen (miss)
                if ball["y"] > HEIGHT:
                    ball["y"] = -random.randint(50, 150)
                    ball["vx"] = math.sin(math.radians(random.uniform(-30, 30))) * initial_velocity_factor
                    ball["vy"] = 0
                    misses += 1  # Increment miss counter

                # Accelerate gravity after a few hits
                if score % 10 == 0 and score != 0 and not accelerate:
                    GRAVITY += 0.1
                    accelerate = True  # Prevent further acceleration until new score milestone
                if score % 10 != 0:
                    accelerate = False

        # Display score and misses
        score_text = font.render(f"Score: {score}", True, BLACK)
        misses_text = font.render(f"Misses: {misses}/{max_misses}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(misses_text, (10, 50))

        # End the game if max misses reached
        if misses >= max_misses:
            running = False

        # Update the display
        pygame.display.flip()
        frame_counter += 1
        clock.tick(60)

    return game_over()

def game_over():
    # Game over screen with restart button
    while True:
        screen.fill(WHITE)
        game_over_text = font.render(f"Game Over! Final Score: {score}", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 3))

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
