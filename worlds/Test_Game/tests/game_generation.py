from .bases import APTestGame_Test

class TestGameBoardGeneration(APTestGame_Test):
    options = {
        "max_keys": 100,
        "required_flags": 50,
        "initial_weights": {
            "Empty": 5,
            "Wall": 10,
            "Key": 25,
            "Skull": 5,
        }
    }
