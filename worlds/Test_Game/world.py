from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import items, locations, regions, rules, web_world
from . import options as APTestGame_Options

class APTestGame_World(World):
    #Description of game for webhost
    """
    A little character randomly moves around in a grid-based world which gets larger when they receive enough keys.
    A bad idea for a game, but a good learning experience.
    """

    game = "APTestGame"

    web = web_world.APTestGameWebWorld()

    options_dataclass = APTestGame_Options.APTestGame_Options
    options: APTestGame_Options.APTestGame_Options # type: ignore

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Game Board"


    def create_regions(self) -> None:
        regions.create_all_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)


    def create_item(self, name: str) -> items.APTestGame_Item:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)


    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
            "max_keys", "required_flags"
        )