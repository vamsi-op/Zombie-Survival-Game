import pygame
import random
import math
import os
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Get desktop info for proper fullscreen scaling
info = pygame.display.Info()
desktop_width = info.current_w
desktop_height = info.current_h

# Create screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
fullscreen = False
scale_factor = 1

# Title and Icon
pygame.display.set_caption("Zombie Apocalypse: Survival")
icon = pygame.Surface((32, 32))
icon.fill((255, 0, 0))
pygame.display.set_icon(icon)

# Create directories for assets if they don't exist
os.makedirs("assets/images", exist_ok=True)
os.makedirs("assets/sounds", exist_ok=True)

# Load background if it exists, otherwise use a color
if os.path.exists("assets/images/background.png"):
    background = pygame.image.load("assets/images/background.png")
    has_background_image = True
else:
    has_background_image = False

# Always define background_color for fallback
background_color = (20, 20, 30)

# Load sounds if they exist
try:
    shoot_sound = mixer.Sound("assets/sounds/shoot.wav") if os.path.exists("assets/sounds/shoot.wav") else None
    explosion_sound = mixer.Sound("assets/sounds/explosion.wav") if os.path.exists("assets/sounds/explosion.wav") else None
    hit_sound = mixer.Sound("assets/sounds/hit.wav") if os.path.exists("assets/sounds/hit.wav") else None
    powerup_sound = mixer.Sound("assets/sounds/powerup.wav") if os.path.exists("assets/sounds/powerup.wav") else None
    gameover_sound = mixer.Sound("assets/sounds/gameover.wav") if os.path.exists("assets/sounds/gameover.wav") else None
    purchase_sound = mixer.Sound("assets/sounds/purchase.wav") if os.path.exists("assets/sounds/purchase.wav") else None
    has_sounds = True
except:
    has_sounds = False

# Try to load background music
try:
    if os.path.exists("assets/sounds/background.wav"):
        mixer.music.load("assets/sounds/background.wav")
        mixer.music.play(-1)  # Play on loop
        mixer.music.set_volume(0.5)  # Set volume to 50%
except:
    pass

# Player
if os.path.exists("assets/images/player.png"):
    player_img = pygame.image.load("assets/images/player.png")
else:
    player_img = pygame.Surface((64, 64))
    player_img.fill((0, 255, 0))
player_x = 370
player_y = 480
player_x_change = 0
player_speed = 5
player_health = 100
player_max_health = 100

# Zombie types
zombie_types = [
    {"health": 2, "speed": 1.5, "damage": 10, "points": 10, "money": 5},
    {"health": 4, "speed": 1.0, "damage": 20, "points": 20, "money": 10},
    {"health": 8, "speed": 0.7, "damage": 30, "points": 30, "money": 15}
]

# Zombies
zombie_img = []
zombie_x = []
zombie_y = []
zombie_x_change = []
zombie_y_change = []
zombie_health = []
zombie_type = []
zombie_speed = []
num_of_zombies = 6

for i in range(num_of_zombies):
    zombie_type_idx = random.randint(0, len(zombie_types)-1)
    zombie_type.append(zombie_type_idx)
    
    # Try to load zombie image, otherwise create a colored rectangle
    if os.path.exists(f"assets/images/zombie{zombie_type_idx+1}.png"):
        temp_zombie = pygame.image.load(f"assets/images/zombie{zombie_type_idx+1}.png")
    else:
        temp_zombie = pygame.Surface((64, 64))
        temp_zombie.fill((255, 0, 0) if zombie_type_idx == 0 else 
                        (150, 0, 150) if zombie_type_idx == 1 else 
                        (150, 150, 0))
    
    zombie_img.append(temp_zombie)
    zombie_x.append(random.randint(0, 736))
    zombie_y.append(random.randint(50, 150))
    zombie_x_change.append(zombie_types[zombie_type_idx]['speed'])
    zombie_y_change.append(40)
    zombie_health.append(zombie_types[zombie_type_idx]['health'])
    zombie_speed.append(zombie_types[zombie_type_idx]['speed'])

# Bullets
bullet_imgs = []
for i in range(4):
    if os.path.exists(f"assets/images/bullet{i+1}.png"):
        bullet_imgs.append(pygame.image.load(f"assets/images/bullet{i+1}.png"))
    else:
        temp_bullet = pygame.Surface((16, 16))
        temp_bullet.fill((255, 255, 255))
        bullet_imgs.append(temp_bullet)

if not bullet_imgs:
    bullet_img = pygame.Surface((16, 16))
    bullet_img.fill((255, 255, 255))
else:
    bullet_img = bullet_imgs[0]

bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 15
bullet_state = "ready"  # Ready - can't see bullet, Fire - bullet is moving

# Explosions
explosion_imgs = []
for i in range(1, 6):
    if os.path.exists(f"assets/images/explosion{i}.png"):
        explosion_imgs.append(pygame.image.load(f"assets/images/explosion{i}.png"))

explosions = []  # List to store active explosions

# Power-ups
powerup_imgs = {
    "health": pygame.image.load("assets/images/health.png") if os.path.exists("assets/images/health.png") else pygame.Surface((32, 32), pygame.SRCALPHA),
    "ammo": pygame.image.load("assets/images/ammo.png") if os.path.exists("assets/images/ammo.png") else pygame.Surface((32, 32), pygame.SRCALPHA)
}

if not os.path.exists("assets/images/health.png"):
    powerup_imgs["health"].fill((0, 255, 0))
if not os.path.exists("assets/images/ammo.png"):
    powerup_imgs["ammo"].fill((255, 255, 0))

powerups = []  # List to store active powerups

# Score
score_value = 0
high_score = 0
font = pygame.font.Font(None, 32)
# Position UI in the top-right corner instead of top-left
text_x = screen_width - 170
text_y = 10

# Game Over text
game_over_font = pygame.font.Font(None, 64)

# Money system
money = 0
money_font = pygame.font.Font(None, 32)

