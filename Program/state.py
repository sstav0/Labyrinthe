import copy
from typing import Union

def showBoard(board: list):
    mat = []
    for i in range(28):
        mat.append([])
        for j in range(28):
            mat[i].append(" ")
    for index, value in enumerate(board):
        i = (index // 7) * 4
        j = (index % 7) * 4
        mat[i][j] = "#"
        mat[i][j + 1] = "#" if not value["N"] else " "
        mat[i][j + 2] = "#"
        mat[i][j + 3] = "|"
        mat[i + 1][j] = "#" if not value["W"] else " "
        mat[i + 1][j + 1] = (
            " " if value["item"] is None else chr(ord("A") + value["item"])
        )
        mat[i + 1][j + 2] = "#" if not value["E"] else " "
        mat[i + 1][j + 3] = "|"
        mat[i + 2][j] = "#"
        mat[i + 2][j + 1] = "#" if not value["S"] else " "
        mat[i + 2][j + 2] = "#"
        mat[i + 2][j + 3] = "|"
        mat[i + 3][j] = "-"
        mat[i + 3][j + 1] = "-"
        mat[i + 3][j + 2] = "-"
        mat[i + 3][j + 3] = "-"

    return "\n".join(["".join(line) for line in mat])

def playerLegalMoves(initialPos: int, board: list) -> list[int]:
    """
    This function returns a list of the possible moves (positions).

    Parameters
    ----------
    initialPos : int
        initial position
    board : list
        list of the dictionaries referring to the walls and free ways of each tile on the board

    Returns
    -------
    list[int]
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

class Board:
    """
    This class gathers all functions related to the management of the board: 

    `update`
    ---
    Allows to update the board after inserting the tile in one of the available gates.

    `getPos`
    ---
    Allows to retrieve the positions of the players on the board.

    `getFreeTile`
    ---
    Allows to retrieve the dictionary of the additional tile.

    `getBoard`
    ---
    Allows to retrieve the dictionary of the board.

    `undo`
    ---
    Cancels the previous update on the board.
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
        """
        This function updates the board after sliding the tile in a gate

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
        """
        This function returns the position on the board of [item].

        Parameters
        ----------
        item : int
            item number

        Returns
        -------
        int
            position of the item on the board
        """
        found = False
        for i, tile in enumerate(self.__board):
            if tile["item"] == item:
                found = True
                return i
        if not found:
            #print("ITEM {} NOT FOUND".format(chr(ord("A")+item)))
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


def nextIndex(initialPos: int, direction: str) -> int:
    """
    Returns the index of the next tile in a chosen direction.

    Parameters
    ----------
    initialPos : int
        index of the initial tile
    direction : str
        abbreviation of the direction `N`, `E`, `S`, or `W`

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

def orientations(tile: dict) -> list[dict]:
    """
    Takes a tile and returns its 4 orientations.

    Parameters
    ----------
    tile : dict
        The tile for which we want all orientations. The tile should be as follows :
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


if __name__ == "__main__":

    state = {'players': ['AImazing1', 'AImazing0'], 'current': 0, 'positions': [0, 47], 'target': 17, 'remaining': [3, 4], 'tile': {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, 'board': [{'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': 14}, {'N': False, 'E': True, 'S': True, 'W': True, 'item': 0}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, {'N': False, 'E': True, 'S': True, 'W': True, 'item': 1}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': 15}, {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': True, 'S': True, 'W': False, 'item': 2}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': 12}, {'N': True, 'E': True, 'S': True, 'W': False, 'item': 3}, {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, {'N': False, 'E': True, 'S': True, 'W': True, 'item': 4}, {'N': False, 'E': True, 'S': True, 'W': True, 'item': 21}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 5}, {'N': False, 'E': True, 'S': True, 'W': True, 'item': 19}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': 13}, {'N': True, 'E': True, 'S': False, 'W': True, 'item': 22}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 20}, {
        'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': True, 'S': True, 'W': False, 'item': 6}, {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, {'N': True, 'E': True, 'S': False, 'W': True, 'item': 7}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 8}, {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 9}, {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': 17}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 23}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 18}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': True, 'S': False, 'W': True, 'item': 10}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': 16}, {'N': True, 'E': True, 'S': False, 'W': True, 'item': 11}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}]}
    
    state["board"][0]["E"] = False
    state["board"][0]["S"] = False
    print(showBoard(state["board"]))
    print("POSITION: {}".format(state["positions"][state["current"]]))
    print("\n\nMOVES: {}".format(playerLegalMoves(state["positions"][state["current"]], state["board"])))