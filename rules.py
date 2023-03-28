import random

def nextIndex(initialPos, direction): 
    """Function that computes the index of the next position with the current position and the direction as inputs

    Args:
        initialPos (int): index of the initial position 
        direction (string): abbreviation of the direction  

    Returns:
        int: index of the next position 
    """
    
    if direction == "N" and initialPos not in range(0,7):
        nextPos = initialPos + 7 
    if direction == "S" and initialPos not in range(42,48)   : 
        nextPos = initialPos - 7 
    if direction == "O" and initialPos%7 != 0: 
        nextPos = initialPos - 1 
    if direction == "E" and (initialPos + 1)%7 != 0 : 
        nextPos = initialPos + 1
    return nextPos
    
def move(initialPos, board, objectif): 
    possibleWays = []
    for orientation, value in board[initialPos]: 
        if value == True : 
            possibleWays.append(orientation)
    
    return nextIndex(possibleWays[random.randint(0, len(possibleWays))]) 

                
board = [
    {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, 
    {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
    {'N': False, 'E': True, 'S': True, 'W': True, 'item': 0}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': 17}, 
    {'N': False, 'E': True, 'S': True, 'W': True, 'item': 1}, 
    {'N': True, 'E': False, 'S': True, 'W': True, 'item': 23}, 
    {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, 
    {'N': True, 'E': True, 'S': False, 'W': True, 'item': 19}, 
    {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
    {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, 
    {'N': True, 'E': True, 'S': False, 'W': True, 'item': 22}, 
    {'N': True, 'E': False, 'S': False, 'W': True, 'item': 15}, 
    {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, 
    {'N': True, 'E': True, 'S': False, 'W': True, 'item': 18}, 
    {'N': True, 'E': True, 'S': True, 'W': False, 'item': 2}, 
    {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, 
    {'N': True, 'E': True, 'S': True, 'W': False, 'item': 3}, 
    {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
    {'N': False, 'E': True, 'S': True, 'W': True, 'item': 4}, 
    {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, 
    {'N': True, 'E': False, 'S': True, 'W': True, 'item': 5}, 
    {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, 
    {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, 
    {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, 
    {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, 
    {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, 
    {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, 
    {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, 
    {'N': True, 'E': True, 'S': True, 'W': False, 'item': 6}, 
    {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, 
    {'N': True, 'E': True, 'S': False, 'W': True, 'item': 7}, 
    {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
    {'N': True, 'E': False, 'S': True, 'W': True, 'item': 8}, 
    {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
    {'N': True, 'E': False, 'S': True, 'W': True, 'item': 9}, 
    {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, 
    {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, 
    {'N': True, 'E': False, 'S': True, 'W': True, 'item': 21}, 
    {'N': False, 'E': False, 'S': True, 'W': True, 'item': 13}, 
    {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
    {'N': True, 'E': False, 'S': False, 'W': True, 'item': 14}, 
    {'N': True, 'E': False, 'S': True, 'W': True, 'item': 20}, 
    {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, 
    {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, 
    {'N': True, 'E': True, 'S': False, 'W': True, 'item': 10}, 
    {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
    {'N': True, 'E': True, 'S': False, 'W': True, 'item': 11}, 
    {'N': True, 'E': True, 'S': False, 'W': False, 'item': 12}, 
    {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}
]

print(move(0,board, 1))