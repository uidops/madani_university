#[derive(Clone, Debug)]
pub struct MultiplicativeMiddle3 {
    digits: usize,
    divisor: f64,
    history: [u64; 3],
    current_index: usize,
}

impl MultiplicativeMiddle3 {
    #[allow(dead_code)]
    pub fn new(seed1: u64, seed2: u64, seed3: u64, digits: usize) -> Self {
        let max_val = 10u64.pow(digits as u32);
        let s1 = seed1 % max_val;
        let s2 = seed2 % max_val;
        let s3 = seed3 % max_val;

        MultiplicativeMiddle3 {
            digits,
            divisor: max_val as f64,
            history: [s1, s2, s3],
            current_index: 0,
        }
    }

    #[allow(dead_code)]
    pub fn new_4digit(seed1: u64, seed2: u64, seed3: u64) -> Self {
        Self::new(seed1, seed2, seed3, 4)
    }

    pub fn extract_middle_digits(product: u128, digits: usize) -> u64 {
        let total_digits = digits * 3;
        let formatted = format!("{:01$}", product, total_digits);

        let len = formatted.len();
        let start = if len >= total_digits {
            (len - digits) / 2
        } else {
            0
        };
        let end = (start + digits).min(len);

        let slice = &formatted[start..end];
        slice.parse::<u64>().unwrap_or(0)
    }

    pub fn next_u64(&mut self) -> u64 {
        if self.current_index < 3 {
            let val = self.history[self.current_index];
            self.current_index += 1;
            return val;
        }

        let p1 = self.history[0] as u128;
        let p2 = self.history[1] as u128;
        let p3 = self.history[2] as u128;

        let product = p1 * p2 * p3;
        let next_val = Self::extract_middle_digits(product, self.digits);

        // Shift history window
        self.history[0] = self.history[1];
        self.history[1] = self.history[2];
        self.history[2] = next_val;

        next_val
    }

    pub fn next_f64(&mut self) -> f64 {
        let val = self.next_u64();
        val as f64 / self.divisor
    }

    #[allow(dead_code)]
    pub fn generate_raw(&mut self, n: usize) -> Vec<u64> {
        (0..n).map(|_| self.next_u64()).collect()
    }

    #[allow(dead_code)]
    pub fn generate_floats(&mut self, n: usize) -> Vec<f64> {
        (0..n).map(|_| self.next_f64()).collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_extract_middle_digits() {
        let product: u128 = 1234 * 5678 * 9012;
        let mid = MultiplicativeMiddle3::extract_middle_digits(product, 4);
        assert_eq!(mid, 4394);
    }

    #[test]
    fn test_initial_seeds() {
        let mut generator = MultiplicativeMiddle3::new_4digit(1234, 5678, 9012);
        assert_eq!(generator.next_u64(), 1234);
        assert_eq!(generator.next_u64(), 5678);
        assert_eq!(generator.next_u64(), 9012);
        assert_eq!(generator.next_u64(), 4394);
    }

    #[test]
    fn test_normalized_floats() {
        let mut generator = MultiplicativeMiddle3::new_4digit(1000, 2000, 3000);
        for _ in 0..10 {
            let val = generator.next_f64();
            assert!(val >= 0.0 && val < 1.0);
        }
    }
}
