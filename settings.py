"""
settings.py: Contains constants and configurations for the game.
"""

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Tile size
TILE_SIZE = 40

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)

# Speeds
PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 2

# Game settings
FPS = 60
ENEMY_COUNT = 5
PLAYER_LIVES = 3
POINTS_PER_ENEMY = 100

# Random seed for determinism
RANDOM_SEED = 42