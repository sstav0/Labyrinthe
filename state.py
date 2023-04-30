from rules import Board
import rules
import ai


def showBoard(board):
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


if __name__ == "__main__":
    
    state = {'players': ['AImazing1', 'AImazing0'], 'current': 0, 'positions': [0, 47], 'board': [{'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': 14}, {'N': False, 'E': True, 'S': True, 'W': True, 'item': 0}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, {'N': False, 'E': True, 'S': True, 'W': True, 'item': 1}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': 15}, {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': True, 'S': True, 'W': False, 'item': 2}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': 12}, {'N': True, 'E': True, 'S': True, 'W': False, 'item': 3}, {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, {'N': False, 'E': True, 'S': True, 'W': True, 'item': 4}, {'N': False, 'E': True, 'S': True, 'W': True, 'item': 21}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 5}, {'N': False, 'E': True, 'S': True, 'W': True, 'item': 19}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': 13}, {'N': True, 'E': True, 'S': False, 'W': True, 'item': 22}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 20}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': True, 'S': True, 'W': False, 'item': 6}, {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, {'N': True, 'E': True, 'S': False, 'W': True, 'item': 7}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 8}, {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 9}, {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': 17}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 23}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 18}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': True, 'S': False, 'W': True, 'item': 10}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': 16}, {'N': True, 'E': True, 'S': False, 'W': True, 'item': 11}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}], 'tile': {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, 'target': 17, 'remaining': [4, 4]}
    # state["board"][24]["S"] = True
    # state["board"][31]["N"] = True
    # state["board"][9]["S"]=False
    # state["board"][2]["S"]=False
    # state["board"][2]["W"]=False
    # state["board"][2]["E"]=False
    
    move = ai.makeMove(state["tile"], state["positions"], state["current"], state["target"], state["board"])
    print(showBoard(state["board"]), "\n\n\n")
    BoardObject2 = Board(state["board"], state["tile"], state["positions"])
    
    
    #print(move)
    
    BoardObject2.changeTile({'N': True, 'E': False, 'S': True, 'W': False, 'item': None})
    BoardObject2.update("A")
    print(showBoard(BoardObject2.getBoard())) 
    print(BoardObject2.getPos(1))
