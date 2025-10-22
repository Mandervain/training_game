"""training_game package initializer.

Keeps package import semantics explicit. No runtime side-effects.
"""

__all__ = [
    'game',
    'player',
    'enemy',
    'bullet',
    'enemy_bullet',
    'level',
    'wall',
    'utils',
    'settings',
]

import logging

# Package-level logger
logger = logging.getLogger('training_game')
