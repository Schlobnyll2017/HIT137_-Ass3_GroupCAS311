# Made from Pygame code sample_week10 by group CAS311 🌟🌟
# Importing the necessary modules 🐍

import pygame  # Pygame library for game development 🎮
import random  # Random module for randomness 🎲

# Initialising Pygame 💡
pygame.init()

# Loading and playing background music 🎵🎶# source from freesound.org
# Importing the necessary modules 🐍# sources from opengameart.org

import pygame  # Pygame library for game development 🎮
import random  # Random module for randomness 🎲

# Initialising Pygame 💡
pygame.init()

# Loading and playing background music 🎵🎶
pygame.mixer.music.load('happybird_Garden_Song.wav')  # Load the background music file 🎧
pygame.mixer.music.play(-1)  # Play the music indefinitely in a loop 🔁
pygame.mixer.music.set_volume(0.5)  # Set the volume level to 50% 🔉

# Setting up the screen dimensions 🖥️
SCREEN_WIDTH = 800  # Width of the game window 📏
SCREEN_HEIGHT = 600  # Height of the game window 📐
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Creating the game window 🪟
pygame.display.set_caption("Hummingbird Adventure")  # Setting the window title 🎮

# Defining the game world dimensions 🌍
GAME_WORLD_WIDTH = 2000  # Width of the game world 🗺️
GAME_WORLD_HEIGHT = 1200  # Height of the game world 🗺️

# Loading images and assets 🖼️
background_img = pygame.image.load("bg_forest.png").convert()  # Background image 🌲
hummingbird_img = pygame.image.load("hummingbird.png").convert_alpha()  # Hummingbird image 🐦
enemy_img = pygame.image.load("enemy.jpg").convert()  # Enemy image 👾
enemy_img.set_colorkey((255, 255, 255))  # Set the white background as transparent 🗑️
cloud_img = pygame.image.load("cloud.png").convert_alpha()  # Cloud image ☁️
collectible_img = pygame.image.load("collectible.jpg").convert()  # Collectible image 💎
collectible_img.set_colorkey((255, 255, 255))  # Set white background as transparent 🗑️
boss_enemy_img = pygame.image.load("BossEnemy.png").convert_alpha()  # Boss enemy image 👹

# Loading flower images for projectiles 🌼🌸🌺
flower_images = [
    pygame.image.load("anthurium-pink.png").convert_alpha(),  # Flower image 1 🌺
    pygame.image.load("daffodils.png").convert_alpha(),  # Flower image 2 🌼
    pygame.image.load("foxglove.png").convert_alpha(),  # Flower image 3 🌸
    pygame.image.load("ginger.png").convert_alpha(),  # Flower image 4 🌺
    pygame.image.load("heather.png").convert_alpha(),  # Flower image 5 🌸
    pygame.image.load("pansies.png").convert_alpha(),  # Flower image 6 🌼
    pygame.image.load("protea.png").convert_alpha(),  # Flower image 7 🌺
    pygame.image.load("scarletstarbromeliad.png").convert_alpha(),  # Flower image 8 🌸
]

# Loading sound effects 🔊
new_enemy_sound = pygame.mixer.Sound('new_enemy.wav')  # Sound when a new enemy appears 🔔

# Resizing images to fit the game scale 📐
hummingbird_img = pygame.transform.scale(hummingbird_img, (50, 50))  # Resising hummingbird 🐦
enemy_img = pygame.transform.scale(enemy_img, (50, 50))  # Resizing enemy 👾
collectible_img = pygame.transform.scale(collectible_img, (30, 30))  # Resising collectible 💎
boss_enemy_img = pygame.transform.scale(boss_enemy_img, (70, 70))  # Resising boss enemy 👹

# Defining colours for health bars and text 🎨
WHITE = (255, 255, 255)  # White colour ⚪
GREEN = (0, 255, 0)  # Green colour for healtth bar 🟢
RED = (255, 0, 0)  # Red colour for health bar 🔴

