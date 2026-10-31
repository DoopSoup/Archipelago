from __future__ import annotations

from typing import TYPE_CHECKING

import random

if TYPE_CHECKING:
    from worlds.Test_Game.world import APTestGame_World

TILE_TYPES : dict[str, int] = {
    "Empty" : 0,
    "Wall" : 1,
    "Key" : 2,
    "Flag" : 3,
    "Skull" : 4,
    "ap_item" : 5,
}
initial_size = 2
initial_keys = 8

class game_cell:
    def __init__(self, cell_type: int, x: int, y: int):
        self.cell_type = cell_type
        self.x = x
        self.y = y

class game_board:
    #features a matrix of cells representing the game board.
    #The matrix has a size determined by (size*2 -1, size*2 -1) with the cell in the center being considered the origin, (0,0).
    def __init__(self, size: int):
        self.size = size
        self.cells = [[game_cell(TILE_TYPES["Empty"], x - size + 1, y - size + 1) for x in range(size * 2 - 1)] for y in range(size * 2 - 1)]
        self.origin = self.cells[size - 1][size - 1]

    def set_cell(self, coords: tuple[int, int], cell_type: int):
        x, y = coords
        #Needs to adapt coordinates from origin-based to matrix-based
        matrix_x = x + self.size - 1
        matrix_y = y + self.size - 1
        self.cells[matrix_y][matrix_x].cell_type = cell_type
        #print("Setting cell at", coords, "to type", cell_type)

    def export(self) -> str:
        import json
        board_string = ""
        for y, row in enumerate(self.cells):
            row_string = ""
            for x, cell in enumerate(row):
                row_string += str(cell.cell_type) + " "
            board_string += row_string + "\n"
        return board_string

def get_tile_ID(str: str) -> int:
    return TILE_TYPES.get(str, -1)

def generate_game_board() -> game_board:
    """
    Creates a matrix of tile types representing the game board.
    Generation starts at tile (0, 0).
    """

    #Determines the maximum possible size of the game board based on the number of keys available
    max_keys = 100
    current_keys = max_keys - initial_keys
    current_size = initial_size

    i = 0
    while current_keys - (4 + i) >= 0:
        current_keys -= (4 + i)
        current_size += 1
        i += 1

    final_size = current_size
    print("Final board size determined:", final_size)

    #Sets up the initial board, a 9x9 grid. 1 empty cell surrounded by 8 keys
    board = game_board(current_size)
    #Place the initial empty cell at the origin
    board.set_cell((0, 0), TILE_TYPES["Empty"])

    #Place the initial keys around the origin
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            board.set_cell((dx, dy), TILE_TYPES["Key"])

    #Expands the board until the board size reaches the final size determined earlier
    #Randomly places tiles on each newly generated layer with weights determined by the world options and remaining keys

    board = expand_board_to_fill(board, final_size)
    return board

def expand_board_to_fill(board: game_board, final_size: int) -> game_board:
    current_size = initial_size
    max_keys = 100
    current_keys = initial_keys

    layer_cost = 4
    required_keys = layer_cost

    print("Expanding board to final size:", final_size)
    while current_size < final_size:
        placed_tiles = 0
        layer_cost += 1
        required_keys += layer_cost
        current_size += 1

        print("Beginning Layer: "+ str(current_size) + " with " + str(current_keys) + " keys placed and " + str(required_keys) + " required keys.")
        for dx in range(-current_size + 1, current_size):
            for dy in range(-current_size + 1, current_size):
                #Determines if the current tile has already been placed in a previous layer, and if so, skips it
                if abs(dx) < current_size - 1 and abs(dy) < current_size - 1:
                    continue

                key_scalar = (current_keys / max_keys) / 2
                #print(key_scalar)
                #Get the random weights for each tile type
                tile_weights = {
                    "Empty": 60,
                    "Wall": 10,
                    "Key": 25,
                    "Skull": 5,
                }
                total_weight = sum(tile_weights.values())
                adjusted_weights = {}
                
                for tile in TILE_TYPES:
                    #If the given tile has a weight assigned in options It's target weight is adjusted according to its type
                    initial_weight = 0

                    if tile in tile_weights.keys():
                        #Then the adjusted weight is added to the adjusted_weights dictionary
                        initial_weight = tile_weights[tile]

                    #current_weight = tile_weights[tile]
                    if tile == "Key":
                        current_weight = (initial_weight + key_scalar * (total_weight - initial_weight))
                    else:
                        current_weight = (initial_weight + key_scalar * (0 - initial_weight))

                    adjusted_weights.update({tile: current_weight/total_weight})
                #print("Adjusted weights:", adjusted_weights)
                #Select a tile based on the weights

                rand_val = random.random()
                cumulative_weight = 0
                selected_tile : str = "Empty"
                for tile, weight in adjusted_weights.items():
                    if tile == "Flag":
                        continue

                    cumulative_weight += weight
                    if rand_val < cumulative_weight:
                        #print("I've decided! This tile will be a " + tile)
                        selected_tile = tile
                        break

                #If the selected tile is a key, there is a (current_keys / max_keys) chance of actually placing it, otherwise it is replaced with a flag
                if selected_tile == "Key":
                    rand_val = random.random()
                    if rand_val < (current_keys / max_keys):
                        current_keys += 1
                    else:
                        #print("Actually, this tile will be a Flag instead.")
                        selected_tile = "Flag"
                #If not, check if there are less than the required number of keys remaining and if so, run in incrementing chance to place a key
                else:
                    if current_keys < required_keys:
                        print("Hmm... There are less keys than there should be... (" + str(current_keys) + " / " + str(required_keys) + ")")
                        rand_val = random.random()
                        key_difference = required_keys - current_keys
                        remaining_tiles = (((current_size - 1) * 8) - placed_tiles) - key_difference
                        key_chance = (
                                placed_tiles / remaining_tiles
                        )
                        print("I think there's a " + str(key_chance * 100) + "% chance that this tile should be a key. Given that there are " + str(remaining_tiles) + " tiles remaining.")
                        if rand_val < key_chance:
                            print("Actually, this tile (" + str(dx) + ", " + str(dy) + ") will be a Key instead.")
                            selected_tile = "Key"
                            current_keys += 1
                
                #Check if there are any remaining keys to place.
                if selected_tile == "Key" and current_keys > max_keys:
                    #print("No more keys can be placed. This tile will be a Flag instead.")
                    current_keys -= 1
                    selected_tile = "Flag"

                board.set_cell((dx, dy), TILE_TYPES[selected_tile])
                placed_tiles += 1
                    
    
    return board
        


def generate_game_board_file(board: game_board):
    from pathlib import Path

    board_size = board.size

    output_file = ("board_size:" + str(board_size) + 
                   "\nboard:" + board.export())
    #Creates a file in the Output folder named game_board_.json containing the board size and the board matrix
    with open(Path(__file__).parent.parent / "Output" / "game_board_.json", "w") as f:
        f.write(output_file)

generate_game_board_file(generate_game_board())