from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import APTestGame_World


ITEM_NAME_TO_ID = {
    "Key" : 1,
    "Flag" : 2,
}

DEFAULT_ITEM_CLASSIFICATION: dict[str, ItemClassification] = {
    "Key": ItemClassification.progression | ItemClassification.filler,
    "Flag": ItemClassification.progression,
}

class APTestGame_Item(Item):
    game = "APTestGame"

def get_random_filler_item_name(world: APTestGame_World) -> str:
    #There will be more items later... trust...
    return "Key"

def create_item_with_correct_classification(world: APTestGame_World, name: str) -> APTestGame_Item:
    classification = DEFAULT_ITEM_CLASSIFICATION[name]

    return APTestGame_Item(name, classification, ITEM_NAME_TO_ID[name], world.player)

def create_all_items(world: APTestGame_World) -> None:
    itempool: list[Item] = []
    
    for location in world.location_names:
        if location.startswith("Key"):
            itempool.append(world.create_filler())

    world.multiworld.itempool += itempool