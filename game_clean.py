"""Clean Game implementation moved to a separate file to recover from a corrupted game.py.

This module contains the actual Game class. `game.py` is a tiny shim that
imports Game from here so we can safely recover and keep history.
"""

import pygame
from training_game.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    COLOR_BLACK,
    LEVEL_TRANSITION_TIME,
    LEVELS,
)
from training_game.player import Player
from training_game.enemy import Enemy
from training_game.level import load_level
from training_game.utils import render_text
from training_game import logger
from training_game.hall_of_fame import add_entry, get_top


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Iron Blitz (MVP)")
        self.clock = pygame.time.Clock()

        self.running = True
        self.state = "RUN"

        self.current_level_index = 0
        self.level_transition_timer = 0.0

        self.walls = []
        self.player = None
        self.enemies = []

        self.score = 0
        self.start_level(self.current_level_index)
        # Name entry state for Hall of Fame
        self.name_buffer = ""

    def start_level(self, index: int) -> None:
        walls, enemy_count, enemy_speed = load_level(index)
        self.walls = walls

        preferred_x = SCREEN_WIDTH // 2
        preferred_y = SCREEN_HEIGHT - 100
        player_w, player_h = 40, 40

        def collides(x: int, y: int) -> bool:
            r = pygame.Rect(x, y, player_w, player_h)
            return any(r.colliderect(w.rect) for w in self.walls)

        sx, sy = preferred_x, preferred_y
        if collides(sx, sy):
            found = False
            step = 40
            for dy in range(0, SCREEN_HEIGHT, step):
                if found:
                    break
                for dx in range(0, SCREEN_WIDTH, step):
                    for ox, oy in ((0, -dy), (dx, -dy), (-dx, -dy)):
                        nx = preferred_x + ox
                        ny = preferred_y + oy
                        nx = max(0, min(SCREEN_WIDTH - player_w, nx))
                        ny = max(0, min(SCREEN_HEIGHT - player_h, ny))
                        if not collides(nx, ny):
                            sx, sy = nx, ny
                            found = True
                            break
                    if found:
                        break

        if self.player is None:
            self.player = Player(sx, sy)
        else:
            self.player.rect.x = sx
            self.player.rect.y = sy
            self.player.bullets.clear()

        self.player.score = getattr(self.player, 'score', 0)

        self.enemies = []
        base_x = 100
        spacing = 60
        for i in range(enemy_count):
            ex = base_x + i * spacing
            ey = 100
            rect = pygame.Rect(ex, ey, 40, 40)
            attempts = 0
            while attempts < 10 and any(rect.colliderect(w.rect) for w in self.walls):
                ey += 40
                rect.y = ey
                attempts += 1
            self.enemies.append(Enemy(ex, ey, speed=enemy_speed))

        self.player.score = self.score
        self.state = 'RUN'

    def _advance_level(self) -> None:
        self.current_level_index += 1
        if self.current_level_index >= len(LEVELS):
            self.state = 'CAMPAIGN_COMPLETE'
            self.score = self.player.score
            logger.info('Campaign complete. Final score: %s', self.score)
        else:
            self.score = self.player.score
            self.start_level(self.current_level_index)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # If entering name after game over, capture text keys first
                if self.state == 'ENTER_NAME':
                    if event.key == pygame.K_RETURN:
                        name = self.name_buffer.strip() or 'Player'
                        add_entry(name, self.player.score)
                        logger.info('Saved high score for %s: %s', name, self.player.score)
                        self.name_buffer = ""
                        # After saving, show high scores screen briefly
                        self.state = 'SHOW_HIGHSCORES'
                    elif event.key == pygame.K_BACKSPACE:
                        self.name_buffer = self.name_buffer[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        # Cancel name entry and restart current level
                        self.name_buffer = ""
                        self.start_level(self.current_level_index)
                        self.state = 'RUN'
                    elif event.key == pygame.K_r:
                        # Restart without saving
                        self.name_buffer = ""
                        self.start_level(self.current_level_index)
                        self.state = 'RUN'
                    else:
                        # Only accept printable characters
                        ch = event.unicode
                        if ch and len(self.name_buffer) < 20 and ch.isprintable():
                            self.name_buffer += ch
                else:
                    if event.key == pygame.K_p:
                        self.state = 'PAUSE' if self.state == 'RUN' else 'RUN'
                    elif event.key == pygame.K_r:
                        # Restart current level
                        self.start_level(self.current_level_index)
                    elif event.key == pygame.K_h:
                        # Show Hall of Fame anytime with H
                        self.state = 'SHOW_HIGHSCORES'

        keys = pygame.key.get_pressed()
        if self.state == 'RUN':
            self.player.handle_input(keys, self.walls)
            if keys[pygame.K_SPACE]:
                self.player.shoot()
        elif self.state == 'VICTORY':
            if keys[pygame.K_n] or keys[pygame.K_RETURN]:
                self._advance_level()
        elif self.state == 'SHOW_HIGHSCORES':
            # Any key returns to main menu / restart current level
            if any(keys):
                self.start_level(0)
                self.state = 'RUN'

    def update(self) -> None:
        if self.state == 'RUN':
            self.player.update(self.walls)
            for e in list(self.enemies):
                e.update(self.walls)

            for b in list(self.player.bullets):
                for e in list(self.enemies):
                    if b.rect.colliderect(e.rect):
                        if b in self.player.bullets:
                            self.player.bullets.remove(b)
                        if e in self.enemies:
                            self.enemies.remove(e)
                            self.player.score += 100
                        break

            for e in list(self.enemies):
                for b in list(e.bullets):
                    if b.rect.colliderect(self.player.rect):
                        self.player.lives -= 1
                        try:
                            e.bullets.remove(b)
                        except ValueError:
                            pass
                        break

            if self.player.lives <= 0:
                # Prompt for name and add to hall of fame
                self.state = 'ENTER_NAME'

            if not self.enemies:
                self.state = 'VICTORY'
                self.level_transition_timer = 0.0

        elif self.state == 'VICTORY':
            self.level_transition_timer += 1.0 / FPS
            if self.level_transition_timer >= LEVEL_TRANSITION_TIME:
                self._advance_level()
        elif self.state == 'SHOW_HIGHSCORES':
            # nothing to update, just display
            pass

    def render(self) -> None:
        self.screen.fill(COLOR_BLACK)
        if self.player:
            self.player.render(self.screen)
        for e in list(self.enemies):
            e.render(self.screen)
        for w in list(self.walls):
            w.render(self.screen)

        render_text(self.screen, f"Score: {self.player.score}", (10, 10))
        render_text(self.screen, f"Lives: {self.player.lives}", (10, 40))

        if self.state == 'GAME_OVER':
            render_text(self.screen, 'GAME OVER', (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2), font_size=48, color=(255, 0, 0))
        elif self.state == 'ENTER_NAME':
            render_text(self.screen, 'GAME OVER', (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 60), font_size=48, color=(255, 0, 0))
            render_text(self.screen, 'Enter your name and press Enter:', (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2), font_size=24)
            render_text(self.screen, self.name_buffer or '_', (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 40), font_size=28)
        elif self.state == 'SHOW_HIGHSCORES':
            render_text(self.screen, 'Hall of Fame - Top Scores', (SCREEN_WIDTH // 2 - 200, 40), font_size=36, color=(255, 215, 0))
            top = get_top(10)
            y = 100
            for i, e in enumerate(top, start=1):
                render_text(self.screen, f"{i}. {e.name} - {e.score}", (SCREEN_WIDTH // 2 - 160, y), font_size=24)
                y += 30
        elif self.state == 'VICTORY':
            render_text(self.screen, f"Victory! Stage {self.current_level_index + 1} Complete", (SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2), font_size=36, color=(0, 255, 0))
            render_text(self.screen, 'Press N or Enter to continue', (SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 50), font_size=24)
        elif self.state == 'CAMPAIGN_COMPLETE':
            render_text(self.screen, f"Campaign Complete! Final Score: {self.player.score}", (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2), font_size=36, color=(255, 215, 0))

        pygame.display.flip()

    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

        pygame.quit()
