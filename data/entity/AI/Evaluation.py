from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWord import GameWorld
    from data.entity.Entity import Entity



def eval(simulated_world: GameWorld, entity_playing: Entity):
        '''
        Output: evaluate the game state depending on the AI position.
        '''
        simulated_world.map.generate_valued_grid()

        ai_x, ai_y = entity_playing.grid_x, entity_playing.grid_y

        player_x, player_y = simulated_world.map.get_enemie_pos(entity_playing)
        
        ai_sgame = simulated_world.map.valued_grid[ai_y][ai_x]
        player_sgame = simulated_world.map.valued_grid[player_y][player_x]
        
        return ai_sgame - player_sgame
