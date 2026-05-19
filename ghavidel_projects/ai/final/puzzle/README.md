# Number Matrix Puzzle

AI final project for solving a number-matrix puzzle as a constraint satisfaction problem.

## Files

| File | Description |
| --- | --- |
| `puzzle.py` | Python solver implementation. |
| `puzzle.txt` | Input puzzle data. |
| `solution.txt` | Saved solution output. |
| `puzzle.pdf` | Project report or problem document. |

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
python3 puzzle.py
```

The default command reads `puzzle.txt` and writes the result to `solution.txt`.

Optional arguments:

```bash
python3 puzzle.py -f puzzle.txt -o solution.txt
python3 puzzle.py -v
python3 puzzle.py -u
```

Flags:

- `-f`: input puzzle file path.
- `-o`: output solution file path.
- `-v`: verbose mode, prints solving progress.
- `-u`: require selected numbers to be unique in each row and column.

## Input Format

`puzzle.txt` uses comma-separated values:

- First line: matrix size as `rows,cols`.
- Second line: target row sums.
- Third line: target column sums.
- Remaining lines: puzzle matrix rows.

## Notes

- The solver uses backtracking, forward checking, and variable-ordering heuristics.
- A valid solution must match all target row and column sums.
