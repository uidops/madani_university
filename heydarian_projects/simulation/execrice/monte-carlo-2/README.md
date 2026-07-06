# Monte Carlo 2

Rust implementation of Monte Carlo estimation of the intersection area of two circles.

## Files

| File | Description |
| --- | --- |
| `Cargo.toml` | Rust package definition. |
| `src/main.rs` | Monte Carlo area estimation and plotting. |

## Simulation

The program estimates the overlapping area of two circles:

- **Circle 1**: centered at `(0, 0)` with radius `4`.
- **Circle 2**: centered at `(4.3, 0)` with radius `1.7`.

Random points are sampled uniformly in the bounding square. Points inside both circles are counted as hits. The estimated area is `area_box × hits / n`. A scatter plot is saved to `image.png` (green = inside both, grey = outside).

## Run

From this directory:

```bash
cargo run
```

## Notes

- Build output is ignored through `.gitignore`.
- Circle definitions and sample count are defined in `src/main.rs`.
