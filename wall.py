"""
wall.py: Defines the Wall class for static, indestructible blocks.
"""

import pygame

class Wall:
    """
    Represents a wall block, which can be destructible or indestructible.
    """
    def __init__(self, rect, destructible=False, health=1):
        """
        Initialize the wall with a pygame.Rect object.
        :param rect: pygame.Rect defining the wall's position and size.
        :param destructible: Boolean indicating if the wall is destructible.
        :param health: Health of the wall (only relevant if destructible).
        """
        self.rect = rect
        self.destructible = destructible
        self.health = health

    def take_damage(self):
        """
        Reduce the wall's health if it is destructible.
        :return: True if the wall is destroyed, False otherwise.
        """
        if self.destructible:
            self.health -= 1
            print(f"Wall at {self.rect.topleft} took damage. Remaining health: {self.health}")
            if self.health <= 0:
                print(f"Wall at {self.rect.topleft} destroyed.")
                return True
        return False

    def render(self, surface):
        """
        Render the wall as a filled rectangle.
        :param surface: The surface to draw the wall on.
        """
        color = (150, 75, 0) if self.destructible else (100, 100, 100)  # Brown for destructible walls
        pygame.draw.rect(surface, color, self.rect)