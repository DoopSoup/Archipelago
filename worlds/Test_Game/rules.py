from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

if TYPE_CHECKING:
    from .world import APTestGame_World


def set_all_rules(world: APTestGame_World) -> None:
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_location_rules(world: APTestGame_World) -> None:
    #Temporary Logic. Simply tells the game that all keys will always be collected in numerical order
    for index in range (1, 101):
        if index > 1:
            world.set_rule(world.get_location("Key #" + str(index)), rule=Has("Key", index - 1))
    
    #In some future version of this, I would probably relegate construction of the game to the APWorld to consolidate save data and allow for more complex logic etc., but for now I just want to hook up the stuff.

def set_completion_condition(world: APTestGame_World) -> None:
    #currently bases victory on having 50 flags. Will inevitably need to integrate with upcoming .options when updating
    world.set_completion_rule(Has("Flag", 50))