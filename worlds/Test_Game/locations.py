from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

# [ ] Create this
from . import items
from .game_board import TILE_TYPES, game_board

if TYPE_CHECKING:
    from .world import PathWanderer_World


#This might not be sufficient, since there are meant to be a variable number of keys
LOCATION_NAME_TO_ID = {
}

LOCATION_TILES = [
     TILE_TYPES["Flag"],
     TILE_TYPES["Key"],
]


class PathWanderer_Location(Location):
    game = "PathWanderer"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: PathWanderer_World) -> None:
    create_regular_locations(world)
    create_events(world)



def create_regular_locations(world: PathWanderer_World) -> None:
    #This portion will need to be entirely reworked if I ever switch how the locations are handled.'
    game_board = world.board


    for cell_type in LOCATION_TILES:
         for cell in game_board.get_cells(cell_type):
            cell_layer = max(abs(cell.x), abs(cell.y))
            if cell_layer < 2:
                layer = world.get_region("Starting Tiles")
            else:
                layer = world.get_region("Layer_" + str(cell_layer))
        
            location_name = cell.get_type_name((cell.x, cell.y)) + " (" + str(cell.x) + ", " + str(cell.y) + ")"
        
            layer.add_locations({location_name: cell.id}, PathWanderer_Location)
            
            LOCATION_NAME_TO_ID.update({location_name: cell.id})
            world.location_name_to_id.update({location_name: cell.id})

    for location in world.get_locations():
        if location.name.startswith("Flag"):
            location.place_locked_item(items.create_item_with_correct_classification(world, "Flag"))




def create_events(world: PathWanderer_World) -> None:
    pass