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

    print("action applied: ", (player.grid_x, player.grid_y))

    if world.turn_status == GameStatus.P1:
        new_world.turn_status = GameStatus.P2

    elif world.turn_status == GameStatus.P2:
        new_world.turn_status = GameStatus.P1
        new_world.turn += 1

    new_world.bomb_group.update(new_world.turn)
    

    return new_world
