from __future__ import annotations
from typing import TYPE_CHECKING, NamedTuple
from BaseClasses import Location
from . import items
from .game.parse_cards import get_obtainable_cards

if TYPE_CHECKING:
    from .world import FortyFiveWorld


class FortyFiveLocation(Location):
    game = "Forty-Five"

class LocData(NamedTuple):
    id: int
    region: str


_cards = get_obtainable_cards()

_TUTORIAL_BULLETS = {"Big Bullet", "Worker Bullet", "Incendiary Bullet", "Silver Bullet"}

_POOL_TO_REGION: dict[int, str] = {
    0: "Aqua Balle",
    1: "Aqua Balle",
    2: "Tabu Letter Outpost",
}

def _build_bullet_locations(start_id: int) -> dict[str, LocData]:
    result = {}
    current_id = start_id
    for card in _cards:
        title = card["title"]
        qty = card["quantity"] - (1 if title in _TUTORIAL_BULLETS else 0)
        if qty <= 0:
            continue
        _region = _POOL_TO_REGION[card["pool"]]
        for n in range(1, qty + 1):
            result[f"{title} {n}"] = LocData(current_id, _region)
            current_id += 1
    return result


location_table: dict[str, LocData] = {
    #Creates "x Enemies Defeated" checks with an ID and region name
    **{f"{n} Enemies Defeated": LocData(1 + i, "Tutorial")
       for i, n in enumerate(range(2, 5, 2))},
    **{f"{n} Enemies Defeated": LocData(3 + i, "Aqua Balle")
       for i, n in enumerate(range(6, 21, 2))},
    **{f"{n} Enemies Defeated": LocData(11 + i, "Tabu Letter Outpost")
       for i, n in enumerate(range(22, 61, 2))},
    **{f"{n} Enemies Defeated": LocData(31 + i, "Salem")
       for i, n in enumerate(range(62, 101, 2))},

    #Does the same for every obtainable bullet, but more complicated
    **_build_bullet_locations(51),
}


def create_all_locations(world: FortyFiveWorld) -> None:
    create_regular_locations(world)
    create_events(world)

def _locs_for(region_name: str) -> dict[str, int]:
    return {loc_name: loc_data.id for loc_name, loc_data in location_table.items() if loc_data.region == region_name}

def create_regular_locations(world: FortyFiveWorld) -> None:
    tutorial = world.get_region("Tutorial")
    aqua_balle = world.get_region("Aqua Balle")
    tabu_letter_outpost = world.get_region("Tabu Letter Outpost")
    salem = world.get_region("Salem")
    spire_outpost = world.get_region("Spire Outpost")

    tutorial.add_locations(_locs_for("Tutorial"), FortyFiveLocation)
    aqua_balle.add_locations(_locs_for("Aqua Balle"), FortyFiveLocation)
    tabu_letter_outpost.add_locations(_locs_for("Tabu Letter Outpost"), FortyFiveLocation)
    salem.add_locations(_locs_for("Salem"), FortyFiveLocation)
    spire_outpost.add_locations(_locs_for("Spire Outpost"), FortyFiveLocation)

def create_events(world: FortyFiveWorld) -> None:
    spire_outpost = world.get_region("Spire Outpost")
    spire_outpost.add_event(
        "Spire Outpost Battle", "Victory", location_type=FortyFiveLocation, item_type=items.FortyFiveItem
    )