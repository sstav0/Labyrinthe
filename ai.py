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

def moveRandom(state: dict)->list:    
    """This function returns a random move base on the state passed in parameter

    Parameters
    ----------
    state : dict
        state of the game 

    Returns
    -------
    list
        list containing the tile to insert, the gate where the tile is inserted and the new position of theplayer
    """
    position = state["positions"][state["current"]]
    tile = state["tile"]
    
    gate = randomChoice(Gates().allLetters()) #choosing a random gate among all the gates available
    board = Board(state["board"], tile, position) #creating a board object for the current board
    
    board.update(gate) #updating the board with the tile inserted in the chosen gate 
    legal_moves = rules.move(board.getPos(), board.getBoard()) #creating a list of all possible moves in the new current board
    
    new_pos = randomChoice(legal_moves) #choosing a random move among the possible moves
    return [tile, gate, new_pos]
