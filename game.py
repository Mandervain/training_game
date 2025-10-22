"""
game.py: Defines the Game class for managing the game loop, states, and rendering.
"""

import pygame
from training_game.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BLACK
from training_game.player import Player
from training_game.enemy import Enemy
from training_game.level import build_map
from training_game.utils import render_text

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
        # Build map first so we can choose a spawn location that isn't
        # inside a wall.
        self.walls = build_map()

        # Find a spawn position near bottom center that doesn't collide
        # with any wall. Start at preferred location and try shifting up
        # and sideways until a free spot is found.
        preferred_x = SCREEN_WIDTH // 2
        preferred_y = SCREEN_HEIGHT - 100
        player_w, player_h = 40, 40

        def collides_with_walls(x, y):
            r = pygame.Rect(x, y, player_w, player_h)
            return any(r.colliderect(w.rect) for w in self.walls)

        spawn_x, spawn_y = preferred_x, preferred_y
        if collides_with_walls(spawn_x, spawn_y):
            # try a small spiral search: move up in steps of TILE_SIZE,
            # then sweep left/right
            step = 40
            found = False
            for dy in range(0, SCREEN_HEIGHT, step):
                for dx in range(0, SCREEN_WIDTH, step):
                    for sx, sy in ((0, -dy), (dx, -dy), (-dx, -dy)):
                        x = preferred_x + sx
                        y = preferred_y + sy
                        # clamp
                        x = max(0, min(SCREEN_WIDTH - player_w, x))
                        y = max(0, min(SCREEN_HEIGHT - player_h, y))
                        if not collides_with_walls(x, y):
                            spawn_x, spawn_y = x, y
                            found = True
                            break
                    if found:
                        break
                if found:
                    break

        self.player = Player(spawn_x, spawn_y)
        self.enemies = [Enemy(100 + i * 60, 100) for i in range(5)]

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
            # Check bullet collisions with enemies (iterate over a copy so we
            # can safely remove bullets/enemies during iteration)
            for bullet in list(self.player.bullets):
                for enemy in list(self.enemies):
                    if bullet.rect.colliderect(enemy.rect):
                        # Remove bullet and enemy if still present
                        if bullet in self.player.bullets:
                            self.player.bullets.remove(bullet)
                        if enemy in self.enemies:
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