# XO AI

AI final project for playing an XO-style board game against a computer player.

## Files

| File | Description |
| --- | --- |
| `xo.py` | Python implementation of the game and AI player. |
| `xo.pdf` | Project report or problem document. |

## Requirements

- Python 3
- NumPy

Install NumPy if needed:

```bash
python3 -m pip install numpy
```

## Run

From this directory:

```bash
python3 xo.py
```

The game starts with a `10x10` board by default. Moves are entered as a row letter followed by a column number, for example:

```text
a1
```

## AI Approach

The AI combines several techniques:

- Board scoring across rows, columns, and diagonals.
- Minimax-style search with alpha-beta pruning.
- Monte Carlo simulations for move evaluation.
- Parallel simulations using Python worker threads.

## Notes

- Game settings are defined near the top of `xo.py`.
- Increasing simulation counts or search depth can improve decisions but will make moves slower.
