from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWorld import GameWorld


from data.entity.AI.decision.turn import turn

from game.GameAction import Action
from game.GameLogic import GameLogic
from game.GameStatus import GameStatus

from data.texture.config import MAX_TURN, SHRINK_INTERVAL


def result(world: GameWorld, action: Action):
    new_world = world.clone()

    player = turn(new_world)
    
    GameLogic.apply_action(new_world, player, action)

    if world.turn_status == GameStatus.P1:
        new_world.turn_status = GameStatus.P2

    elif world.turn_status == GameStatus.P2:
        new_world.turn_status = GameStatus.P1
        new_world.turn += 1

    new_world.update(new_world.turn)

    if world.turn > MAX_TURN and (world.turn - MAX_TURN) % SHRINK_INTERVAL == 0:
        SHRINK_MARGIN = (world.turn - MAX_TURN) // SHRINK_INTERVAL
        world.map.shrink_boundary(SHRINK_MARGIN)

    return new_world
