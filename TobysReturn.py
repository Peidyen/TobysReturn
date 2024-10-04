import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font for displaying the score
font = pygame.font.SysFont(None, 36)

# Load Toby Image and resize it
toby_image = pygame.image.load("toby.gif")
toby_image = pygame.transform.scale(toby_image, (100, 100))  # Resize Toby
bark_sound = pygame.mixer.Sound('bark.wav')

# Load and resize the worm image
worm_image = pygame.image.load("worm.png")
worm_image = pygame.transform.scale(worm_image, (50, 50))

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Levels configuration with critters
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


current_level = 1
wave_count = 0
critters_spawned = 0
wave_timer = pygame.time.get_ticks()  # Timer for controlling waves
wave_delay = 2000  # 2-second delay between waves
score = 0  # Initial score

def load_and_resize_image(image_file, size):
    image = pygame.image.load(image_file)
    return pygame.transform.scale(image, size)

def spawn_critter_for_wave():
    global critters_spawned
    critter_data = level_critters[wave_count % len(level_critters)]
    for _ in range(critter_data["count"]):
        x = random.randint(0, SCREEN_WIDTH - 50)
        y = random.randint(0, SCREEN_HEIGHT // 2)
        speed = random.randint(2, 5)
        direction = random.choice([-1, 1])
        critter = Critter(x, y, speed, direction, critter_data["type"], (50, 50))  # Set size dynamically
        critter_group.add(critter)
        critters_spawned += 1

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

    def reverse_direction(self):
        self.direction *= -1

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
        # Grow the sonic wave
        new_size = (self.rect.width + self.growth_speed, self.rect.height + self.growth_speed)
        self.image = pygame.transform.scale(self.original_image, new_size)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Debugging: print rect size
        print(f"SonicWave rect: {self.rect}")

        # Remove wave if it's too large
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

# Initialize sprite groups
toby_group = pygame.sprite.Group()
sonic_wave_group = pygame.sprite.Group()
critter_group = pygame.sprite.Group()

# Create Toby
toby = Toby()
toby_group.add(toby)

# Game Loop
running = True
while running:
    # Handle events
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

    # Spawn new wave if enough time has passed
    current_time = pygame.time.get_ticks()
    if current_time - wave_timer > wave_delay:
        if wave_count < current_level:  # Limit waves to the current level
            spawn_critter_for_wave()
            wave_count += 1
            wave_timer = current_time  # Reset the timer for the next wave

    # Update sprites
    toby_group.update()
    sonic_wave_group.update()
    critter_group.update()

    # Check for collisions between sonic waves and critters
    for wave in sonic_wave_group:
        # Debugging: print critters and wave rect info
        for critter in critter_group:
            print(f"Critter rect: {critter.rect}, SonicWave rect: {wave.rect}")
        
        critters_hit = pygame.sprite.spritecollide(wave, critter_group, False)  # False to not remove critters yet
        for critter in critters_hit:
            # Increase score based on the current wave
            score += current_level  # 1 point per critter in wave 1, 2 points per critter in wave 2, etc.
            print(f"Collision detected! Score: {score}")
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

    # Level up if all waves are spawned and critters cleared
    if wave_count >= current_level and not critter_group:
        current_level += 1  # Go to the next level
        wave_count = 0  # Reset wave count for the new level

pygame.quit()
