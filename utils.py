"""
utils.py: Contains utility functions for the game.
"""

import pygame

# Simple cache for pygame.Font objects keyed by size to avoid creating a
# new Font instance every frame (expensive).
_FONT_CACHE = {}

def clamp(value, min_value, max_value):
    """
    Clamp a value between a minimum and maximum.
    :param value: The value to clamp.
    :param min_value: The minimum value.
    :param max_value: The maximum value.
    :return: The clamped value.
    """
    return max(min_value, min(value, max_value))

def render_text(surface, text, position, font_size=24, color=(255, 255, 255)):
    """
    Render text on the given surface.
    :param surface: The surface to render the text on.
    :param text: The text to render.
    :param position: Tuple (x, y) for the text position.
    :param font_size: Font size of the text.
    :param color: Color of the text.
    """
    # Reuse font instances where possible to improve performance
    font = _FONT_CACHE.get(font_size)
    if font is None:
        font = pygame.font.Font(None, font_size)
        _FONT_CACHE[font_size] = font

    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)