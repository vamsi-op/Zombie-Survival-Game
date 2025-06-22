# Zombie Apocalypse: Survival

A zombie shooter game with weapon upgrades, created with Pygame.

## Setup

1. Clone the Repository

```bash
git clone https://github.com/vamsi-op/zombie-survival-game.git
cd zombie-survival-game
```

2. Create a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

3. Install requirements:
```
pip install -r requirements.txt
```

4. Run the game:
```
python zombie.py
```

## Features

- Multiple zombie types with different health, speed, and damage
- Weapon upgrade system with 4 different weapons
- Wave-based gameplay that gets progressively harder
- Health and ammo powerups
- Visual effects including explosions
- Sound effects for actions
- Shop system to buy weapons and ammo
- Fullscreen support

## Controls

- Move: LEFT/RIGHT arrow keys
- Shoot: SPACEBAR
- Open Shop: B key
- Pause Game: P key
- Toggle Fullscreen: F11 key
- Select/Buy Weapons: 1-4 keys (in shop)
- Buy Ammo: A key (in shop)
- Exit Shop: ESC key
- Restart (after game over): R key

## Asset Generation

The game includes an asset generator script that creates custom graphics and sound placeholders:

```
python assets_creator.py
```

This will create all necessary images and sound files in the assets directory.

## Game Structure

- `zombie.py`: Main game file
- `assets_creator.py`: Script to generate game assets
- `requirements.txt`: Required Python packages
- `assets/`: Directory containing game resources
  - `images/`: Game graphics
  - `sounds/`: Sound effects

## Credits

Created as a learning project for game development with Pygame and part of submission of #AmazonQDevCLI.
