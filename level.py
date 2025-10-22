"""
level.py: Defines the map layout and generates walls.
"""

import pygame
from training_game.wall import Wall
from training_game.settings import TILE_SIZE, LEVELS, ENEMY_BASE_SPEED


# LEVEL SYSTEM: define simple level layouts and parameters
def _layout_from_ascii(ascii_map):
    walls = []
    for row_index, row in enumerate(ascii_map):
        for col_index, ch in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            if ch == '1':
                walls.append(Wall(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE), destructible=False))
            elif ch == '2':
                walls.append(Wall(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE), destructible=True, health=3))
    return walls


def load_level(index):
    """Return (walls, enemy_count, enemy_speed) for the requested level index.
    If index is out of range, raises IndexError.
    """
    # Simple predefined ASCII maps (rows x cols consistent with TILE_SIZE)
    # '1' = indestructible wall, '2' = destructible wall, '0' = empty
    ascii_levels = [
        [
            "11111111111111111111",
            "10000000000000000001",
            "10002000020000002001",
            "10000000000000000001",
            "10000000000000000001",
            "10000000000000000001",
            "10000000000000000001",
            "10000000000000000001",
            "10000000000000000001",
            "10000000000000000001",
            "10000000000000000001",
            "10000000000000000001",
            "10000000000000000001",
            "10000000000000000001",
            "11111111111111111111",
        ],
        [
            "11111111111111111111",
            "10000000200000000001",
            "10001110001110001101",
            "10100000000000000101",
            "10000000200002000001",
            "10001110001110001101",
            "10100000000000000101",
            "10000000000000000001",
            "10000000000000000001",
            "10000000000000000001",
            "10000000000000000001",
            "10000000000000000001",
            "10000000000000000001",
            "10000000000000000001",
            "11111111111111111111",
        ],
        [
            "11111111111111111111",
            "10022002200220022001",
            "10220022002200220021",
            "10022002200220022001",
            "10220022002200220021",
            "10022002200220022001",
            "10220022002200220021",
            "10000000000000000001",
            "10000000000000000001",
            "10000000000000000001",
            "10000000000000000001",
            "10000000000000000001",
            "10000000000000000001",
            "10000000000000000001",
            "11111111111111111111",
        ],
    ]

    if index < 0 or index >= len(ascii_levels):
        raise IndexError("Level index out of range")

    walls = _layout_from_ascii(ascii_levels[index])

    # enemy counts per level (level 1 -> 3 enemies, +1 per level)
    enemy_count = 3 + index
    # increase enemy speed by 10% per level (index 0 is base)
    enemy_speed = ENEMY_BASE_SPEED * (1 + 0.1 * index)

    return walls, enemy_count, enemy_speed


def build_map():
    """
    Creates a simple map layout using Wall objects.
    Returns a list of Wall objects.
    """
    walls = []

    # Example layout (1 = indestructible wall, 2 = destructible wall, 0 = empty space)
    layout = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 2, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 1],
        [1, 0, 2, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    for row_index, row in enumerate(layout):
        for col_index, cell in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            if cell == 1:
                walls.append(Wall(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE), destructible=False))
            elif cell == 2:
                walls.append(Wall(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE), destructible=True, health=3))

    return walls