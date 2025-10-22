"""
bullet.py: Defines the Bullet class for handling movement and collisions.
"""

import pygame
from training_game.settings import BULLET_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT

class Bullet:
    """
    Represents a bullet fired by the player.
    """
    def __init__(self, x, y, direction):
        """
        Initialize the bullet.
        :param x: Initial x-coordinate of the bullet.
        :param y: Initial y-coordinate of the bullet.
        :param direction: Direction of the bullet (tuple dx, dy).
        """
        self.rect = pygame.Rect(x, y, 5, 5)  # Bullet size is 5x5
        self.direction = direction

    def update(self, walls):
        """
        Update the bullet's position and check for collisions with walls.
        :param walls: List of wall objects to check for collisions.
        :return: Tuple (should_remove_bullet, wall_to_remove or None)
        """
        self.rect.x += self.direction[0] * BULLET_SPEED
        self.rect.y += self.direction[1] * BULLET_SPEED

        # Check for collisions with walls
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if wall.destructible:
                    print(f"Bullet hit destructible wall at {wall.rect.topleft}. Wall health: {wall.health}")
                    if wall.take_damage():
                        print(f"Wall at {wall.rect.topleft} destroyed.")
                        return (True, wall)  # Indicate bullet and wall should be removed
                else:
                    print(f"Bullet hit indestructible wall at {wall.rect.topleft}.")
                return (True, None)  # Indicate that the bullet should be removed
        return (False, None)

    def is_off_screen(self):
        """
        Check if the bullet is off the screen.
        :return: True if the bullet is outside the screen bounds, False otherwise.
        """
        return (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
                self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT)

    def render(self, surface):
        """
        Render the bullet on the screen.
        :param surface: The surface to draw the bullet on.
        """
        pygame.draw.rect(surface, (255, 255, 0), self.rect)  # Yellow bullet