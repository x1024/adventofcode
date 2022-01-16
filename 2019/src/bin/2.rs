use std::fs;

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

#[cfg(test)]
pub mod tests {
    use super::*;

    #[test]
    pub fn test_easy() {
        assert_eq!(
            run_program(Vec::from([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]))[0],
            3500
        );
        assert_eq!(run_program(Vec::from([1, 0, 0, 0, 99]))[0], 2);
        assert_eq!(run_program(Vec::from([2, 3, 0, 3, 99]))[3], 6);
        assert_eq!(run_program(Vec::from([2, 4, 4, 5, 99, 0]))[5], 9801);
        assert_eq!(run_program(Vec::from([1, 1, 1, 4, 99, 5, 6, 0, 99]))[0], 30);
    }

    #[test]
    pub fn test_hard() {
        // assert_eq!(process_hard(&12), 2);
    }
}

fn parse_input() -> Result<Vec<i32>> {
    let res = fs::read_to_string("input/2.txt")?
        .split(",")
        .map(|line| line.parse::<i32>().unwrap())
        .collect::<Vec<_>>();
    Ok(res)
}

fn run_program(code: Vec<i32>) -> Vec<i32> {
    let mut index = 0;
    let mut code = code.clone();

    loop {
        let steps = match code[index] {
            1 => {
                let ia = code[index + 1] as usize;
                let ib = code[index + 2] as usize;
                let ic = code[index + 3] as usize;
                let va = code[ia];
                let vb = code[ib];
                code[ic] = va + vb;
                4
            }
            2 => {
                let ia = code[index + 1] as usize;
                let ib = code[index + 2] as usize;
                let ic = code[index + 3] as usize;
                let va = code[ia];
                let vb = code[ib];
                code[ic] = va * vb;
                4
            }
            _ => break,
        };

        index += steps
    }

    code
}

fn easy(code: &Vec<i32>) -> i32 {
    let mut code = code.clone();
    code[1] = 12;
    code[2] = 2;
    let code = run_program(code);
    code[0]
}

fn hard(code: &Vec<i32>) -> i32 {
    let expected = 19690720;
    for noun in 0..100 {
        for verb in 0..100 {
            let mut code = code.clone();
            code[1] = noun;
            code[2] = verb;
            let result = run_program(code);
            if result[0] == expected {
                return 100 * noun + verb
            }
        }
    }

    -1
}

fn main() {
    let code = parse_input().unwrap();
    println!("{}", easy(&code));
    println!("{}", hard(&code));
    ()
}
