"""Minimal shim: export Game from the cleaned implementation.

This file intentionally contains only a small export to preserve the
public module path `training_game.game` while the working
implementation lives in `game_clean.py`. Replacing the corrupted
original with this shim unblocks imports and runtime checks.
"""

from training_game.game_clean import Game

__all__ = ["Game"]