# Weapons system
weapon_imgs = []
for i in range(4):
    if os.path.exists(f"assets/images/weapon{i+1}.png"):
        weapon_imgs.append(pygame.image.load(f"assets/images/weapon{i+1}.png"))
    else:
        temp_weapon = pygame.Surface((32, 32))
        temp_weapon.fill((200, 200, 200) if i == 0 else 
                        (150, 75, 0) if i == 1 else 
                        (100, 100, 100) if i == 2 else 
                        (50, 50, 50))
        weapon_imgs.append(temp_weapon)

weapons = [
    {"name": "Pistol", "damage": 1, "cost": 0, "owned": True, "ammo": 50, "max_ammo": 100, "fire_rate": 0.5, "img": weapon_imgs[0]},
    {"name": "Shotgun", "damage": 2, "cost": 50, "owned": False, "ammo": 0, "max_ammo": 50, "fire_rate": 0.8, "img": weapon_imgs[1]},
    {"name": "Rifle", "damage": 3, "cost": 100, "owned": False, "ammo": 0, "max_ammo": 80, "fire_rate": 0.3, "img": weapon_imgs[2]},
    {"name": "Rocket Launcher", "damage": 5, "cost": 200, "owned": False, "ammo": 0, "max_ammo": 20, "fire_rate": 1.2, "img": weapon_imgs[3]}
]
current_weapon = 0
last_shot_time = 0

# Wave system
wave_number = 1
zombies_per_wave = 6
zombies_killed_in_wave = 0
# Define reset_game function early so it can be called anywhere

def reset_game():
    global player_x, player_y, player_health, score_value, game_over, money
    global zombie_x, zombie_y, zombie_health, zombie_type, zombie_x_change, zombie_speed
    global bullet_state, bullet_y, explosions, powerups, shopping, paused
    global wave_number, zombies_killed_in_wave, show_wave_notification_timer
    global current_weapon, weapons, zombie_img, zombie_y_change
    global num_of_zombies  # Add this to reset the number of zombies
    
    # Reset player
    player_x = 370
    player_y = 480
    player_health = player_max_health
    
    # Reset game state
    game_over = False
    shopping = False
    paused = False
    score_value = 0
    money = 0
    
    # Reset weapons to initial state
    current_weapon = 0
    weapons = [
        {"name": "Pistol", "damage": 1, "cost": 0, "owned": True, "ammo": 50, "max_ammo": 100, "fire_rate": 0.5, "img": weapon_imgs[0]},
        {"name": "Shotgun", "damage": 2, "cost": 50, "owned": False, "ammo": 0, "max_ammo": 50, "fire_rate": 0.8, "img": weapon_imgs[1]},
        {"name": "Rifle", "damage": 3, "cost": 100, "owned": False, "ammo": 0, "max_ammo": 80, "fire_rate": 0.3, "img": weapon_imgs[2]},
        {"name": "Rocket Launcher", "damage": 5, "cost": 200, "owned": False, "ammo": 0, "max_ammo": 20, "fire_rate": 1.2, "img": weapon_imgs[3]}
    ]
    
    # Reset number of zombies to initial value
    num_of_zombies = zombies_per_wave
    
    # Reset zombies
    zombie_x.clear()
    zombie_y.clear()
    zombie_health.clear()
    zombie_type.clear()
    zombie_x_change.clear()
    zombie_y_change.clear()
    zombie_img.clear()
    zombie_speed.clear()
    
    # Initialize zombies for first wave
    for i in range(num_of_zombies):
        zombie_type_idx = random.randint(0, len(zombie_types)-1)
        zombie_type.append(zombie_type_idx)
        
        # Try to load zombie image, otherwise create a colored rectangle
        if os.path.exists(f"assets/images/zombie{zombie_type_idx+1}.png"):
            temp_zombie = pygame.image.load(f"assets/images/zombie{zombie_type_idx+1}.png")
        else:
            temp_zombie = pygame.Surface((64, 64))
            temp_zombie.fill((255, 0, 0) if zombie_type_idx == 0 else 
                            (150, 0, 150) if zombie_type_idx == 1 else 
                            (150, 150, 0))
        
        zombie_img.append(temp_zombie)
        zombie_x.append(random.randint(0, 736))
        zombie_y.append(random.randint(50, 150))
        zombie_x_change.append(zombie_types[zombie_type_idx]['speed'])
        zombie_y_change.append(40)
        zombie_health.append(zombie_types[zombie_type_idx]['health'])
        zombie_speed.append(zombie_types[zombie_type_idx]['speed'])
    
    # Reset bullet
    bullet_state = "ready"
    bullet_y = 480
    
    # Clear effects
    explosions.clear()
    powerups.clear()
    
    # Reset wave
    wave_number = 1
    zombies_killed_in_wave = 0
    show_wave_notification_timer = 180  # Show for 3 seconds

