import copy
from typing import Union


class Board:
    """This class gathers all functions related to the management of the board: 

        "update"
        ---
        Allows to update the board after inserting the tile in one of the available gates

        "getPos"
        ---
        Allows to retrieve the positions of the players on the board

        "getFreeTile"
        ---
        Allows to retrieve the dictionary of the additional tile

        "getBoard"
        ---
        Allows to retrieve the dictionary of the board

        "undo"
        ---
        Cancels the previous update on the board
    """
    outlineNorth = [0, 1, 2, 3, 4, 5, 6]
    outlineEast = [6, 13, 20, 27, 34, 41, 48]
    outlineSouth = [42, 43, 44, 45, 46, 47, 48]
    outlineWest = [0, 7, 14, 21, 28, 35, 42]
    allOutlines = [0, 1, 2, 3, 4, 5, 6, 7, 14, 21, 28, 35,
                   42, 43, 44, 45, 46, 47, 48, 41, 34, 27, 20, 13]

    def __init__(self, board: list[dict], freeTile: dict, positions: list) -> None:
        self.__board = copy.deepcopy(board)
        self.__freeTile = copy.deepcopy(freeTile)
        self.__positions = copy.deepcopy(positions)
        self.__oldBoard = []
        self.__oldPos = []
        self.__oldFree = {}

    def update(self, gate: str) -> None:
        """This function updates the board after sliding the tile in a gate

        Parameters
        ----------
        gate : str      
            letter of the gate
        """
        self.__oldBoard = copy.deepcopy(self.__board)
        self.__oldPos = copy.deepcopy(self.__positions)
        self.__oldFree = copy.deepcopy(self.__freeTile)
        new_column_row = []  # creating a list for the shifted tiles with the old free tile first
        prevFree = self.__freeTile  # saves the dictionary of the previous free tile

        column_row_indexes = columnList(Gates().index(gate))

        for index in column_row_indexes:
            # Set the new column/row tiles
            new_column_row.append(self.__board[index])
        self.__freeTile = new_column_row.pop()  # Saves the ejected free tile
        # Insert the free tile at the start of the column/row
        new_column_row.insert(0, prevFree)

        for i, index in zip(list(range(0, len(column_row_indexes))), column_row_indexes):
            # Updating the original board with the shifted row/column
            self.__board[index] = new_column_row[i]

        for i, position in enumerate(self.__positions):
            # checks if the position of the player is on the gate row/column in which the tile is inserted
            if position in column_row_indexes:
                # checks if the position is not on the outlines of the board and then recalculates it
                if position not in self.allOutlines:
                    if gate in Gates().eastGates():
                        self.__positions[i] = self.__positions[i] - 1
                    elif gate in Gates().westGates():
                        self.__positions[i] = self.__positions[i] + 1
                    elif gate in Gates().northGates():
                        self.__positions[i] = self.__positions[i] + 7
                    elif gate in Gates().southGates():
                        self.__positions[i] = self.__positions[i] - 7
                else:  # if the player is on the outlines of the board, he may be returned to the beginning of the row/column
                    if gate in Gates().eastGates():
                        if position in self.outlineWest:
                            self.__positions[i] = self.__positions[i] + 6
                        else:
                            self.__positions[i] = self.__positions[i] - 1
                    elif gate in Gates().westGates():
                        if position in self.outlineEast:
                            self.__positions[i] = self.__positions[i] - 6
                        else:
                            self.__positions[i] = self.__positions[i] + 1
                    elif gate in Gates().northGates():
                        if position in self.outlineSouth:
                            self.__positions[i] = self.__positions[i] - 42
                        else:
                            self.__positions[i] = self.__positions[i] + 7
                    elif gate in Gates().southGates():
                        if position in self.outlineNorth:
                            self.__positions[i] = self.__positions[i] + 42
                        else:
                            self.__positions[i] = self.__positions[i] - 7

    def findItem(self, item: int) -> Union[int, None]:
        """This function returns the position of [item]

        Parameters
        ----------
        item : int
            item number

        Returns
        -------
        int
            position of the item 
        """
        found = False
        for i, tile in enumerate(self.__board):
            if tile["item"] == item:
                found = True
                return i
        if not found:
            print("ITEM {} NOT FOUND".format(chr(ord("A")+item)))
            return None

    def changeTile(self, free: dict) -> None:
        self.__freeTile = free

    def getPos(self, index: int) -> int:
        return self.__positions[index]

    def getFreeTile(self) -> dict:
        return self.__freeTile

    def getBoard(self) -> list:
        return self.__board

    def undo(self) -> None:
        self.__board = self.__oldBoard
        self.__freeTile = self.__oldFree
        self.__positions = self.__oldPos


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

    def index(self, letter: str) -> int:
        return self.__gate_to_index[letter]

    def allIndexes(self) -> list[int]:
        return [1, 3, 5, 13, 27, 41, 47, 45, 43, 35, 21, 7]

    def rowIndexes(self) -> list[int]:
        """
        Output indexes correspond to `["D", "E", "F", "J", "K", "L"]`
        """
        return [13, 27, 41, 35, 21, 7]

    def columnIndexes(self) -> list[int]:
        """
        Output indexes correspond to `["A", "B", "C", "G", "H", "I"]`
        """
        return [1, 3, 5, 47, 45, 43]

    def letter(self, index: int) -> str:
        return self.__index_to_gate[index]

    def eastGates(self) -> list[str]:
        return ["D", "E", "F"]

    def westGates(self) -> list[str]:
        return ["L", "K", "J"]

    def northGates(self) -> list[str]:
        return ["A", "B", "C"]

    def southGates(self) -> list[str]:
        return ["I", "H", "G"]

    def allLetters(self) -> list[str]:
        return ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

    def rowLetters(self) -> list[str]:
        return ["D", "E", "F", "J", "K", "L"]

    def columnLetters(self) -> list[str]:
        return ["A", "B", "C", "G", "H", "I"]

    def exceptGate(self, pos, move):
        """This function takes the gate that is on the same row/column of the position and next position(move) passed in parameter

        Parameters
        ----------
        pos : int
            position 
        move : _type_
            next position

        Returns
        -------
        list
            list of the gate letters that are not on the same column/row of the position and next position
        """
        list = []
        for gate in Gates().allIndexes():
            if pos in columnList(gate) or move in columnList(gate):
                pass
            else:
                list.append(self.letter(gate))
        return list


