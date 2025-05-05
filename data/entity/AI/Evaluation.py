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
        
        # Get bomb positions owned by AI
        ai_bombs = [bomb for bomb in simulated_world.bomb_group if bomb.owner == ai]

        obstacle_destruction_score = 0

        MAX_SEARCH_RADIUS = 6
        if abs(player_x - ai_x) + abs(player_y - ai_y) <  MAX_SEARCH_RADIUS:
            # If AI is near the player but is blocked by obstacle 
            bomb_threatens_obstacle = False
            obstacle_positions = simulated_world.map.get_obstacles_between((ai_x, ai_y), (player_x, player_y))
            
            obstacles_in_path = len(obstacle_positions)

            for bomb in ai_bombs:
                bx, by = bomb.grid_x, bomb.grid_y
                for ox, oy in obstacle_positions:
                    # Check if bomb is in range (example: radius = 1)
                    if abs(bx - ox) + abs(by - oy) < bomb.spread:
                        bomb_threatens_obstacle = True
                        break
                if bomb_threatens_obstacle:
                    break

            # Adjust score
            obstacle_destruction_score = 0
            if obstacles_in_path > 0:
                if bomb_threatens_obstacle:
                    obstacle_destruction_score = 100
                else:
                    obstacle_destruction_score = -10 * obstacles_in_path

        return distance_score + obstacle_destruction_score
