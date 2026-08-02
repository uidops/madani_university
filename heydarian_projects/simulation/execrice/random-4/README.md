# Random 4 - Linear Congruential Generator (LCG)

Rust simulation of the **Linear Congruential Generator (LCG)** (`الگوریتم همنهشتی خطی`) and Chi-Square Uniformity Test.

## Files

| File | Description |
| --- | --- |
| `Cargo.toml` | Package manifest (`random-4`). |
| `.gitignore` | Build output ignore rules (`/target`). |
| `src/lcg.rs` | Linear Congruential Generator implementation and period analysis. |
| `src/stats.rs` | Chi-Square Goodness-of-Fit Test for Uniformity. |
| `src/main.rs` | Sequence generation across 100/1000+ iterations and statistical evaluation. |

## Recurrence Formula

$$X_{n+1} = (a \cdot X_n + c) \pmod m$$
$$U_n = \frac{X_n}{m}$$

- **$X_0$**: Seed
- **$a$**: Multiplier
- **$c$**: Increment
- **$m$**: Modulus

## Slide Example

- **Modulus ($m$)**: 100
- **Multiplier ($a$)**: 5
- **Increment ($c$)**: 7
- **Initial Seed ($X_0$)**: 7983 (modulo 100 = 83)

Sequence produced: $83 \to 22 \to 17 \to 92 \dots$

## Run

From this directory:

```bash
cargo run
```

Run unit tests:

```bash
cargo test
```
