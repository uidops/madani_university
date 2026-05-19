# Genetic Algorithm 2

Rust implementation of a modified genetic algorithm for the same integer-expression search problem as `genetic-1`.

## Files

| File | Description |
| --- | --- |
| `Cargo.toml` | Rust package definition. |
| `src/main.rs` | Runs repeated experiments and prints summary results. |
| `src/genetic.rs` | Genetic algorithm implementation. |

## Goal

The algorithm searches for integer genes `[x, y, z]` that minimize:

```text
2x + 12y - 6z - 20
```

This version chooses crossover and mutation positions from a normal distribution, then clamps them to valid chromosome indexes.

## Run

From this directory:

```bash
cargo run
```

## Notes

- Population size, mutation rate, generation limit, and gene interval are defined in `src/genetic.rs`.
- This project depends on `rand` and `rand_distr`.
- Build output is ignored through `.gitignore`.