# Camera class to handle the scrolling of the game world 🎥
class Camera:
    def __init__(self, width, height):
        self.camera_rect = pygame.Rect(0, 0, width, height)  # Camera view rectangle 📷
        self.width = width  # Width of the game world 🗺️
        self.height = height  # Height of the game world 🗺️

    def apply(self, rect):
        # Apply the camera offset to a sprite's rectangle 🧭
        return rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def update(self, target_rect):
        # Update the camera position to follow the target (hummingbird) smoothly 🐦
        x = target_rect.centerx - SCREEN_WIDTH // 2
        y = target_rect.centery - SCREEN_HEIGHT // 2

        # Limit scrolling to game world boundaries 🚧
        x = max(0, min(x, self.width - SCREEN_WIDTH))
        y = max(0, min(y, self.height - SCREEN_HEIGHT))

        self.camera_rect = pygame.Rect(x, y, SCREEN_WIDTH, SCREEN_HEIGHT)  # Update camera rectangle 🎯

# Hummingbird (Player) class 🐦
class Hummingbird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = hummingbird_img  # Hummingbird image 🖼️
        self.rect = self.image.get_rect()  # Hummingbird rectangle 📐
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Starting position in the center 📍
        self.speed = 5  # Movement speed 🚀
        self.health = 10  # Starting health points ❤️
        self.is_dashing = False  # Dash state 💨
        self.dash_speed = 15  # Speed during dash ⚡
        self.dash_duration = 10  # Frames the dash lasts ⏳
        self.dash_timer = 0  # Timer for dash duration ⏲️
        self.dash_cooldown = 60  # Frames before the dash can be used again ⏳
        self.dash_cooldown_timer = 0  # Timer for dash cooldown ⏲️

    def update(self):
        # Handling player input and movement 🎮
        keys = pygame.key.get_pressed()

        # Vertical movement ⬆️⬇️
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Horizontal movement ⬅️➡️
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Dash mechanics 💨
        if self.is_dashing:
            # Move the hummingbird forward quickly 🚀
            self.rect.x += self.dash_speed
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.dash_cooldown_timer = self.dash_cooldown
        else:
            # Apply dash cooldown ⏲️
            if self.dash_cooldown_timer > 0:
                self.dash_cooldown_timer -= 1

        # Keep the hummingbird within the game world boundaries 🗺️
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > GAME_WORLD_HEIGHT:
            self.rect.bottom = GAME_WORLD_HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > GAME_WORLD_WIDTH:
            self.rect.right = GAME_WORLD_WIDTH

# Enemy class 👾
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, is_boss=False):
        super().__init__()
        self.image = boss_enemy_img if is_boss else enemy_img  # Boss or regular enemy image 🖼️
        self.rect = self.image.get_rect()
        self.rect.x = x  # Enemy's starting x position 📍
        self.rect.y = y  # Enemy's starting y position 📍
        self.is_boss = is_boss  # Is this enemy a boss? 👹

    def update(self):
        # Enemies move towards the hummingbird to engage in combat ⚔️
        if self.rect.x > hummingbird.rect.x:
            self.rect.x -= 2  # Move left ⬅️
        if self.rect.x < hummingbird.rect.x:
            self.rect.x += 2  # Move right ➡️
        if self.rect.y > hummingbird.rect.y:
            self.rect.y -= 2  # Move up ⬆️
        if self.rect.y < hummingbird.rect.y:
            self.rect.y += 2  # Move down ⬇️

# Collectible class 💎
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = collectible_img  # Collectible image 🖼️
        self.rect = self.image.get_rect()
        self.rect.x = x  # Position x 📍
        self.rect.y = y  # Position y 📍

    def update(self):
        # Collectibles remain stationary or can have their own movement logic 🎁
        pass  # No movement for now 🚫

# Flower (Projectile) class 🌼
class Flower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = random.choice(flower_images)  # Randomly choose a flower image 🌸
        self.image = pygame.transform.scale(self.image, (30, 30))  # Resize the flower image 📐
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Starting position of the projectile 📍
        self.speed = 10  # Speed of the projectile 🚀

    def update(self):
        self.rect.x += self.speed  # Move the flower to the right ➡️
        if self.rect.left > GAME_WORLD_WIDTH:
            self.kill()  # Remove the flower if it goes off screen 🗑️

# GroundFlower class 🌺
class GroundFlower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = random.choice(flower_images)  # Random flower image 🌸
        self.image = pygame.transform.scale(self.image, (40, 40))  # Resize the flower image 📐
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Position on the ground 📍

    def update(self):
        # Ground flowers remain stationarry 🌼
        pass  # No movement 🚫

