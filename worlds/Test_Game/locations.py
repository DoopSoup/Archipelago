from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

# [ ] Create this
from . import items
from .game_board import TILE_TYPES

if TYPE_CHECKING:
    from .world import APTestGame_World


#This might not be sufficient, since there are meant to be a variable number of keys
LOCATION_NAME_TO_ID = {
}

class APTestGame_Location(Location):
    game = "APTestGame"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: APTestGame_World) -> None:
    create_regular_locations(world)
    create_events(world)



def create_regular_locations(world: APTestGame_World) -> None:
    #This portion will need to be entirely reworked if I ever switch how the locations are handled.'
    game_board = world.board

    #Temporary solution, works but isn't readable.
    #game_board.add_locations(get_location_names_with_ids(list("Key #" + str(index) for index in range(1, 101))), APTestGame_Location)
    for cell in game_board.get_cells():
        if cell.cell_type == TILE_TYPES["Key"]:
            cell_layer = max(abs(cell.x), abs(cell.y))
            layer = world.get_region("Layer_" + str(cell_layer))

            location_name = cell.get_type_name((cell.x, cell.y)) + " (" + str(cell.x) + ", " + str(cell.y) + ")"

            layer.add_locations({location_name: cell.id}, APTestGame_Location)
            LOCATION_NAME_TO_ID.update({location_name: cell.id})


def create_events(world: APTestGame_World) -> None:
    # game_board = world.get_region("Game Board")

    # for index in range(1, 51):
    #     game_board.add_event(("Flag #" + str(index)), "Flag", location_type=APTestGame_Location, item_type=items.APTestGame_Item)
    game_board = world.board
    
    for cell in game_board.get_cells():
        if cell.cell_type == TILE_TYPES["Flag"]:
            cell_layer = max(abs(cell.x), abs(cell.y))
            layer = world.get_region("Layer_" + str(cell_layer))

            location_name = cell.get_type_name((cell.x, cell.y)) + " (" + str(cell.x) + ", " + str(cell.y) + ")"

            layer.add_event(location_name, "Flag", location_type=APTestGame_Location, item_type=items.APTestGame_Item, show_in_spoiler=False)
            LOCATION_NAME_TO_ID.update({location_name: cell.id})