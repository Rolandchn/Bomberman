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

        ai = None
        for player in simulated_world.player_group:
            if player.status == status:
                ai = player
                break

        if ai is None:
            raise ValueError("MINMAX caller was not found")


        # Base score: distance to player (lower is better)
        ai_x, ai_y = (ai.grid_x, ai.grid_y)
        player_x, player_y = simulated_world.map.get_enemie_pos(ai)
        
        ai_sgame = simulated_world.map.valued_grid[ai_y][ai_x]
        player_sgame = simulated_world.map.valued_grid[player_y][player_x]
        distance_score = ai_sgame - player_sgame
        

        # Bomb score: distance to Get bomb positions owned by AI
        ai_bombs = [bomb for bomb in simulated_world.bomb_group if bomb.owner == ai]

        obstacle_destruction_score = 0

        CENTER_POS = (7, 7)  # assuming 1-based grid and center of 13x13 map
        MAX_SEARCH_RADIUS = 6

        obstacle_destruction_score = 0

        # Check path to player
        player_distance = abs(player_x - ai_x) + abs(player_y - ai_y)

        if player_distance < MAX_SEARCH_RADIUS:
            target_pos = (player_x, player_y)
        else:
            target_pos = CENTER_POS  # fallback objective

        # Count obstacles and check for bombs threatening them
        obstacle_positions = simulated_world.map.get_obstacles_between((ai_x, ai_y), target_pos)
        obstacles_in_path = len(obstacle_positions)
        bomb_threatens_obstacle = False

        for bomb in ai_bombs:
            bx, by = bomb.grid_x, bomb.grid_y
            for ox, oy in obstacle_positions:
                if abs(bx - ox) + abs(by - oy) <= bomb.spread:
                    bomb_threatens_obstacle = True
                    break
            if bomb_threatens_obstacle:
                break

        # Adjust score based on bomb placement
        if obstacles_in_path > 0:
            if bomb_threatens_obstacle:
                obstacle_destruction_score = 100
            else:
                obstacle_destruction_score = -10 * obstacles_in_path

        return distance_score + obstacle_destruction_score