# Cloud class ☁️
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = cloud_img  # Cloud image 🖼️
        self.rect = self.image.get_rect()
        self.rect.x = x  # Starting x position 📍
        self.rect.y = y  # Starting y position 📍

    def update(self):
        # Clouds move slowly for a parallax effect 🌥️
        self.rect.x -= 1  # Move to the left ⬅️
        if self.rect.right < 0:
            self.rect.left = GAME_WORLD_WIDTH  # Reset position to the right end of the game world 🔄

# Function to spawn enemies 👾
def spawn_enemy(is_boss=False):
    enemy = Enemy(random.randint(0, GAME_WORLD_WIDTH - 50), random.randint(0, GAME_WORLD_HEIGHT - 50), is_boss)
    all_sprites.add(enemy)
    enemies.add(enemy)

# Main game loop function 🔄
def main_game_loop():
    # Using global variables so they can be modified within this function 🌐
    global running, lives, level, score, boss_killed, regular_enemy_killed, level_2_initialized, level_3_initialized

    # Initialise game variables 📝
    lives = 3  # Starting number of lives ❤️
    level = 1  # Starting level 🚩
    score = 0  # Starting score 🏆
    boss_killed = False  # Boss defeated status 👹
    regular_enemy_killed = False  # Regular enemy defeated status 👾
    level_2_initialized = False  # Level 2 initialisation status 🚧
    level_3_initialized = False  # Level 3 initialisation status 🚧

    # Reset sprite groups 🔄
    all_sprites.empty()
    enemies.empty()
    flowers.empty()
    collectibles.empty()
    ground_flowers.empty()
    clouds.empty()

    # Reinitialise hummingbird 🐦
    hummingbird.rect.center = (GAME_WORLD_WIDTH // 2, GAME_WORLD_HEIGHT // 2)
    hummingbird.health = 10  # Reset health ❤️
    all_sprites.add(hummingbird)

    # Reinitialise camera 🎥
    camera.camera_rect = pygame.Rect(0, 0, GAME_WORLD_WIDTH, GAME_WORLD_HEIGHT)

    # Spawn initial enemies 👾
    for i in range(5):
        spawn_enemy()

    # Add ground flowers 🌺
    for i in range(50):
        ground_flower = GroundFlower(random.randint(0, GAME_WORLD_WIDTH), random.randint(GAME_WORLD_HEIGHT - 100, GAME_WORLD_HEIGHT - 20))
        all_sprites.add(ground_flower)
        ground_flowers.add(ground_flower)

    # Add clouds ☁️
    for i in range(10):
        cloud = Cloud(random.randint(0, GAME_WORLD_WIDTH), random.randint(0, 200))
        all_sprites.add(cloud)
        clouds.add(cloud)

    # Main game loop 🕹️
    while running:
        # Event handling 🎮
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the game 🚪

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Shoot a flower projectile 🌼
                    flower = Flower(hummingbird.rect.right, hummingbird.rect.centery)
                    all_sprites.add(flower)
                    flowers.add(flower)
                elif event.key == pygame.K_d:
                    # Initiate dash if not currently dashing and not on cooldown 💨
                    if not hummingbird.is_dashing and hummingbird.dash_cooldown_timer <= 0:
                        hummingbird.is_dashing = True
                        hummingbird.dash_timer = hummingbird.dash_duration

        # Update all sprites and camera 🎥
        all_sprites.update()
        camera.update(hummingbird.rect)

        # Spawn collectibles at random intervals 🎁
        if random.randint(1, 200) == 1:
            collectible = Collectible(random.randint(0, GAME_WORLD_WIDTH - 30), random.randint(0, GAME_WORLD_HEIGHT - 30))
            all_sprites.add(collectible)
            collectibles.add(collectible)

        # Check for collisions between flowers and enemies 🌼 vs 👾
        for flower in flowers:
            hits = pygame.sprite.spritecollide(flower, enemies, False)
            if hits:
                flower.kill()  # Remove the flower 🗑️
                for hit in hits:
                    if hit.is_boss:
                        boss_killed = True  # Boss defeated 👹
                    else:
                        regular_enemy_killed = True  # Regular enemy defeated 👾
                    enemies.remove(hit)
                    all_sprites.remove(hit)
                    if level < 3:
                        spawn_enemy(is_boss=hit.is_boss)  # Spawn a new enemy 👾
                    new_enemy_sound.play()  # Play sound effect 🔊
                    score += 10  # Increase score 🏆

        # Check for collisions between hummingbird and enemies 🐦 vs 👾
        hits = pygame.sprite.spritecollide(hummingbird, enemies, False)
        if hits:
            for hit in hits:
                if hummingbird.is_dashing:
                    # If dashing, destroy the enemy without taking damage 💨
                    if hit.is_boss:
                        boss_killed = True
                    else:
                        regular_enemy_killed = True
                    enemies.remove(hit)
                    all_sprites.remove(hit)
                    if level < 3:
                        spawn_enemy(is_boss=hit.is_boss)
                    new_enemy_sound.play()
                    score += 10  # Award points 🏆
                else:
                    hummingbird.health -= 1  # Reduce health ❤️
                    if hit.is_boss:
                        boss_killed = True
                    else:
                        regular_enemy_killed = True
                    enemies.remove(hit)
                    all_sprites.remove(hit)
                    if level < 3:
                        spawn_enemy(is_boss=hit.is_boss)
                    new_enemy_sound.play()

        # Check for collisions between hummingbird and collectibles 🐦 vs 💎
        hits = pygame.sprite.spritecollide(hummingbird, collectibles, True)
        if hits:
            hummingbird.health += 1  # Increase health ❤️
            if hummingbird.health > 10:
                hummingbird.health = 10  # Max health cap 🔝

        # Level progression 🚀
        if score >= 100 and level == 1 and not level_2_initialized:
            level = 2
            level_2_initialized = True
            boss_killed = False
            regular_enemy_killed = False
            for i in range(3):  # Add boss enemies for level 2 👹
                spawn_enemy(is_boss=True)

        if level == 2 and score >= 150 and boss_killed and regular_enemy_killed and not level_3_initialized:
            level = 3
            level_3_initialized = True
            # Remove all enemies for level 3 🌟
            for enemy in enemies:
                all_sprites.remove(enemy)
            enemies.empty()

        # Handle health and lives ❤️
        if hummingbird.health <= 0:
            lives -= 1  # Lose a life 💔
            if lives > 0:
                hummingbird.health = 10  # Reset health ❤️
            else:
                game_over_screen()  # Show game over screen 🛑
                break  # Exit the main game loop 🔚

        # Drawing code 🖌️
        # Clear screen with black 🖤
        screen.fill((0, 0, 0))

        # Draw background surface 🌲
        screen.blit(background_surface, camera.apply(background_surface_rect))

        # Draw all sprites 🎨
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite.rect))

        # Draw UI elements 🖥️
        draw_health_bar()
        draw_lives()
        draw_level()
        draw_score()

        # Flip the display to update the screen 🖥️
        pygame.display.flip()

        # Cap the frame rate to 60 FPS ⏱️
        clock.tick(60)

