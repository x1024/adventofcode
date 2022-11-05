use std::fs;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_easy_small() {
        assert_eq!(easy(65, 8921, 5), 1);
    }

    #[test]
    fn test_easy() {
        assert_eq!(easy(65, 8921, 40*1000*1000), 588);
    }

    #[test]
    fn test_hard_small() {
        assert_eq!(hard(65, 8921, 5), 0);
        assert_eq!(hard(65, 8921, 1100), 1);
    }

    #[test]
    fn test_hard() {
        assert_eq!(hard(65, 8921, 5 * 1000 * 1000), 309);
    }
}

pub fn easy(val_a: u64, val_b: u64, steps: usize) -> i64 {
    let bits = 2_u64.pow(16);
    let modulo = 2147483647;
    let mul_a = 16807;
    let mul_b = 48271;

    let mut val_a = val_a;
    let mut val_b = val_b;
    let mut count = 0;

    for _ in 0..steps {
        val_a = (val_a * mul_a) % modulo;
        val_b = (val_b * mul_b) % modulo;
        // println!("{} {}", val_a, val_b);
        count += (val_a % bits == val_b % bits) as i64;
    }

    count
}

pub fn hard(val_a: u64, val_b: u64, steps: usize) -> i64 {
    let bits = 2_u64.pow(16);
    let modulo = 2147483647;
    let mul_a = 16807;
    let mul_b = 48271;

    let mut val_a = val_a;
    let mut val_b = val_b;
    let mut count = 0;

    for _ in 0..steps {
        loop {
            val_a = (val_a * mul_a) % modulo;
            if val_a % 4 == 0 { break }
        }

        loop {
            val_b = (val_b * mul_b) % modulo;
            if val_b % 8 == 0 { break }
        }

        // println!("{} {}", val_a, val_b);
        count += (val_a % bits == val_b % bits) as i64;
    }

    count
}

pub fn main() {
    let input = fs::read_to_string("input/15.txt").unwrap();
    let inputs = input.split("\n")
        .map(|s| s.split_whitespace()
            .last()
            .unwrap()
            .parse::<u64>()
            .unwrap())
        .collect::<Vec<_>>();
    let steps_easy = 40 * 1000 * 1000;
    let steps_hard = 5 * 1000 * 1000;
    println!("{}", easy(inputs[0], inputs[1], steps_easy));
    println!("{}", hard(inputs[0], inputs[1], steps_hard));
}
