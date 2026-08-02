#[derive(Clone, Debug)]
pub struct Lcg {
    state: u64,
    a: u64,
    c: u64,
    m: u64,
}

impl Lcg {
    pub fn new(seed: u64, a: u64, c: u64, m: u64) -> Self {
        Lcg {
            state: seed % m,
            a,
            c,
            m,
        }
    }

    pub fn standard(seed: u64) -> Self {
        Self::new(seed, 1664525, 1013904223, 2u64.pow(32))
    }

    #[allow(dead_code)]
    pub fn slide_example(seed: u64) -> Self {
        Self::new(seed, 5, 7, 100)
    }

    pub fn next_u64(&mut self) -> u64 {
        let val = self.state;
        self.state = (self.a.wrapping_mul(self.state).wrapping_add(self.c)) % self.m;
        val
    }

    pub fn next_f64(&mut self) -> f64 {
        let val = self.next_u64();
        val as f64 / self.m as f64
    }

    pub fn generate_raw(&mut self, n: usize) -> Vec<u64> {
        (0..n).map(|_| self.next_u64()).collect()
    }

    pub fn generate_floats(&mut self, n: usize) -> Vec<f64> {
        (0..n).map(|_| self.next_f64()).collect()
    }

    #[allow(dead_code)]
    pub fn find_period(&mut self, max_steps: usize) -> Option<usize> {
        let start_state = self.state;
        for step in 1..=max_steps {
            self.next_u64();
            if self.state == start_state {
                return Some(step);
            }
        }
        None
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_slide_example() {
        let mut lcg = Lcg::slide_example(7983);
        assert_eq!(lcg.next_u64(), 83);
        assert_eq!(lcg.next_u64(), 22);
        assert_eq!(lcg.next_u64(), 17);
        assert_eq!(lcg.next_u64(), 92);
    }

    #[test]
    fn test_normalized_floats() {
        let mut lcg = Lcg::standard(12345);
        for _ in 0..100 {
            let val = lcg.next_f64();
            assert!(val >= 0.0 && val < 1.0);
        }
    }
}
