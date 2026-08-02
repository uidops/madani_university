#[derive(Debug, Clone)]
#[allow(dead_code)]
pub struct ChiSquareResult {
    pub chi_square: f64,
    pub critical_value: f64,
    pub passed: bool,
    pub counts: Vec<usize>,
    pub expected: f64,
}

pub fn chi_square_uniformity_test(data: &[f64], k: usize) -> ChiSquareResult {
    let n = data.len();
    let expected = n as f64 / k as f64;
    let mut counts = vec![0; k];

    for &x in data {
        let bin = (x * k as f64).floor() as usize;
        let bin = bin.min(k - 1);
        counts[bin] += 1;
    }

    let chi_square: f64 = counts
        .iter()
        .map(|&observed| {
            let diff = observed as f64 - expected;
            (diff * diff) / expected
        })
        .sum();

    // Critical value for k=10 (df=9) at alpha=0.05
    let critical_value = 16.919;
    let passed = chi_square <= critical_value;

    ChiSquareResult {
        chi_square,
        critical_value,
        passed,
        counts,
        expected,
    }
}
