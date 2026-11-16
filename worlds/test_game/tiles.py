from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from world import PathWanderer_World

class game_tile:
    tile_name : str
    tile_id : int
    tile_layer : int
    can_walk_through : bool


#Type Info

TILE_LAYERS : dict[str, int] = {
    "Terrain" : 0,
    "Items" : 1,
}


#Game Tiles:

class tile_empty(game_tile):
    """
    Empty floor tiles. Considered the default tile option.
    """
    tile_name = "Empty"
    tile_id = 0
    tile_layer = TILE_LAYERS["Terrain"]
    can_walk_through = True

class tile_wall(game_tile):
    """
    Wall tiles. Simply impassible.
    """
    tile_name = "Wall"
    tile_id = 1
    tile_layer = TILE_LAYERS["Terrain"]
    can_walk_through = False

class tile_key(game_tile):
    """
    Key tiles are the most important tiles in the game. The character must collect a certain number of these in order ot expand the board. As keys are placed, there is an incrementing chance that they are turned into flags.
    """
    tile_name = "Key"
    tile_id = 2
    tile_layer = TILE_LAYERS["Items"]
    can_walk_through = True

class tile_flag(game_tile):
    """
    Flag tiles are the second most important tiles. The character must collect a certain number of these in order to win.
    """
    tile_name = "Flag"
    tile_id = 3
    tile_layer = TILE_LAYERS["Items"]
    can_walk_through = True

class tile_skull(game_tile):
    """
    Similar to walls, but will instantly kill the player when stepped on.
    """
    tile_name = "Skull"
    tile_id = 4
    tile_layer = TILE_LAYERS["Terrain"]
    can_walk_through = False

class tile_ap_item(game_tile):
    """
    A dummy tile used to represent all multiworld items.
    """
    tile_name = "ap_item"
    tile_id = 5
    tile_layer = TILE_LAYERS["Items"]
    can_walk_through = True


#Dictionary of types
TILE_TYPES : dict[str, type] = {
    "Empty" : tile_empty,
    "Wall" : tile_wall,
    "Key" : tile_key,
    "Flag" : tile_flag,
    "Skull" : tile_skull,
    "ap_item" : tile_ap_item,
}


#Functions

def get_rando_weights(world : PathWanderer_World) -> dict[str, float]:
    VAR_SUFFIX : str = "_weight"
    weights : dict[str, float] = {}

    for tile_type in TILE_TYPES.keys():
        #ap_item and Flag tiles do not spawn according to the world generation, and so they are removed from consideration to avoid flooding the console with unhelpful information
        if tile_type == "Flag" or tile_type == "ap_item":
            continue

        var_name = (tile_type.lower() + VAR_SUFFIX)
        try:
            weights.update(
                {tile_type : getattr(world.options, var_name)}
            )
        except:
            print("No attribute found for Tile Type: " + tile_type)

    return weights