# Random Walk 1

Rust simulation of a bead moving on a `10x10` board from a start cell to a destination cell.

## Files

| File | Description |
| --- | --- |
| `Cargo.toml` | Rust package definition. |
| `src/main.rs` | Simulation logic and experiment output. |
| `src/rng.rs` | Small self-contained xorshift random number generator. |

## Simulation

The program compares two movement strategies:

- Uniform random walk: each direction has equal probability.
- Non-uniform random walk: movement probabilities are weighted toward up and right.

For each strategy, it runs multiple trials and reports average moves, failed moves, minimum/maximum moves, and a move/failure ratio.

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
