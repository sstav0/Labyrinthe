def foundTreasure(board: list, playerPos: list[int], playerIndex: int, targetId: int) -> bool:
    """
    Determines if the tile at the position of the player contains a treasure.

    Parameters
    ----------
    board : list
        Actual state of the board.
    playerPos : list[int]
        List containing the index of the tile at the position of each player.
    playerIndex : int
        Index of the current player needed to pick the right index from `playerPos`.
    targetId : int
        Contains the ID of the treasure to reach (to not be confused with the index of the tile).

    Returns
    -------
    bool
        Returns `True` if the treasure is found (on the current player location), `False` otherwise.
    """
    # return state["board"][state["positions"][state["current"]]]["item"] == state["target"]
    return board[playerPos[playerIndex]]["item"] == targetId


# TODO Function that returns the value of a given move depending on the current state of the game
def moveValue() -> int:
    ...


def columnlist(pos) -> list[int]:
    """
    This function returns a list of the tile's indexes of a column or row.

    Parameters
    ----------
    pos : int
        Index of the position where the new tile is inserted.

    Returns
    -------
    list 
        All indexes of the column/row.
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


def gate(action: str, parameter=None):
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
    column_row_indexes = columnlist(gate("index", move["gate"]))

    for index in column_row_indexes:
        new_column_row.append(board[index])  # Set the new column/row tiles
    freeTile = new_column_row.pop()  # Saves the ejected free tile
    # Insert the free tile at the start of the column/row
    new_column_row.insert(0, move["tile"])

    for i, index in zip(list(range(0, len(column_row_indexes), 1)), column_row_indexes):
        # Updating the original board with the shifted row/column
        board[index] = new_column_row[i]
    return board, freeTile


# TODO Function that returns the list of all legal moves dictionaries
def tile_legal_moves(board: list, tile: dict) -> list:
    legal_moves = ["move dico", "move2 dico"]
    return legal_moves


def negamaxPruning(board: list, tile: dict, playerPos: list[int], playerIndex: int, targetId: int, player, depth: int = 4, alpha=float("-inf"), beta=float("inf")):
    """
    Negamax algorithm using alpha-beta pruning to find the best move (with the best value) for a given state of the game.

    Parameters
    ----------
    board : list
        Current state of the board.
    tile : dict
        Current free tile to be inserted.
    playerPos : list[int]
        List containing the index of the tile at the position of each player.
    playerIndex : int
        Index of the current player needed to pick the right index from `playerPos`.
    targetId : int
        Contains the ID of the treasure to reach (to not be confused with the index of the tile).
    player : 
        Current playing player.
    depth : int, optional
        Depth of the recursive algorithm, by default 4.
    alpha : int | float, optional
        Actual highest move value, by default float("-inf").
    beta : int | float, optional
        Actual lowest move value, by default float("inf").

    Returns
    -------
    tuple[int, dict]
        Best value with the best move to play.
    """
    # Returns the value of the board state when we are at the max depth and when we find a treasure
    if depth == 0 or foundTreasure(board, playerPos, playerIndex, targetId):
        return -moveValue(), None

    bestVal = alpha
    bestMove = None

    for move in tile_legal_moves(board, tile):
        child_board, freeTile = apply(move, board)
        # Checks further until depth = 0
        value, _ = negamaxPruning(child_board, freeTile, playerPos,
                                  playerIndex, targetId, player % 2+1, depth-1, -beta, -alpha)
        # Keep the value and move with the best score for the current player
        if value > bestVal:
            bestVal = value
            bestMove = move
        # Determines whether we keep searching or we break the branch
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    # Returns the negative so that the next player is choosing the opposite (min/max)
    return -bestVal, bestMove
