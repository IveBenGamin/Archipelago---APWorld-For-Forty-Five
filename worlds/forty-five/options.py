from dataclasses import dataclass

from Options import Accessibility, DeathLink, OptionGroup, PerGameCommonOptions, Range, Toggle, Visibility


class FortyFiveAccessibility(Accessibility):
    visibility = Visibility.none


# Game Settings

class RatioOfUsefulToFiller(Range):
    """
    The percentage of non-bullet filler slots that will be filled with useful items,
    as defined by probability weight below.
    The remainder will be filler items, also defined by probability weight below.
    """
    display_name = "Ratio of Useful to Filler"
    range_start = 0
    range_end = 100
    default = 70

class TownUnlocks(Range):
    """
    The number of Progressive Town Unlock items placed in the item pool.
    The more you have, the less likely you are to get stuck.
    """
    display_name = "Town Unlocks"
    range_start = 4
    range_end = 7
    default = 5

class ObscuredChoices(Toggle):
    """
    When enabled, cards offered in the shop and card-pick events show only
    "It's... something... for <player>," instead of revealing the item and category.
    """
    display_name = "Obscured Choices"


# Useful Item Pool

class TwentyFiveCashWeight(Range):
    """
    Weight of "25 Cash" in the useful item pool. Set to 0 to exclude.
    """
    display_name = "25 Cash Weight"
    range_start = 0
    range_end = 100
    default = 7

class FiftyCashWeight(Range):
    """
    Weight of "50 Cash" in the useful item pool. Set to 0 to exclude.
    """
    display_name = "50 Cash Weight"
    range_start = 0
    range_end = 100
    default = 1

class SeventyFiveCashWeight(Range):
    """
    Weight of "75 Cash" in the useful item pool. Set to 0 to exclude.
    """
    display_name = "75 Cash Weight"
    range_start = 0
    range_end = 100
    default = 1

class OneHundredCashWeight(Range):
    """
    Weight of "100 Cash" in the useful item pool. Set to 0 to exclude.
    """
    display_name = "100 Cash Weight"
    range_start = 0
    range_end = 100
    default = 1

class PartialHealWeight(Range):
    """
    Weight of "Partial Heal" in the useful item pool. Set to 0 to exclude.
    """
    display_name = "Partial Heal Weight"
    visibility = Visibility.none
    range_start = 0
    range_end = 100
    default = 0

class FullHealWeight(Range):
    """
    Weight of "Full Heal" in the useful item pool. Set to 0 to exclude.
    """
    display_name = "Full Heal Weight"
    visibility = Visibility.none
    range_start = 0
    range_end = 100
    default = 0

class HealthUpgradeWeight(Range):
    """
    Weight of "Health Upgrade" in the useful item pool. Set to 0 to exclude.
    """
    display_name = "Health Upgrade Weight"
    visibility = Visibility.none
    range_start = 0
    range_end = 100
    default = 0


# Filler Item Pool

class HotPotatoTrapWeight(Range):
    """
    Weight of "Hot Potato Trap" in the filler item pool. Set to 0 to exclude.
    Gives you a Scorching Bullet, Pyro's most annoying attack.
    """
    display_name = "Hot Potato Trap Weight"
    range_start = 0
    range_end = 100
    default = 1

class BewitchedTrapWeight(Range):
    """
    Weight of "Bewitched Trap" in the filler item pool. Set to 0 to exclude.
    Gives you the "Bewitched" effect.
    """
    display_name = "Bewitched Trap Weight"
    range_start = 0
    range_end = 100
    default = 3

class BewitchingTrapWeight(Range):
    """
    Weight of "Bewitching Trap" in the filler item pool. Set to 0 to exclude.
    Rotates the revolver one slot to the left.
    """
    display_name = "Bewitching Trap Weight"
    range_start = 0
    range_end = 100
    default = 3

class BurningTrapWeight(Range):
    """
    Weight of "Burning Trap" in the filler item pool. Set to 0 to exclude.
    Gives you the "Burning" effect.
    """
    display_name = "Burning Trap Weight"
    range_start = 0
    range_end = 100
    default = 2

class OneCashWeight(Range):
    """
    Weight of "1 Cash" in the filler item pool. Set to 0 to exclude.
    """
    display_name = "1 Cash Weight"
    range_start = 0
    range_end = 100
    default = 20

class FiveCashWeight(Range):
    """
    Weight of "5 Cash" in the filler item pool. Set to 0 to exclude.
    """
    display_name = "5 Cash Weight"
    range_start = 0
    range_end = 100
    default = 5

class TenCashWeight(Range):
    """
    Weight of "10 Cash" in the filler item pool. Set to 0 to exclude.
    """
    display_name = "10 Cash Weight"
    range_start = 0
    range_end = 100
    default = 5


@dataclass
class FortyFiveOptions(PerGameCommonOptions):
    accessibility: FortyFiveAccessibility
    # Game Settings
    death_link: DeathLink
    obscured_choices: ObscuredChoices
    town_unlocks: TownUnlocks
    ratio_of_useful_to_filler: RatioOfUsefulToFiller
    # Useful Item Pool
    twenty_five_cash_weight: TwentyFiveCashWeight
    fifty_cash_weight: FiftyCashWeight
    seventy_five_cash_weight: SeventyFiveCashWeight
    one_hundred_cash_weight: OneHundredCashWeight
    partial_heal_weight: PartialHealWeight
    full_heal_weight: FullHealWeight
    health_upgrade_weight: HealthUpgradeWeight
    # Filler Item Pool
    hot_potato_trap_weight: HotPotatoTrapWeight
    bewitched_trap_weight: BewitchedTrapWeight
    bewitching_trap_weight: BewitchingTrapWeight
    burning_trap_weight: BurningTrapWeight
    one_cash_weight: OneCashWeight
    five_cash_weight: FiveCashWeight
    ten_cash_weight: TenCashWeight


# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = [
    OptionGroup("Game Settings", [
        TownUnlocks,
        ObscuredChoices,
        DeathLink,
        RatioOfUsefulToFiller,
    ]),
    OptionGroup("Useful Item Pool", [
        TwentyFiveCashWeight,
        FiftyCashWeight,
        SeventyFiveCashWeight,
        OneHundredCashWeight,
        PartialHealWeight,
        FullHealWeight,
        HealthUpgradeWeight,
    ]),
    OptionGroup("Filler Item Pool", [
        HotPotatoTrapWeight,
        BewitchedTrapWeight,
        BewitchingTrapWeight,
        BurningTrapWeight,
        OneCashWeight,
        FiveCashWeight,
        TenCashWeight,
    ]),
]

# We can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets: dict = {
    "Default": {
        # Game Settings
        "death_link": 0,
        "obscured_choices": 0,
        "town_unlocks": 5,
        "ratio_of_useful_to_filler": 70,
        # Useful Item Pool
        "twenty_five_cash_weight": 7,
        "fifty_cash_weight": 1,
        "seventy_five_cash_weight": 1,
        "one_hundred_cash_weight": 1,
        # Filler Item Pool
        "hot_potato_trap_weight": 1,
        "bewitched_trap_weight": 3,
        "bewitching_trap_weight": 3,
        "burning_trap_weight": 2,
        "one_cash_weight": 20,
        "five_cash_weight": 5,
        "ten_cash_weight": 5,
    },
}