from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .options import option_groups, option_presets


class FortyFiveWebWorld(WebWorld):

    game = "Forty-Five"

    theme = "dirt"

    # Order: Title, a description, a language, a filepath, a link, and authors.
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Forty-Five for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["IveBenGamin"],
    )

    tutorials = [setup_en,]

    option_groups = option_groups
    options_presets = option_presets
