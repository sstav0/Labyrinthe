import time
from rules import Board, foundTreasure, legalMoves, Gates
import rules
import signal

class Minimax:
    def __init__(self, board: list, tile: dict, playersPos: list[int], playerIndex:int, targetID: int, opponent:int, aiLevel:int=2, depth:int = 2, alpha= float("-inf"), beta=float("inf"), timeLimit: float=2.5):
        self.__board = board
        self.__tile = tile
        self.__playersPos = playersPos
        self.__playerIndex = playerIndex
        self.__targetID = targetID
        self.__opponent = opponent
        self.__aiLevel = aiLevel
        self.__depth = depth
        self.__alpha = alpha
        self.__beta = beta
        self.__timeLimit = timeLimit
        self.__start_time = 0
        
        self.__initialBoard = []
        self.__initialPos = []
        self.__initialIndex = 0
        self.__initialTile = {}
    
    def runMinimax(self):
        self.__start_time = time.time()
        self.__initialBoard = self.__board.copy()
        self.__initialPos = self.__playersPos.copy()
        self.__initialIndex = self.__playerIndex
        self.__initialTile = self.__tile
        self.minimax_(self.__board, self.__tile)
        
    
    def minimax_(self, childBoard, childTile)->tuple:
        self.__aiLevel+=1
        print(self.__aiLevel)
    
        current_board = Board(self.__board, self.__tile, self.__playersPos[self.__playerIndex])
        
        best_score = float('-inf')
        
        if time.time()-self.__start_time > self.__timeLimit:
            print("TIME!!!!!!!!!!!!!!!!!")
            if best_move != None:
                return best_score, best_move
            else:
                best_move = randomMove(self.__initialBoard, self.__initialTile, self.__initialPos, self.__initialIndex)
                return 0, best_move
        
        if self.__depth == 0 or foundTreasure(current_board.getBoard(), self.__playersPos, self.__playerIndex, self.__targetID) or noMove(current_board.getBoard(), self.__playersPos, self.__playerIndex):
            if foundTreasure(current_board.getBoard(), self.__playersPos, self.__playerIndex, self.__targetID) and self.__playerIndex != self.__opponent:
                return 1000, None
            elif noMove(current_board.getBoard(), self.__playersPos, self.__playerIndex) and self.__playerIndex == self.__opponent:
                return 20, None
            elif self.__depth == 0 and self.__playerIndex != self.__opponent:
                itemIndex = current_board.findItem(self.__targetID)
                if itemIndex != None:
                    return 200 - 5*rules.distance(self.__playersPos[self.__playerIndex], itemIndex), None
                else:
                    return 0, None
            else:
                return -5*noMove(current_board.getBoard(), self.__playersPos, self.__playerIndex, parameter="int"), None
          
        for move in legalMoves(current_board):
            if time.time()-self.__start_time > self.__timeLimit:
                print("TIME!!!!!!!!!!!!!!!!!")
                if best_move != None:
                    return best_score, best_move
                else:
                    best_move = randomMove(self.__initialBoard, self.__initialTile, self.__initialPos, self.__initialIndex)
                    return 0, best_move
                
            current_board.update(move["gate"])
            child_board, freeTile = current_board.getBoard(), current_board.getFreeTile()
            self.__playersPos[self.__playerIndex]=move["new_position"]
            
            score, _ = self.minimax_(child_board, freeTile)
            
            if score > best_score:
                best_score, best_move = score, move
                print(score)
            if self.__playerIndex != self.__opponent:
                self.__alpha = max(self.__alpha, score)
                if self.__beta <= self.__alpha:
                    break
            else:
                self.__beta = min(self.__beta, score)
                if self.__beta <= self.__alpha:
                    break
            current_board.undo()
        return best_score, best_move
            
        


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def noMove(board, playersPos, playerIndex, parameter ="bool"):
    if parameter =="bool":
        if len(rules.playerLegalMoves(playersPos[playerIndex], board)) == 1:
            return True
        else: 
            return False
    else:
        return len(rules.playerLegalMoves(playersPos[playerIndex], board))
    

def randomMove(board, tile, playersPos, playerIndex):
    move = rules.playerLegalMoves(playersPos[playerIndex], board)
    gate  = Gates().exceptGate(playersPos[playerIndex], move)
    return {"gate": gate, "tile": tile, "new_position": move}

    
def minimax(board: list, tile: dict, playersPos: list[int], playerIndex:int, targetID: int, opponent:int, aiLevel:int=2, depth:int = 4, alpha= float("-inf"), beta=float("inf"), timeLimit: float=0.3)->tuple:
    current_board = Board(board, tile, playersPos[playerIndex])
    
    best_score = float('-inf')
   # best_move = randomMove(board, tile, playersPos, playerIndex)
    
    if depth == 0 or foundTreasure(current_board.getBoard(), playersPos, playerIndex, targetID) or noMove(current_board.getBoard(), playersPos, playerIndex):
        if foundTreasure(current_board.getBoard(), playersPos, playerIndex, targetID) and playerIndex != opponent:
            print("found")
            return 1000, None
        elif noMove(current_board.getBoard(), playersPos, playerIndex) and playerIndex == opponent:
            return 20, None
        elif depth == 0 and playerIndex != opponent:
            itemIndex = current_board.findItem(targetID)
            if itemIndex != None:
                return 200 - 5*rules.distance(playersPos[playerIndex], itemIndex), None
            else:
                return 0, None
        else:
            return -5*noMove(current_board.getBoard(), playersPos, playerIndex, parameter="int"), None
    
    
    for move in legalMoves(current_board):
        current_board.update(move["gate"])
        child_board, freeTile = current_board.getBoard(), current_board.getFreeTile()
        playersPos[playerIndex]=move["new_position"]
        score, _ = minimax(child_board, freeTile, playersPos, playerIndex%-2+1, targetID, opponent, aiLevel+1, depth -1, alpha, beta)
        if score > best_score:
            best_score, best_move = score, move
            #print(score)
        if playerIndex != opponent:
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        else:
            beta = min(beta, score)
            if beta <= alpha:
                break
        current_board.undo()
        # if best_move is None:
        #     best_move = randomMove(current_board.getBoard(), current_board.getFreeTile(), current_board.getPos(), playerIndex)
    return best_score, best_move
    
    

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
        Index of the current player needed to pick the right index from `playersPos`.
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
            value = 834
            return -value, None
        return -1000000, None

    start_time = time.time()
    bestVal = -100000
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
