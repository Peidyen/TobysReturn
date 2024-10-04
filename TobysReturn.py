import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280  # Increase width
SCREEN_HEIGHT = 720  # Increase height (or higher for larger screens)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)

# Load Toby Image and resize it
toby_image = pygame.image.load("toby.gif")
toby_image = pygame.transform.scale(toby_image, (100, 100))  # Resize Toby to 100x100 pixels
bark_sound = pygame.mixer.Sound('bark.wav')

# Load and resize the worm image
worm_image = pygame.image.load("worm.png")
worm_image = pygame.transform.scale(worm_image, (50, 50))  # Adjust size to 50x50 pixels

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Levels configuration with critters
level_critters = [
    {"type": "worm.png", "count": 10},
    {"type": "chick.png", "count": 10},
    {"type": "frog.png", "count": 10},
    # Add more critters for higher levels...
]

current_level = 1
wave_count = 0
critters_spawned = 0
wave_timer = pygame.time.get_ticks()  # Timer for controlling waves
wave_delay = 2000  # 2-second delay between waves

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
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 255), (25, 25), 25)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def update(self):
        self.rect.width += self.speed
        self.rect.height += self.speed
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        if self.rect.width > 300:
            self.kill()

# Define Toby Class
class Toby(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = toby_image  # Toby's resized image
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
        critters_hit = pygame.sprite.spritecollide(wave, critter_group, False)
        for critter in critters_hit:
            critter.reverse_direction()

    # Drawing
    screen.fill(WHITE)
    toby_group.draw(screen)
    sonic_wave_group.draw(screen)
    critter_group.draw(screen)

    pygame.display.flip()
    clock.tick(60)

    # Level up if all waves are spawned and critters cleared
    if wave_count >= current_level and not critter_group:
        level_up()

pygame.quit()
