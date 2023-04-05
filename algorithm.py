def foundTreasure(state: dict) -> bool:
    """
    Determines whether the current position of the player is a treasure

    Parameters
    ----------
    state : dict
        Dictionary containing the state of the game including the position of players, treasure location, and current board

    Returns
    -------
    bool
        Returns `True` if the treasure is found (on the current player location), `False` otherwise
    """
    # ! '0' should be the index of our player (depending if we play first or second)
    return state["positions"][0] == state["target"]
    # TODO Target is the id of the treasure not the id of the tile


def moveValue(state) -> int:
    ...


def columnlist(pos) -> list[int]:
    """
    This function returns a list of the tile's indexes of a column or a row with pos, the first tile's index of the row/column

    Parameters
    ----------
    pos : int
        index of the position where the new tile is inserted

    Returns
    -------
    list 
        delta 
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
    else:  # pos in downSide:
        delta = list(range(pos, pos-42-7, -7))
        return delta


def gate(action, parameter=None):
    # Convert gate into index and index into gate. Can also provide row/column gates/indexes.
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
        print("Invalid action for gate function, please use `index`, `letter`, `rowLetters`, `rowIndexes`, `columnLetters`, or `columnIndexes`")


def apply(move: dict, board: list) -> tuple:
    # Apply a move to the board and returning the new board with the new free tile.
    new_column_row = []
    column_row_indexes = columnlist(gate("index", move["gate"]))

    for index in column_row_indexes:
        new_column_row.append(board[index])
    freeTile = new_column_row.pop()
    new_column_row.insert(0, move["tile"])

    for i, index in zip(list(range(0, len(column_row_indexes), 1)), column_row_indexes):
        board[index] = new_column_row[i]
    return board, freeTile


def tile_legal_moves(state) -> list:
    # ! To replace with function that returns the list of moves dictionaries
    legal_moves = [['board', 'move'], ['board', 'move']]
    return legal_moves


def negamaxPruning(state, player, depth=4, alpha=float("-inf"), beta=float("inf")):
    # Returns the value of the board state when we are at the max depth and when we find a treasure
    if depth == 0 or foundTreasure(state):
        return -moveValue(state)

    maxVal = alpha
    for move in tile_legal_moves(state):
        value = -negamaxPruning(move[0], player % 2+1, depth-1, -beta, -alpha)
        maxVal = max(maxVal, value)
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return maxVal
