from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

class APTestGameWebWorld(WebWorld):
    game = "APTestGame"

    theme = "stone"

    setup_en = Tutorial(
        "Hehe... >:)",
        "HOW DID YOU FIND THIS",
        "English",
        "rude.txt",
        "Ummmm?",
        ["Digital Ghost"]
    )

    tutorials = [setup_en]