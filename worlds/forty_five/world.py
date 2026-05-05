import math
from collections.abc import Mapping
from typing import Any
from worlds.AutoWorld import World
from . import items, locations, regions, rules, web_world
from . import options as forty_five_options  # rename due to a name conflict with World.options


class FortyFiveWorld(World):
    """
    Forty-Five is a perfect mix of card game, rogue-lite, and pure wild west mayhem.
    Explore an ever-changing map, collect interesting cards, and battle enemies.
    """

    game = "Forty-Five"

    web = web_world.FortyFiveWebWorld()

    options_dataclass = forty_five_options.FortyFiveOptions

    options: forty_five_options.FortyFiveOptions

    location_name_to_id = {name: data.id for name, data in locations.location_table.items()}

    item_name_to_id = {name: data.code for name, data in items.item_table.items() if data.code is not None}

    origin_region_name = "Tutorial"


    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        definite = items.get_definite_items(self)
        remaining = len(self.location_name_to_id) - len(definite)
        nbr_useful = math.ceil(remaining * self.options.ratio_of_useful_to_filler.value / 100)
        nbr_filler = remaining - nbr_useful

        itempool = definite
        itempool += [self.create_item(items.get_random_useful_item_name(self)) for _ in range(nbr_useful)]
        itempool += [self.create_item(items.get_random_filler_item_name(self)) for _ in range(nbr_filler)]
        self.multiworld.itempool += itempool

    def create_item(self, name: str) -> items.FortyFiveItem:
        return items.create_a_item(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def get_unfilled_locations(self) -> int:
        return len(self.multiworld.get_unfilled_locations(self.player))

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            **self.options.as_dict("death_link", "obscured_choices"),
        }
