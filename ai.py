import random
import rules
from rules import Gates
from rules import Board

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

def moveRandom(state: dict):                               #! test function that makes a random moves in the legal_moves list and inserts the free tile in a random gate 
    current = state["current"]
    position = state["positions"][current]
    tile = state["tile"]
    gate = randomChoice(Gates().allLetters())
    board = Board(state["board"], tile, position)
    print(f"GATELETTER: {gate}")
    print(f"POSITION: {position}")
    new_board, new_tile, position2 = board.update(gate, position)
    #board = rules.apply({"tile": tile, "gate": gateLetter, "new_position": position}, state["board"])[0]
    legal_moves = rules.move(position2, new_board) 
    new_pos = randomChoice(legal_moves)
    return [new_tile, gate, new_pos]

state = {'players': ['AImazing0', 'AImazing3'], 'current': 0, 'positions': [1, 48], 'board': [{'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, {'N': False, 'E': True, 'S': True, 'W': True, 'item': 0}, {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, {'N': False, 'E': True, 'S': True, 'W': True, 'item': 1}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': 14}, {'N': False, 'E': True, 'S': True, 'W': False, 'item': 17}, {'N': True, 'E': True, 'S': False, 'W': True, 'item': 23}, {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': True, 'S': True, 'W': False, 'item': 2}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': True, 'S': True, 'W': False, 'item': 3}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, {'N': False, 'E': True, 'S': True, 'W': True, 'item': 4}, {'N': True, 'E': True, 'S': False, 'W': True, 'item': 21}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 5}, {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': True, 'S': True, 'W': False, 'item': 19}, {'N': True, 'E': True, 'S': True, 'W': False, 'item': 6}, {'N': True, 'E': True, 'S': False, 'W': True, 'item': 22}, {'N': True, 'E': True, 'S': False, 'W': True, 'item': 7}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 8}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 9}, {'N': False, 'E': False, 'S': True, 'W': True, 'item': 15}, {'N': False, 'E': True, 'S': True, 'W': False, 'item': 13}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': 12}, {'N': True, 'E': True, 'S': True, 'W': False, 'item': 20}, {'N': False, 'E': True, 'S': True, 'W': True, 'item': 18}, {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, {'N': False, 'E': True, 'S': True, 'W': False, 'item': 16}, {'N': True, 'E': True, 'S': False, 'W': True, 'item': 10}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': True, 'S': False, 'W': True, 'item': 11}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}], 'tile': {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 'target': 3, 'remaining': [4, 4]}
print(moveRandom(state))