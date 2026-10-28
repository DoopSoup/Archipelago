from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

#TODO make these:
# [ ] items.py
# [-] locations.py
# [x] regions.py
# [ ] rules.py
# [ ] web_world.py
from . import items, locations, regions, rules, web_world
from . import options as APTestGame_Options

class APTestGame_World(World):
    #Description of game for webhost
    """
    A little character randomly moves around in a grid-based world which gets larger when they receive enough keys.
    A bad idea for a game, but a good learning experience.
    """