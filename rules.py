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

def columnlist(pos):
    """function that returns a list of the tile's indexes of a column or a row with pos, the first tile's index of the row/column

    Args:
        pos (int): index of the position where the new tile is inserted

    Returns:
        delta(list)
    """
    delta = []
    
    upSide = [1, 3, 5]
    leftSide = [7, 21, 35]
    rightSide = [13, 27, 41]
    downSide = [43, 45, 47]
    if pos in upSide : 
        delta = list(range(pos, pos+42+7, 7))
        return delta
    if pos in leftSide:
        delta = list(range(pos, pos+7+1, 1))
        return delta 
    if pos in rightSide: 
        delta = list(range(pos, pos-7-1, -1))
        return delta 
    if pos in downSide: 
        delta = list(range(pos, pos-42-7, -7))
        return delta 
    
    
        
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
    for direction, value in board[initialPos].items():                      #* iters through the dictionary of the initial tile
        if value == True :                                                  #* if the value is true means that there is no wall in that orientation 
            nextTile = nextIndex(initialPos, direction)                     #* nextTile is the index (= position) of your next position if you move in the direction 
            if board[nextTile][oppositeDirection(direction)] == True:       #* checks if there is a wall in the direction on the next Tile (/!\ the next tile's direction is the opposite of the previous tile's direction)
                board_legalMoves.append(nextIndex(initialPos, direction))   #* if there is no wall, it adds the next tile's index in the legal moves list
    return board_legalMoves


def insertTile(tile, pos, board):
    """function that takes the free tile, the position where you want to insert the free tile and the actual board in parameters and then 
    returns the updated board (after shifting the row/column)

    Args:
        tile (dict): description of the tile (with directions and walls)
        pos (int): index position on the board where you want to insert the free tile
        board (list): description of the actual board

    Returns:
        updated board (list): the updated board, after shifting the row/column
    """
    global nextTile                                                     #*making the variable containing the next free tile global 
                                                                        #? maybe the function could return the nextTile variable instead of making it global
    indexes = columnlist(pos)                                           #* list of the tile's indexes of the row/column that's gonna be shifted
    savedBoard = []                                                     #* empty list that's gonna be filled with the original tiles of the row/column that's gonna be shifted
    
    for index in indexes :                                              
        savedBoard.append(board[index])                                 #*filling in the savedBoard list with the orignal tiles of the row/column 
    nextTile = savedBoard.pop()                                         #*taking the last tile (the one that's gonna fall of the board) off the list and saving it in nextTile for later on
    savedBoard.insert(0, tile)                                          #*putting the previous free tile in the beginning/end of the column/row (depending on which side you insert the free tile)
    
    for i, index in zip(list(range(0, len(indexes), 1)),indexes) :      #*iterating through two lists at the same time : the first one is a list containing the indexes of the indexes list (we also could have created a variable i=0 outside of the loop and incrementing it at each turn of the loop)
        board[index] = savedBoard[i]                                    #*updating the original board with the shifted row/column
    return board                                          


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
print(insertTile("O", 47, list(range(0, 49, 1))))