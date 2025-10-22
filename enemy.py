"""
enemy.py: Defines the Enemy class with simple random movement and anti-stuck logic.
"""

import pygame
import random
import training_game.settings as settings
from training_game.enemy_bullet import EnemyBullet
from training_game import logger
random.seed(settings.RANDOM_SEED)


class Enemy:
    """Represents an enemy tank with simple random movement and shooting."""

    def __init__(self, x, y, speed=None):
        self.rect = pygame.Rect(x, y, 40, 40)  # Enemy size is 40x40
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.stuck_counter = 0
        self.bullets = []
        self.shoot_cooldown = random.randint(60, 120)  # Random cooldown in frames
        # per-enemy movement speed
        self.speed = speed if speed is not None else settings.ENEMY_BASE_SPEED

    def update(self, walls):
        """Update movement, handle collisions, shooting, and update bullets.

        :param walls: List of Wall objects for collision checks.
        """
        # Move the enemy
        self.rect.x += int(self.direction[0] * self.speed)
        self.rect.y += int(self.direction[1] * self.speed)

        # Check for collisions with walls
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                # undo movement
                self.rect.x -= int(self.direction[0] * self.speed)
                self.rect.y -= int(self.direction[1] * self.speed)
                self.stuck_counter += 1
                break
        else:
            self.stuck_counter = 0

        # Change direction if stuck for too long
        if self.stuck_counter > 30:
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.stuck_counter = 0

        # Clamp to screen bounds
        self.rect.x = max(0, min(settings.SCREEN_WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(settings.SCREEN_HEIGHT - self.rect.height, self.rect.y))

        # Handle shooting
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        else:
            # simple downwards shot
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery, (0, 1))
            self.bullets.append(bullet)
            logger.info("Enemy at %s fired a bullet.", self.rect.topleft)
            self.shoot_cooldown = random.randint(60, 120)

        # Update bullets and collect walls to remove
        walls_to_remove = []
        for bullet in self.bullets[:]:
            result = bullet.update(walls)
            # result may be a bool or (bool, wall)
            should_remove = result[0] if isinstance(result, tuple) else result
            wall_to_remove = result[1] if isinstance(result, tuple) and len(result) > 1 else None

            if wall_to_remove and wall_to_remove not in walls_to_remove:
                walls_to_remove.append(wall_to_remove)

            if should_remove or bullet.is_off_screen():
                logger.debug("Bullet at %s removed.", bullet.rect.topleft)
                try:
                    self.bullets.remove(bullet)
                except ValueError:
                    pass

        # Remove destroyed walls
        for wall in walls_to_remove:
            if wall in walls:
                walls.remove(wall)

    def render(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)  # Red enemy
        for bullet in self.bullets:
            bullet.render(surface)