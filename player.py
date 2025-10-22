"""
player.py: Defines the Player class for movement, shooting, and collision handling.
"""

import pygame
from settings import PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_LIVES
from bullet import Bullet

class Player:
    """
    Represents the player-controlled tank.
    """
    def __init__(self, x, y):
        """
        Initialize the player.
        :param x: Initial x-coordinate of the player.
        :param y: Initial y-coordinate of the player.
        """
        self.rect = pygame.Rect(x, y, 40, 40)  # Player size is 40x40
        self.lives = PLAYER_LIVES
        self.score = 0
        self.bullets = []
        self.shoot_cooldown = 0

    def handle_input(self, keys, walls):
        """
        Handle player input for movement, considering wall collisions.
        :param keys: The keys currently pressed.
        :param walls: List of wall objects to check for collisions.
        """
        dx, dy = 0, 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = PLAYER_SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = PLAYER_SPEED

        if dx != 0 or dy != 0:
            print(f"Player trying to move: dx={dx}, dy={dy}, walls count={len(walls)}")

        # Check for collisions before moving
        new_rect = self.rect.move(dx, 0)
        collision_x = any(new_rect.colliderect(wall.rect) for wall in walls)
        if not collision_x:
            self.rect.x = new_rect.x
        else:
            print(f"Player blocked in X direction at {self.rect.topleft}")

        new_rect = self.rect.move(0, dy)
        collision_y = any(new_rect.colliderect(wall.rect) for wall in walls)
        if not collision_y:
            self.rect.y = new_rect.y
        else:
            print(f"Player blocked in Y direction at {self.rect.topleft}")

    def shoot(self):
        """
        Shoot a bullet if not on cooldown.
        """
        if self.shoot_cooldown == 0:
            bullet = Bullet(self.rect.centerx, self.rect.top, (0, -1))  # Shoot upwards
            self.bullets.append(bullet)
            print(f"Player fired a bullet at {self.rect.topleft}. Total bullets: {len(self.bullets)}")
            self.shoot_cooldown = 20  # Cooldown in frames

    def update(self, walls):
        """
        Update the player state.
        :param walls: List of wall objects to check for bullet collisions.
        """
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # Update bullets and collect walls to remove
        walls_to_remove = []
        for bullet in self.bullets[:]:
            result = bullet.update(walls)
            should_remove_bullet = result[0] if isinstance(result, tuple) else result
            wall_to_remove = result[1] if isinstance(result, tuple) and len(result) > 1 else None
            
            if wall_to_remove and wall_to_remove not in walls_to_remove:
                walls_to_remove.append(wall_to_remove)
            
            is_off = bullet.is_off_screen()
            if should_remove_bullet or is_off:
                print(f"Player bullet at {bullet.rect.topleft} removed. Collision: {should_remove_bullet}, Off-screen: {is_off}")
                self.bullets.remove(bullet)
        
        # Remove destroyed walls
        for wall in walls_to_remove:
            if wall in walls:
                walls.remove(wall)

    def render(self, surface):
        """
        Render the player and its bullets.
        :param surface: The surface to draw on.
        """
        pygame.draw.rect(surface, (0, 255, 0), self.rect)  # Green player
        for bullet in self.bullets:
            bullet.render(surface)