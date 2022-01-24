use std::fs;

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;
use advent_of_code_2019::intcode::run_intcode;

#[cfg(test)]
pub mod tests {
    use super::*;

    #[test]
    pub fn test_quinne() {
        let input = vec!(109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99);
        let result = run_intcode(&input, ||0, |_val| ());
        
        assert_eq!(input, result[..input.len()]);
    }

    #[test]
    pub fn test_large_number() {
        let input = vec!(1102,34915192,34915192,7,4,7,99,0);
        let mut result: i64 = 0;
        run_intcode(&input, || 0, |val| result = val);
        assert_eq!(result.to_string().len(), 16);
    }

    #[test]
    pub fn test_large_number_2() {
        let input = vec!(104,1125899906842624,99);
        let mut result: i64 = 0;
        run_intcode(&input, || 0, |val| result = val);
        assert_eq!(result, 1125899906842624);
    }
}

fn parse_input(data: String) -> Result<Vec<i64>> {
    let res = data
        .split(",")
        .map(|line| line.parse::<i64>().unwrap())
        .collect::<Vec<_>>();
    Ok(res)
}

fn easy(code: &Vec<i64>) -> i64 {
    let mut res: i64 = 0;
    run_intcode(code, || 1, |val| res = val);
    res
}

fn hard(code: &Vec<i64>) -> i64 {
    let mut res: i64 = 0;
    run_intcode(code, || 2, |val| res = val);
    res
}

fn main() {
    let code = fs::read_to_string("input/9.txt").expect("Unable to read input file");
    let code = parse_input(code).unwrap();
    println!("{}", easy(&code));
    println!("{}", hard(&code));
    ()
}
