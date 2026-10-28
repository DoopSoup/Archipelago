from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

# [ ] Create this
from . import items

if TYPE_CHECKING:
    from .world import APTestGame_World


#This might not be sufficient, since there are meant to be a variable number of keys
LOCATION_NAME_TO_ID = {
    {("Key #" + str(index)): index for index in range(1,101)}
}
LOCATION_NAME_TO_ID.update({
    ("Flag #" + str(index)): index for index in range(101, 151)
})

class APTestGame_Location(Location):
    game = "APTestGame"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: APTestGame_World) -> None:
    create_regular_locations(world)
    #create_events(world)


def create_regular_locations(world: APTestGame_World) -> None:
    #This portion will need to be entirely reworked if I ever switch how the locations are handled.'
    game_board = world.get_region("Game Board")

    #Temporary solution, works but isn't readable.
    game_board.add_locations(LOCATION_NAME_TO_ID, APTestGame_Location)