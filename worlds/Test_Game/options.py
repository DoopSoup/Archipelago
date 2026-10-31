from dataclasses import dataclass

from Options import Choice, OptionCounter, OptionGroup, Option, PerGameCommonOptions, Range, Toggle

#OPTIONS ARE CURRENTLY NONFUNCTIONAL.

class MaxKeys(Range):
    """
    Maximum number of keys that can be placed on the game board. As keys are expended, there is an incremental chance that they are replaced with flags.
    """
    range_start = 8
    range_end = 100 #Gotta think about what the max should be. Testing is required.
    default = 100

class RequiredFlags(Range):
    """
    The number of flags required to win the game.
    """
    range_start = 1
    range_end = 50 #This should be able to be algorithmically determined based on the number of keys, although past a certain point the board will be too big to reasonably get ANY keys at all.
    default = 10

class InitialWeights(OptionCounter):
    """
    Initial weights for different types of tiles on the game board.
    Tiles other than flags or keys become decreasingly likely to appear as more keys are collected.
    """
    Default = {
        "Empty": 5,
        "Wall": 10,
        "Key": 25,
        "Skull": 5,
    }


@dataclass
class APTestGame_Options(PerGameCommonOptions):
    max_keys: MaxKeys
    required_flags: RequiredFlags
    initial_weights: InitialWeights