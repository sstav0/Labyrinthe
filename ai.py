import random
import rules
from rules import gates
from rules import outlineEast
from rules import outlineNorth
from rules import outlineSouth
from rules import outlineWest


def randomChoice(liste, parameter = None): 
    """This function returns a random item of a list. If "parameter" != None : the value returned by the function will be different from the value of "parameter"

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
            target = parameter[0]
            while target in parameter : 
                target = liste[random.randint(0, len(liste)-1)]
            return target
        else : 
            return liste[random.randint(0, len(liste)-1)]
    else : 
        return liste[0]

def saveMessage(player_number, message):
    """This functions saves any message (dictionary) in a .txt file 

    Parameters
    ----------
        player_number (int): number of the player (0 or 1)
        message (dict): message that's going to be saved in the .txt file
    """
    with open('errors.txt', 'a') as file:
        file.write('LIST OF ERRORS PLAYER {}: {}\n'.format(player_number, message))

def move_test(state: dict, key):                               #! test function that makes a random moves in the legal_moves list and inserts the free tile in a random gate 
    player = state["current"]
    position = state["positions"][player]
    
    saveMessage(player, position)
    
    legal_moves = rules.move(position, state["board"])
    new_pos = randomChoice(legal_moves)
    restriction = rules.columnlist(new_pos, parameter = position)
       
    if key == "tile" : 
        return state["tile"] 
    elif key == "gate&position" :
        legal_moves = rules.move(position, state["board"])  
        new_pos = randomChoice(legal_moves)
        restriction = rules.columnlist(new_pos, parameter = position)
        gateIndex = randomChoice(gates('indexes'), parameter = restriction)
        return gates('letters')[rules.findTarget(gates('indexes'), gateIndex)]
    elif key == "new_pos": 
        return new_pos
    else : 
        print("invalid parameters for 'move_test' function, please write 'tile', 'new_pos' or 'gate'")

