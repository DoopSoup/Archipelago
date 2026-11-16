from dataclasses import dataclass

from Options import Choice, OptionCounter, OptionGroup, Option, PerGameCommonOptions, Range, Toggle



class MaxKeys(Range):
    """
    The number of 'Key' items that are placed in the multiworld. 
    Receiving a certain number of keys (4 to start, increases by 1 each time) will expand the game board.
    """

    display_name = "Keys in Pool"

    range_start = 8
    range_end = 1000 #Gotta think about what the max should be. Testing is required.
    default = 100

class RequiredFlags(Range):
    """
    The number of 'Flag' items required to win the game.
    Flags have an increasing chance to appear instead of keysa as more keys are collected.
    It is recommemded to keep this number less than the number of keys.
    """

    display_name = "Required Flags"

    range_start = 1
    range_end = 1000 #This should be able to be algorithmically determined based on the number of keys, although past a certain point the board will be too big to reasonably get ANY keys at all.
    default =  100



#Tile Randomization Weights
class KeyWeight(Range):
    """
    The initial weight for 'Key' tiles on the game board.
    Keys/Flags become more common in each layer generated. The outermost layer will always be entirely be Keys/Flags.
    The game board will always generate enough keys to reach the next layer.
    """

    display_name = "Key/Flag Tile Weight"

    range_start = 0
    range_end = 100
    default = 25

class EmptyWeight(Range):
    """
    The initial weight for 'Empty' tiles on the game board.
    """

    display_name = "Empty Tile Weight"

    range_start = 0
    range_end = 100
    default = 60

class WallWeight(Range):
    """
    The initial weight for 'Wall' tiles on the game board.
    """

    display_name = "Wall Tile Weight"

    range_start = 0
    range_end = 100
    default = 10

class SkullWeight(Range):
    """
    The initial weight for 'Skull' tiles on the game board.
    Skull tiles will instantly kill the characer if they step on them.
    """

    display_name = "Skull Tile Weight"

    range_start = 0
    range_end = 100
    default = 5



@dataclass
class PathWanderer_Options(PerGameCommonOptions):
    max_keys: MaxKeys
    required_flags: RequiredFlags

    key_weight: KeyWeight
    empty_weight: EmptyWeight
    wall_weight: WallWeight
    skull_weight: SkullWeight

option_groups = [
    OptionGroup(
        "Gameboard Generation Options",
        [
            KeyWeight,
            EmptyWeight,
            WallWeight,
            SkullWeight,
        ]
    )
]