# Function to draw the health bar ❤️
def draw_health_bar():
    pygame.draw.rect(screen, RED, (10, 10, 100, 10))  # Background bar 🔴
    pygame.draw.rect(screen, GREEN, (10, 10, hummingbird.health * 10, 10))  # Health level 🟢

# Function to draw the lives count ❤️
def draw_lives():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(text, (10, 30))  # Display lives in the top-left corner 📍

# Function to draw the current level 🚩
def draw_level():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH - 150, 10))  # Display level in the top-right corner 📍

# Function to draw the score 🏆
def draw_score():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - 50, 10))  # Display score at the top-center 📍

# Game over screen function 🛑
def game_over_screen():
    global running
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, RED)  # Game over message 🛑
    restart_text = pygame.font.Font(None, 36).render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 10))
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                running = False  # Exit the game 🚪
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    main_game_loop()  # Restart the game 🔄
                elif event.key == pygame.K_q:
                    waiting = False
                    running = False  # Exit the game 🚪

# Main execution point of the game 🚀
running = True
clock = pygame.time.Clock()

# Initialise sprite groups 🌟
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
flowers = pygame.sprite.Group()
collectibles = pygame.sprite.Group()
ground_flowers = pygame.sprite.Group()
clouds = pygame.sprite.Group()

# Initialise hummingbird and camera 🐦🎥
hummingbird = Hummingbird()
camera = Camera(GAME_WORLD_WIDTH, GAME_WORLD_HEIGHT)

# Create background surface 🌲
background_surface = pygame.Surface((GAME_WORLD_WIDTH, GAME_WORLD_HEIGHT))
background_surface_rect = background_surface.get_rect()

