# Traveling Salesman Problem

Dynamic-programming solution for the traveling salesman problem.

## Files

| File | Description |
| --- | --- |
| `tsp.go` | Go implementation using bitmask subsets. |
| `doregard.py` | Python implementation using memoization and path reconstruction. |
| `go.mod` | Go module definition. |

## Run The Go Version

From this directory:

```bash
go run .
```

## Run The Python Version

Install NumPy if needed:

```bash
python3 -m pip install numpy
```

Then run:

```bash
python3 doregard.py
```

## Notes

- The sample distance matrix is defined in each source file.
- Both implementations print the minimum tour length and selected path.
