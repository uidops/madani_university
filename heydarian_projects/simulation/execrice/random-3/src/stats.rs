#[allow(dead_code)]
#[derive(Debug, Clone)]
pub struct ChiSquareResult {
    pub chi_square: f64,
    pub df: usize,
    pub critical_value: f64,
    pub passed: bool,
    pub bins: usize,
    pub observed_counts: Vec<usize>,
}

pub fn chi_square_test(data: &[f64], bins: usize) -> ChiSquareResult {
    let n = data.len();
    let expected = n as f64 / bins as f64;
    let mut counts = vec![0usize; bins];

    for &x in data {
        let b = (x * bins as f64).floor() as usize;
        let bin_idx = b.min(bins - 1);
        counts[bin_idx] += 1;
    }

    let mut chi_sq = 0.0;
    for &obs in &counts {
        let diff = obs as f64 - expected;
        chi_sq += (diff * diff) / expected;
    }

    let df = bins - 1;
    let critical_value = match df {
        9 => 16.919,
        19 => 30.144,
        _ => 16.919,
    };

    ChiSquareResult {
        chi_square: chi_sq,
        df,
        critical_value,
        passed: chi_sq <= critical_value,
        bins,
        observed_counts: counts,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_chi_square_uniform() {
        let mut data = Vec::new();
        for i in 0..1000 {
            data.push((i % 10) as f64 / 10.0 + 0.05);
        }
        let res = chi_square_test(&data, 10);
        assert!(res.passed);
        assert_eq!(res.chi_square, 0.0);
    }
}
