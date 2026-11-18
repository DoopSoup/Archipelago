from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

if TYPE_CHECKING:
    from .world import PathWanderer_World


def set_all_rules(world: PathWanderer_World) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: PathWanderer_World) -> None:
    pass

def set_all_location_rules(world: PathWanderer_World) -> None:
    pass

def set_completion_condition(world: PathWanderer_World) -> None:
    world.set_completion_rule(Has("Flag", world.options.required_flags.value))