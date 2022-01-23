use num::abs;
use std::fs;

#[cfg(test)]
pub mod tests {
    use super::*;

    #[test]
    fn test_easy_1() {
        let data = parse_input("12345678");

        assert_eq!(fft(&data, 1), parse_input("48226158"));
        assert_eq!(fft(&data, 2), parse_input("34040438"));
        assert_eq!(fft(&data, 3), parse_input("03415518"));
        assert_eq!(fft(&data, 4), parse_input("01029498"));
    }
}

fn parse_input(data: &str) -> Vec<i64> {
    data.chars().map(|c| c.to_string().parse().unwrap()).collect::<Vec<_>>()
}

fn process_digit(data: &Vec<i64>, pattern: &Vec<i64>) -> i64 {
    let l = pattern.len();
    let total = data.iter().enumerate().map(|(i, n)| pattern[i % l] * n).sum::<i64>();
    abs(total) % 10
}

fn get_pattern(digit: i64) -> Vec<i64> {
    let mut pattern = Vec::<i64>::new();
    for _ in 0..digit + 1 { pattern.push(0); }
    for _ in 0..digit + 1 { pattern.push(1); }
    for _ in 0..digit + 1 { pattern.push(0); }
    for _ in 0..digit + 1 { pattern.push(-1); }

    pattern
}

fn run_phase(input: &Vec<i64>) -> Vec<i64> {
    let mut data = vec!(0);
    data.extend(input);

    (0..input.len() as i64).map(|digit| {
        let pattern = get_pattern(digit);
        let result = process_digit(&data, &pattern);
        result
    }).collect::<Vec<_>>()
}

fn fft(data: &Vec<i64>, phases: i64) -> Vec<i64> {
    let mut data: Vec<i64> = data.clone();

    for _ in 0..phases {
        data = run_phase(&data);
    }

    data
}

fn easy(input: &str) -> String {
    let data = fft(&parse_input(input), 100);

    data.iter()
        .map(|i| i.to_string())
        .collect::<Vec<String>>()
        .join("")
        [..8].to_string()
}

fn hard(input: &str) -> String {
    // ProTip: the entire sequence is _very_ difficult to implement
    // However, the last 1/4 of it is actually trivial.
    // And the answer just happens to be in the last 1/4 of the sequence.

    let mut input = parse_input(input).repeat(10000);
    let offset = input[..7]
        .iter()
        .map(|i| i.to_string())
        .collect::<Vec<String>>()
        .join("")
        .parse::<usize>()
        .unwrap();

    let n = input.len();
    let phases = 100;
    for _ in 0..phases {
        let mut new_data = Vec::<i64>::new();
        new_data.resize(n, 0);
        new_data[n-1] = input[n-1];
        for i in (0..n-2).rev() {
            new_data[i] = (input[i] + new_data[i+1]) % 10;
        }
        input = new_data;
    }

    let res = input[offset..offset+8]
        .iter()
        .map(|i| i.to_string())
        .collect::<Vec<String>>()
        .join("");

    res
}

fn main() {
    let input = fs::read_to_string("input/16.txt").expect("Unable to read input file");
    println!("{}", easy(&input));
    println!("{}", hard(&input));
    ()
}
