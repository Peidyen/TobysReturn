import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Font for displaying the score and wave messages
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)

# Load Toby Image and resize it
toby_image = pygame.image.load("toby.gif")
toby_image = pygame.transform.scale(toby_image, (100, 100))  # Resize Toby
bark_sound = pygame.mixer.Sound('bark.wav')

# Clock for controlling frame rate
clock = pygame.time.Clock()

# List of creatures from their file names
creature_images = [
    "turtle.png", "rabbit.png", "fox.png", "owl.png",
    "lion.png", "elephant.png", "fish.png", "worm.png",
    "chick.png", "frog.png"
]

# Matrix size and tracking
matrix_size = 3000
creatures_in_matrix = []  # To track creatures added to the matrix

# Define level configuration with critters
level_critters = [
    {"type": "worm.png", "count": 10},
    {"type": "chick.png", "count": 10},
    {"type": "frog.png", "count": 10},
    {"type": "turtle.png", "count": 10},
    {"type": "rabbit.png", "count": 10},
    {"type": "fox.png", "count": 10},
    {"type": "owl.png", "count": 10},
    {"type": "lion.png", "count": 10},
    {"type": "elephant.png", "count": 10},
    {"type": "fish.png", "count": 10}
]

# Initialize level-related variables
current_level = 1
wave_count = 0
critters_spawned = 0
wave_timer = pygame.time.get_ticks()  # Timer for controlling waves
wave_delay = 3000  # 3-second delay between waves
wave_complete_delay = 2000  # 2-second delay after wave completion
score = 0  # Initial score
high_score = 0  # Initial high score
creatures_seen = []  # Track which creatures have been introduced

def load_and_resize_image(image_file, size):
    image = pygame.image.load(image_file)
    return pygame.transform.scale(image, size)

def start_wave_message(creatures, wave_number):
    """Display the wave message at the beginning of the wave."""
    wave_message = f"Wave {wave_number}: " + " and ".join([creature.split(".")[0].capitalize() for creature in creatures]) + " Wave!!!"
    wave_message_render = font.render(wave_message, True, BLACK)
    screen.blit(wave_message_render, (SCREEN_WIDTH // 2 - 200, 20))
    pygame.display.flip()
    time.sleep(2)  # Simulate flashing the message by pausing for 2 seconds

def spawn_critter_for_wave():
    """Spawn critters cumulatively up to the current wave."""
    global critters_spawned, wave_count
    new_creatures = []

    # Spawn all creatures from the current and previous waves
    for i in range(wave_count + 1):  # Cumulative wave logic
        critter_data = level_critters[i]
        creature_type = critter_data["type"]

        # Check if this creature type is new for this cumulative wave
        if creature_type not in creatures_seen:
            creatures_seen.append(creature_type)  # Add to the list of seen creatures
            new_creatures.append(creature_type)  # Track new creatures introduced in this wave

        # Spawn critters of this type
        for _ in range(critter_data["count"]):
            x = random.randint(0, SCREEN_WIDTH - 50)
            y = random.randint(0, SCREEN_HEIGHT // 2)
            speed = random.randint(2, 5)
            direction = random.choice([-1, 1])
            critter = Critter(x, y, speed, direction, creature_type, (50, 50))
            critter_group.add(critter)
            critters_spawned += 1

            # Add the critter to the matrix progressively and stop if the matrix is full
            if len(creatures_in_matrix) < matrix_size:
                creatures_in_matrix.append(creature_type)
            else:
                end_game()

    # Display the wave message
    if new_creatures:
        start_wave_message(new_creatures, wave_count + 1)

    # Increment the wave count
    wave_count += 1

# Define Critter Class
class Critter(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction, image_file, size):
        super().__init__()
        self.image = load_and_resize_image(image_file, size)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.direction = direction

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

# Define SonicWave Class
class SonicWave(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.original_image, (0, 0, 255), (25, 25), 25)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.max_size = 300
        self.growth_speed = 5

    def update(self):
        new_size = (self.rect.width + self.growth_speed, self.rect.height + self.growth_speed)
        self.image = pygame.transform.scale(self.original_image, new_size)
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.rect.width > self.max_size:
            self.kill()

# Define Toby Class
class Toby(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = toby_image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

# Function to display score on the screen
def draw_score(score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH - 150, 20))

# End the game and show final statistics
def end_game():
    global running, high_score
    if score > high_score:
        high_score = score  # Update the high score if the current score is higher
    show_game_over_screen()

def show_game_over_screen():
    """Display the Game Over screen with the score and high score."""
    screen.fill(WHITE)

    # Display "Game Over" text
    game_over_text = large_font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100))

    # Display the final score
    score_text = font.render(f"Final Score: {score}", True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

    # Display the high score
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()
    time.sleep(3)  # Pause for 3 seconds before closing the game

    pygame.quit()  # Exit the game
    exit()

# Initialize sprite groups
toby_group = pygame.sprite.Group()
sonic_wave_group = pygame.sprite.Group()
critter_group = pygame.sprite.Group()

# Create Toby
toby = Toby()
toby_group.add(toby)

# Game Loop
running = True
wave_completed = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bark_sound.play()
                wave = SonicWave(toby.rect.centerx, toby.rect.centery)
                sonic_wave_group.add(wave)

    keys = pygame.key.get_pressed()
    toby.move(keys)

    # If all critters from the previous wave are cleared, wait before starting the next wave
    if not critter_group and wave_completed:
        pygame.time.delay(wave_complete_delay)  # Delay between waves
        wave_completed = False

    # Spawn new wave if enough time has passed and no critters remain
    current_time = pygame.time.get_ticks()
    if current_time - wave_timer > wave_delay and not critter_group and wave_count < len(level_critters):
        spawn_critter_for_wave()
        wave_timer = pygame.time.get_ticks()  # Reset the timer for the next wave

    # Update sprites
    toby_group.update()
    sonic_wave_group.update()
    critter_group.update()

    # Check for collisions between sonic waves and critters
    for wave in sonic_wave_group:
        critters_hit = pygame.sprite.spritecollide(wave, critter_group, False)
        for critter in critters_hit:
            score += current_level
            critter.kill()  # Remove critter after collision

    # Drawing
    screen.fill(WHITE)
    toby_group.draw(screen)
    sonic_wave_group.draw(screen)
    critter_group.draw(screen)

    # Draw the score
    draw_score(score)

    pygame.display.flip()
    clock.tick(60)

    # Check if the wave is complete and wait for the next wave
    if not critter_group and wave_count >= len(level_critters):
        end_game()

    if not critter_group and wave_count < len(level_critters):
        wave_completed = True

pygame.quit()