# Tile the background image across the background surface 🧩
for x in range(0, GAME_WORLD_WIDTH, background_img.get_width()):
    for y in range(0, GAME_WORLD_HEIGHT, background_img.get_height()):
        background_surface.blit(background_img, (x, y))

# Start the main game loop 🔄
main_game_loop()

# Quit Pygame when the game loop ends 🚪
pygame.quit()
pygame.mixer.music.load('happybird_Garden_Song.wav')  # Loads the background music file 🎧
pygame.mixer.music.play(-1)  # Play the music indefinitely in a loop 🔁
pygame.mixer.music.set_volume(0.5)  # Set the volume level to 50% 🔉

# Setting up the screen dimensions 🖥️
SCREEN_WIDTH = 800  # Width of the game window 📏
SCREEN_HEIGHT = 600  # Height of the game winndow 📐
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Creating the game window 🪟
pygame.display.set_caption("Hummingbird Adventure")  # Setting the window title 🎮

# Defining the game world dimensions 🌍
GAME_WORLD_WIDTH = 2000  # Width of the game world 🗺️
GAME_WORLD_HEIGHT = 1200  # Height of the game world 🗺️

# Loading images and assets 🖼️
background_img = pygame.image.load("bg_forest.png").convert()  # Background image 🌲
hummingbird_img = pygame.image.load("hummingbird.png").convert_alpha()  # Hummingbird image 🐦
enemy_img = pygame.image.load("enemy.jpg").convert()  # Enemy image 👾
enemy_img.set_colorkey((255, 255, 255))  # Set the white background as transparent 🗑️
cloud_img = pygame.image.load("cloud.png").convert_alpha()  # Cloud image ☁️
collectible_img = pygame.image.load("collectible.jpg").convert()  # Collectible image 💎
collectible_img.set_colorkey((255, 255, 255))  # Set white background as transparent 🗑️
boss_enemy_img = pygame.image.load("BossEnemy.png").convert_alpha()  # Boss enemy image 👹

# Loading flower images for projectiles 🌼🌸🌺
flower_images = [
    pygame.image.load("anthurium-pink.png").convert_alpha(),  # Flower image 1 🌺
    pygame.image.load("daffodils.png").convert_alpha(),  # Flower image 2 🌼
    pygame.image.load("foxglove.png").convert_alpha(),  # Flower image 3 🌸
    pygame.image.load("ginger.png").convert_alpha(),  # Flower image 4 🌺
    pygame.image.load("heather.png").convert_alpha(),  # Flower image 5 🌸
    pygame.image.load("pansies.png").convert_alpha(),  # Flower image 6 🌼
    pygame.image.load("protea.png").convert_alpha(),  # Flower image 7 🌺
    pygame.image.load("scarletstarbromeliad.png").convert_alpha(),  # Flower image 8 🌸
]

# Loading sound effects 🔊
new_enemy_sound = pygame.mixer.Sound('new_enemy.wav')  # Sound when a new enemy appears 🔔

# Resizing images to fit the game scale 📐
hummingbird_img = pygame.transform.scale(hummingbird_img, (50, 50))  # Resizing hummingbird 🐦
enemy_img = pygame.transform.scale(enemy_img, (50, 50))  # Resizing enemy 👾
collectible_img = pygame.transform.scale(collectible_img, (30, 30))  # Resizing collectible 💎
boss_enemy_img = pygame.transform.scale(boss_enemy_img, (70, 70))  # Resizing boss enemy 👹

# Defining colours for health bars and text 🎨
WHITE = (255, 255, 255)  # White colour ⚪
GREEN = (0, 255, 0)  # Green colour for health bar 🟢
RED = (255, 0, 0)  # Red colour for health bar 🔴

# Camera class to handle the scrolling of the game world 🎥
class Camera:
    def __init__(self, width, height):
        self.camera_rect = pygame.Rect(0, 0, width, height)  # Camera view rectangle 📷
        self.width = width  # Width of the game world 🗺️
        self.height = height  # Height of the game world 🗺️

    def apply(self, rect):
        # Apply the camera offset to a sprite's rectangle 🧭
        return rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def update(self, target_rect):
        # Update the camera position to follow the target (hummingbird) smoothly 🐦
        x = target_rect.centerx - SCREEN_WIDTH // 2
        y = target_rect.centery - SCREEN_HEIGHT // 2

        # Limit scrolling to game world boundaries 🚧
        x = max(0, min(x, self.width - SCREEN_WIDTH))
        y = max(0, min(y, self.height - SCREEN_HEIGHT))

        self.camera_rect = pygame.Rect(x, y, SCREEN_WIDTH, SCREEN_HEIGHT)  # Update camera rectangle 🎯

