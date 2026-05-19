# Random Walk 2

Rust simulation of a dice-based random walk on a `10x10` board.

## Files

| File | Description |
| --- | --- |
| `Cargo.toml` | Rust package definition. |
| `src/main.rs` | Board, dice movement rules, and experiment logic. |
| `src/rng.rs` | Small self-contained xorshift random number generator. |

## Simulation

The program moves from a start cell to a destination cell while avoiding blocked cells. Direction is selected by a six-sided dice rule:

- Rolls `1`, `2`, `3`: move up.
- Roll `4`: move down.
- Roll `5`: move right.
- Roll `6`: move left.

It reports completed runs, average moves, average failures, minimum/maximum moves, and the `A / (A+B)` ratio.

## Run

From this directory:

```bash
cargo run
```

Run tests for the RNG module:

```bash
cargo test
```

## Notes

- Build output is ignored through `.gitignore`.
- Trial count and board settings are defined in `src/main.rs`.