def show_ui(x, y):
    if fullscreen:
        # Apply scaling and offset in fullscreen mode
        scaled_x = offset_x + x * scale_factor
        scaled_y = offset_y + y * scale_factor
        
        # Create a smaller semi-transparent background for UI elements
        ui_width = 180 * scale_factor
        ui_height = 220 * scale_factor
        ui_bg = pygame.Surface((ui_width, ui_height), pygame.SRCALPHA)
        ui_bg.fill((0, 0, 0, 150))  # Slightly more opaque for better readability
        screen.blit(ui_bg, (scaled_x - 10 * scale_factor, scaled_y - 10 * scale_factor))
        
        # Draw border
        pygame.draw.rect(screen, (100, 100, 100), 
                        (scaled_x - 10 * scale_factor, scaled_y - 10 * scale_factor, 
                         ui_width, ui_height), 
                        max(1, int(2 * scale_factor)))
        
        # Score display - smaller font
        small_font = pygame.font.Font(None, int(24 * scale_factor))
        score = small_font.render(f"Score: {score_value}", True, (255, 255, 255))
        high_score_text = small_font.render(f"High: {high_score}", True, (255, 255, 255))
        screen.blit(score, (scaled_x, scaled_y))
        screen.blit(high_score_text, (scaled_x, scaled_y + 20 * scale_factor))
        
        # Money display with icon
        money_text = small_font.render(f"${money}", True, (255, 255, 0))
        money_icon = small_font.render("$", True, (255, 255, 0))
        screen.blit(money_icon, (scaled_x, scaled_y + 45 * scale_factor))
        screen.blit(money_text, (scaled_x + 15 * scale_factor, scaled_y + 45 * scale_factor))
        
        # Weapon display with icon
        weapon_text = small_font.render(f"{weapons[current_weapon]['name']}", True, (255, 255, 255))
        screen.blit(weapon_text, (scaled_x, scaled_y + 70 * scale_factor))
        
        # Ammo display
        ammo_text = small_font.render(f"Ammo: {weapons[current_weapon]['ammo']}", True, (255, 255, 255))
        screen.blit(ammo_text, (scaled_x, scaled_y + 95 * scale_factor))
        
        # Wave display
        wave_text = small_font.render(f"Wave: {wave_number}", True, (255, 200, 100))
        screen.blit(wave_text, (scaled_x, scaled_y + 120 * scale_factor))
        
        # Health bar - smaller
        pygame.draw.rect(screen, (100, 100, 100), 
                        (scaled_x, scaled_y + 145 * scale_factor, 
                         160 * scale_factor, 15 * scale_factor))
        health_width = max(0, (player_health / player_max_health) * 160 * scale_factor)
        health_color = (0, 255, 0) if player_health > 70 else (255, 255, 0) if player_health > 30 else (255, 0, 0)
        pygame.draw.rect(screen, health_color, 
                        (scaled_x, scaled_y + 145 * scale_factor, 
                         health_width, 15 * scale_factor))
        
        # Health percentage
        health_percent = int((player_health / player_max_health) * 100)
        health_text = small_font.render(f"{health_percent}%", True, (255, 255, 255))
        text_width = health_text.get_width()
        screen.blit(health_text, (scaled_x + (80 * scale_factor) - text_width//2, scaled_y + 145 * scale_factor))
    else:
        # Normal UI in windowed mode
        # Create a smaller semi-transparent background for UI elements
        ui_bg = pygame.Surface((180, 220), pygame.SRCALPHA)
        ui_bg.fill((0, 0, 0, 130))
        screen.blit(ui_bg, (x-10, y-10))
        
        # Draw border
        pygame.draw.rect(screen, (100, 100, 100), (x-10, y-10, 180, 220), 2)
        
        # Score display - smaller font
        small_font = pygame.font.Font(None, 24)
        score = small_font.render(f"Score: {score_value}", True, (255, 255, 255))
        high_score_text = small_font.render(f"High: {high_score}", True, (255, 255, 255))
        screen.blit(score, (x, y))
        screen.blit(high_score_text, (x, y + 20))
        
        # Money display with icon
        money_text = small_font.render(f"${money}", True, (255, 255, 0))
        money_icon = small_font.render("$", True, (255, 255, 0))
        screen.blit(money_icon, (x, y + 45))
        screen.blit(money_text, (x + 15, y + 45))
        
        # Weapon display with icon
        weapon_text = small_font.render(f"{weapons[current_weapon]['name']}", True, (255, 255, 255))
        screen.blit(weapon_text, (x, y + 70))
        
        # Ammo display
        ammo_text = small_font.render(f"Ammo: {weapons[current_weapon]['ammo']}", True, (255, 255, 255))
        screen.blit(ammo_text, (x, y + 95))
        
        # Wave display
        wave_text = small_font.render(f"Wave: {wave_number}", True, (255, 200, 100))
        screen.blit(wave_text, (x, y + 120))
        
        # Health bar - smaller
        pygame.draw.rect(screen, (100, 100, 100), (x, y + 145, 160, 15))
        health_width = max(0, (player_health / player_max_health) * 160)
        health_color = (0, 255, 0) if player_health > 70 else (255, 255, 0) if player_health > 30 else (255, 0, 0)
        pygame.draw.rect(screen, health_color, (x, y + 145, health_width, 15))
        
        # Health percentage
        health_percent = int((player_health / player_max_health) * 100)
        health_text = small_font.render(f"{health_percent}%", True, (255, 255, 255))
        text_width = health_text.get_width()
        screen.blit(health_text, (x + 80 - text_width//2, y + 145))

def player(x, y):
    # Apply scaling and offset in fullscreen mode
    if fullscreen:
        scaled_x = offset_x + x * scale_factor
        scaled_y = offset_y + y * scale_factor
        
        # Scale the image
        scaled_img = pygame.transform.scale(player_img, 
                                          (int(player_img.get_width() * scale_factor), 
                                           int(player_img.get_height() * scale_factor)))
        
        # Draw player
        screen.blit(scaled_img, (scaled_x, scaled_y))
        
        # Draw current weapon
        scaled_weapon = pygame.transform.scale(weapons[current_weapon]["img"], 
                                             (int(weapons[current_weapon]["img"].get_width() * scale_factor), 
                                              int(weapons[current_weapon]["img"].get_height() * scale_factor)))
        screen.blit(scaled_weapon, (scaled_x + 40 * scale_factor, scaled_y + 30 * scale_factor))
    else:
        # Normal drawing in windowed mode
        screen.blit(player_img, (x, y))
        # Draw current weapon
        screen.blit(weapons[current_weapon]["img"], (x + 40, y + 30))

def zombie(x, y, i):
    if fullscreen:
        # Apply scaling and offset in fullscreen mode
        scaled_x = offset_x + x * scale_factor
        scaled_y = offset_y + y * scale_factor
        
        # Scale the image
        scaled_img = pygame.transform.scale(zombie_img[i], 
                                          (int(zombie_img[i].get_width() * scale_factor), 
                                           int(zombie_img[i].get_height() * scale_factor)))
        
        # Draw zombie
        screen.blit(scaled_img, (scaled_x, scaled_y))
        
        # Draw health bar above zombie
        health_percent = zombie_health[i] / zombie_types[zombie_type[i]]["health"]
        bar_width = 50 * scale_factor
        health_width = max(0, health_percent * bar_width)
        pygame.draw.rect(screen, (100, 100, 100), (scaled_x + 7 * scale_factor, scaled_y - 10 * scale_factor, bar_width, 5 * scale_factor))
        health_color = (0, 255, 0) if health_percent > 0.7 else (255, 255, 0) if health_percent > 0.3 else (255, 0, 0)
        pygame.draw.rect(screen, health_color, (scaled_x + 7 * scale_factor, scaled_y - 10 * scale_factor, health_width, 5 * scale_factor))
    else:
        # Normal drawing in windowed mode
        screen.blit(zombie_img[i], (x, y))
        
        # Draw health bar above zombie
        health_percent = zombie_health[i] / zombie_types[zombie_type[i]]["health"]
        bar_width = 50
        health_width = max(0, health_percent * bar_width)
        pygame.draw.rect(screen, (100, 100, 100), (x + 7, y - 10, bar_width, 5))
        health_color = (0, 255, 0) if health_percent > 0.7 else (255, 255, 0) if health_percent > 0.3 else (255, 0, 0)
        pygame.draw.rect(screen, health_color, (x + 7, y - 10, health_width, 5))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    
    if fullscreen:
        # Apply scaling and offset in fullscreen mode
        scaled_x = offset_x + x * scale_factor
        scaled_y = offset_y + y * scale_factor
        
        # Choose the right bullet image based on weapon
        if len(bullet_imgs) > current_weapon:
            bullet_img_to_use = bullet_imgs[current_weapon]
        else:
            bullet_img_to_use = bullet_img
            
        # Scale the bullet image
        scaled_bullet = pygame.transform.scale(bullet_img_to_use, 
                                             (int(bullet_img_to_use.get_width() * scale_factor), 
                                              int(bullet_img_to_use.get_height() * scale_factor)))
        
        # Draw bullet
        screen.blit(scaled_bullet, (scaled_x + 24 * scale_factor, scaled_y + 10 * scale_factor))
    else:
        # Normal drawing in windowed mode
        if len(bullet_imgs) > current_weapon:
            screen.blit(bullet_imgs[current_weapon], (x + 24, y + 10))
        else:
            screen.blit(bullet_img, (x + 24, y + 10))
    
    if has_sounds and shoot_sound:
        shoot_sound.play()

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2)
    if distance < 32:
        return True
    return False

def game_over_text():
    if fullscreen:
        # Apply scaling and offset in fullscreen mode
        # Semi-transparent overlay
        overlay = pygame.Surface((desktop_width, desktop_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Game over panel
        panel_width, panel_height = 500 * scale_factor, 300 * scale_factor
        panel_x = desktop_width//2 - panel_width//2
        panel_y = desktop_height//2 - panel_height//2
        
        panel_bg = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_bg.fill((40, 0, 0, 230))
        screen.blit(panel_bg, (panel_x, panel_y))
        
        # Panel border
        pygame.draw.rect(screen, (150, 0, 0), (panel_x, panel_y, panel_width, panel_height), max(1, int(3 * scale_factor)))
        
        # Game over text
        scaled_font = pygame.font.Font(None, int(64 * scale_factor))
        over_text = scaled_font.render("GAME OVER", True, (255, 50, 50))
        screen.blit(over_text, (desktop_width//2 - over_text.get_width()//2, panel_y + 50 * scale_factor))
        
        # Final score
        small_font = pygame.font.Font(None, int(32 * scale_factor))
        score_text = small_font.render(f"Final Score: {score_value}", True, (255, 255, 255))
        screen.blit(score_text, (desktop_width//2 - score_text.get_width()//2, panel_y + 120 * scale_factor))
        
        # High score
        if score_value >= high_score:
            high_score_text = small_font.render(f"NEW HIGH SCORE!", True, (255, 255, 0))
        else:
            high_score_text = small_font.render(f"High Score: {high_score}", True, (200, 200, 200))
        screen.blit(high_score_text, (desktop_width//2 - high_score_text.get_width()//2, panel_y + 150 * scale_factor))
        
        # Wave reached
        wave_text = small_font.render(f"Waves Survived: {wave_number}", True, (200, 200, 255))
        screen.blit(wave_text, (desktop_width//2 - wave_text.get_width()//2, panel_y + 180 * scale_factor))
        
        # Restart instruction
        restart_text = small_font.render("Press R to restart", True, (255, 255, 255))
        screen.blit(restart_text, (desktop_width//2 - restart_text.get_width()//2, panel_y + 220 * scale_factor))
    else:
        # Normal drawing in windowed mode
        # Semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Game over panel
        panel_width, panel_height = 500, 300
        panel_x = screen_width//2 - panel_width//2
        panel_y = screen_height//2 - panel_height//2
        
        panel_bg = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_bg.fill((40, 0, 0, 230))
        screen.blit(panel_bg, (panel_x, panel_y))
        
        # Panel border
        pygame.draw.rect(screen, (150, 0, 0), (panel_x, panel_y, panel_width, panel_height), 3)
        
        # Game over text
        over_text = game_over_font.render("GAME OVER", True, (255, 50, 50))
        screen.blit(over_text, (screen_width//2 - over_text.get_width()//2, panel_y + 50))
        
        # Final score
        score_text = font.render(f"Final Score: {score_value}", True, (255, 255, 255))
        screen.blit(score_text, (screen_width//2 - score_text.get_width()//2, panel_y + 120))
        
        # High score
        if score_value >= high_score:
            high_score_text = font.render(f"NEW HIGH SCORE!", True, (255, 255, 0))
        else:
            high_score_text = font.render(f"High Score: {high_score}", True, (200, 200, 200))
        screen.blit(high_score_text, (screen_width//2 - high_score_text.get_width()//2, panel_y + 150))
        
        # Wave reached
        wave_text = font.render(f"Waves Survived: {wave_number}", True, (200, 200, 255))
        screen.blit(wave_text, (screen_width//2 - wave_text.get_width()//2, panel_y + 180))
        
        # Restart instruction
        restart_text = font.render("Press R to restart", True, (255, 255, 255))
        screen.blit(restart_text, (screen_width//2 - restart_text.get_width()//2, panel_y + 220))

def show_shop():
    # Semi-transparent overlay for the entire screen
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    # Shop panel
    shop_bg = pygame.Surface((600, 450), pygame.SRCALPHA)
    shop_bg.fill((40, 40, 50, 230))
    screen.blit(shop_bg, (100, 75))
    
    # Shop border
    pygame.draw.rect(screen, (100, 100, 120), (100, 75, 600, 450), 3)
    
    # Shop header
    header_bg = pygame.Surface((600, 60), pygame.SRCALPHA)
    header_bg.fill((60, 60, 80, 230))
    screen.blit(header_bg, (100, 75))
    
    # Title
    shop_title = game_over_font.render("WEAPON SHOP", True, (255, 255, 255))
    screen.blit(shop_title, (screen_width//2 - shop_title.get_width()//2, 90))
    
    # Show current money
    money_text = font.render(f"Your Money: ${money}", True, (255, 255, 0))
    screen.blit(money_text, (120, 150))
    
    # Shop instructions
    shop_instructions = font.render("Press B to open/close shop", True, (255, 255, 255))
    screen.blit(shop_instructions, (400, 150))
    
    # Weapon list
    y_pos = 190
    for i, weapon in enumerate(weapons):
        # Weapon panel background
        weapon_bg_color = (0, 100, 0, 150) if weapon["owned"] and i == current_weapon else \
                         (0, 70, 0, 150) if weapon["owned"] else \
                         (70, 70, 70, 150)
        weapon_bg = pygame.Surface((560, 60), pygame.SRCALPHA)
        weapon_bg.fill(weapon_bg_color)
        screen.blit(weapon_bg, (120, y_pos))
        
        # Weapon border
        border_color = (0, 255, 0) if weapon["owned"] and i == current_weapon else \
                      (100, 255, 100) if weapon["owned"] else \
                      (150, 150, 150)
        pygame.draw.rect(screen, border_color, (120, y_pos, 560, 60), 2)
        
        # Status indicator
        status = "EQUIPPED" if i == current_weapon and weapon["owned"] else \
                "OWNED" if weapon["owned"] else \
                f"${weapon['cost']}"
        status_color = (0, 255, 0) if weapon["owned"] and i == current_weapon else \
                      (100, 255, 100) if weapon["owned"] else \
                      (255, 255, 255)
        
        # Draw weapon image if available
        if "img" in weapon:
            scaled_img = pygame.transform.scale(weapon["img"], (40, 40))
            screen.blit(scaled_img, (130, y_pos + 10))
        
        # Draw weapon info
        weapon_text = font.render(f"{i+1}. {weapon['name']} - Damage: {weapon['damage']}", True, (255, 255, 255))
        screen.blit(weapon_text, (180, y_pos + 10))
        
        # Draw status
        status_text = font.render(status, True, status_color)
        screen.blit(status_text, (600 - status_text.get_width(), y_pos + 10))
        
        # Draw ammo info
        ammo_text = font.render(f"Ammo: {weapon['ammo']}/{weapon['max_ammo']} - Fire Rate: {weapon['fire_rate']}s", True, (200, 200, 200))
        screen.blit(ammo_text, (180, y_pos + 35))
        
        y_pos += 70
    
    # Buy ammo option
    ammo_bg = pygame.Surface((560, 50), pygame.SRCALPHA)
    ammo_bg.fill((70, 70, 0, 150))
    screen.blit(ammo_bg, (120, y_pos))
    pygame.draw.rect(screen, (200, 200, 0), (120, y_pos, 560, 50), 2)
    
    ammo_text = font.render(f"Press A: Buy Ammo for {weapons[current_weapon]['name']} ($20)", True, (255, 255, 0))
    screen.blit(ammo_text, (150, y_pos + 15))
    
    # Instructions
    instructions = font.render("Press 1-4 to select/buy weapons", True, (200, 200, 255))
    screen.blit(instructions, (screen_width//2 - instructions.get_width()//2, y_pos + 70))
    
    exit_text = font.render("Press ESC to exit shop", True, (200, 200, 200))
    screen.blit(exit_text, (screen_width//2 - exit_text.get_width()//2, y_pos + 100))

def add_explosion(x, y):
    explosions.append({"x": x, "y": y, "frame": 0})
    if has_sounds and explosion_sound:
        explosion_sound.play()

def update_explosions():
    i = 0
    while i < len(explosions):
        explosion = explosions[i]
        if explosion["frame"] >= len(explosion_imgs) if explosion_imgs else 5:
            explosions.pop(i)
        else:
            if fullscreen:
                # Apply scaling and offset in fullscreen mode
                scaled_x = offset_x + explosion["x"] * scale_factor
                scaled_y = offset_y + explosion["y"] * scale_factor
                
                if explosion_imgs:
                    # Scale the explosion image
                    scaled_exp = pygame.transform.scale(explosion_imgs[explosion["frame"]], 
                                                     (int(explosion_imgs[explosion["frame"]].get_width() * scale_factor), 
                                                      int(explosion_imgs[explosion["frame"]].get_height() * scale_factor)))
                    screen.blit(scaled_exp, (scaled_x, scaled_y))
                else:
                    # Draw explosion (simple circle that grows and fades)
                    radius = (explosion["frame"] + 1) * 10 * scale_factor
                    alpha = 255 - (explosion["frame"] * 50)
                    s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                    pygame.draw.circle(s, (255, 165, 0, alpha), (radius, radius), radius)
                    screen.blit(s, (scaled_x - radius + 32 * scale_factor, scaled_y - radius + 32 * scale_factor))
            else:
                # Normal drawing in windowed mode
                if explosion_imgs:
                    screen.blit(explosion_imgs[explosion["frame"]], (explosion["x"], explosion["y"]))
                else:
                    # Draw explosion (simple circle that grows and fades)
                    radius = (explosion["frame"] + 1) * 10
                    alpha = 255 - (explosion["frame"] * 50)
                    s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                    pygame.draw.circle(s, (255, 165, 0, alpha), (radius, radius), radius)
                    screen.blit(s, (explosion["x"] - radius + 32, explosion["y"] - radius + 32))
            
            explosion["frame"] += 1
            i += 1

def spawn_powerup(x, y):
    if random.random() < 0.3:  # 30% chance to spawn a powerup
        powerup_type = "health" if random.random() < 0.5 else "ammo"
        powerups.append({"type": powerup_type, "img": powerup_imgs[powerup_type], "x": x, "y": y})

def update_powerups():
    i = 0
    while i < len(powerups):
        powerup = powerups[i]
        # Move powerup down
        powerup["y"] += 1
        
        # Check if player collected powerup
        if player_x < powerup["x"] + 32 and player_x + 64 > powerup["x"] and player_y < powerup["y"] + 32 and player_y + 64 > powerup["y"]:
            if powerup["type"] == "health":
                global player_health
                player_health = min(player_max_health, player_health + 30)
            elif powerup["type"] == "ammo":
                weapons[current_weapon]["ammo"] = min(weapons[current_weapon]["max_ammo"], weapons[current_weapon]["ammo"] + 20)
            
            if has_sounds and powerup_sound:
                powerup_sound.play()
            powerups.pop(i)
        # Remove if out of screen
        elif powerup["y"] > screen_height:
            powerups.pop(i)
        else:
            if fullscreen:
                # Apply scaling and offset in fullscreen mode
                scaled_x = offset_x + powerup["x"] * scale_factor
                scaled_y = offset_y + powerup["y"] * scale_factor
                
                # Scale the powerup image
                scaled_img = pygame.transform.scale(powerup["img"], 
                                                 (int(powerup["img"].get_width() * scale_factor), 
                                                  int(powerup["img"].get_height() * scale_factor)))
                
                screen.blit(scaled_img, (scaled_x, scaled_y))
            else:
                # Normal drawing in windowed mode
                screen.blit(powerup["img"], (powerup["x"], powerup["y"]))
            i += 1

def show_wave_notification():
    if fullscreen:
        # Apply scaling and offset in fullscreen mode
        # Display wave notification at the center of the screen
        wave_bg = pygame.Surface((400 * scale_factor, 100 * scale_factor), pygame.SRCALPHA)
        wave_bg.fill((0, 0, 0, 180))
        screen.blit(wave_bg, (desktop_width//2 - 200 * scale_factor, desktop_height//2 - 50 * scale_factor))
        
        # Scale font size
        scaled_font = pygame.font.Font(None, int(64 * scale_factor))
        wave_title = scaled_font.render(f"WAVE {wave_number}", True, (255, 200, 100))
        title_width = wave_title.get_width()
        screen.blit(wave_title, (desktop_width//2 - title_width//2, desktop_height//2 - 30 * scale_factor))
        
        if wave_number > 1:
            small_font = pygame.font.Font(None, int(32 * scale_factor))
            wave_subtitle = small_font.render("Zombies are getting stronger!", True, (255, 255, 255))
            subtitle_width = wave_subtitle.get_width()
            screen.blit(wave_subtitle, (desktop_width//2 - subtitle_width//2, desktop_height//2 + 20 * scale_factor))
    else:
        # Normal drawing in windowed mode
        # Display wave notification at the center of the screen
        wave_bg = pygame.Surface((400, 100), pygame.SRCALPHA)
        wave_bg.fill((0, 0, 0, 180))
        screen.blit(wave_bg, (screen_width//2 - 200, screen_height//2 - 50))
        
        wave_title = game_over_font.render(f"WAVE {wave_number}", True, (255, 200, 100))
        title_width = wave_title.get_width()
        screen.blit(wave_title, (screen_width//2 - title_width//2, screen_height//2 - 30))
        
        if wave_number > 1:
            wave_subtitle = font.render("Zombies are getting stronger!", True, (255, 255, 255))
            subtitle_width = wave_subtitle.get_width()
            screen.blit(wave_subtitle, (screen_width//2 - subtitle_width//2, screen_height//2 + 20))

def next_wave():
    global wave_number, num_of_zombies, zombies_killed_in_wave
    global zombie_img, zombie_x, zombie_y, zombie_x_change, zombie_y_change, zombie_health, zombie_type, zombie_speed
    global show_wave_notification_timer
    
    wave_number += 1
    zombies_killed_in_wave = 0
    show_wave_notification_timer = 180  # Show for 3 seconds (60 frames per second)
    
    # Increase number of zombies each wave
    new_zombies = min(3, wave_number)  # Add up to 3 zombies per wave
    
    for _ in range(new_zombies):
        zombie_type_idx = random.randint(0, len(zombie_types)-1)
        zombie_type.append(zombie_type_idx)
        
        # Try to load zombie image, otherwise create a colored rectangle
        if os.path.exists(f"assets/images/zombie{zombie_type_idx+1}.png"):
            temp_zombie = pygame.image.load(f"assets/images/zombie{zombie_type_idx+1}.png")
        else:
            temp_zombie = pygame.Surface((64, 64))
            temp_zombie.fill((255, 0, 0) if zombie_type_idx == 0 else 
                            (150, 0, 150) if zombie_type_idx == 1 else 
                            (150, 150, 0))
        
        zombie_img.append(temp_zombie)
        zombie_x.append(random.randint(0, 736))
        zombie_y.append(random.randint(50, 150))
        zombie_x_change.append(zombie_types[zombie_type_idx]['speed'])
        zombie_y_change.append(40)
        zombie_health.append(zombie_types[zombie_type_idx]['health'])
        zombie_speed.append(zombie_types[zombie_type_idx]['speed'])
    
    num_of_zombies += new_zombies
    
    # Make zombies slightly faster and stronger each wave
    for i in range(num_of_zombies):
        base_type = zombie_types[zombie_type[i]]
        zombie_speed[i] = base_type['speed'] * (1 + wave_number * 0.1)  # 10% faster each wave
        zombie_health[i] = base_type['health'] * (1 + wave_number * 0.2)  # 20% more health each wave

# Game Loop
running = True
shopping = False
game_over = False
paused = False
clock = pygame.time.Clock()
show_wave_notification_timer = 180  # Show wave notification for 3 seconds at start

# Variables for fullscreen scaling
offset_x = 0
offset_y = 0

while running:
    # Clear screen first to prevent ghosting
    if fullscreen:
        screen.fill((0, 0, 0))  # Fill entire screen with black
    else:
        screen.fill(background_color)
    
    # Draw background
    if has_background_image:
        if fullscreen:
            # Scale background to fit screen while maintaining aspect ratio
            bg_scaled = pygame.transform.scale(background, 
                                             (int(screen_width * scale_factor), 
                                              int(screen_height * scale_factor)))
            screen.blit(bg_scaled, (offset_x, offset_y))
        else:
            screen.blit(background, (0, 0))
    
    # Show shop instruction at the bottom of the screen
    if not shopping and not game_over and not paused:
        shop_hint = font.render("Press B to open shop", True, (200, 200, 255))
        screen.blit(shop_hint, (screen_width//2 - shop_hint.get_width()//2, screen_height - 30))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Keystroke check
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_speed
            if event.key == pygame.K_RIGHT:
                player_x_change = player_speed
            if event.key == pygame.K_SPACE and bullet_state == "ready" and not shopping and not game_over and not paused:
                if weapons[current_weapon]["ammo"] > 0:
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
                    weapons[current_weapon]["ammo"] -= 1
                    last_shot_time = pygame.time.get_ticks()
            if event.key == pygame.K_b and not game_over and not paused:
                shopping = not shopping
            if event.key == pygame.K_ESCAPE and shopping:
                shopping = False
            if event.key == pygame.K_r and game_over:
                reset_game()
            if event.key == pygame.K_p and not game_over and not shopping:
                paused = not paused
            
            # Toggle fullscreen with F11
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    # Save original screen size for calculations
                    original_width, original_height = screen_width, screen_height
                    
                    # Switch to fullscreen mode using desktop resolution
                    screen = pygame.display.set_mode((desktop_width, desktop_height), pygame.FULLSCREEN)
                    
                    # Calculate scaling factors
                    scale_x = desktop_width / original_width
                    scale_y = desktop_height / original_height
                    scale_factor = min(scale_x, scale_y)  # Use the smaller scale to maintain aspect ratio
                    
                    # Calculate offset to center the game
                    offset_x = (desktop_width - original_width * scale_factor) / 2
                    offset_y = (desktop_height - original_height * scale_factor) / 2
                    
                    print(f"Fullscreen enabled: {desktop_width}x{desktop_height}, scale: {scale_factor}")
                else:
                    # Return to windowed mode with original dimensions
                    pygame.display.quit()
                    pygame.display.init()
                    screen = pygame.display.set_mode((screen_width, screen_height))
                    scale_factor = 1
                    offset_x = 0
                    offset_y = 0
                    print("Windowed mode enabled")
            
            # Weapon switching with number keys
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4] and not shopping:
                weapon_idx = event.key - pygame.K_1
                if weapon_idx < len(weapons) and weapons[weapon_idx]["owned"]:
                    current_weapon = weapon_idx
            
            # Shop controls - handle weapon purchase and ammo purchase
            if shopping:
                # Handle weapon selection/purchase with number keys
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    weapon_idx = event.key - pygame.K_1
                    if weapon_idx < len(weapons):
                        if weapons[weapon_idx]["owned"]:
                            current_weapon = weapon_idx
                            shopping = False
                            print(f"Selected weapon: {weapons[weapon_idx]['name']}")
                        elif money >= weapons[weapon_idx]["cost"]:
                            money -= weapons[weapon_idx]["cost"]
                            weapons[weapon_idx]["owned"] = True
                            weapons[weapon_idx]["ammo"] = weapons[weapon_idx]["max_ammo"] // 2
                            current_weapon = weapon_idx
                            shopping = False
                            if has_sounds and purchase_sound:
                                purchase_sound.play()
                            print(f"Purchased weapon: {weapons[weapon_idx]['name']} for ${weapons[weapon_idx]['cost']}")
                        else:
                            print(f"Not enough money for {weapons[weapon_idx]['name']}. Need ${weapons[weapon_idx]['cost']}, have ${money}")
                
                # Buy ammo
                if event.key == pygame.K_a:
                    if money >= 20 and weapons[current_weapon]["ammo"] < weapons[current_weapon]["max_ammo"]:
                        money -= 20
                        weapons[current_weapon]["ammo"] = min(weapons[current_weapon]["max_ammo"], 
                                                           weapons[current_weapon]["ammo"] + weapons[current_weapon]["max_ammo"] // 2)
                        if has_sounds and purchase_sound:
                            purchase_sound.play()
                        print(f"Purchased ammo for {weapons[current_weapon]['name']}")
                    else:
                        if money < 20:
                            print(f"Not enough money for ammo. Need $20, have ${money}")
                        else:
                            print(f"Ammo is already full for {weapons[current_weapon]['name']}")
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
    
    if shopping:
        show_shop()
        
        # Shop controls - handle in the event loop instead of here
        # This ensures we catch single key presses properly
    
    elif paused:
        # Display pause screen
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        pause_text = game_over_font.render("PAUSED", True, (255, 255, 255))
        screen.blit(pause_text, (screen_width//2 - pause_text.get_width()//2, 250))
        resume_text = font.render("Press P to resume", True, (255, 255, 255))
        screen.blit(resume_text, (screen_width//2 - resume_text.get_width()//2, 320))
    
    elif game_over:
        game_over_text()
        
        # Update high score
        if score_value > high_score:
            high_score = score_value
    
    else:
        # Player movement
        player_x += player_x_change
        
        # Boundaries
        if player_x <= 0:
            player_x = 0
        elif player_x >= 736:
            player_x = 736
            
        # Check if all zombies in wave are killed
        if zombies_killed_in_wave >= num_of_zombies:
            next_wave()
        
        # Show wave notification if timer is active
        if show_wave_notification_timer > 0:
            show_wave_notification()
            show_wave_notification_timer -= 1
            
        # Zombie movement
        for i in range(num_of_zombies):
            # Game Over
            if zombie_y[i] > 440 and zombie_health[i] > 0:
                player_health -= zombie_types[zombie_type[i]]["damage"]
                zombie_y[i] = random.randint(50, 150)
                zombie_x[i] = random.randint(0, 736)
                
                if player_health <= 0:
                    game_over = True
                    if has_sounds and gameover_sound:
                        gameover_sound.play()
                    break
                
            zombie_x[i] += zombie_x_change[i]
            if zombie_x[i] <= 0:
                zombie_x_change[i] = zombie_speed[i]
                zombie_y[i] += zombie_y_change[i]
            elif zombie_x[i] >= 736:
                zombie_x_change[i] = -zombie_speed[i]
                zombie_y[i] += zombie_y_change[i]
                
            # Collision
            if bullet_state == "fire":
                collision = is_collision(zombie_x[i], zombie_y[i], bullet_x, bullet_y)
                if collision and zombie_health[i] > 0:
                    # Apply damage based on weapon
                    damage = weapons[current_weapon]["damage"]
                    zombie_health[i] -= damage
                    
                    # Reset bullet
                    bullet_y = 480
                    bullet_state = "ready"
                    
                    # Play hit sound
                    if has_sounds and hit_sound:
                        hit_sound.play()
                    
                    # Check if zombie is killed
                    if zombie_health[i] <= 0:
                        # Add explosion
                        add_explosion(zombie_x[i], zombie_y[i])
                        
                        # Add score and money
                        score_value += zombie_types[zombie_type[i]]["points"]
                        money += zombie_types[zombie_type[i]]["money"]
                        
                        # Chance to spawn powerup
                        spawn_powerup(zombie_x[i], zombie_y[i])
                        
                        # Reset zombie
                        zombie_type_idx = random.randint(0, len(zombie_types)-1)
                        zombie_type[i] = zombie_type_idx
                        
                        # Try to load zombie image, otherwise create a colored rectangle
                        if os.path.exists(f"assets/images/zombie{zombie_type_idx+1}.png"):
                            zombie_img[i] = pygame.image.load(f"assets/images/zombie{zombie_type_idx+1}.png")
                        else:
                            zombie_img[i].fill((255, 0, 0) if zombie_type_idx == 0 else 
                                              (150, 0, 150) if zombie_type_idx == 1 else 
                                              (150, 150, 0))
                        
                        zombie_x[i] = random.randint(0, 736)
                        zombie_y[i] = random.randint(50, 150)
                        zombie_x_change[i] = zombie_types[zombie_type_idx]['speed'] * (1 + wave_number * 0.1)
                        zombie_health[i] = zombie_types[zombie_type_idx]['health'] * (1 + wave_number * 0.2)
                        zombie_speed[i] = zombie_types[zombie_type_idx]['speed'] * (1 + wave_number * 0.1)
                        
                        zombies_killed_in_wave += 1
            
            # Only draw zombies that are alive
            if zombie_health[i] > 0:
                zombie(zombie_x[i], zombie_y[i], i)
            
        # Bullet Movement
        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = "ready"
            
        if bullet_state == "fire":
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change
        
        # Update explosions
        update_explosions()
        
        # Update powerups
        update_powerups()
        
        player(player_x, player_y)
        show_ui(text_x, text_y)
    
    pygame.display.update()
    clock.tick(60)


# Move reset_game function to the beginning of the file
def reset_game():
    global player_x, player_y, player_health, score_value, game_over, money
    global zombie_x, zombie_y, zombie_health, zombie_type, zombie_x_change, zombie_speed
    global bullet_state, bullet_y, explosions, powerups, shopping, paused
    global wave_number, zombies_killed_in_wave, show_wave_notification_timer
    global current_weapon, weapons, zombie_img, zombie_y_change
    global num_of_zombies  # Add this to reset the number of zombies
    
    # Reset player
    player_x = 370
    player_y = 480
    player_health = player_max_health
    
    # Reset game state
    game_over = False
    shopping = False
    paused = False
    score_value = 0
    money = 0
    
    # Reset weapons to initial state
    current_weapon = 0
    weapons = [
        {"name": "Pistol", "damage": 1, "cost": 0, "owned": True, "ammo": 50, "max_ammo": 100, "fire_rate": 0.5, "img": weapon_imgs[0]},
        {"name": "Shotgun", "damage": 2, "cost": 50, "owned": False, "ammo": 0, "max_ammo": 50, "fire_rate": 0.8, "img": weapon_imgs[1]},
        {"name": "Rifle", "damage": 3, "cost": 100, "owned": False, "ammo": 0, "max_ammo": 80, "fire_rate": 0.3, "img": weapon_imgs[2]},
        {"name": "Rocket Launcher", "damage": 5, "cost": 200, "owned": False, "ammo": 0, "max_ammo": 20, "fire_rate": 1.2, "img": weapon_imgs[3]}
    ]
    
    # Reset number of zombies to initial value
    num_of_zombies = zombies_per_wave
    
    # Reset zombies
    zombie_x.clear()
    zombie_y.clear()
    zombie_health.clear()
    zombie_type.clear()
    zombie_x_change.clear()
    zombie_y_change.clear()
    zombie_img.clear()
    zombie_speed.clear()
    
    # Initialize zombies for first wave
    for i in range(num_of_zombies):
        zombie_type_idx = random.randint(0, len(zombie_types)-1)
        zombie_type.append(zombie_type_idx)
        
        # Try to load zombie image, otherwise create a colored rectangle
        if os.path.exists(f"assets/images/zombie{zombie_type_idx+1}.png"):
            temp_zombie = pygame.image.load(f"assets/images/zombie{zombie_type_idx+1}.png")
        else:
            temp_zombie = pygame.Surface((64, 64))
            temp_zombie.fill((255, 0, 0) if zombie_type_idx == 0 else 
                            (150, 0, 150) if zombie_type_idx == 1 else 
                            (150, 150, 0))
        
        zombie_img.append(temp_zombie)
        zombie_x.append(random.randint(0, 736))
        zombie_y.append(random.randint(50, 150))
        zombie_x_change.append(zombie_types[zombie_type_idx]['speed'])
        zombie_y_change.append(40)
        zombie_health.append(zombie_types[zombie_type_idx]['health'])
        zombie_speed.append(zombie_types[zombie_type_idx]['speed'])
    
    # Reset bullet
    bullet_state = "ready"
    bullet_y = 480
    
    # Clear effects
    explosions.clear()
    powerups.clear()
    
    # Reset wave
    wave_number = 1
    zombies_killed_in_wave = 0
    show_wave_notification_timer = 180  # Show for 3 seconds