# Hummingbird (Player) class 🐦
class Hummingbird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = hummingbird_img  # Hummingbird image 🖼️
        self.rect = self.image.get_rect()  # Hummingbird rectangle 📐
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Starting position in the center 📍
        self.speed = 5  # Movement speed 🚀
        self.health = 10  # Starting health points ❤️
        self.is_dashing = False  # Dash state 💨
        self.dash_speed = 15  # Speed during dash ⚡
        self.dash_duration = 10  # Frames the dash lasts ⏳
        self.dash_timer = 0  # Timer for dash duration ⏲️
        self.dash_cooldown = 60  # Frames before the dash can be used again ⏳
        self.dash_cooldown_timer = 0  # Timer for dash cooldown ⏲️

    def update(self):
        # Handling player input and movement 🎮
        keys = pygame.key.get_pressed()

        # Vertical movement ⬆️⬇️
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Horizontal movement ⬅️➡️
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Dash mechanics 💨
        if self.is_dashing:
            # Move the hummingbird forward quickly 🚀
            self.rect.x += self.dash_speed
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.dash_cooldown_timer = self.dash_cooldown
        else:
            # Apply dash cooldown ⏲️
            if self.dash_cooldown_timer > 0:
                self.dash_cooldown_timer -= 1

        # Keep the hummingbird within the game world boundaries 🗺️
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > GAME_WORLD_HEIGHT:
            self.rect.bottom = GAME_WORLD_HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > GAME_WORLD_WIDTH:
            self.rect.right = GAME_WORLD_WIDTH

# Enemy class 👾
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, is_boss=False):
        super().__init__()
        self.image = boss_enemy_img if is_boss else enemy_img  # Boss or regular enemy image 🖼️
        self.rect = self.image.get_rect()
        self.rect.x = x  # Enemy's starting x position 📍
        self.rect.y = y  # Enemy's starting y position 📍
        self.is_boss = is_boss  # Is this enemy a boss? 👹

    def update(self):
        # Enemies move towards the hummingbird to engage in combat ⚔️
        if self.rect.x > hummingbird.rect.x:
            self.rect.x -= 2  # Move left ⬅️
        if self.rect.x < hummingbird.rect.x:
            self.rect.x += 2  # Move right ➡️
        if self.rect.y > hummingbird.rect.y:
            self.rect.y -= 2  # Move up ⬆️
        if self.rect.y < hummingbird.rect.y:
            self.rect.y += 2  # Move down ⬇️

# Collectible class 💎
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = collectible_img  # Collectible image 🖼️
        self.rect = self.image.get_rect()
        self.rect.x = x  # Position x 📍
        self.rect.y = y  # Position y 📍

    def update(self):
        # Collectibles remain stationary or can have their own movement logic 🎁
        pass  # No movement for now 🚫

# Flower (Projectile) class 🌼
class Flower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = random.choice(flower_images)  # Randomly choose a flower image 🌸
        self.image = pygame.transform.scale(self.image, (30, 30))  # Resize the flower image 📐
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Starting position of the projectile 📍
        self.speed = 10  # Speed of the projectile 🚀

    def update(self):
        self.rect.x += self.speed  # Move the flower to the right ➡️
        if self.rect.left > GAME_WORLD_WIDTH:
            self.kill()  # Remove the flower if it goes off screen 🗑️

# GroundFlower class 🌺
class GroundFlower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = random.choice(flower_images)  # Random flower image 🌸
        self.image = pygame.transform.scale(self.image, (40, 40))  # Resize the flower image 📐
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Position on the ground 📍

    def update(self):
        # Ground flowers remain stationary 🌼
        pass  # No movement 🚫

# Cloud class ☁️
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = cloud_img  # Cloud image 🖼️
        self.rect = self.image.get_rect()
        self.rect.x = x  # Starting x position 📍
        self.rect.y = y  # Starting y position 📍

    def update(self):
        # Clouds move slowly for a parallax effect 🌥️
        self.rect.x -= 1  # Move to the left ⬅️
        if self.rect.right < 0:
            self.rect.left = GAME_WORLD_WIDTH  # Reset position to the right end of the game world 🔄

