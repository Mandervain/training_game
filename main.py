"""
main.py: Entry point for the game. Initializes and starts the game.
"""

# Support running as a module (python -m training_game.main) and
# running the file directly (python training_game\main.py).
import sys
from pathlib import Path
import logging
import os

# Try to import the package normally. If that fails (for example when the
# script is executed directly as `python training_game\main.py`), add the
# project root to sys.path so package-qualified imports inside the package
# succeed.
try:
    from training_game.game import Game
except ModuleNotFoundError:
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from training_game.game import Game


if __name__ == "__main__":
    # Configure logging: default WARNING. Set TRAINING_GAME_DEBUG=1 to enable DEBUG.
    log_level = logging.DEBUG if os.getenv('TRAINING_GAME_DEBUG') in ('1', 'true', 'True') else logging.WARNING
    logging.basicConfig(level=log_level, format='%(asctime)s %(levelname)s [%(name)s] %(message)s')
    game = Game()
    game.run()