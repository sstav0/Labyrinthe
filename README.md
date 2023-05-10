# Labyrinthe

'AImazing' is a research algorithm AI developed by `21151` and `21211`.

It has been design to compete in the board game [Labyrinthe](https://www.ravensburger.org/frbe/produits/jeux/jeux-de-soci%C3%A9t%C3%A9-pour-la-famille/labyrinthe-26743/index.html) developed by Ravensburger, a treasure hunt in a sliding maze.

## Project Requirements

To run this project, no packages must be installed but the following are needed to process unit tests:

- `pytest`
- `coverage`

You can install them by running the command :

```python
pip install -r requirements.txt
```

Or :

```python
python -m pip install -r requirements.txt
```

## Algorithm

Our algorithm is using the `A* (A star)` path finding algorithm to find the best and easiest path to reach the desired target.
Each node is defined by a free tile orientation, a gate in which the free tile can be inserted, and a position where the player can move.

The algorithm starts by exploring neighboring nodes, evaluating their costs, and assigning scores based on the Manhattan distance and the number of legal moves available.
By calculating the Manhattan distance between the current player position and the next possible positions, the algorithm evaluates the proximity of each option to the target.
The algorithm also takes into account the number of legal moves available for both players in a way that maximize that number for the player and minimize it for the enemy, evaluating the liberty and the range of possible solutions.

It then selects the node with the lowest score to continue the search. This process continues until the target is reached or all possible paths have been explored.

### Start algorithm

To start the algorithm, make sure the path is in the `.\Labyrinthe` directory and run the batch file as follows :

```python
start batch_starter.bat
```

An AI index must be specified, corresponding to a number from 0 to 10, for referencing the AI.

The batch file is executing the `ai_starter.py` file which makes the inscription to the ChampionshipRunner server and starts the AI with correct parameters without having to enter it in the terminal (allowing testing with the same AI).
