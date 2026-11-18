from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region
from .game_board import game_board

if TYPE_CHECKING:
    from .world import PathWanderer_World

def create_and_connect_regions(world: PathWanderer_World) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: PathWanderer_World) -> None:
    #This game only really has a single region.
    #In theory, I could have a dynamic region system that detects how many times the board can be expanded (either by doing some simple math based on the keys or by having a preset limit)
    starting_tiles = Region("Starting Tiles", world.player, world.multiworld)
    game_board = world.board
    
    regions = [starting_tiles]
    for i in range(2, game_board.size):
        layer_region = Region("Layer_" + str(i), world.player, world.multiworld)
        regions.append(layer_region)
        print(world.game + " Created region: " + layer_region.name)

    #It seems I can access the world's option file via world.options

    world.multiworld.regions += regions

def connect_regions(world: PathWanderer_World) -> None:
    max_size = world.board.size
    print(world.game + " Connecting regions..." + " (Max size: " + str(max_size) + ")")

    #In the future, I could just use a simple system something like:
    #max_size = world.options.max_size (or however I get this working later)

    world.get_region("Starting Tiles").connect(world.get_region("Layer_2"), "Layer 2 Unlocked", lambda state: state.has("Key", world.player, 4))
    for i in range(2, max_size - 1):
        current_layer = world.get_region("Layer_" + str(i))
        next_layer = world.get_region("Layer_" + str(i + 1))

        required_keys = (i * 4) + (i - 1)

        current_layer.connect(next_layer, "Layer " + str(i + 1) + " Unlocked", lambda state, keys = required_keys: state.has("Key", world.player, keys))

        print(world.game + " Connected region: " + current_layer.name + " to region: " + next_layer.name + " with key requirement: " + str(required_keys))      
