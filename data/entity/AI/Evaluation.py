from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWorld import GameWorld
    from data.entity.Entity import Entity

from data.entity.AI.Terminal import terminal
from data.entity.AI.Value import value


def eval(simulated_world: GameWorld, status: Entity):
        '''
        Output: evaluate the game state depending on the AI position.
        '''
        if terminal(simulated_world):
            return value(simulated_world)
              
        simulated_world.map.generate_valued_grid()

        for player in simulated_world.player_group:
            if player.status == status:
                ai: Entity = player

        # Base score: distance to player (lower is better)
        ai_x, ai_y = (ai.grid_x, ai.grid_y)
        player_x, player_y = simulated_world.map.get_enemie_pos(ai)
        
        ai_sgame = simulated_world.map.valued_grid[ai_y][ai_x]
        player_sgame = simulated_world.map.valued_grid[player_y][player_x]
        distance_score = ai_sgame - player_sgame

        # Count obstacles between AI and player
        obstacles_in_path = simulated_world.map.count_obstacles_between((ai_x, ai_y), (player_x, player_y))

        # Reward the AI for destroying or planning to destroy obstacles
        has_bomb = any(bomb.owner == ai for bomb in simulated_world.bomb_group)

        obstacle_destruction_score = 0
        if obstacles_in_path > 0:
            if has_bomb:
                # AI placed a bomb to destroy obstacles
                obstacle_destruction_score = 100  # reward
            else:
                # Penalize being blocked without acting
                obstacle_destruction_score = -10 * obstacles_in_path

        return distance_score + obstacle_destruction_score
