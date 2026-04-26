//! Simple xorshift64 RNG module.
//!
//! This provides a small, self-contained RNG compatible with the usage in
//! `src/main.rs`: `Rng::new(seed)`, `next_u64`, `next_f64`, and `next_range`.
//!
//! The implementation mirrors the xorshift variant used previously:
//! x ^= x << 13; x ^= x >> 7; x ^= x << 17;

#[derive(Clone, Copy, Debug)]
pub struct Rng {
    state: u64,
}

impl Rng {
    const FALLBACK_SEED: u64 = 0xDEADBEEFCAFEBABE;

    pub fn new(seed: u64) -> Self {
        let s = if seed == 0 { Self::FALLBACK_SEED } else { seed };
        Rng { state: s }
    }

    pub fn next_u64(&mut self) -> u64 {
        let mut x = self.state;

        x ^= x.wrapping_shl(13);
        x ^= x.wrapping_shr(7);
        x ^= x.wrapping_shl(17);

        self.state = x;
        x
    }

    pub fn next_f64(&mut self) -> f64 {
        // take top 53 bits (shift right by 11) to form a f64 mantissa
        // divide by 2^53 to get range [0, 1)
        const MAX_U53: f64 = (1u64 << 53) as f64;
        ((self.next_u64() >> 11) as f64) / MAX_U53
    }

    pub fn next_range(&mut self, n: u64) -> u64 {
        if n == 0 {
            return 0;
        }
        self.next_u64() % n
    }
}

impl Default for Rng {
    fn default() -> Self {
        Rng::new(0)
    }
}

#[cfg(test)]
mod tests {
    use super::Rng;

    #[test]
    fn deterministic_sequence() {
        let mut a = Rng::new(0x123456789ABCDEF0);
        let mut b = Rng::new(0x123456789ABCDEF0);
        for _ in 0..100 {
            assert_eq!(a.next_u64(), b.next_u64());
        }
    }

    #[test]
    fn next_f64_range() {
        let mut r = Rng::new(42);
        for _ in 0..1000 {
            let v = r.next_f64();
            assert!(v >= 0.0 && v < 1.0);
        }
    }

    #[test]
    fn next_range_basic() {
        let mut r = Rng::new(1);
        assert_eq!(r.next_range(1), 0);
        for n in [2u64, 3, 4, 10, 100] {
            for _ in 0..100 {
                let v = r.next_range(n);
                assert!(v < n);
            }
        }
    }
}
