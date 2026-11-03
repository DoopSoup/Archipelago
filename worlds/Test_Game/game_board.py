from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from world import APTestGame_World

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
    def __init__(self, cell_type: int, x: int, y: int, id: int):
        self.cell_type = cell_type
        self.x = x
        self.y = y
        self.id = id
        self.location_name = ""

    def get_type_name(self, coords: tuple[int, int]) -> str:
        for name, type_id in TILE_TYPES.items():
            if type_id == self.cell_type:
                return name
        return "Unknown"

    def get_cell_info(self) -> dict:
        return {
            "type": self.get_type_name((self.x, self.y)),
            "coords" : (self.x, self.y),
            "id" : self.id,
            "location_name" : self.location_name
        }

    def set_location_name(self, name: str) -> None:
        self.location_name = name

class game_board:
    #features a matrix of cells representing the game board.
    #The matrix has a size determined by (size*2 -1, size*2 -1) with the cell in the center being considered the origin, (0,0).
    def __init__(self, size: int):
        self.size = size
        self.cells = [[game_cell(TILE_TYPES["Empty"], x - size + 1, y - size + 1, 0) for x in range(size * 2 - 1)] for y in range(size * 2 - 1)]
        self.origin = self.cells[size - 1][size - 1]

    def set_cell(self, coords: tuple[int, int], cell_type: int, id: int) -> None:
        x, y = coords
        #Needs to adapt coordinates from origin-based to matrix-based
        matrix_x = x + self.size - 1
        matrix_y = y + self.size - 1
        self.cells[matrix_y][matrix_x].cell_type = cell_type
        self.cells[matrix_y][matrix_x].id = id
        #print("Setting cell at", coords, "to type", cell_type)

    def export(self) -> list[dict]:
        board_list = []
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                board_list.append(cell.get_cell_info())
        return board_list

    def get_cell(self, coords: tuple[int, int]) -> game_cell:
        x, y = coords
        matrix_x = x + self.size - 1
        matrix_y = y + self.size - 1
        return self.cells[matrix_y][matrix_x]

    def get_cells(self, type: int = -1) -> list[game_cell]:
        if type < 0:
            return [cell for row in self.cells for cell in row]
        else:
            return [cell for row in self.cells for cell in row if cell.cell_type == type]

    def update_with_item_placements(self, world: APTestGame_World, item_placement: dict[str, str]) -> None:
        for location_name, item_name in item_placement.items():
            #First, extract the coordinates from the location name string, which is in the format "Location (x, y)"
            cell_coords = location_name.split("(")[-1].split(")")[0].split(",")
            cell_coords = (int(cell_coords[0]), int(cell_coords[1]))

            self.get_cell(cell_coords).set_location_name(location_name)

            #Check whether or not the item is local to this game, if it is not, then the tile type should be set to 5 for ap_item
            if item_name in world.item_name_to_id.keys():
                tile_type = TILE_TYPES[item_name]
            else:
                tile_type = TILE_TYPES["ap_item"]

def get_tile_ID(str: str) -> int:
    return TILE_TYPES.get(str, -1)

def generate_game_board(world: APTestGame_World):
    """
    Creates a matrix of tile types representing the game board.
    Generation starts at tile (0, 0).
    """

    #Determines the maximum possible size of the game board based on the number of keys available
    max_keys = world.options.max_keys
    current_keys = max_keys - initial_keys
    current_size = initial_size

    i = 0
    while current_keys - (4 + i) > 0:
        current_keys -= (4 + i)
        current_size += 1
        i += 1

    final_size = current_size

    #Sets up the initial board, a 9x9 grid. 1 empty cell surrounded by 8 keys
    board = game_board(current_size)
    #Place the initial empty cell at the origin
    board.set_cell((0, 0), TILE_TYPES["Empty"], 1)

    #Place the initial keys around the origin
    id_counter = 2
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            board.set_cell((dx, dy), TILE_TYPES["Key"], id_counter)
            id_counter += 1

    #Expands the board until the board size reaches the final size determined earlier
    #Randomly places tiles on each newly generated layer with weights determined by the world options and remaining keys

    expand_board_to_fill(world, board, final_size)
    return board

def expand_board_to_fill(world: APTestGame_World, board: game_board, final_size: int) -> game_board:
    current_size = initial_size
    current_keys = initial_keys
    max_keys = world.options.max_keys

    id_counter = 9
    layer_cost = 4
    required_keys = layer_cost

    while current_size < final_size:
            placed_tiles = 0
            layer_cost += 1
            required_keys += layer_cost
            current_size += 1
    
            #print("Beginning Layer: "+ str(current_size) + " with " + str(current_keys) + " keys placed and " + str(required_keys) + " required keys.")
            for dx in range(-current_size + 1, current_size):
                for dy in range(-current_size + 1, current_size):
                    #Determines if the current tile has already been placed in a previous layer, and if so, skips it
                    if abs(dx) < current_size - 1 and abs(dy) < current_size - 1:
                        continue
    
                    key_scalar = (current_keys / max_keys) / 2
                    #print(key_scalar)
                    #Get the random weights for each tile type
                    tile_weights = world.options.initial_weights
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
    
                    rand_val = world.multiworld.random.random()
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
                        rand_val = world.multiworld.random.random()
                        if rand_val < (current_keys / max_keys):
                            current_keys += 1
                        else:
                            #print("Actually, this tile will be a Flag instead.")
                            selected_tile = "Flag"
                    #If not, check if there are less than the required number of keys remaining and if so, run in incrementing chance to place a key
                    else:
                        if current_keys < required_keys:
                            #print("Hmm... There are less keys than there should be... (" + str(current_keys) + " / " + str(required_keys) + ")")
                            rand_val = world.multiworld.random.random()
                            key_difference = required_keys - current_keys
                            remaining_tiles = (((current_size - 1) * 8) - placed_tiles) - key_difference
                            key_chance = (
                                    placed_tiles / remaining_tiles
                            )
                            #print("I think there's a " + str(key_chance * 100) + "% chance that this tile should be a key. Given that there are " + str(remaining_tiles) + " tiles remaining.")
                            if rand_val < key_chance:
                                #print("Actually, this tile (" + str(dx) + ", " + str(dy) + ") will be a Key instead.")
                                selected_tile = "Key"
                                current_keys += 1
                    
                    #Check if there are any remaining keys to place.
                    if selected_tile == "Key" and current_keys > max_keys:
                        #print("No more keys can be placed. This tile will be a Flag instead.")
                        current_keys -= 1
                        selected_tile = "Flag"
    
                    board.set_cell((dx, dy), TILE_TYPES[selected_tile], id_counter)
                    id_counter += 1
                    placed_tiles += 1
                        
    return board


def generate_game_board_file(world, board, path: str = "nil") -> None:
    from pathlib import Path
    import json
    
    board_size = board.size
    
    output_file = {"board_size" : board_size, 
                    "board": board.export()}
    #Creates a file in the Output folder named game_board_.json containing the board size and the board matrix
    if path == "nil":
        path = Path(__file__).parent / "Output" / "game_board_" + world.multiworld.seed_name + ".json"
    with open(path, "w") as f:
        json.dump(output_file, f)
