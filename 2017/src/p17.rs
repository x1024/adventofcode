use std::fs;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_easy() {
        assert_eq!(easy(3), 638);
    }

    #[test]
    fn test_easy_2() {
        assert_eq!(solve(3, 10, 10), 4);
    }
}

pub fn solve(step: usize, limit: usize, result_index: usize) -> usize {
    let mut next = Vec::<usize>::new();
    next.resize(limit, 0);
    let mut index = 0;
    next.insert(0, 0);

    for value in 1..limit+1 {
        if value % 100000 == 0 {
            println!("{}", value);
        }
        for _ in 0..step {
            index = next[index];
        }
        let n = next[index];
        next[index] = value;
        next[value] = n;
        index = value;
    }

    next[result_index]
}

pub fn easy(step: usize) -> usize {
    solve(step, 2017, 2017)
}

pub fn hard(step: usize) -> usize {
    solve(step, 50 * 1000 * 1000, 0)
}

pub fn main() {
    let input = fs::read_to_string("input/17.txt").unwrap();
    let input = input.parse::<usize>().unwrap();
    println!("{}", easy(input));
    println!("{}", hard(input));
}
