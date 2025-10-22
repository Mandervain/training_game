"""
enemy_bullet.py: Defines the EnemyBullet class for handling enemy bullet movement and collisions.
"""

import pygame
from training_game.settings import BULLET_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT
from training_game import logger

class EnemyBullet:
    """
    Represents a bullet fired by an enemy.
    """
    def __init__(self, x, y, direction):
        """
        Initialize the enemy bullet.
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
                    logger.debug("Enemy bullet hit destructible wall at %s. Wall health: %s", wall.rect.topleft, wall.health)
                    if wall.take_damage():
                        logger.info("Wall at %s destroyed.", wall.rect.topleft)
                        return (True, wall)  # Indicate bullet and wall should be removed
                else:
                    logger.debug("Enemy bullet hit indestructible wall at %s.", wall.rect.topleft)
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
        pygame.draw.rect(surface, (255, 0, 0), self.rect)  # Red bullet