# Function to spawn enemies 👾
def spawn_enemy(is_boss=False):
    enemy = Enemy(random.randint(0, GAME_WORLD_WIDTH - 50), random.randint(0, GAME_WORLD_HEIGHT - 50), is_boss)
    all_sprites.add(enemy)
    enemies.add(enemy)

# Main game loop function 🔄
def main_game_loop():
    # Using global variables so they can be modified within this function 🌐
    global running, lives, level, score, boss_killed, regular_enemy_killed, level_2_initialized, level_3_initialized

    # Initialise game variables 📝
    lives = 3  # Starting number of lives ❤️
    level = 1  # Starting level 🚩
    score = 0  # Starting score 🏆
    boss_killed = False  # Boss defeated status 👹
    regular_enemy_killed = False  # Regular enemy defeated status 👾
    level_2_initialized = False  # Level 2 initialisation status 🚧
    level_3_initialized = False  # Level 3 initialisation status 🚧

    # Reset sprite groups 🔄
    all_sprites.empty()
    enemies.empty()
    flowers.empty()
    collectibles.empty()
    ground_flowers.empty()
    clouds.empty()

    # Reinitialise hummingbird 🐦
    hummingbird.rect.center = (GAME_WORLD_WIDTH // 2, GAME_WORLD_HEIGHT // 2)
    hummingbird.health = 10  # Reset health ❤️
    all_sprites.add(hummingbird)

    # Reinitialise camera 🎥
    camera.camera_rect = pygame.Rect(0, 0, GAME_WORLD_WIDTH, GAME_WORLD_HEIGHT)

    # Spawn initial enemies 👾
    for i in range(5):
        spawn_enemy()

    # Add ground flowers 🌺
    for i in range(50):
        ground_flower = GroundFlower(random.randint(0, GAME_WORLD_WIDTH), random.randint(GAME_WORLD_HEIGHT - 100, GAME_WORLD_HEIGHT - 20))
        all_sprites.add(ground_flower)
        ground_flowers.add(ground_flower)

    # Add clouds ☁️
    for i in range(10):
        cloud = Cloud(random.randint(0, GAME_WORLD_WIDTH), random.randint(0, 200))
        all_sprites.add(cloud)
        clouds.add(cloud)

    # Main game looop 🕹️
    while running:
        # Event handling 🎮
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the game 🚪

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Shoot a flower projectile 🌼
                    flower = Flower(hummingbird.rect.right, hummingbird.rect.centery)
                    all_sprites.add(flower)
                    flowers.add(flower)
                elif event.key == pygame.K_d:
                    # Initiate dash if not currently dashing and not on cooldown 💨
                    if not hummingbird.is_dashing and hummingbird.dash_cooldown_timer <= 0:
                        hummingbird.is_dashing = True
                        hummingbird.dash_timer = hummingbird.dash_duration

        # Update all sprites and camera 🎥
        all_sprites.update()
        camera.update(hummingbird.rect)

        # Spawn collectibles at random intervals 🎁
        if random.randint(1, 200) == 1:
            collectible = Collectible(random.randint(0, GAME_WORLD_WIDTH - 30), random.randint(0, GAME_WORLD_HEIGHT - 30))
            all_sprites.add(collectible)
            collectibles.add(collectible)

        # Check for collisions between flowers and enemies 🌼 vs 👾
        for flower in flowers:
            hits = pygame.sprite.spritecollide(flower, enemies, False)
            if hits:
                flower.kill()  # Remove the flower 🗑️
                for hit in hits:
                    if hit.is_boss:
                        boss_killed = True  # Boss defeated 👹
                    else:
                        regular_enemy_killed = True  # Regular enemy defeated 👾
                    enemies.remove(hit)
                    all_sprites.remove(hit)
                    if level < 3:
                        spawn_enemy(is_boss=hit.is_boss)  # Spawn a new enemy 👾
                    new_enemy_sound.play()  # Play sound effect 🔊
                    score += 10  # Increase score 🏆

        # Check for collisions between hummingbird and enemies 🐦 vs 👾
        hits = pygame.sprite.spritecollide(hummingbird, enemies, False)
        if hits:
            for hit in hits:
                if hummingbird.is_dashing:
                    # If dashing, destroy the enemy without taking damage 💨
                    if hit.is_boss:
                        boss_killed = True
                    else:
                        regular_enemy_killed = True
                    enemies.remove(hit)
                    all_sprites.remove(hit)
                    if level < 3:
                        spawn_enemy(is_boss=hit.is_boss)
                    new_enemy_sound.play()
                    score += 10  # Award points 🏆
                else:
                    hummingbird.health -= 1  # Reduce health ❤️
                    if hit.is_boss:
                        boss_killed = True
                    else:
                        regular_enemy_killed = True
                    enemies.remove(hit)
                    all_sprites.remove(hit)
                    if level < 3:
                        spawn_enemy(is_boss=hit.is_boss)
                    new_enemy_sound.play()

        # Check for collisions between hummingbird and collectibles 🐦 vs 💎
        hits = pygame.sprite.spritecollide(hummingbird, collectibles, True)
        if hits:
            hummingbird.health += 1  # Increase health ❤️
            if hummingbird.health > 10:
                hummingbird.health = 10  # Max health cap 🔝

        # Level progression 🚀
        if score >= 100 and level == 1 and not level_2_initialized:
            level = 2
            level_2_initialized = True
            boss_killed = False
            regular_enemy_killed = False
            for i in range(3):  # Add boss enemies for level 2 👹
                spawn_enemy(is_boss=True)

        if level == 2 and score >= 150 and boss_killed and regular_enemy_killed and not level_3_initialized:
            level = 3
            level_3_initialized = True
            # Remove all enemies for level 3 🌟
            for enemy in enemies:
                all_sprites.remove(enemy)
            enemies.empty()

        # Handle health and lives ❤️
        if hummingbird.health <= 0:
            lives -= 1  # Lose a life 💔
            if lives > 0:
                hummingbird.health = 10  # Reset health ❤️
            else:
                game_over_screen()  # Show game over screen 🛑
                break  # Exit the main game loop 🔚

        # Drawing code 🖌️
        # Clear screen with black 🖤
        screen.fill((0, 0, 0))

        # Draw background surface 🌲
        screen.blit(background_surface, camera.apply(background_surface_rect))

        # Draw all sprites 🎨
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite.rect))

        # Draw UI elements 🖥️
        draw_health_bar()
        draw_lives()
        draw_level()
        draw_score()

        # Flip the display to update the screen 🖥️
        pygame.display.flip()

        # Cap the frame rate to 60 FPS ⏱️
        clock.tick(60)

