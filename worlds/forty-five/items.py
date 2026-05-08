from __future__ import annotations
from typing import TYPE_CHECKING, NamedTuple, Optional
from BaseClasses import Item, ItemClassification
from .game.parse_cards import get_obtainable_cards

if TYPE_CHECKING:
    from .world import FortyFiveWorld


class ItemData(NamedTuple):
    code: Optional[int]
    classification: ItemClassification

class FortyFiveItem(Item):
    game = "Forty-Five"

_cards = get_obtainable_cards()


item_table: dict[str, ItemData] = {
    "Hot Potato Trap": ItemData(1, ItemClassification.trap),
    "Bewitched Trap": ItemData(2, ItemClassification.trap),
    "Bewitching Trap": ItemData(3, ItemClassification.trap),
    "Burning Trap": ItemData(4, ItemClassification.trap),
    "1 Cash": ItemData(5, ItemClassification.filler),
    "5 Cash": ItemData(6, ItemClassification.filler),
    "10 Cash": ItemData(7, ItemClassification.filler),
    "25 Cash": ItemData(8, ItemClassification.useful),
    "50 Cash": ItemData(9, ItemClassification.useful),
    "75 Cash": ItemData(10, ItemClassification.useful),
    "100 Cash": ItemData(11, ItemClassification.useful),
    "Partial Heal": ItemData(12, ItemClassification.useful),
    "Full Heal": ItemData(13, ItemClassification.useful),
    "Health Upgrade": ItemData(14, ItemClassification.progression_deprioritized),
    "Progressive Town Unlock": ItemData(15, ItemClassification.progression),
    **{card["title"]: ItemData(16 + i, ItemClassification.useful)
       for i, card in enumerate(_cards)},
}

# item groups for better hinting
item_groups: dict[str, set] = {
    "Traps": {
        "Hot Potato Trap",
        "Bewitched Trap",
        "Bewitching Trap",
        "Burning Trap",
    },
    "Cash": {
        "1 Cash",
        "5 Cash",
        "10 Cash",
        "25 Cash",
        "50 Cash",
        "75 Cash",
        "100 Cash",
    },
    "Healing": {
        "Partial Heal",
        "Full Heal",
        "Health Upgrade",
    },
    "Bullets": {card["title"] for card in _cards},

    # Bullet categories because why not.
    # I don't know that the pool categories make much sense, but... ¯\_(ツ)_/¯
    "Common Bullets":{card["title"] for card in _cards if card["quantity"] == 3},
    "Uncommon Bullets": {card["title"] for card in _cards if card["quantity"] == 2},
    "Rare Bullets": {card["title"] for card in _cards if card["quantity"] == 1},
    "Mid-Game Bullets": {card["title"] for card in _cards if card["pool"] == 1},
    "Late-Game Bullets": {card["title"] for card in _cards if card["pool"] == 2},

    # Renamed for hinting convenience
    "Town Unlock": {"Progressive Town Unlock"},
}


def get_random_filler_item_name(world: FortyFiveWorld) -> str:
    opts = world.options
    names = ["Hot Potato Trap", "Bewitched Trap", "Bewitching Trap", "Burning Trap", "1 Cash", "5 Cash", "10 Cash"]
    weights = [
        opts.hot_potato_trap_weight.value,
        opts.bewitched_trap_weight.value,
        opts.bewitching_trap_weight.value,
        opts.burning_trap_weight.value,
        opts.one_cash_weight.value,
        opts.five_cash_weight.value,
        opts.ten_cash_weight.value,
    ]
    if all(w == 0 for w in weights):
        weights[names.index("1 Cash")] = 100
    return world.random.choices(names, weights)[0]


def get_random_useful_item_name(world: FortyFiveWorld) -> str:
    opts = world.options
    names = ["25 Cash", "50 Cash", "75 Cash", "100 Cash", "Partial Heal", "Full Heal", "Health Upgrade"]
    weights = [
        opts.twenty_five_cash_weight.value,
        opts.fifty_cash_weight.value,
        opts.seventy_five_cash_weight.value,
        opts.one_hundred_cash_weight.value,
        opts.partial_heal_weight.value,
        opts.full_heal_weight.value,
        opts.health_upgrade_weight.value,
    ]
    if all(w == 0 for w in weights):
        weights[names.index("25 Cash")] = 100
    return world.random.choices(names, weights)[0]


def create_a_item(world: FortyFiveWorld, name: str) -> FortyFiveItem:
    data = item_table[name]
    return FortyFiveItem(name, data.classification, data.code, world.player)


def get_definite_items(world: FortyFiveWorld) -> list[FortyFiveItem]:
    bullets = [create_a_item(world, card["title"]) for card in _cards for _ in range(card["quantity"])]
    towns = [create_a_item(world, "Progressive Town Unlock") for _ in range(world.options.town_unlocks.value)]
    return bullets + towns