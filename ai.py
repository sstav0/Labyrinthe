import random
import rules
from rules import gates

def randomChoice(liste): 
    """This function returns a random item of the list passed in parameter

    Parameters
    ----------
    liste : list
        List containing several items

    Returns
    -------
    unknown
        returns a random item of the list; could be str, int,...
    """
    if len(liste)>1: 
        return liste[random.randint(0, len(liste)-1)]
    else : 
        return liste[0]


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

def move_test(state: dict, player, key):                               #! test function that makes a random moves in the legal_moves list and inserts the free tile in a random gate 
    
    tile = state["tile"]
    legal_moves = rules.move(state["positions"][player], state["board"])
    
    if legal_moves != []:
        new_pos = randomChoice(legal_moves)
        gate = randomChoice(gates('letters'))
    else:
        i=0
        found = False
        for index in gates('indexes'): 
            if state["positions"][player] == rules.columnlist(index) : 
                gate = gates('letters')[i]
                found = True  
            i+=1
        if not found : 
            new_pos = state["positions"][player]
            gate = randomChoice(gates('letters'))
            
    if key == "tile" : 
        return tile 
    if key == "gate" :   
        return gate 
    if key == "new_pos": 
        return new_pos
    else : 
        print("invalid parameters for 'move_test' function, please write 'tile', 'new_pos' or 'gate'")

