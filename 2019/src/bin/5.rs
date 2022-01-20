use std::fs;

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

use advent_of_code_2019::intcode::run_intcode;


fn parse_input() -> Result<Vec<i32>> {
    let res = fs::read_to_string("input/5.txt")?
        .split(",")
        .map(|line| line.parse::<i32>().unwrap())
        .collect::<Vec<_>>();
    Ok(res)
}

fn easy(code: &Vec<i32>) -> i32 {
    let mut result = 0;
    run_intcode(code.clone(), || 1, |val| result = val);
    result
}

fn hard(code: &Vec<i32>) -> i32 {
    let mut result = 0;
    run_intcode(code.clone(), || 5, |val| result = val);
    result
}

fn main() {
    let code = parse_input().unwrap();
    println!("{}", easy(&code));
    println!("{}", hard(&code));
    ()
}
