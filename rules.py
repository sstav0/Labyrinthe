import random
import game_board

def gates(action: str, parameter=None):
    """
    Give all gates information depending on the action inserted.
    Parameters
    ----------
    action : str
        Say which information should be returned.
    parameter : str | int, optional
        Gate or gate's index if a particular gate is search with `index` or `letter`, by default None.
    Actions
    -------
        - `index` : Returns all gates indexes. If a letter is provided in `parameter`, returns that gate index.
        - `letter` : Returns all gates letters. If an index is provided in `parameter`, returns that gate letter.
        - `rowLetters` : Returns all row gates letters.
        - `rowIndexes` : Returns all row gates indexes.
        - `columnLetters` : Returns all column gates letters.
        - `columnIndexes` : Returns all column gates indexes.
    Returns
    -------
    int | list[int] | str | list[str]
        Depend on the action.
    """
    # Convert gate into index and index into gate
    gate_to_index = {
        "A": 1, "B": 3, "C": 5,
        "D": 13, "E": 27, "F": 41,
        "G": 47, "H": 45, "I": 43,
        "J": 35, "K": 21, "L": 7
    }
    index_to_gate = {
        1: "A", 3: "B", 5: "C",
        13: "D", 27: "E", 41: "F",
        47: "G", 45: "H", 43: "I",
        35: "J", 21: "K", 7: "L"
    }

    if action == "index":
        if parameter is not None:
            return gate_to_index[parameter]

        indexes: list[int] = []
        for index in gate_to_index.values():
            indexes.append(index)
        return indexes  # [1, 3, 5, 13, 27, 41, 47, 45, 43, 35, 21, 7]

    elif action == "letter":
        if parameter is not None:
            return index_to_gate[parameter]

        gates: list[str] = []
        for gate in index_to_gate.values():
            gates.append(gate)
        return gates
        # ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

    elif action == "rowLetters":
        return ["D", "E", "F", "J", "K", "L"]
    elif action == "rowIndexes":
        return [13, 27, 41, 35, 21, 7]
    elif action == "columnLetters":
        return ["A", "B", "C", "G", "H", "I"]
    elif action == "columnIndexes":
        return [1, 3, 5, 47, 45, 43]
    else:
        print("Invalid action for gate function, please use `index`, `letter`, `rowLetters`, `rowIndexes`, `columnLetters` or `columnIndexes`")



def findTarget(list, target):
    """This functions searches for a target in a list and returns its index if found 

    Parameters
    ----------
    list : list
        list in which the target may be 
    target : unknown 
        the element to search for

    Returns
    -------
    str 
        error message 'TARGET NOT FOUND'
    
    OR
    
    unknown 
        the target
    """
    found = False
    i = 0
    for elem in list : 
        if elem == target:
            found = True
            return i 
        i+=1
    if not found: 
        return 'TARGET NOT FOUND'

def outlineNorth():
    return [0, 1, 2, 3, 4, 5, 6]
def outlineWest():
    return [0, 7, 14, 21, 28, 35, 42]
def outlineEast():
    return [6, 13, 20, 27, 34, 41, 48]
def outlineSouth():
    return [42, 43, 44, 45, 46, 47, 48]

def nextIndex(initialPos, direction): 
    """Function that computes the index of the next position with the current position and the direction as inputs

    Parameters
    ----------
        initialPos (int): index of the initial position 
        direction (string): abbreviation of the direction  

    Returns
    -------
    int
        index of the next position 
    """
    
    if direction == "N" and initialPos not in outlineNorth():
        nextPos = initialPos-7 
        #print(f"NORTH: {outlineNorth}; {nextPos}")
    elif direction == "S" and initialPos not in outlineSouth():
        nextPos = initialPos + 7 
        #print(f"SOUTH: {outlineSouth}; {nextPos}")
    elif direction == "W" and initialPos not in outlineWest():
        nextPos = initialPos-1 
        #print(f"WEST: {outlineWest}; {nextPos}")
    elif direction == "E" and initialPos not in outlineEast():
        nextPos = initialPos + 1
        #print(f"EAST: {outlineEast}; {nextPos}") 
    else : 
        #print(f"FAILED; {initialPos}")
        nextPos = initialPos
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

def columnlist(pos, parameter = None)->list:
    """This function returns a list of the tile's indexes of a column or a row with pos, the first tile's index of the row/column

    Parameters
    ----------
    pos : int
        index of the position where the new tile is inserted
    parameter : int 
        Integer to add in the returned list (delta)

    Returns
    -------
    list 
        column or row of the position passed in parameters
    """
    delta = []
    upSide = [1, 3, 5]
    leftSide = [7, 21, 35]
    rightSide = [13, 27, 41]
    downSide = [43, 45, 47]
    if parameter!=None:
        delta.append(parameter)
    else:
        if pos in upSide : 
            delta = list(range(pos, pos+42+7, 7))
            return delta
        elif pos in leftSide:
            delta = list(range(pos, pos+7, 1))
            return delta 
        elif pos in rightSide: 
            delta = list(range(pos, pos-7, -1))
            return delta 
        elif pos in downSide: 
            delta = list(range(pos, pos-42-7, -7))
            return delta 

def dontMove(initialPos):
    return [initialPos]
        
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
    board_legalMoves = [initialPos]
    for direction, value in board[initialPos].items():                      #* iters through the dictionary of the initial tile
        if value == True :                                                  #* if the value is true means that there is no wall in that orientation 
            nextTile = nextIndex(initialPos, direction)                     #* nextTile is your next position if you move in the direction 
            #print(f"---------\ndirection:{direction}\nvalue: {value}\nnextTile: {nextTile}")
            if board[nextTile][oppositeDirection(direction)] == True and nextTile != initialPos:                  #* checks if there is a wall in the direction on the next Tile (/!\ the next tile's direction is the opposite of the previous tile's direction)
                board_legalMoves.append(nextTile)                                                                   #* if there is no wall, it adds the next tile's index in the legal moves list
    return board_legalMoves


def insertTile(tile, pos, board):
    """This function takes the free tile, the position where you want to insert the free tile and the actual board in parameters and then 
    returns the updated board (after shifting the row/column)

    Parameters
    ----------
    tile : dict
        description of the tile (with directions and walls)
    pos : int
        index position on the board where you want to insert the free tile
    board : list
        description of the actual board

    Returns
    -------
    board : list
        the updated board, after shifting the row/column
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

def apply(move: dict, board: list) -> tuple[list, dict]:
    """
    Apply a move to the board and return the new board with the new free tile.
    Parameters
    ----------
    move : dict
        Move to apply to the board, containing the free tile, the gate, and the new position of the player.
    board : list
        Current state of the board.
    Returns
    -------
    tuple[list, dict]
        New board and new free tile after applying the move.
    """
    new_column_row = []
    
    column_row_indexes = columnlist(gates("index", move["gate"]))

    for index in column_row_indexes:
        new_column_row.append(board[index])  # Set the new column/row tiles
    freeTile = new_column_row.pop()  # Saves the ejected free tile
    # Insert the free tile at the start of the column/row
    new_column_row.insert(0, move["tile"])

    for i, index in zip(list(range(0, len(column_row_indexes), 1)), column_row_indexes):
        # Updating the original board with the shifted row/column
        board[index] = new_column_row[i]
    return board, freeTile