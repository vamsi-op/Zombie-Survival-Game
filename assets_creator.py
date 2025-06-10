import pygame
import os
import math
import random

# Initialize pygame
pygame.init()

# Create directories for assets if they don't exist
os.makedirs("assets/images", exist_ok=True)
os.makedirs("assets/sounds", exist_ok=True)

# Create background
def create_background():
    bg = pygame.Surface((800, 600))
    # Create a dark gradient background
    for y in range(600):
        color = (max(0, 50 - y//10), max(0, 10 - y//30), max(0, 30 - y//20))
        pygame.draw.line(bg, color, (0, y), (800, y))
    
    # Add some fog/mist effect
    for _ in range(100):
        x = random.randint(0, 800)
        y = random.randint(0, 600)
        radius = random.randint(20, 100)
        s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (200, 200, 200, 10), (radius, radius), radius)
        bg.blit(s, (x-radius, y-radius))
    
    pygame.image.save(bg, "assets/images/background.png")
    print("Background created")

# Create player image
def create_player():
    player_surf = pygame.Surface((64, 64), pygame.SRCALPHA)
    
    # Body
    pygame.draw.rect(player_surf, (0, 100, 200), (16, 24, 32, 32))
    
    # Head
    pygame.draw.circle(player_surf, (255, 200, 150), (32, 16), 12)
    
    # Eyes
    pygame.draw.circle(player_surf, (255, 255, 255), (28, 14), 4)
    pygame.draw.circle(player_surf, (255, 255, 255), (36, 14), 4)
    pygame.draw.circle(player_surf, (0, 0, 0), (28, 14), 2)
    pygame.draw.circle(player_surf, (0, 0, 0), (36, 14), 2)
    
    pygame.image.save(player_surf, "assets/images/player.png")
    print("Player created")

# Create zombie images
def create_zombies():
    for i in range(1, 4):
        zombie_surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        
        # Body color based on zombie type
        if i == 1:  # Regular zombie
            body_color = (0, 150, 0)
            head_color = (100, 255, 100)
        elif i == 2:  # Toxic zombie
            body_color = (150, 0, 150)
            head_color = (200, 100, 200)
        else:  # Elite zombie
            body_color = (150, 150, 0)
            head_color = (200, 200, 100)
        
        # Body
        pygame.draw.rect(zombie_surf, body_color, (16, 24, 32, 32))
        
        # Head
        pygame.draw.circle(zombie_surf, head_color, (32, 16), 12)
        
        # Eyes (red for all zombies)
        pygame.draw.circle(zombie_surf, (255, 255, 255), (28, 14), 4)
        pygame.draw.circle(zombie_surf, (255, 255, 255), (36, 14), 4)
        pygame.draw.circle(zombie_surf, (255, 0, 0), (28, 14), 2)
        pygame.draw.circle(zombie_surf, (255, 0, 0), (36, 14), 2)
        
        pygame.image.save(zombie_surf, f"assets/images/zombie{i}.png")
    print("Zombies created")

# Create weapon images
def create_weapons():
    weapon_sizes = [(16, 8), (20, 10), (24, 12), (30, 16)]
    weapon_colors = [(200, 200, 200), (150, 75, 0), (100, 100, 100), (50, 50, 50)]
    
    for i in range(4):
        weapon_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        w, h = weapon_sizes[i]
        
        # Main body of weapon
        pygame.draw.rect(weapon_surf, weapon_colors[i], (0, 12, w, h))
        
        # Handle for pistol, shotgun, rifle
        if i < 3:
            pygame.draw.rect(weapon_surf, (50, 30, 0), (w-8, 12+h, 6, 10))
        
        pygame.image.save(weapon_surf, f"assets/images/weapon{i+1}.png")
    print("Weapons created")

# Create bullet images
def create_bullets():
    bullet_colors = [(255, 255, 0), (255, 100, 0), (0, 100, 255), (255, 0, 0)]
    bullet_sizes = [(8, 8), (10, 10), (12, 12), (16, 16)]
    
    for i in range(4):
        bullet_surf = pygame.Surface((16, 16), pygame.SRCALPHA)
        w, h = bullet_sizes[i]
        
        if i < 3:  # Regular bullets
            pygame.draw.circle(bullet_surf, bullet_colors[i], (8, 8), w//2)
        else:  # Rocket
            pygame.draw.rect(bullet_surf, (100, 100, 100), (4, 2, 8, 12))
            pygame.draw.polygon(bullet_surf, (255, 0, 0), [(8, 2), (12, 6), (4, 6)])
            pygame.draw.polygon(bullet_surf, (255, 165, 0), [(4, 14), (12, 14), (8, 16)])
        
        pygame.image.save(bullet_surf, f"assets/images/bullet{i+1}.png")
    print("Bullets created")

# Create explosion animation frames
def create_explosions():
    for i in range(1, 6):
        exp_surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        size = i * 10
        
        # Yellow center
        pygame.draw.circle(exp_surf, (255, 255, 0), (32, 32), size)
        
        # Orange middle
        pygame.draw.circle(exp_surf, (255, 100, 0), (32, 32), size-4)
        
        # Red outer
        pygame.draw.circle(exp_surf, (255, 0, 0), (32, 32), size-8)
        
        pygame.image.save(exp_surf, f"assets/images/explosion{i}.png")
    print("Explosions created")

# Create health pack
def create_health_pack():
    health_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    
    # White background
    pygame.draw.rect(health_surf, (255, 255, 255), (8, 2, 16, 28))
    pygame.draw.rect(health_surf, (255, 255, 255), (2, 8, 28, 16))
    
    # Red cross
    pygame.draw.rect(health_surf, (255, 0, 0), (10, 4, 12, 24))
    pygame.draw.rect(health_surf, (255, 0, 0), (4, 10, 24, 12))
    
    pygame.image.save(health_surf, "assets/images/health.png")
    print("Health pack created")

# Create ammo pack
def create_ammo_pack():
    ammo_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    
    # Box
    pygame.draw.rect(ammo_surf, (200, 200, 0), (8, 4, 16, 24))
    pygame.draw.rect(ammo_surf, (100, 100, 0), (12, 8, 8, 16))
    
    # Bullets
    for i in range(3):
        pygame.draw.rect(ammo_surf, (255, 200, 0), (10, 6 + i*8, 12, 4))
    
    pygame.image.save(ammo_surf, "assets/images/ammo.png")
    print("Ammo pack created")

# Generate sound effects
def create_sound_effects():
    # We can't actually generate sound files programmatically with pygame.mixer.Sound
    # Instead, let's create empty files as placeholders
    import wave
    import struct
    import array
    
    for sound_name in ["shoot", "explosion", "hit", "powerup", "gameover", "purchase", "background"]:
        # Create a simple WAV file with a beep sound
        with wave.open(f"assets/sounds/{sound_name}.wav", 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes per sample
            wav_file.setframerate(44100)  # 44.1kHz
            
            # Create a short beep sound (0.2 seconds)
            frequency = 440  # A4 note
            if sound_name == "shoot":
                frequency = 880  # Higher pitch for shoot
            elif sound_name == "explosion":
                frequency = 220  # Lower pitch for explosion
            elif sound_name == "hit":
                frequency = 660  # Medium-high for hit
            elif sound_name == "powerup":
                frequency = 1320  # Very high for powerup
            elif sound_name == "gameover":
                frequency = 110  # Very low for game over
            elif sound_name == "purchase":
                frequency = 550  # Medium for purchase
            elif sound_name == "background":
                frequency = 330  # Background music
                
            duration = 0.2  # seconds
            samples = int(44100 * duration)
            audio_data = array.array('h')
            
            for i in range(samples):
                # Simple sine wave
                value = int(32767 * 0.5 * math.sin(2 * math.pi * frequency * i / 44100))
                audio_data.append(value)
                
            wav_file.writeframes(audio_data.tobytes())
    
    print("Sound effects created with beep sounds")

if __name__ == "__main__":
    import random
    
    print("Creating game assets...")
    
    try:
        create_background()
        create_player()
        create_zombies()
        create_weapons()
        create_bullets()
        create_explosions()
        create_health_pack()
        create_ammo_pack()
        create_sound_effects()
        
        print("All assets created successfully!")
    except Exception as e:
        print(f"Error creating assets: {e}")
