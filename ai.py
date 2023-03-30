import random
import rules

def move(state: dict) -> dict:
    """
    Defines the move to execute

    Parameters
    ----------
    state : dict -- Dictionary from the server containing the state of the game

    Returns
    -------
    dict
        - tile containing its orientation
        - gate in which we insert the tile
        - new position of the tile
    """
    def move_calculator() -> list:
        return [state["state"]["tile"], "A", 1]

    next_move = {
        "tile": move_calculator()[0],
        "gate": move_calculator()[1],
        "new_position": move_calculator()[2]
    }
    return next_move

def move_test(state: dict, player, key = "tile"):                               #! test function that makes a random moves in the legal_moves list and inserts the free tile in a random gate 
    list_gates = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
    
    gate = list_gates[random.randint(0, len(list_gates)-1)]
    tile = state["tile"]
    legal_moves = rules.move(state["positions"][player])
    new_pos = legal_moves[random.randint(0, len(legal_moves)-1)]
    
    if key == "tile" : 
        return tile 
    if key == "gate" : 
        return gate 
    if key == "new_pos": 
        return new_pos
