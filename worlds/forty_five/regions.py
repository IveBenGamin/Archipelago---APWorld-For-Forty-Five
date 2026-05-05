from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Region

if TYPE_CHECKING:
    from .world import FortyFiveWorld


def create_and_connect_regions(world: FortyFiveWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: FortyFiveWorld) -> None:
    tutorial = Region("Tutorial", world.player, world.multiworld)
    aqua_balle = Region("Aqua Balle", world.player, world.multiworld)
    tabu_letter_outpost = Region("Tabu Letter Outpost", world.player, world.multiworld)
    salem = Region("Salem", world.player, world.multiworld)
    spire_outpost = Region("Spire Outpost", world.player, world.multiworld)

    world.multiworld.regions += [tutorial, aqua_balle, tabu_letter_outpost, salem, spire_outpost]


def connect_regions(world: FortyFiveWorld) -> None:
    tutorial = world.get_region("Tutorial")
    aqua_balle = world.get_region("Aqua Balle")
    tabu_letter_outpost = world.get_region("Tabu Letter Outpost")
    salem = world.get_region("Salem")
    spire_outpost = world.get_region("Spire Outpost")

    tutorial.connect(aqua_balle, "Tutorial to Aqua Balle",
        lambda state: state.has("Progressive Town Unlock", world.player, 1))
    aqua_balle.connect(tabu_letter_outpost, "Aqua Balle to Tabu Letter Outpost",
        lambda state: state.has("Progressive Town Unlock", world.player, 2))
    tabu_letter_outpost.connect(salem, "Tabu Letter Outpost to Salem",
        lambda state: state.has("Progressive Town Unlock", world.player, 3))
    salem.connect(spire_outpost, "Salem to Spire Outpost",
        lambda state: state.has("Progressive Town Unlock", world.player, 4))