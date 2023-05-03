import time
from rules import Board, Gates
import rules
from rules import playerLegalMoves, nextIndex, oppositeDirection, distance, orientations
from typing import Union

            


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"\n-----------Execution time: {end_time - start_time:.3f} seconds--------\n")
        return result
    return wrapper

def h(initPos:int, target:int)->int:
    """This function returns the distance between the position of the player and the position of the target

    Parameters
    ----------
    initPos : int
        current index
    target : int
        index of the target

    Returns
    -------
    int
        Manhattan distance between the current position and the target
    """
    return rules.distance(initPos, target)
    

def boardMap(board:list[dict])->list[int]:
    """This function creates a list that contains a score value of 'inf' for each tile on the board

    Parameters
    ----------
    board : list[dict]
        list of the tiles on the board

    Returns
    -------
    list[int]
        list of the values for each tile on the board
    """
    map_ = {}
    for i, tile in enumerate(board): 
        map_[i] = 100000
    return map_

def bestNode(openSet:list, target:int)->int:
    """This function returns the index that is the closest to the target index in the openSet list

    Parameters
    ----------
    openSet : list
        list of the indexes to explore
    target : int
        index of the target

    Returns
    -------
    int
        best index to explore based on it's distance to the target
    """
    bestScore = float('-inf')
    bestElem = None
    for elem in openSet:
        fScore = h(elem, target)
        if fScore >= bestScore:
            bestScore = fScore
            bestElem = elem 
    return bestElem

def reconstructPath(cameFrom:dict, current:int)->list[int]:
    """This function returns the indexes of the path taken in the right order

    Parameters
    ----------
    cameFrom : dict
        dict that assign for each index(key), the previous index(value)
    current : int
        current player 

    Returns
    -------
    list[int]
        list of the path's indexes in the right order 
    """
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
                nextTile = nextIndex(initialPos, direction)
                # checks if there is a wall in the direction on the next Tile (/!\ the next tile's direction is the opposite of the previous tile's direction)
                if board[nextTile][oppositeDirection(direction)] == True and nextTile != initialPos:
                    # if there is no wall, it adds the next tile's index in the legal moves list
                    board_legalMoves.append(nextTile)
        else:
            pass
    return board_legalMoves

def A_star(initPos:int, targetPos:int, board:list)->Union[list[int], str]:
    """This function finds the best way on the board passed in parameter to reach the target position passed in parameter

    Parameters
    ----------
    initPos : int
        initial position of the player
    targetPos : int
        position of the target on the board
    board : list
        list of the tiles on the board

    Returns
    -------
    list[int]|str
        If the algorithm is not blocked, it returns a list of the path indexes, otherwise it returns "CAN'T MOVE
    """

    openSet = [initPos]  #indexes to explore/re-explore
    
    cameFrom = {}#for each new position, the value is the previous position. Example {1:0} means you went from 0 to 1
    
    gScore = boardMap(board)    #initialize the score map: for each tile, boardMap sets the value to 'inf'
    gScore[initPos]= 0  #the score of the initial position 
    
    fScore = boardMap(board)    #initialize the score map: for each tile, boardMap sets the value to 'inf'
    fScore[initPos]= h(initPos, targetPos)  #the score of the initial position is the distance between the position and the target
    
    while openSet != []:
        
        current = bestNode(openSet, targetPos)
        if current == targetPos:
            return reconstructPath(cameFrom, current)
        if playerLegalMoves(current, board) != []:
            openSet.remove(current)
            for neighbor in (playerLegalMoves(current, board)):
                tentativeScore = gScore[current]+distance(current, neighbor)
                if tentativeScore < gScore[neighbor]:
                    cameFrom[neighbor]=current
                    gScore[neighbor]=tentativeScore
                    fScore[neighbor]=tentativeScore+ h(neighbor, targetPos)
                    if neighbor not in openSet:
                        openSet.append(neighbor)
        
                
        else: 
            return "CAN'T MOVE"
    
    return reconstructPath(cameFrom, current)

            
@timeit            
def makeMove(tile:dict, positions:list, current:int, target:int, board:list)->dict: 
    """This function handles the calls of the function algorithm and assigns a score to each move possible

    Parameters
    ----------
    tile : dict
        the free tile
    positions : list
        list of the two positions of the players on the board
    current : int
        index of the current player
    target : int
        target's number 
    board : list
        list of each tile on the board

    Returns
    -------
    dict
        best move
    """
    move_dict = {}
    bestScore = float("+inf")
    bestMove = None
    bestGate = ""
    BoardObject = Board(board, tile, positions)
    
    for orientation in orientations(BoardObject.getFreeTile()):
        BoardObject.changeTile(orientation)
        for gate in Gates().allLetters():
            BoardObject.update(gate)
            itemPos = BoardObject.findItem(target)
            if itemPos != None:
                move = A_star(BoardObject.getPos(current), itemPos, BoardObject.getBoard())
                if type(move[-1])==int:
                    score = distance(move[-1], itemPos)*10+len(playerLegalMoves(BoardObject.getPos(current%-2+1), BoardObject.getBoard()))
                else:
                    score = 100
                    move = [BoardObject.getPos(current)]
            else:
                score = 100
                move = [BoardObject.getPos(current)]
            if score < bestScore:
                bestMove = move 
                bestScore = score
                bestGate = gate
                bestTile = orientation 
                
            BoardObject.undo()
    
    if current == 0: 
        print(f"\nYELLOW  =>  BEST MOVE: {bestMove}\n")  
    else:
        print(f"\nBLUE  =>  BEST MOVE: {bestMove}\n")  
        
    time.sleep(1.5)
    move_dict = {
        "tile": bestTile,
        "gate": bestGate,
        "new_position": bestMove[-1]
    }
    return move_dict

        