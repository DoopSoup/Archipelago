from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from world import PathWanderer_World
    import tiles

INITIAL_SIZE = 2
INITIAL_KEYS = 8


class game_cell:
    def __init__(self, cell_type: tiles.game_tile, x: int, y: int, id: int):
        self.cell_type = cell_type
        self.x = x
        self.y = y
        self.id = id
        self.location_name = ""

    def get_type_name(self) -> str:
        for type_name, type_id in tiles.TILE_TYPES:
            if type_id == self.cell_type:
                return type_name
        return "Unknown"

    def get_cell_info(self) -> dict:
        return {
            "type": self.get_type_name(),
            "coords" : (self.x, self.y),
            "id" : self.id,
            "location_name" : self.location_name
        }

    def set_location_name(self, name: str) -> None:
        self.location_name = name



class game_board:
    #currently features a matrix of cells, with the origin at (0, 0) and the top left corner at (-size + 1, -size + 1), 
    def __init__(self, size: int = INITIAL_SIZE):
        self.size = size
        self.cells : dict[int, list[game_cell]] = {}
        self.origin = self.cells[size - 1][size - 1]
                    
        id_counter = 1
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                self.set_cell((dx, dy), tiles.tile_empty())
                if dx == 0 and dy == 0:
                    continue

                self.set_cell((dx, dy), tiles.tile_key(), id_counter)
                id_counter += 1

    def set_cell(self, coords: tuple[int, int], cell_type: tiles.game_tile, location_id: int = 0) -> None:
        x, y = coords
        layer = cell_type.tile_layer
        #check if there is a cell at the given coordinates.
        #If so, update the cell type and id. If not, create a new cell at the given coordinates with the given type and id.
        if self.get_cell(layer, coords) is not None:
            cell = self.get_cell(layer, coords)
            cell.cell_type = cell_type
            cell.id = location_id
        else:
            cell = game_cell(cell_type, x, y, location_id)
            self.cells[layer].append(cell)

    def export(self) -> dict[int, list[game_cell]]:
        return self.cells

    def get_cell(self, layer: int, coords: tuple[int, int]) -> game_cell:
        x, y = coords
        if layer in self.cells:
            for cell in self.cells[layer]:
                if cell.x == x and cell.y == y:
                    return cell
        return None # type: ignore

    def get_cells(self, type: int = -1) -> dict[int, list[game_cell]]:
        if type < 0:
            return self.cells
        else:
            output : dict[int, list[game_cell]] = {}

            for layer in self.cells:
                output.update({layer: []})
                for cell in self.cells[layer]:
                    if cell.cell_type == type:
                        output[layer].append(cell)
            
            return output

    def update_with_item_placements(self, world: PathWanderer_World, item_placement: dict[str, str]) -> None:
        for location_name, item_name in item_placement.items():
            #First, extract the coordinates from the location name string, which is in the format "Location (x, y)"
            cell_coords = location_name.split("(")[-1].split(")")[0].split(",")
            cell_coords = (int(cell_coords[0]), int(cell_coords[1]))

            target_cell = self.get_cell(tiles.TILE_LAYERS["Items"], cell_coords)
            target_cell.set_location_name(location_name)

            #Check whether or not the item is local to this game, if it is not, then the tile type should be set to 5 for ap_item
            if item_name in world.item_name_to_id.keys():
                target_cell.cell_type = tiles.TILE_TYPES[item_name]()
            else:
                target_cell.cell_type = tiles.tile_ap_item()


def generate_game_board(world: PathWanderer_World):
    """
    Creates a matrix of tile types representing the game board.
    Generation starts at tile (0, 0).
    """

    #Determines the maximum possible size of the game board based on the number of keys available
    max_keys = world.options.max_keys
    current_keys = max_keys - INITIAL_KEYS
    current_size = INITIAL_SIZE

    i = 0
    while current_keys - (4 + i) > 0:
        current_keys -= (4 + i)
        current_size += 1
        i += 1

    final_size = current_size +1

    board = game_board()

    #Expands the board until the board size reaches the final size determined earlier
    #Randomly places tiles on each newly generated layer with weights determined by the world options and remaining keys

    expand_board_to_fill(world, board, final_size)
    return board

def expand_board_to_fill(world: PathWanderer_World, board: game_board, final_size: int) -> game_board:
    current_size = INITIAL_SIZE
    current_keys = INITIAL_KEYS
    max_keys = world.options.max_keys

    id_counter = 9
    layer_cost = 4
    required_keys = layer_cost

    flag_count = 0

    while current_size < final_size:
            placed_tiles = 0
            layer_cost += 1
            required_keys += layer_cost
            current_size += 1

            #Retrieve the tile weights from the world options and calculate the total weight for normalization
            tile_weights = tiles.get_rando_weights(world)
            total_weight = sum(tile_weights.values())

            #print("Beginning Layer: "+ str(current_size) + " with " + str(current_keys) + " keys placed and " + str(required_keys) + " required keys.")
            for dx in range(-current_size + 1, current_size):
                for dy in range(-current_size + 1, current_size):
                    #Determines if the current tile has already been placed in a previous layer, and if so, skips it
                    if abs(dx) < current_size - 1 and abs(dy) < current_size - 1:
                        continue

                    #Key Scalar is a value representative of the percentage of keys placed.
                    key_scalar = (current_keys / max_keys)

                    adjusted_weights = {}
                    
                    for tile in tiles.TILE_TYPES:
                        #If the given tile has a weight assigned in options It's target weight is adjusted according to its type
                        initial_weight = 0
    
                        if tile in tile_weights.keys():
                            #Then the adjusted weight is added to the adjusted_weights dictionary
                            initial_weight = tile_weights[tile]
    
                        #current_weight = tile_weights[tile]
                        if tile == tiles.TILE_TYPES["Key"]:
                            current_weight = (initial_weight + (key_scalar/2) * (total_weight - initial_weight))
                        else:
                            current_weight = (initial_weight + (key_scalar/2) * (0 - initial_weight))
    
                        adjusted_weights.update({tile: current_weight/total_weight})
                    #print("Adjusted weights:", adjusted_weights)

                    #Select a tile based on the weights
                    selected_tile = get_random_tile(world, adjusted_weights)
    
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

                    if selected_tile == "Flag":
                        flag_count += 1

                    board.set_cell((dx, dy), tiles.TILE_TYPES[selected_tile](), id_counter)
                    id_counter += 1
                    placed_tiles += 1

    board.size = final_size
 
    if flag_count < world.options.required_flags:
        raise Exception("Not enough flags were placed on the board. Please lower the required flags to " + str(flag_count) + " (or less) or increase the number of keys available.")

    return board

def get_random_tile(world: PathWanderer_World, weights: dict) -> str:
    rand_val = world.multiworld.random.random()
    cumulative_weight = 0
    selected_tile : str = "Empty"
    for tile, weight in weights.items():
        if tile == "Flag":
            continue

        cumulative_weight += weight
        if rand_val < cumulative_weight:
            selected_tile = tile
            break

    return selected_tile

def generate_game_board_file(world, board, path: str = "nil") -> None:
    from pathlib import Path
    import json
    
    board_size = board.size
    
    output_file = {"board_size" : board_size, 
                    "board": board.export(),
                    "cell_types": tiles.TILE_TYPES}
    #Creates a file in the Output folder named game_board_.json containing the board size and the board matrix
    if path == "nil":
        path = Path(__file__).parent / "Output" / "game_board_" + world.multiworld.seed_name + ".json"
    with open(path, "w") as f:
        json.dump(output_file, f)
