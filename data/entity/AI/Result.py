from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWord import GameWorld


from game.GameAction import Action
from game.GameLogic import GameLogic
from game.GameStatus import GameStatus

from data.entity.AI.Turn import turn


def result(world: GameWorld, action: Action):

    new_world = world.clone()

    player = turn(new_world)

    GameLogic.apply_action(new_world, player, action)

    if world.turn_status == GameStatus.P1:
        new_world.turn_status = GameStatus.P2

    if world.turn_status == GameStatus.P2:
        new_world.turn_status = GameStatus.P1
        new_world.turn += 1

    return new_world