def nextIndex(initialPos: int, direction: str) -> int:
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


def oppositeDirection(direction: str) -> str:
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
    opposite = ""
    directions = {"N": "S", "W": "E"}
    for key, value in directions.items():
        if direction == key:
            opposite = value
        elif direction == value:
            opposite = key
    return opposite


def orientations(tile: dict) -> list[dict]:
    """
    Takes a tile and returns its 4 orientations.

    Parameters
    ----------
    tile : dict
        The tile for which we want all orientations.
        The tile should be as follows :
        ```
        {"N": true, "E": false, "S": true, "W": true, "item": 1}
        ```

    Returns
    -------
    list[dict]
        List of all 4 orientations of the tile.
    """
    N, E, S, W = tile["N"], tile["E"], tile["S"], tile["W"]

    result = []
    # Rotates 4 times for each orientation
    for i in range(4):
        result.append({
            "N": N,
            "E": E,
            "S": S,
            "W": W,
            "item": tile["item"]
        })
        N, E, S, W = E, S, W, N  # Rotate the boolean values
    return result


def columnList(pos: int) -> list:
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


def playerLegalMoves(initialPos: int, board: list) -> list[int]:
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

    # iters through the dictionary of the initial tile
    for direction, value in board[initialPos].items():
        if direction != "item":  # checks if it's not iterating through the item of the tile
            if value == True:  # if the value is true means that there is no wall in that orientation
                # nextTile is your next position if you'd move in the direction
                nextTile = nextIndex(initialPos, direction)
                # checks if there is a wall in the direction on the next Tile (/!\ the next tile's direction is the opposite of the previous tile's direction)
                if board[nextTile][oppositeDirection(direction)] == True and nextTile != initialPos:
                    # if there is no wall, it adds the next tile's index in the legal moves list
                    board_legalMoves.append(nextTile)
        else:
            pass
    return board_legalMoves


def cartesian(target: int) -> tuple:
    """This function returns the cartesian coordinates of a tile on the board

    Parameters
    ----------
    target : int
        the position to be converted into Cartesian coordinates

    Returns
    -------
    tuple
        the x and y coordinates 
    """
    x = target % 7
    y = 0
    rows = [range(0, 7), range(7, 14), range(14, 21), range(
        21, 28), range(28, 35), range(35, 42), range(42, 49)]
    i = 7
    for row in rows:
        i -= 1
        if target in row:
            y = i
    return (x, y)


def distance(pos: int, item: int) -> int:
    """This function calculates the distance between the player's position and the item he has to find

    Parameters
    ----------
    pos : int
        index position of the player
    item : int
        index position of the item targeted

    Returns
    -------
    float
        distance 
    """
    cartPos = cartesian(pos)
    cartItem = cartesian(item)
    d1 = abs(cartPos[0]-cartItem[0])
    d2 = abs(cartPos[1]-cartItem[1])
    return d1+d2
