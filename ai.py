def move(state: dict) -> dict:
    """
    Defines the move to execute

    Parameters
    ----------
    state : dict -- Dictionary from the server containing the state of the game

    Returns
    -------
    dict
        - tile containing its orientation
        - gate in which we insert the tile
        - new position of the tile
    """
    def move_calculator() -> list:
        return [state["state"]["tile"], "A", 1]

    next_move = {
        "tile": move_calculator()[0],
        "gate": move_calculator()[1],
        "new_position": move_calculator()[2]
    }
    return next_move
