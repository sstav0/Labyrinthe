import time
from rules import Board, foundTreasure, legalMoves, Gates
import rules
import random

class Minimax:
    def __init__(self, board: list, tile: dict, playersPos: list[int], playerIndex:int, targetID: int, opponent:int, aiLevel:int=2, depth:int =4, alpha= float("-inf"), beta=float("inf"), timeLimit: float=30):
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
        
        value, move = self.minimax_(self.__board, self.__tile, self.__playersPos, self.__playerIndex, self.__aiLevel, self.__depth, self.__alpha, self.__beta)
        if move!= None:
            print("EXECUTED IN: {}".format(time.time()-self.__start_time))
            return value, move
        else: 
            random = randomMove(self.__initialBoard, self.__initialTile, self.__initialPos, self.__initialIndex)
            print("RANDOM")
            print(random)
            return 0, random
    
    def minimax_(self, childBoard, childTile, playersPos, playerIndex, aiLevel, depth, alpha, beta)->tuple:
        
        current_board = Board(childBoard,  childTile, playersPos[playerIndex])
        best_score = float('-inf')
        #print(f"DEPTH: {depth}, PLAYERINDEX:{playerIndex}")
        
        if depth == 0 or foundTreasure(current_board.getBoard(), playersPos, playerIndex, self.__targetID):
            itemIndex = current_board.findItem(self.__targetID)
            if playerIndex != self.__opponent and itemIndex !=None:
                return 1000-rules.distance(playersPos[playerIndex], itemIndex), None
            elif playerIndex != self.__opponent:
                return 0, None
            else:
                return -30*noMove(current_board.getBoard(), playersPos, playerIndex, parameter="int"), None
            
        for move in legalMoves(current_board):
            #print(f"MOVE: {move}")
            
            current_board.update(move["gate"])
            child_board, freeTile = current_board.getBoard(), current_board.getFreeTile()
            playersPos[playerIndex]=move["new_position"]
            
            score, _ = self.minimax_(child_board, freeTile, playersPos, opposite(playerIndex), aiLevel, depth-1, alpha, beta)
            # print(f"SCORE:{score}")
            if score > best_score :
                best_score, best_move = score, move
                print(score, "MOVE: ",move["new_position"], "PLAYER: ", playerIndex)
            
            #print(f"DEPTH: {depth}PLAYER: {playerIndex}")
            if playerIndex == self.__opponent:
                alpha = max(alpha, score)
                if beta <= alpha:
                    #print(f"\n11BREAK=> ALPHA: {alpha} =>>>>>>> BETA:{beta}")
                    break
            else:
                beta = min(beta, score)
                if beta <= alpha:
                    #print(f"\n22BREAK=> ALPHA: {alpha} =>>>>>>> BETA:{beta}")
                    break
                
            if time.time()-self.__start_time > self.__timeLimit:
                print("\nTIME!!!!!!!!!!!!!!!!!\n")
                return best_score, best_move
                
            current_board.undo()
        return best_score, best_move
            
        
def opposite(playerIndex):
    return playerIndex%-2+1


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
    
    legals = rules.playerLegalMoves(playersPos[playerIndex], board)
    move = legals[random.randint(0, len(legals)-1)]
    gates  = Gates().exceptGate(playersPos[playerIndex], move)
    gate = gates[random.randint(0, len(gates)-1)]
    return {"gate": gate, "tile": tile, "new_position": move}

#####################################################################################################

def findItem(board:list, item: int):
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
    for i, tile in enumerate(board):
        if tile["item"] == item:
            found = True
            return i
    if not found:
        print("ITEM {} NOT FOUND".format(chr(ord("A")+item)))

def h(initPos, target):
    if rules.distance(initPos, target)==0:
        return 1000
    elif rules.distance(initPos, target) <= 2:
        return 500-10*rules.distance(initPos, target)
    else: 
        return 300-10*rules.distance(initPos, target)
    

def boardMap(board):
    map_ = {}
    for i, tile in enumerate(board): 
        map_[i] = -100000
    return map_

def bestNode(openSet, target):
    bestScore = float("-inf")
    bestElem = None
    for elem in openSet:
        fScore = h(elem, target)
        if fScore >= bestScore:
            bestScore = fScore
            bestElem = elem 
    return bestElem

def reconstructPath(cameFrom, current):
    totalPath = [current]
    while current in cameFrom:
        current = cameFrom[current]
        totalPath.insert(0, current)
    return totalPath

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
    board_legalMoves = []

    # iters through the dictionary of the initial tile
    for direction, value in board[initialPos].items():
        if direction != "item":  # checks if it's not iterating through the item of the tile
            if value == True:  # if the value is true means that there is no wall in that orientation
                # nextTile is your next position if you'd move in the direction
                nextTile = rules.nextIndex(initialPos, direction)
                # checks if there is a wall in the direction on the next Tile (/!\ the next tile's direction is the opposite of the previous tile's direction)
                if board[nextTile][rules.oppositeDirection(direction)] == True and nextTile != initialPos:
                    # if there is no wall, it adds the next tile's index in the legal moves list
                    board_legalMoves.append(nextTile)
        else:
            pass
    return board_legalMoves

def A_star(initPos, target, board):
    targetPos = findItem(board, target)
    openSet = [initPos]
    
    cameFrom = {}
    
    gScore = boardMap(board)
    gScore[initPos]= 0
    
    fScore = boardMap(board)
    fScore[initPos]= h(initPos, targetPos)
    
    while openSet != []:
        
        current = bestNode(openSet, targetPos)
        print(current)
        time.sleep(1)
        if current == targetPos:
            return reconstructPath(cameFrom, current)
        if playerLegalMoves(current, board) != []:
            
            for neighbor in (playerLegalMoves(current, board)):
                tentativeScore = gScore[current]+rules.distance(initPos, neighbor)
                if tentativeScore < gScore[neighbor]:
                    cameFrom[neighbor]=current
                    gScore[neighbor]=tentativeScore
                    fScore[neighbor]=tentativeScore+ h(neighbor, targetPos)
                    if neighbor not in openSet:
                        openSet.append(neighbor)
                print(f"NEIGHBOR: {neighbor}; TENTATIVE: {tentativeScore};GSCORE: {gScore[neighbor]}; OPENSET:{openSet}")
                time.sleep(2)
                
        else: 
            return "CAN'T MOVE"
    
    return 'PATH NOT FOUND'
            