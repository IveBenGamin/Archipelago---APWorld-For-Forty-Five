from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import CollectionState

if TYPE_CHECKING:
    from .world import FortyFiveWorld


def set_all_rules(world: FortyFiveWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: FortyFiveWorld) -> None:
    # All entrances are already set in locations.py
    pass


def set_all_location_rules(world: FortyFiveWorld) -> None:
    # All locations are accessible within their region in the normal gameplay loop
    pass


def set_completion_condition(world: FortyFiveWorld) -> None:
    from .options import GoalCondition
    if world.options.goal_condition == GoalCondition.option_early_goal:
        world.multiworld.completion_condition[world.player] = lambda state: state.has("Early Victory", world.player)
    else:
        world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)