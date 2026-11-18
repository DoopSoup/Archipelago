from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import PathWanderer_World


ITEM_NAME_TO_ID = {
    "Key" : 1,
    "Flag" : 2,
}

DEFAULT_ITEM_CLASSIFICATION: dict[str, ItemClassification] = {
    "Key": ItemClassification.progression | ItemClassification.filler,
    "Flag": ItemClassification.progression,
}

class PathWanderer_Item(Item):
    game = "PathWanderer"

def get_random_filler_item_name(world: PathWanderer_World) -> str:
    #There will be more items later... trust...
    return "Key"

def create_item_with_correct_classification(world: PathWanderer_World, name: str) -> PathWanderer_Item:
    classification = DEFAULT_ITEM_CLASSIFICATION[name]

    return PathWanderer_Item(name, classification, ITEM_NAME_TO_ID[name], world.player)

def create_all_items(world: PathWanderer_World) -> None:
    itempool: list[Item] = []
    
    for _ in range(1, world.options.max_keys + 1):
        itempool.append(world.create_item("Key"))

    world.multiworld.itempool += itempool