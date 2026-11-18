from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from world import PathWanderer_World

class game_tile:
    name : str
    id : int
    layer : int
    can_walk_through : bool

    def dump_tile(self):
        output: dict =  {
            "name" : self.name,
            "id" : self.id,
            "layer" : self.layer,
            "passable" : True,
        }
        return output


#Layer dict.
#Keys refer to name of the layer, values are the layer's z index. 
#Layers are generated in the order they are presented here.
LAYERS : dict[str, int] = {
    "Terrain" : 0,
    "Items" : 1,
}


#Game Tiles:

class empty(game_tile):
    """
    Empty floor tiles. Considered the default tile option.
    """
    name = "Empty"
    id = 0
    layer = LAYERS["Terrain"]
    can_walk_through = True

class wall(game_tile):
    """
    Wall tiles. Simply impassible.
    """
    name = "Wall"
    id = 1
    layer = LAYERS["Terrain"]
    can_walk_through = False

class key(game_tile):
    """
    Key tiles are the most important tiles in the game. The character must collect a certain number of these in order ot expand the board. As keys are placed, there is an incrementing chance that they are turned into flags.
    """
    name = "Key"
    id = 2
    layer = LAYERS["Items"]
    can_walk_through = True

class flag(game_tile):
    """
    Flag tiles are the second most important tiles. The character must collect a certain number of these in order to win.
    """
    name = "Flag"
    id = 3
    layer = LAYERS["Items"]
    can_walk_through = True

class skull(game_tile):
    """
    Similar to walls, but will instantly kill the player when stepped on.
    """
    name = "Skull"
    id = 4
    layer = LAYERS["Terrain"]
    can_walk_through = False

class ap_item(game_tile):
    """
    A dummy tile used to represent all multiworld items.
    """
    name = "ap_item"
    id = 5
    layer = LAYERS["Items"]
    can_walk_through = True


#Dictionary of types
TYPES : dict[str, type] = {
    "Empty" : empty,
    "Wall" : wall,
    "Key" : key,
    "Flag" : flag,
    "Skull" : skull,
    "ap_item" : ap_item,
}


#Functions

def get_rando_weights(world : PathWanderer_World) -> dict[str, float]:
    VAR_SUFFIX : str = "_weight"
    weights : dict[str, float] = {}

    for type in TYPES.keys():
        #ap_item and Flag tiles do not spawn according to the world generation, and so they are removed from consideration to avoid flooding the console with unhelpful information
        if type == "Flag" or type == "ap_item":
            continue

        var_name = (type.lower() + VAR_SUFFIX)
        try:
            weights.update(
                {type : getattr(world.options, var_name)}
            )
            
        except:
            print("No attribute found for Tile Type: " + type)

    return weights

def get_tile_layer(tile : type[game_tile]) -> int:
    return tile.layer