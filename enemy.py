"""
enemy.py: Defines the Enemy class with simple random movement and anti-stuck logic.
"""

import pygame
import random
from training_game.settings import ENEMY_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, RANDOM_SEED
from training_game.enemy_bullet import EnemyBullet

random.seed(RANDOM_SEED)

class Enemy:
    """
    Represents an enemy tank with simple random movement.
    """
    def __init__(self, x, y):
        """
        Initialize the enemy.
        :param x: Initial x-coordinate of the enemy.
        :param y: Initial y-coordinate of the enemy.
        """
        self.rect = pygame.Rect(x, y, 40, 40)  # Enemy size is 40x40
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.stuck_counter = 0
        self.bullets = []
        self.shoot_cooldown = random.randint(60, 120)  # Random cooldown in frames

    def update(self, walls):
        """
        Update the enemy's position and handle random movement.
        :param walls: List of wall objects to check for collisions.
        """
        # Move the enemy
        self.rect.x += self.direction[0] * ENEMY_SPEED
        self.rect.y += self.direction[1] * ENEMY_SPEED

        # Check for collisions with walls
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.x -= self.direction[0] * ENEMY_SPEED
                self.rect.y -= self.direction[1] * ENEMY_SPEED
                self.stuck_counter += 1
                break
        else:
            self.stuck_counter = 0

        # Change direction if stuck for too long
        if self.stuck_counter > 30:
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.stuck_counter = 0

        # Clamp position to screen bounds
        self.rect.x = max(0, min(SCREEN_WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(SCREEN_HEIGHT - self.rect.height, self.rect.y))

        # Handle shooting
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        else:
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery, (0, 1))  # Shoot downwards
            self.bullets.append(bullet)
            # Debug log for bullet creation
            print(f"Enemy at {self.rect.topleft} fired a bullet.")
            self.shoot_cooldown = random.randint(60, 120)  # Reset cooldown

        # Update bullets
        walls_to_remove = []
        for bullet in self.bullets[:]:
            # Debug log for bullet removal
            result = bullet.update(walls)
            should_remove_bullet = result[0] if isinstance(result, tuple) else result
            wall_to_remove = result[1] if isinstance(result, tuple) and len(result) > 1 else None
            
            if wall_to_remove and wall_to_remove not in walls_to_remove:
                walls_to_remove.append(wall_to_remove)
            
            if should_remove_bullet or bullet.is_off_screen():
                print(f"Bullet at {bullet.rect.topleft} removed.")
                self.bullets.remove(bullet)
        
        # Remove destroyed walls
        for wall in walls_to_remove:
            if wall in walls:
                walls.remove(wall)

    def render(self, surface):
        """
        Render the enemy and its bullets on the screen.
        :param surface: The surface to draw the enemy and bullets on.
        """
        pygame.draw.rect(surface, (255, 0, 0), self.rect)  # Red enemy
        for bullet in self.bullets:
            bullet.render(surface)