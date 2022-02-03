use std::fs;

#[cfg(test)]
mod tests {
    use super::{easy, hard, parse_input};

    #[test]
    fn test_easy() {
        let input = parse_input("5 1 9 5
                                 7 5 3
                                 2 4 6 8");
        assert_eq!(easy(&input), 18);
    }

    #[test]
    fn test_hard() {
        let input = parse_input("5 9 2 8
                                 9 4 7 3
                                 3 8 6 5");
        assert_eq!(hard(&input), 9);
    }
}

type Input = std::vec::Vec<std::vec::Vec<i32>>;

pub fn easy(data: &Input) -> i32 {
    data.iter().map(|row| row.iter().max().unwrap() - row.iter().min().unwrap()).sum()
}

fn parse_row(row: &Vec<i32>) -> i32 {
    for a in row.iter() {
        for b in row.iter() {
            if a == b { continue }
            if a % b == 0 { return a / b }
        }
    }
    0
}

pub fn hard(data: &Input) -> i32 {
    data.iter().map(|row| parse_row(row)).sum()
}

fn parse_input(data: &str) -> Input {
    data.split("\n")
        .map(|row| row.trim().split_whitespace()
                .map(|cell| cell.parse::<i32>().unwrap())
                .collect::<Vec<_>>())
        .collect::<Vec<_>>()
}

pub fn main() {
    let input = fs::read_to_string("input/2.txt").unwrap();
    let input = parse_input(&input);
    println!("{}", easy(&input));
    println!("{}", hard(&input));
}