# Function to draw the health bar ❤️
def draw_health_bar():
    pygame.draw.rect(screen, RED, (10, 10, 100, 10))  # Background bar 🔴
    pygame.draw.rect(screen, GREEN, (10, 10, hummingbird.health * 10, 10))  # Health level 🟢

# Function to draw the lives count ❤️
def draw_lives():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(text, (10, 30))  # Display lives in the top-left corner 📍

# Function to draw the current level 🚩
def draw_level():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH - 150, 10))  # Display level in the top-right corner 📍

# Function to draw the score 🏆
def draw_score():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - 50, 10))  # Display score at the top-center 📍

# Game over screen function 🛑
def game_over_screen():
    global running
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, RED)  # Game over message 🛑
    restart_text = pygame.font.Font(None, 36).render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 10))
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                running = False  # Exit the game 🚪
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    main_game_loop()  # Restart the game 🔄
                elif event.key == pygame.K_q:
                    waiting = False
                    running = False  # Exit the game 🚪

# Main execution point of the game 🚀
running = True
clock = pygame.time.Clock()

# Initialise sprite groups 🌟
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
flowers = pygame.sprite.Group()
collectibles = pygame.sprite.Group()
ground_flowers = pygame.sprite.Group()
clouds = pygame.sprite.Group()

# Initialise hummingbird and camera 🐦🎥
hummingbird = Hummingbird()
camera = Camera(GAME_WORLD_WIDTH, GAME_WORLD_HEIGHT)

# Create background surface 🌲
background_surface = pygame.Surface((GAME_WORLD_WIDTH, GAME_WORLD_HEIGHT))
background_surface_rect = background_surface.get_rect()

# Tile the background image across the background surface 🧩
for x in range(0, GAME_WORLD_WIDTH, background_img.get_width()):
    for y in range(0, GAME_WORLD_HEIGHT, background_img.get_height()):
        background_surface.blit(background_img, (x, y))

# Start the main game loop 🔄
main_game_loop()

# Quit Pygame when the game loop ends 🚪
pygame.quit()





















