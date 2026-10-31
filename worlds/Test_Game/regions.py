from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region
from game_board import game_board

if TYPE_CHECKING:
    from .world import APTestGame_World

def create_and_connect_regions(world: APTestGame_World) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: APTestGame_World) -> None:
    #This game only really has a single region.
    #In theory, I could have a dynamic region system that detects how many times the board can be expanded (either by doing some simple math based on the keys or by having a preset limit)
    starting_tiles = Region("Starting Tiles", world.player, world.multiworld)
    game_board = world.board
    #If this game features multiple regions in the future, I would have to put them together here, but for now, I will simple do this
    regions = [starting_tiles]
    for i in range(2, game_board.size + 1):
        layer_region = Region("Layer_" + str(i), world.player, world.multiworld)
        regions.append(layer_region)

    #It seems I can access the world's option file via world.options

    world.multiworld.regions += regions

def connect_regions(world: APTestGame_World) -> None:
    #uuuh my region doesn't connect to anything???
    max_size = world.board.size

    #In the future, I could just use a simple system something like:
    #max_size = world.options.max_size (or however I get this working later)

    world.get_region("Starting Tiles").connect(world.get_region("Layer_2"), "Layer 2 Unlocked", lambda state: state.has("Key", world.player, 4))
    for i in range(2, max_size + 1):
        current_layer = world.get_region("Layer_" + str(i))
        next_layer = world.get_region("Layer_" + str(i + 1))
        current_layer.connect(next_layer, "Layer " + str(i + 1) + " Unlocked", lambda state: state.has("Key", world.player, (i * 4) + (i - 1) * 2))
