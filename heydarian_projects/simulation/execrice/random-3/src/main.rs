use std::time::{SystemTime, UNIX_EPOCH};

mod generator;
mod stats;

use generator::MultiplicativeMiddle3;
use stats::chi_square_test;

fn generate_random_seed(offset: u64) -> u64 {
    let nanos = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_nanos();
    1000 + (((nanos.wrapping_add(offset as u128)) % 9000) as u64)
}

fn print_header() {
    println!(
        "                   3-TERM MULTIPLICATIVE MIDDLE GENERATOR                                "
    );
}

fn print_sequence_sample(s1: u64, s2: u64, s3: u64, count: usize) {
    println!(
        "--- Sample Sequence Generation (Seeds: {}, {}, {}) ---",
        s1, s2, s3
    );
    println!(
        "{:<6} | {:<12} | {:<20} | {:<10}",
        "Step n", "Integer X_n", "Product (3 terms)", "Float U_n"
    );
    println!("------------------------------------------------------------------");

    let mut history = [s1, s2, s3];
    for i in 0..count {
        if i < 3 {
            let u = history[i] as f64 / 10000.0;
            println!(
                "{:<6} | {:<12} | {:<20} | {:.4}",
                i + 1,
                history[i],
                "(Seed)",
                u
            );
        } else {
            let p1 = history[0] as u128;
            let p2 = history[1] as u128;
            let p3 = history[2] as u128;
            let prod = p1 * p2 * p3;
            let x_n = MultiplicativeMiddle3::extract_middle_digits(prod, 4);
            let u_n = x_n as f64 / 10000.0;
            println!("{:<6} | {:<12} | {:<20} | {:.4}", i + 1, x_n, prod, u_n);

            history[0] = history[1];
            history[1] = history[2];
            history[2] = x_n;
        }
    }
    println!();
}

fn print_chi_square_evaluation(seed_sets: &[(u64, u64, u64)]) {
    println!(
        "=================================== CHI-SQUARE TEST FOR UNIFORMITY ==================================="
    );
    println!(
        "{:<22} | {:<6} | {:<16} | {:<16} | {:<10}",
        "Seeds (S1, S2, S3)", "N", "Chi-Square (χ²)", "Critical Value", "Result"
    );
    println!(
        "------------------------------------------------------------------------------------------------------"
    );

    let sample_sizes = vec![100, 1000];

    for &(s1, s2, s3) in seed_sets {
        for &n in &sample_sizes {
            let mut generator = MultiplicativeMiddle3::new_4digit(s1, s2, s3);
            let floats = generator.generate_floats(n);
            let res = chi_square_test(&floats, 10);

            let result_str = if res.passed { "UNIFORM" } else { "NOT UNIFORM" };

            println!(
                "({:<4}, {:<4}, {:<4})       | {:<6} | {:<16.2} | {:<16.3} | {:<10}",
                s1, s2, s3, n, res.chi_square, res.critical_value, result_str
            );
        }
    }
    println!(
        "------------------------------------------------------------------------------------------------------\n"
    );
}

fn main() {
    print_header();

    // 1. Fixed and Dynamic seeds for sample outputs
    let s1 = (1234, 5678, 9012);
    let s2 = (5432, 8765, 2345);

    let r1 = generate_random_seed(11);
    let r2 = generate_random_seed(1013);
    let r3 = generate_random_seed(9973);
    let dyn_seed1 = (r1, r2, r3);

    let r4 = generate_random_seed(5557);
    let r5 = generate_random_seed(7723);
    let r6 = generate_random_seed(1234567);
    let dyn_seed2 = (r4, r5, r6);

    // Print sample sequences
    print_sequence_sample(s1.0, s1.1, s1.2, 12);
    print_sequence_sample(s2.0, s2.1, s2.2, 12);
    print_sequence_sample(dyn_seed1.0, dyn_seed1.1, dyn_seed1.2, 12);
    print_sequence_sample(dyn_seed2.0, dyn_seed2.1, dyn_seed2.2, 12);

    // 2. Perform Chi-square uniformity test
    let seed_sets = vec![s1, s2, dyn_seed1, dyn_seed2];
    print_chi_square_evaluation(&seed_sets);
}
