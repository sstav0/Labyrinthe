import random
import rules
from rules import gates
from rules import outlineEast
from rules import outlineNorth
from rules import outlineSouth
from rules import outlineWest

def randomChoice(liste, parameter = None): 
    """This function returns a random item of a list. If "parameter" != None : the value returned by the function will be different from the value of "parameter

    Parameters
    ----------
    liste : list
        List containing several items
    parameter : list or integer 
        If != None: the value that you want to exclude from the list 

    Returns
    -------
    unknown
        returns a random item of the list; could be str, int,...
    """
        
    if len(liste)>1: 
        
        if parameter != None and type(parameter) == int:
            target = parameter 
            while target == parameter: 
                target = liste[random.randint(0, len(liste)-1)]
            return target
        elif parameter != None and type(parameter)== list: 
            target = liste[1]
            while target in parameter : 
                target = liste[random.randint(0, len(liste)-1)]
            return target
        else : 
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
    
    position = state["positions"][player]
    tile = state["tile"]
    legal_moves = rules.move(position, state["board"])
    
    if legal_moves != []:
        new_pos = randomChoice(legal_moves)
        gateIndex = randomChoice(gates('indexes'), parameter = rules.columnlist(new_pos))
        gateLetter = gates('letters')[rules.findTarget(gates('indexes'), gateIndex)]
  
                    
    else : 
        new_pos = state["positions"][player]
        gateIndex = randomChoice(gates('indexes'), parameter = rules.columnlist(new_pos))
        gateLetter = gates('letters')[rules.findTarget(gates('indexes'), gateIndex)]
            
    if key == "tile" : 
        return tile 
    if key == "gate" :   
        return gateLetter
    if key == "new_pos": 
        return new_pos
    else : 
        print("invalid parameters for 'move_test' function, please write 'tile', 'new_pos' or 'gate'")

