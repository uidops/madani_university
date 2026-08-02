# Simulation Exercises

Rust exercises for simulation topics.

## Projects

| Directory | Description |
| --- | --- |
| `random-1/` | Random walk simulation with uniform and non-uniform movement probabilities. |
| `random-2/` | Dice-based random walk simulation. |
| `random-3/` | 3-term multiplicative middle random number generator and uniformity evaluation. |
| `random-3-webpage/` | Web application for interactive 3-term multiplicative middle RNG simulation and live charts. |
| `random-4/` | Linear Congruential Generator (LCG) simulation and Chi-Square uniformity evaluation. |
| `genetic-1/` | Genetic algorithm with fixed crossover and mutation positions. |
| `genetic-2/` | Genetic algorithm with normally sampled crossover and mutation positions. |
| `monte-carlo-1/` | Monte Carlo integration of `x² - 3x + 11` compared with the trapezoidal rule. |
| `monte-carlo-2/` | Monte Carlo estimation of the intersection area of two circles. |
| `monte-carlo-3/` | Monte Carlo estimation of Pi (π) using quarter circle integration. |
| `monte-carlo-3-webpage/` | Web application for interactive Monte Carlo Pi estimation and scatter/convergence charts. |
| `routing-lab-webpage/` | Paint-like canvas web app for building network topologies, configuring bandwidth/delays, and ranking fastest routing paths. |

Each project is an independent Cargo package with its own `README.md`.

## Run A Project

From a project directory:

```bash
cargo run
```

Run tests when available:

```bash
cargo test
```
