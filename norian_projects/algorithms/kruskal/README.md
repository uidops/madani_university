# Kruskal

Kruskal minimum-spanning-tree algorithm implemented in Go.

## Files

| File | Description |
| --- | --- |
| `kruskal.go` | Graph model, set-based component tracking, Kruskal algorithm, and sample graph. |
| `go.mod` | Go module definition. |
| `Makefile` | Helper commands for building or running the project. |
| `SUMMARY.md` | Additional summary notes. |
| `SET_VS_UNIONFIND.md` | Notes comparing set-based tracking with union-find. |

## Run

From this directory:

```bash
go run .
```

If using the Makefile:

```bash
make
```

## Notes

- The sample graph is defined as an adjacency matrix in `kruskal.go`.
- Generated binaries such as `kruskal` or files under `bin/` should not be committed.
