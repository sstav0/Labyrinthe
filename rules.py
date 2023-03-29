import random

def nextIndex(initialPos, direction): 
    """Function that computes the index of the next position with the current position and the direction as inputs

    Args:
        initialPos (int): index of the initial position 
        direction (string): abbreviation of the direction  

    Returns:
        int: index of the next position 
    """
    
    if direction == "N":
        nextPos = initialPos - 7 
    if direction == "S": 
        nextPos = initialPos + 7 
    if direction == "W": 
        nextPos = initialPos - 1 
    if direction == "E": 
        nextPos = initialPos + 1
    return nextPos

def oppositeDirection(direction):
    """ This function returns the opposite direction of the parameter 

    Parameters
    ----------
    direction : string
        North, South, East, West 

    Returns
    -------
    string
        North, South, East, West 

    """
    directions = {"N": "S", "W": "E"}
    for key, value in directions.items():
        if direction == key : 
            opposite = value
        elif direction == value:
            opposite = key 
    return opposite
        
def move(initialPos, board): 
    """This function returns a list of the index of the tiles that are accessible => legal moves

    Parameters
    ----------
    initialPos : int
        index of the initial tile
    board : list
        list of the dictionaries referring to the walls and free ways of each tile on the board

    Returns
    -------
    list 
        list of the legal moves; if the list is empty, you are trapped! 
    """
    board_legalMoves = []
    for orientation, value in board[initialPos].items(): 
        if value == True : 
            nextTile = nextIndex(initialPos, orientation)
            if board[nextTile][oppositeDirection(orientation)] == True:
                board_legalMoves.append(nextIndex(initialPos, orientation))
    return board_legalMoves

                
board = [
    {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, 
    {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
    {'N': False, 'E': True, 'S': True, 'W': True, 'item': 0}, 
    {'N': True, 'E': True, 'S': False, 'W': False, 'item': 17}, 
    {'N': False, 'E': True, 'S': True, 'W': True, 'item': 1}, 
    {'N': True, 'E': False, 'S': True, 'W': True, 'item': 23}, 
    {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, 
    {'N': True, 'E': True, 'S': False, 'W': True, 'item': 19}, 
    {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
    {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, 
    {'N': True, 'E': True, 'S': False, 'W': True, 'item': 22}, 
    {'N': True, 'E': False, 'S': False, 'W': True, 'item': 15}, 
    {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, 
    {'N': True, 'E': True, 'S': False, 'W': True, 'item': 18}, 
    {'N': True, 'E': True, 'S': True, 'W': False, 'item': 2}, 
    {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, 
    {'N': True, 'E': True, 'S': True, 'W': False, 'item': 3}, 
    {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
    {'N': False, 'E': True, 'S': True, 'W': True, 'item': 4}, 
    {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, 
    {'N': True, 'E': False, 'S': True, 'W': True, 'item': 5}, 
    {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, 
    {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, 
    {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, 
    {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, 
    {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, 
    {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, 
    {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, 
    {'N': True, 'E': True, 'S': True, 'W': False, 'item': 6}, 
    {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, 
    {'N': True, 'E': True, 'S': False, 'W': True, 'item': 7}, 
    {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
    {'N': True, 'E': False, 'S': True, 'W': True, 'item': 8}, 
    {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
    {'N': True, 'E': False, 'S': True, 'W': True, 'item': 9}, 
    {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, 
    {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, 
    {'N': True, 'E': False, 'S': True, 'W': True, 'item': 21}, 
    {'N': False, 'E': False, 'S': True, 'W': True, 'item': 13}, 
    {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
    {'N': True, 'E': False, 'S': False, 'W': True, 'item': 14}, 
    {'N': True, 'E': False, 'S': True, 'W': True, 'item': 20}, 
    {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, 
    {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, 
    {'N': True, 'E': True, 'S': False, 'W': True, 'item': 10}, 
    {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
    {'N': True, 'E': True, 'S': False, 'W': True, 'item': 11}, 
    {'N': True, 'E': True, 'S': False, 'W': False, 'item': 12}, 
    {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}
]

print(move(27,board))