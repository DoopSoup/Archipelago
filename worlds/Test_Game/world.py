from collections.abc import Mapping
import os
from typing import Any

from worlds.AutoWorld import World

from . import items, locations, regions, rules, web_world, game_board
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

    board: game_board.game_board

    def generate_early(self) -> None:
        #Read options file; determine maximum board size
        #Generate game board
        #Pass board size to regions
        #Pass key and flag locations to locations (give pointer to xy coords for id)
        #(Generate game)
        #Update game board, all non-key, non-flag item tiles receive new tile id
        #Move game board to final zip file
        
        self.board = game_board.generate_game_board(self)
        


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

    def generate_output(self, output_directory: str) -> None:
        #Need to retrieve the generated multiworld data somehow, and amend the game board with it, if a location has an item from another world, the tile_id should be replaced with 5 for apitem

        #Location:Item Dict
        Item_Placement = {
            location.name: location.item.name
            for location in self.get_filled_locations(self.player)
        }

        self.board.update_with_item_placements(self, Item_Placement)

        #Output path
        mod_name = self.multiworld.get_out_file_name_base(self.player)
        output_path = os.path.join(output_directory + mod_name + ".zip")

        game_board.generate_game_board_file(self, self.board, output_path)