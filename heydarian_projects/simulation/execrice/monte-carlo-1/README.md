# Monte Carlo 1

Rust implementation of Monte Carlo integration for `f(x) = x² - 3x + 11` over the interval `[-4, 5]`.

## Files

| File | Description |
| --- | --- |
| `Cargo.toml` | Rust package definition. |
| `src/main.rs` | Monte Carlo integration, trapezoidal rule, and plotting. |

## Simulation

The program computes the definite integral using three approaches:

- **Trapezoidal rule** with `n=9` and `n=10_000` subintervals.
- **Monte Carlo hit-or-miss**: samples random points in the bounding box and counts hits under the curve.
- **Monte Carlo mean value**: averages random function evaluations over the interval.

It prints the estimated area for each method and saves a plot to `image.png` showing the function curve with Monte Carlo sample points (green = hit, red = miss).

The exact value is `148.5`.

## Run

From this directory:

```bash
cargo run
```

## Notes

- Build output is ignored through `.gitignore`.
- Trial count and interval settings are defined in `src/main.rs`.
