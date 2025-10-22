"""
game.py: Defines the Game class for managing the game loop, states, and rendering.
"""

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BLACK
from player import Player
from enemy import Enemy
from level import build_map
from utils import render_text

class Game:
    """
    Manages the game loop, states, and rendering.
    """
    def __init__(self):
        """
        Initialize the game.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Iron Blitz (MVP)")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "RUN"

        # Game objects
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.enemies = [Enemy(100 + i * 60, 100) for i in range(5)]
        self.walls = build_map()

    def handle_events(self):
        """
        Handle user input events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.state = "PAUSE" if self.state == "RUN" else "RUN"
                elif event.key == pygame.K_r:
                    self.__init__()  # Restart the game

        keys = pygame.key.get_pressed()
        if self.state == "RUN":
            self.player.handle_input(keys, self.walls)
            if keys[pygame.K_SPACE]:
                self.player.shoot()

    def update(self):
        """
        Update the game state.
        """
        if self.state == "RUN":
            self.player.update(self.walls)
            for enemy in self.enemies:
                enemy.update(self.walls)

            # Check bullet collisions with enemies
            for bullet in self.player.bullets[:]:
                if bullet not in self.player.bullets:
                    continue  # Skip if the bullet was already removed
                for enemy in self.enemies[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        if bullet in self.player.bullets:
                            self.player.bullets.remove(bullet)
                        self.enemies.remove(enemy)
                        self.player.score += 100
                        break

            # Update enemy bullets
            for enemy in self.enemies:
                for bullet in enemy.bullets:
                    if bullet.rect.colliderect(self.player.rect):
                        self.player.lives -= 1  # Player loses a life
                        enemy.bullets.remove(bullet)
                        break

            # Check if player is out of lives
            if self.player.lives <= 0:
                self.state = "GAME_OVER"

    def render(self):
        """
        Render the game objects and HUD.
        """
        self.screen.fill(COLOR_BLACK)

        # Render game objects
        self.player.render(self.screen)
        for enemy in self.enemies:
            enemy.render(self.screen)
        for wall in self.walls:
            wall.render(self.screen)

        # Render HUD
        render_text(self.screen, f"Score: {self.player.score}", (10, 10))
        render_text(self.screen, f"Lives: {self.player.lives}", (10, 40))

        if self.state == "GAME_OVER":
            render_text(self.screen, "GAME OVER", (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2), font_size=48, color=(255, 0, 0))

        pygame.display.flip()

    def run(self):
        """
        Run the game loop.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

        pygame.quit()