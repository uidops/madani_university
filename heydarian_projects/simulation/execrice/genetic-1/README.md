# Genetic Algorithm 1

Rust implementation of a genetic algorithm for finding integer values that make the target expression close to zero.

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

This version uses fixed crossover and mutation positions.

## Run

From this directory:

```bash
cargo run
```

## Notes

- Population size, mutation rate, generation limit, and gene interval are defined in `src/genetic.rs`.
- Build output is ignored through `.gitignore`.
