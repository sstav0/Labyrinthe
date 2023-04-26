import time

from rules import Board, foundTreasure, legalMoves




def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.2f} seconds")
        return result
    return wrapper


# @timeit
def negamaxPruning(board: list, tile: dict, playersPos: list[int], playerIndex: int, targetId: int, aiLevel: int, depth: int = 3, alpha=float("-inf"), beta=float("inf"), timeLimit: float = 3.0) -> tuple:
    """
    Negamax algorithm using alpha-beta pruning to find the best move (with the best value) for a given state of the game.

    Parameters
    ----------
    board : list
        Current state of the board.
    tile : dict
        Current free tile to be inserted.
    playersPos : list[int]
        List containing the index of the tile at the position of each player.
    playerIndex : int
        Index of the current player needed to pick the right index from `playerPos`.
    targetId : int
        Contains the ID of the treasure to reach (to not be confused with the index of the tile).
    playersScore : list[int]
        List containing the remaining treasures to reach by the two players.
    aiLevel : int
        Level of the AI from 1 to 3.
    depth : int, optional
        Depth of the recursive algorithm, by default 4.
    alpha : int | float, optional
        Actual highest move value, by default float("-inf").
    beta : int | float, optional
        Actual lowest move value, by default float("inf").
    timeLimit : float, optional
        Time limit in seconds of the recursive algorithm, by default 3.0

    Returns
    -------
    tuple[int, dict]
        Best value with the best move to play.
    """
    current_board = Board(board, tile, playersPos[playerIndex])
    #print(board[playersPos[playerIndex]], "------------")
    
    # Returns the value of the board state when we are at the max depth and when we find a treasure
    if depth == 0 or foundTreasure(current_board.getBoard(), playersPos, playerIndex, targetId):
        if foundTreasure(current_board.getBoard(), playersPos, playerIndex, targetId):
            print(f"\nPLAYERSPOS: {playersPos} ------ PLAYERINDEX:{playerIndex} -------- TARGETID: {targetId} ------- \n")
            value = 1000
            return -value, None
        return 0, None

    start_time = time.time()
    bestVal = float("-inf")
    bestMove = None
    

    for move in legalMoves(current_board):
        current_board.update(move["gate"])
        child_board, freeTile = current_board.getBoard(), current_board.getFreeTile()
        playersPos[playerIndex]=move["new_position"]
        # Checks further until depth = 0
        value, _ = negamaxPruning(child_board, freeTile, playersPos,
                                  playerIndex % -2 + 1, targetId, aiLevel, depth-1, -beta, -alpha)
        # Keep the value and move with the best score for the current player
        if value > bestVal:
            #print(f"\nVALUE: {value} ----- MOVE: {move}")
            bestVal = value
            bestMove = move
            print(bestVal, bestMove)
        # Determines whether we keep searching or we break the branch
        alpha = max(alpha, value)
        if alpha >= beta:
            break

        # Check if the time limit has been reached
        elapsed_time = time.time() - start_time
        if elapsed_time >= timeLimit:
            break
        current_board.undo()
    # Returns the negative so that the next player is choosing the opposite (min/max)
    return -bestVal, bestMove

# TODO Function that returns the value of a given move depending on the current state of the game
def moveValue(level: int, playerIndex: int, parameter=False) -> int:
    #playersScore = foundTreasure(board, playersPos, playerIndex, targetId, playersScore)[1]
    if parameter:
        score = 1000
    else:
        score = 0
    return score
