import random
import game_board


class Board:
    """This class gathers all functions related to the management of the board: 
    
        "update"
        ---
        Allows to update the board after inserting the tile in one of the available gates
        
        "getPos"
        ---
        Allows to retrieve the position of the player on the board
        
        "getFreeTile"
        ---
        Allows to retrieve the dictionary of the additional tile
        
        "getBoard"
        ---
        Allows to retrieve the dictionary of the board
    """
    outlineNorth = [0, 1, 2, 3, 4, 5, 6]
    outlineEast = [6, 13, 20, 27, 34, 41, 48]
    outlineSouth = [42, 43, 44, 45, 46, 47, 48]
    outlineWest = [0, 7, 14, 21, 28, 35, 42]
    allOutlines = [0, 1, 2, 3, 4, 5, 6, 7, 14, 21, 28, 35,
                   42, 43, 44, 45, 46, 47, 48, 41, 34, 27, 20, 13]

    def __init__(self, board, freeTile, position) -> None:
        self.board = board
        self.freeTile = freeTile
        self.position = position

    def update(self, gate):
        """This function updates the board after sliding the tile in a gate

        Parameters
        ----------
        gate : str      
            letter of the gate
        """ 
        new_column_row = [] #creating a list for the shifted tiles with the old free tile first
        prevFree = self.freeTile #saves the dictionary of the previous free tile

        column_row_indexes = columnlist(Gates().index(gate))

        for index in column_row_indexes:
            # Set the new column/row tiles
            new_column_row.append(self.board[index])
        self.freeTile = new_column_row.pop()  # Saves the ejected free tile
        # Insert the free tile at the start of the column/row
        new_column_row.insert(0, prevFree)

        for i, index in zip(list(range(0, len(column_row_indexes), 1)), column_row_indexes):
            # Updating the original board with the shifted row/column
            self.board[index] = new_column_row[i]

        if self.position in column_row_indexes: #checks if the position of the player is on the gate row/column in which the tile is inserted
            if self.position not in self.allOutlines: #checks if the position is on the outlines of the board and then recalculates it 
                if gate in Gates().eastGates():
                    self.position = self.position - 1
                elif gate in Gates().westGates():
                    self.position = self.position + 1
                elif gate in Gates().northGates():
                    self.position = self.position + 7
                elif gate in Gates().southGates():
                    self.position = self.position - 7
            else:                                       #if the player is on the outlines of the board, he may be returned to the beginning of the row/column
                if gate in Gates().eastGates():
                    if self.position in self.outlineWest:
                        self.position = self.position + 6
                    else:
                        self.position = self.position - 1
                elif gate in Gates().westGates():
                    if self.position in self.outlineEast:
                        self.position = self.position - 6
                    else:
                        self.position = self.position + 1
                elif gate in Gates().northGates():
                    if self.position in self.outlineSouth:
                        self.position = self.position - 42
                    else:
                        self.position = self.position + 7
                elif gate in Gates().southGates():
                    if self.position in self.outlineNorth:
                        self.position = self.position + 42
                    else:
                        self.position = self.position - 7

    def getPos(self):
        return self.position

    def getFreeTile(self):
        return self.freeTile

    def getBoard(self):
        return self.board


