from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import APTestGame_World

def create_and_connect_regions(world: APTestGame_World) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: APTestGame_World) -> None:
    #This game only really has a single region.
    #In theory, I could have a dynamic region system that detects how many times the board can be expanded (either by doing some simple math based on the keys or by having a preset limit)
    game_board = Region("Game Board", world.player, world.multiworld)

    #If this game features multiple regions in the future, I would have to put them together here, but for now, I will simple do this
    regions = game_board

    #It seems I can access the world's option file via world.options

    world.multiworld.regions += regions

def connect_regions(world: APTestGame_World) -> None:
    #uuuh my region doesn't connect to anything???

    #In the future, I could just use a simple system something like:
    #max_size = world.options.max_size (or however I get this working later)
    #for i in max_size:
    #  world.get_region("Layer_" + str(i)).connect(world.get_region("Layer_" + str(i+1)), "")
    #(Maybe use variables or something for easier readability)

    pass