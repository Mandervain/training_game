# Iron Blitz (MVP)

## Game Description
Iron Blitz is a top-down 2D tank game inspired by classic arcade games. The goal is to destroy all enemy tanks while avoiding collisions and managing your lives. The game features simple graphics and mechanics, making it easy to play and extend.

### Controls
- **Movement**: Use `W`, `A`, `S`, `D` or arrow keys.
- **Shoot**: Press `Space`.
- **Pause**: Press `P`.
- **Restart**: Press `R`.

### Objective
- Destroy all enemy tanks to earn points.
- Avoid losing all your lives.
- Each enemy destroyed gives you +100 points.

## How to Run
1. Install the required library:
   ```
   pip install pygame
   ```
2. Run the game:
   ```
   python3 main.py
   ```

## Project Structure
```
Iron Blitz (MVP)
├── settings.py   # Game constants and configurations
├── level.py      # Map layout and wall generation
├── wall.py       # Wall class for static blocks
├── utils.py      # Utility functions (e.g., render_text, clamp)
├── bullet.py     # Bullet class for movement and collisions
├── player.py     # Player class for movement, shooting, and collisions
├── enemy.py      # Enemy class with random movement
├── game.py       # Game class for the game loop and rendering
├── main.py       # Entry point for the game
└── README.md     # Project documentation
```

## Roadmap
### Phase 2
- Add shooting enemies.
- Introduce destructible walls.
- Implement sound effects using `pygame.mixer`.
- Create a start menu.

### Phase 3
- Add power-ups (e.g., health, speed boost).
- Design multiple maps.
- Implement simple pathfinding AI (e.g., grid-based BFS).

## Mini-Presentation
### 1. Inspiration + Goal
Inspired by classic arcade tank games, the goal was to create a simple yet engaging MVP within a limited time.

### 2. Requirements and Constraints
- Python 3.10+ and Pygame.
- Focus on simplicity and expandability.
- No external assets.

### 3. Architecture and Structure
The project is modular, with separate files for each game component (e.g., player, enemy, bullet).

### 4. Demo and Testing
- Movement, shooting, and collisions work as expected.
- Game states (RUN, PAUSE, GAME_OVER) are functional.
- Restart and scoring are implemented.

### 5. Roadmap
- Phase 2: Shooting enemies, destructible walls, sound effects.
- Phase 3: Power-ups, multiple maps, advanced AI.

## Checklist for Testing
- [ ] Install `pygame`.
- [ ] Run `main.py`.
- [ ] Test player movement and shooting.
- [ ] Verify enemy movement and collisions.
- [ ] Check scoring and game-over functionality.
- [ ] Test pause and restart features.

## Progress Updates

### Completed Features
- **Player Movement and Collisions**: The green tank cannot pass through walls.
- **Enemy Movement and Collisions**: Enemies avoid walls and screen boundaries.
- **Bullet Collisions**: Bullets disappear upon hitting walls or enemies.
- **Game States**: The game supports running, pausing, and restarting.
- **Enemy Shooting (In Progress)**: Added `EnemyBullet` class to handle enemy bullets.

### Next Steps
- Integrate enemy shooting logic into the `Enemy` class.
- Update the `Game` class to handle enemy bullets.
- Implement Phase 2 features from the roadmap, such as destructible walls or sound effects.
- Optimize and refactor the code for better readability and maintainability.

### Future Development
Refer to `# TODO(Faza 2)` comments in the code for areas to expand functionality.

## Level system
- Gra zawiera 3 levele.
- Po zniszczeniu wszystkich wrogów automatycznie przechodzisz dalej.
- Każdy level ma inny układ przeszkód i rosnącą trudność.
- Po ukończeniu ostatniego levelu pojawia się ekran „Campaign Complete”.