import time
from rules import Board, Gates
import rules
import random
            


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"\n-----------Execution time: {end_time - start_time:.2f} seconds--------\n")
        return result
    return wrapper

    

def randomMove(board, tile, playersPos, playerIndex):
    
    legals = rules.playerLegalMoves(playersPos[playerIndex], board)
    move = legals[random.randint(0, len(legals)-1)]
    gates  = Gates().exceptGate(playersPos[playerIndex], move)
    gate = gates[random.randint(0, len(gates)-1)]
    return {"gate": gate, "tile": tile, "new_position": move}

#####################################################################################################
def saveMessage(player_number, message1, message2=None):
    """This functions saves any message (dictionary) in a .txt file 

    Parameters
    ----------
        player_number (int): number of the player (0 or 1)
        message (dict): message that's going to be saved in the .txt file
    """
    if message2 != None:
        with open('errors.txt', 'a') as file:
            file.write('LIST OF ERRORS PLAYER {}: {}\n{}\n'.format(
                player_number, message1, message2))
    else:
        with open('errors.txt', 'a') as file:
            file.write('LIST OF ERRORS PLAYER {}: {}\n'.format(
                player_number, message1))

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
    return rules.distance(initPos, target)
    

def boardMap(board):
    map_ = {}
    for i, tile in enumerate(board): 
        map_[i] = 100000
    return map_

def bestNode(openSet, target):
    bestScore = float('-inf')
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

def A_star(initPos, targetPos, board):
    openSet = [initPos]
    
    cameFrom = {}
    
    gScore = boardMap(board)
    gScore[initPos]= 0
    
    fScore = boardMap(board)
    fScore[initPos]= h(initPos, targetPos)
    
    while openSet != []:
        
        current = bestNode(openSet, targetPos)
        if current == targetPos:
            return reconstructPath(cameFrom, current)
        if playerLegalMoves(current, board) != []:
            openSet.remove(current)
            for neighbor in (playerLegalMoves(current, board)):
                #print(f"\nPOS: {current}; LEGAL MOVES:{playerLegalMoves(current, board)}; OPENSET: {openSet}\n")
                #time.sleep(1)
                tentativeScore = gScore[current]+rules.distance(current, neighbor)
                
                #origin = gScore[current]
                #oldG = gScore[neighbor]
                
                if tentativeScore < gScore[neighbor]:
                    cameFrom[neighbor]=current
                    gScore[neighbor]=tentativeScore
                    fScore[neighbor]=tentativeScore+ h(neighbor, targetPos)
                    if neighbor not in openSet:
                        openSet.append(neighbor)
                #print(f"CURRENT: {current}; NEIGHBOR: {neighbor}; ORIGIN G: {origin}; OLDG: {oldG}; TENTATIVE: {tentativeScore}; GSCORE: {gScore[neighbor]}; OPENSET:{openSet}; CAMEFROM: {cameFrom}")
                #time.sleep(3)
                
        else: 
            return "CAN'T MOVE"
    
    return reconstructPath(cameFrom, current)

            
@timeit            
def makeMove(tile, positions, current, target, board): 
    
    # initPos = positions[current]
    # opPos = positions[current%-2+1]
    move_dict = {}
    bestScore = float("+inf")
    bestMove = None
    bestGate = ""
    BoardObject = Board(board, tile, positions)
    
    for orientation in rules.orientations(BoardObject.getFreeTile()):
        BoardObject.changeTile(orientation)
        for gate in Gates().allLetters():
            BoardObject.update(gate)
            itemPos = BoardObject.findItem(target)
            if itemPos != None:
                #print(f"TILE:{orientation}; GATE:{gate}")
                move = A_star(BoardObject.getPos(current), itemPos, BoardObject.getBoard())
                if type(move[-1])==int:
                    score = rules.distance(move[-1], itemPos)*10+len(playerLegalMoves(BoardObject.getPos(current%-2+1), BoardObject.getBoard()))
            else:
                score = len(playerLegalMoves(BoardObject.getPos(current%-2+1), BoardObject.getBoard()))
                #print(f"NO OBJECT; SCORE: {score}")
                move = [BoardObject.getPos(current)]
            if score < bestScore:
  
                bestMove = move 
                bestScore = score
                bestGate = gate
                bestTile = orientation 
                #print(f"\nBESTMOVE: {bestMove}\n")  
            BoardObject.undo()
    
    
    move_dict = {
        "tile": bestTile,
        "gate": bestGate,
        "new_position": bestMove[-1]
    }
    return move_dict

        