mod lcg;
mod stats;

use lcg::Lcg;
use stats::chi_square_uniformity_test;
use std::collections::HashSet;

fn analyze_sequence(name: &str, generator: Lcg, counts: &[usize]) {
    println!("\n========================================================");
    println!("  Analyzing LCG Model: {}", name);
    println!("========================================================");

    for &n in counts {
        let mut gen = generator.clone();
        let raw_seq = gen.generate_raw(n);
        let float_seq = gen.generate_floats(n);

        // Check if values gradually become identical (cycle / repetition detection)
        let unique_count = raw_seq.iter().collect::<HashSet<_>>().len();
        let is_identical_repeating = unique_count < n;

        // Chi-Square uniformity test
        let chi_res = chi_square_uniformity_test(&float_seq, 10);

        println!("\n---> Test with N = {} numbers:", n);
        println!("     Sample first 10 numbers: {:?}", &raw_seq[..10.min(n)]);
        println!(
            "     Unique values produced: {}/{} ({:.2}%)",
            unique_count,
            n,
            (unique_count as f64 / n as f64) * 100.0
        );

        if is_identical_repeating {
            println!("     [Result] Numbers repeat / become identical -> NOT strictly pseudo-random for long sequences.");
        } else {
            println!("     [Result] Numbers remain distinct across sequence -> Random behavior maintained.");
        }

        println!(
            "     [Uniformity] Chi-Square = {:.3} (Critical = 16.919) -> Uniform: {}",
            chi_res.chi_square, chi_res.passed
        );
    }
}

fn main() {
    println!("=== Random 4: Congruential Algorithm Randomness & Uniformity Test ===");

    // 1. Weak LCG (Small Modulus m=100 from slides: X_{n+1} = (5 * X_n + 7) mod 100)
    let weak_lcg = Lcg::new(7983, 5, 7, 100);
    analyze_sequence(
        "Weak LCG (Slide Example: a=5, c=7, m=100)",
        weak_lcg,
        &[100, 1000],
    );

    // 2. Large Period Standard LCG (m=2^32, a=1664525, c=1013904223)
    let standard_lcg = Lcg::standard(123456789);
    analyze_sequence(
        "Standard Full-Period LCG (m=2^32, a=1664525, c=1013904223)",
        standard_lcg,
        &[100, 1000],
    );
}
