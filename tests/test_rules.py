from Program import rules
import pytest


@pytest.fixture
def current_test():
    return 0


@pytest.fixture
def positions_test():
    return [0, 47]


@pytest.fixture
def freeTile_test():
    return {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}


@pytest.fixture
def board_test():
    return [{'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': 14}, {'N': False, 'E': True, 'S': True, 'W': True, 'item': 0}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, {'N': False, 'E': True, 'S': True, 'W': True, 'item': 1}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': 15}, {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': True, 'S': True, 'W': False, 'item': 2}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': 12}, {'N': True, 'E': True, 'S': True, 'W': False, 'item': 3}, {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, {'N': False, 'E': True, 'S': True, 'W': True, 'item': 4}, {'N': False, 'E': True, 'S': True, 'W': True, 'item': 21}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 5}, {'N': False, 'E': True, 'S': True, 'W': True, 'item': 19}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': 13}, {'N': True, 'E': True, 'S': False, 'W': True, 'item': 22}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 20}, {
        'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': True, 'S': True, 'W': False, 'item': 6}, {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, {'N': True, 'E': True, 'S': False, 'W': True, 'item': 7}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 8}, {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 9}, {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': 17}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 23}, {'N': True, 'E': False, 'S': True, 'W': True, 'item': 18}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, {'N': True, 'E': True, 'S': False, 'W': True, 'item': 10}, {'N': True, 'E': True, 'S': False, 'W': False, 'item': 16}, {'N': True, 'E': True, 'S': False, 'W': True, 'item': 11}, {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}]


@pytest.fixture
def BoardClass(board_test, freeTile_test, positions_test):
    b = rules.Board(board_test, freeTile_test, positions_test)
    return b


@pytest.fixture
def GatesClass():
    g = rules.Gates()
    return g

# * Board class tests


def test_update(BoardClass):
    assert BoardClass.update("A") == None


def test_findItem(BoardClass):
    assert isinstance(BoardClass.findItem(17), int)
    assert BoardClass.findItem(50) == None


def test_changeTile(BoardClass, freeTile_test):
    assert BoardClass.changeTile(freeTile_test) == None


def test_getPos(BoardClass, current_test):
    assert isinstance(BoardClass.getPos(current_test), int)


def test_getFreeTile(BoardClass):
    assert isinstance(BoardClass.getFreeTile(), dict)


def test_getBoard(BoardClass):
    assert isinstance(BoardClass.getBoard(), list)


def test_undo(BoardClass) -> None:
    assert BoardClass.undo() == None

# * Gates class tests


def test_index(GatesClass):
    assert isinstance(GatesClass.index("A"), int)


def test_allIndexes(GatesClass):
    assert isinstance(GatesClass.allIndexes(), list)


def test_rowIndexes(GatesClass):
    assert isinstance(GatesClass.rowIndexes(), list)


def test_columnIndexes(GatesClass):
    assert isinstance(GatesClass.columnIndexes(), list)


def test_letter(GatesClass):
    assert isinstance(GatesClass.letter(3), str)


def test_eastGates(GatesClass):
    assert isinstance(GatesClass.eastGates(), list)


def test_westGates(GatesClass):
    assert isinstance(GatesClass.westGates(), list)


def test_northGates(GatesClass):
    assert isinstance(GatesClass.northGates(), list)


def test_southGates(GatesClass):
    assert isinstance(GatesClass.southGates(), list)


def test_allLetters(GatesClass):
    assert isinstance(GatesClass.allLetters(), list)


def test_rowLetters(GatesClass):
    assert isinstance(GatesClass.rowLetters(), list)


def test_columnLetters(GatesClass):
    assert isinstance(GatesClass.columnLetters(), list)

# * Basic function tests


def test_nextIndex():
    assert isinstance(rules.nextIndex(27, "N"), int)
    assert isinstance(rules.nextIndex(27, "S"), int)
    assert isinstance(rules.nextIndex(27, "E"), int)
    assert isinstance(rules.nextIndex(27, "W"), int)
    assert isinstance(rules.nextIndex(27, "A"), int)


def test_oppositeDirection():
    assert rules.oppositeDirection("N") == "S"
    assert rules.oppositeDirection("S") == "N"
    assert rules.oppositeDirection("W") == "E"
    assert rules.oppositeDirection("E") == "W"
    assert rules.oppositeDirection("") == ""
    # with pytest.raises(TypeError):
    #    rules.oppositeDirection(0)  # type: ignore


def test_orientations(freeTile_test):
    assert isinstance(rules.orientations(freeTile_test), list)


def test_columnList():
    assert isinstance(rules.columnList(1), list)
    assert isinstance(rules.columnList(7), list)
    assert isinstance(rules.columnList(13), list)
    assert isinstance(rules.columnList(43), list)


def test_playerLegalMoves(positions_test, current_test, board_test):
    assert isinstance(rules.playerLegalMoves(
        positions_test[current_test], board_test), list)


def test_cartesian():
    assert isinstance(rules.cartesian(1), tuple)
    assert rules.cartesian(0) == (0, 6)


def test_distance():
    assert isinstance(rules.distance(0, 48), int)
