from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWorld import GameWorld
    from data.entity.Entity import Entity

import math

from game.GameStatus import GameStatus
from data.entity.AI.decision.terminal import terminal
from data.entity.AI.decision.value import value

from data.entity.AI.evaluation.behavior.attack import evaluate_attack_behavior
from data.entity.AI.evaluation.behavior.center import evaluate_center_behavior


def eval(simulated_world: GameWorld, status: GameStatus):
        '''
        Output: evaluate the game state depending on the AI position.
        '''
        pass

