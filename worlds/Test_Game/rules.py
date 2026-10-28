from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

if TYPE_CHECKING:
    from .world import APTestGame_World


def set_all_rules(world: APTestGame_World) -> None:
    set_all_location_rules(world)


def set_all_location_rules(world: APTestGame_World) -> None:
    pass
    #In some future version of this, I would probably relegate construction of the game to the APWorld to consolidate save data and allow for more complex logic etc., but for now I just want to hook up the stuff.