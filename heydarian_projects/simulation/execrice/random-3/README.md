# Random 3 - 3-Term Multiplicative Middle Generator

Rust simulation of the **3-Term Multiplicative Middle Random Number Generator** (الگوریتم میان ضربی ۳ جمله‌ای) with Chi-Square Uniformity Test.

## Files

| File | Description |
| --- | --- |
| `Cargo.toml` | Package manifest (`random-3`). |
| `.gitignore` | Build output ignore rules (`/target`). |
| `src/generator.rs` | 3-term multiplicative middle RNG logic & digit extraction. |
| `src/stats.rs` | Chi-Square Goodness-of-Fit Test for Uniformity. |
| `src/main.rs` | Sample sequence generation and Chi-Square evaluation. |

## Algorithm

The generator starts with 3 initial $D$-digit seeds ($Seed_1, Seed_2, Seed_3$). Each subsequent term is computed by multiplying the 3 preceding terms and extracting the middle $D$ digits:

$$P_n = X_{n-1} \times X_{n-2} \times X_{n-3}$$
$$U_n = \frac{\text{middle\_digits}(P_n)}{10^D}$$

## Chi-Square Test

The implementation evaluates sequence uniformity using the Chi-Square Goodness-of-Fit test across $k=10$ intervals at significance level $\alpha = 0.05$ (critical value $\chi^2_{0.05, 9} = 16.919$).

## Run

From this directory:

```bash
cargo run
```

Run unit tests:

```bash
cargo test
```
