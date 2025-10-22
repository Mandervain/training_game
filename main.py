"""
main.py: Entry point for the game. Initializes and starts the game.
"""

# Support running as a module (python -m training_game.main) and
# running the file directly (python training_game\main.py).
import sys
from pathlib import Path

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
    game = Game()
    game.run()