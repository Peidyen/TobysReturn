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
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load sound effect for the blip
blip_sound = pygame.mixer.Sound("blip_sound.wav")

# Ball parameters
BALL_RADIUS = 15
GRAVITY = 0.3  # Slower gravity to reduce speed
num_balls = 30  # Number of balls
extra_ball_interval = 6  # Extra ball every 6th drop
drop_interval = 60  # Slower delay between drops in frames

# Paddle parameters
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
paddle_x = WIDTH // 2 - PADDLE_WIDTH // 2
paddle_y = HEIGHT - 50
paddle_speed = 10

# Set up the ball data
balls = []
for i in range(num_balls):
    x_position = random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS)
    y_position = -random.randint(50, 150)  # Start above the screen
    angle = random.uniform(-30, 30)  # Random angle
    balls.append({
        "x": x_position,
        "y": y_position,
        "vx": math.sin(math.radians(angle)) * 2,  # X velocity reduced for slower movement
        "vy": 0,  # Start with no Y velocity
        "active": False  # Balls will activate based on the timer
    })
    # Add an extra ball every 6th drop
    if (i + 1) % extra_ball_interval == 0:
        balls.append({
            "x": random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS),
            "y": -random.randint(50, 150),
            "vx": math.sin(math.radians(random.uniform(-30, 30))) * 2,
            "vy": 0,
            "active": False
        })

# Main loop
clock = pygame.time.Clock()
frame_counter = 0
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
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
        paddle_x += paddle_speed

    # Draw paddle
    pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

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

            # Ball bouncing off the paddle
            if (paddle_y - BALL_RADIUS < ball["y"] < paddle_y and
                paddle_x < ball["x"] < paddle_x + PADDLE_WIDTH):
                ball["vy"] = -abs(ball["vy"]) * 0.9  # Reverse Y velocity with damping
                blip_sound.play()  # Play blip sound on paddle hit

            # Draw the ball
            pygame.draw.circle(screen, RED, (int(ball["x"]), int(ball["y"])), BALL_RADIUS)

            # Reset the ball if it falls off the screen
            if ball["y"] > HEIGHT:
                ball["y"] = -random.randint(50, 150)
                ball["vx"] = math.sin(math.radians(random.uniform(-30, 30))) * 2
                ball["vy"] = 0

    # Update the display
    pygame.display.flip()
    frame_counter += 1
    clock.tick(60)

pygame.quit()