class Gates:
    """This class gathers all the functions related to the gates' indexes/letters: 

        "index"
        ---
        Returns the index of a gate's letter
        
        "letter"
        ---
        Returns the letter of a gate's index
        
        "allIndexes"
        ---
        Returns the indexes of every gate
        
        "allLetters"
        ---
        Returns the letters of every gate
        
        "rowIndexes"
        ---
        Returns the indexes of the gates located on the right or left side of the board
        
        "columnIndexes"
        ---
        Return the indexes of the gates located on the top and bottom side of the board
        
        "rowLetters"
        ---
        Returns the letters of the gates located on the right or left side of the board
        
        "columnLetters"
        ---
        Returns the letters of the gates located on the right or left side of the board
        
        "eastGates"
        ---
        Return the gates located on the right of the board
        
        "westGates"
        ---
        Return the gates located on the left of the board
        
        "northGates"
        ---
        Return the gates located on the top of the board
        
        "southGates"
        --- 
        Return the gates located on the right of the board
    """
    def __init__(self) -> None:
        self.__gate_to_index = {
            "A": 1, "B": 3, "C": 5,
            "D": 13, "E": 27, "F": 41,
            "G": 47, "H": 45, "I": 43,
            "J": 35, "K": 21, "L": 7
        }
        self.__index_to_gate = {
            1: "A", 3: "B", 5: "C",
            13: "D", 27: "E", 41: "F",
            47: "G", 45: "H", 43: "I",
            35: "J", 21: "K", 7: "L"
        }

    def index(self, letter: str):
        return self.__gate_to_index[letter]

    def allIndexes(self):
        return [1, 3, 5, 13, 27, 41, 47, 45, 43, 35, 21, 7]

    def rowIndexes(self):
        """
        Output indexes correspond to `["D", "E", "F", "J", "K", "L"]`
        """
        return [13, 27, 41, 35, 21, 7]

    def columnIndexes(self):
        """
        Output indexes correspond to `["A", "B", "C", "G", "H", "I"]`
        """
        return [1, 3, 5, 47, 45, 43]

    def letter(self, index: int):
        return self.__index_to_gate[index]

    def eastGates(self):
        return ["D", "E", "F"]

    def westGates(self):
        return ["L", "K", "J"]

    def northGates(self):
        return ["A", "B", "C"]

    def southGates(self):
        return ["I", "H", "G"]

    def allLetters(self):
        return ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

    def rowLetters(self):
        return ["D", "E", "F", "J", "K", "L"]

    def columnLetters(self):
        return ["A", "B", "C", "G", "H", "I"]


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
    for elem in list:
        if elem == target:
            found = True
            return i
        i += 1
    if not found:
        return 'TARGET NOT FOUND'


def nextIndex(initialPos, direction):
    """Returns the index of the next tile a chosen direction

    Parameters
    ----------
    initialPos : int
        index of the initial tile
    direction : str
        abbreviation of the direction   

    Returns
    -------
    int
        index of the next tile
    """

    if direction == "N" and initialPos not in Board.outlineNorth:
        nextPos = initialPos-7
    elif direction == "S" and initialPos not in Board.outlineSouth:
        nextPos = initialPos + 7
    elif direction == "W" and initialPos not in Board.outlineWest:
        nextPos = initialPos-1
    elif direction == "E" and initialPos not in Board.outlineEast:
        nextPos = initialPos + 1
    else:
        nextPos = initialPos
    return nextPos


def oppositeDirection(direction):
    """ This function returns the opposite direction of direction given

    Parameters
    ----------
    direction : str
        "N"; "S"; "W"; "O" 

    Returns
    -------
    str
        The opposite direction 
    """
    opposite = None
    directions = {"N": "S", "W": "E"}
    for key, value in directions.items():
        if direction == key:
            opposite = value
        elif direction == value:
            opposite = key
    return opposite


def columnlist(pos) -> list:
    """This function returns a list of the tile's indexes of a column or a row with pos, the first tile's index of the row/column

    Parameters
    ----------
    pos : int
        index of the position where the new tile is inserted
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

    if pos in upSide:
        delta = list(range(pos, pos+42+7, 7))
        return delta
    elif pos in leftSide:
        delta = list(range(pos, pos+7, 1))
        return delta
    elif pos in rightSide:
        delta = list(range(pos, pos-7, -1))
        return delta
    else:
        delta = list(range(pos, pos-42-7, -7))
        return delta


def move(initialPos, board):
    """This function returns a list of the possible moves (positions)

    Parameters
    ----------
    initialPos : int
        initial position
    board : list
        list of the dictionaries referring to the walls and free ways of each tile on the board

    Returns
    -------
    list 
        list of the legal moves. It contains at least the initial position
    """
    board_legalMoves = [initialPos]
    
    for direction, value in board[initialPos].items(): #iters through the dictionary of the initial tile
        if direction != "item": #checks if it's not iterating through the item of the tile
            if value == True:  #if the value is true means that there is no wall in that orientation
                nextTile = nextIndex(initialPos, direction) #nextTile is your next position if you'd move in the direction
                if board[nextTile][oppositeDirection(direction)] == True and nextTile != initialPos: #checks if there is a wall in the direction on the next Tile (/!\ the next tile's direction is the opposite of the previous tile's direction)
                    
                    board_legalMoves.append(nextTile) #if there is no wall, it adds the next tile's index in the legal moves list
        else:
            pass 
    return board_legalMoves
